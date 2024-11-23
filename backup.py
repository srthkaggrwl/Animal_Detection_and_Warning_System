import streamlit as st
import paho.mqtt.client as mqtt
import cv2
import tempfile
import time

# MQTT Broker details
MQTT_BROKER = "0.tcp.in.ngrok.io"  # Replace with your ngrok public address
MQTT_PORT = 16954                 # Replace with your ngrok port
MQTT_TOPIC = "test/topic"         # Topic to publish to

# MQTT Publisher function
def publish_message(message):
    try:
        client = mqtt.Client()  # Ensure no outdated API options are used
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()  # Explicitly start the loop
        client.publish(MQTT_TOPIC, payload=message, qos=1)
        client.loop_stop()  # Stop the loop after publishing
        client.disconnect()
        st.success(f"Message '{message}' sent successfully!")
    except Exception as e:
        st.error(f"Failed to send message: {str(e)}")

# Streamlit interface
st.title("Animal Detection System")
st.write("Press the button below to simulate animal detection.")

if st.button("Detect Animal", key="detect_animal"):
    publish_message("on")  # Send "on" message to activate the buzzer

if st.button("Turn Off", key="turn_off"):
    publish_message("off")  # Send "off" message to deactivate the buzzer

# Video upload and playback
st.write("### Upload a video to display")
uploaded_video = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_video is not None:
    # Save the uploaded video to a temporary file
    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_file.write(uploaded_video.read())
    temp_video_file.close()

    # Open the video using OpenCV
    cap = cv2.VideoCapture(temp_video_file.name)

    # Display video frames
    stframe = st.empty()  # Create a Streamlit container for video frames
    paused = st.checkbox("Pause Video", value=False)  # Single pause button

    # Slider for playback speed
    playback_speed = st.slider("Playback Speed (frames per second)", 1, 30, 15)

    frame_number = 0

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                st.warning("Video playback finished.")
                break

            frame_number += 1

            # Convert frame to RGB (Streamlit displays images in RGB format)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame and current frame number
            stframe.image(frame, channels="RGB", caption=f"Frame number: {frame_number}")

            # Control playback speed
            time.sleep(1 / playback_speed)

    cap.release()
    st.success("Video playback completed.")