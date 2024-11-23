import streamlit as st
import paho.mqtt.client as mqtt
import os
import tempfile
import glob  # Import glob for file pattern matching
from ultralytics import YOLO
import subprocess  # Import subprocess for video conversion

# Paths and settings
MODEL_PATH = "/home/sarthak/animal_detection_and_warning_system/best.pt"  # Path to YOLO model
SAVE_DIR = "/home/sarthak/animal_detection_and_warning_system/runs/detect"  # Directory to save processed videos
os.makedirs(SAVE_DIR, exist_ok=True)

# MQTT Broker details
MQTT_BROKER = "0.tcp.in.ngrok.io"  # Replace with your ngrok public address
MQTT_PORT = 16954  # Replace with your ngrok port
MQTT_TOPIC = "test/topic"  # Topic to publish to

# Load YOLO model
model = YOLO(MODEL_PATH)

# MQTT Publisher function
def publish_message(message):
    try:
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        client.publish(MQTT_TOPIC, payload=message, qos=1)
        client.loop_stop()
        client.disconnect()
        st.success(f"Message '{message}' sent successfully!")
    except Exception as e:
        st.error(f"Failed to send message: {str(e)}")

# Video conversion function
def convert_to_mp4(input_path, output_path):
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-vcodec", "libx264", "-acodec", "aac", output_path],
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to convert video: {e}")
        return None

# Streamlit interface
st.title("Animal Detection and Warning System")
st.write("This application detects animals in uploaded videos using thermal sensors and a trained ML model, triggering deterrents when necessary.")

# Control buttons for buzzer
if st.button("Detect Animal", key="detect_animal"):
    publish_message("on")  # Activate the buzzer

if st.button("Turn Off", key="turn_off"):
    publish_message("off")  # Deactivate the buzzer

# Video upload and processing
st.write("### Upload a video for animal detection")
uploaded_video = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_video is not None:
    # Save the uploaded video to a temporary file
    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_file.write(uploaded_video.read())
    temp_video_file.close()

    # Process the video with YOLO model
    st.info("Processing the video through the YOLO model. Please wait...")
    try:
        # YOLO model inference
        results = model.track(
            source=temp_video_file.name,
            show=False,
            save=True,
            save_txt=False,
            save_dir=SAVE_DIR
        )

        # Dynamically find the processed video directory
        processed_dirs = sorted(glob.glob(f"{SAVE_DIR}/*"), key=os.path.getctime, reverse=True)
        if not processed_dirs:
            raise FileNotFoundError("No processed directories found!")
        processed_dir = processed_dirs[0]  # Get the most recent directory

        # Find the video file within the processed directory
        processed_video_path = glob.glob(f"{processed_dir}/*.avi")  # Adjust file extension if needed
        if not processed_video_path:
            raise FileNotFoundError("Processed video file not found!")
        processed_video_path = processed_video_path[0]  # Get the first video file

        # Convert the AVI file to MP4
        mp4_video_path = os.path.join(processed_dir, "output.mp4")
        converted_video_path = convert_to_mp4(processed_video_path, mp4_video_path)

        if converted_video_path:
            st.success(f"Video processed and converted successfully! Path: {converted_video_path}")

            # Display the processed video
            st.write("### Processed Video")
            with open(converted_video_path, "rb") as processed_file:
                st.video(processed_file.read())  # Show the processed video to the user

    except Exception as e:
        st.error(f"Failed to process video: {str(e)}")
