import cv2
import glob
import os
from matplotlib import pyplot as plt

# Specify the directory where processed videos are stored
SAVE_DIR = "/home/sarthak/animal_detection_and_warning_system/runs/detect"  # Directory to save processed videos

# Dynamically find the processed video directory
processed_dirs = sorted(glob.glob(f"{SAVE_DIR}/*"), key=os.path.getctime, reverse=True)
if not processed_dirs:
    raise FileNotFoundError("No processed directories found!")
processed_dir = processed_dirs[0]  # Get the most recent directory

# Find the AVI file in the processed directory
avi_files = glob.glob(f"{processed_dir}/*.avi")
if not avi_files:
    raise FileNotFoundError("Processed video file not found!")
avi_file_path = avi_files[0]  # Get the first AVI video file

# Open the video file
cap = cv2.VideoCapture(avi_file_path)

# Check if the video file was successfully opened
if not cap.isOpened():
    raise IOError(f"Error: Could not open the AVI file at {avi_file_path}")

# Process and display the video frames
while True:
    ret, frame = cap.read()  # Read a frame
    if not ret:
        print("End of video reached or error reading the frame.")
        break

    # Display the frame using matplotlib
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for matplotlib
    plt.axis('off')  # Hide axes
    plt.show(block=False)  # Show frame
    plt.pause(0.05)  # Pause for a short time to simulate video playback
    plt.close()  # Close the frame to display the next one

    # Optional: Add user input to quit early
    user_input = input("Press Enter to continue, or type 'q' to quit: ")
    if user_input.lower() == 'q':
        print("Video playback interrupted by user.")
        break

# Release resources
cap.release()
print("Video processing completed.")
