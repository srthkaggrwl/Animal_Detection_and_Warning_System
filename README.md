### README.md

```markdown
# Animal Detection and Warning System

This project is an **Animal Detection and Warning System** implemented using **YOLO** (You Only Look Once) for real-time object detection, and **Streamlit** for the user interface. It detects the presence of animals, particularly dogs, in a video stream and triggers warning signals through MQTT based on consecutive detection.

## Features

- **Real-time Object Detection**: Uses the YOLO model to detect objects in video streams.
- **Animal Detection**: Specifically detects dogs using the YOLO model.
- **Warning System**: Sends MQTT messages to trigger a warning system when a dog is detected for consecutive frames.
- **User Interface**: Streamlit is used for creating the front-end to interact with the system and visualize the processed video.

## Technologies Used

- **YOLOv8**: For object detection.
- **Streamlit**: For creating the web-based interface.
- **MQTT**: For sending warnings and messages based on detection.
- **Python**: Main programming language for implementing the backend logic.
- **Ultralytics**: For YOLO model implementation and inference.
- **OpenCV**: For handling video processing and manipulation.
- **Git**: For version control.

## Setup

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/srthkaggrwl/Animal_Detection_and_Warning_System.git
cd Animal_Detection_and_Warning_System
```

### 2. Create a Virtual Environment

It's recommended to create a Python virtual environment for managing dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the core dependencies directly:

```bash
pip install streamlit ultralytics paho-mqtt opencv-python
```

### 4. Run the Streamlit App

To run the Streamlit application, use the following command:

```bash
streamlit run streamlit_app.py
```

### 5. Access the Application

Once the app starts, you can access it on your browser:

- **Local URL**: `http://localhost:8501`
- **Network URL**: `http://<your-server-ip>:8501`

## How It Works

1. **Video Input**: Users upload a video to the Streamlit app.
2. **Real-time Detection**: The video is processed frame by frame, and YOLO detects objects in each frame.
3. **Dog Detection**: The system specifically checks for the presence of a dog in the frames.
4. **Consecutive Detection**: If a dog is detected consecutively for 10 frames, an MQTT message is sent with the `"on"` signal to trigger a warning. If no dog is detected for 10 frames, an `"off"` signal is sent.
5. **Live Video Stream**: The processed video with detected objects is displayed to the user.

## MQTT Integration

The system uses MQTT to send warning signals based on the detection of a dog:

- The warning is sent if the dog is detected consecutively in multiple frames.
- A signal `"on"` is sent when the dog is detected for 10 consecutive frames.
- A signal `"off"` is sent when no dog is detected for 10 consecutive frames.

To set up MQTT, make sure to replace the MQTT broker information in the script:

```python
mqtt_broker = "your_broker_ip"
mqtt_port = 1883
mqtt_topic = "animal_warning"
```

## File Structure

```plaintext
.
├── .gitignore            # Git ignore file
├── backup.py             # Backup scripts for the project
├── backup2.py            # Backup script 2
├── backup3.py            # Backup script 3
├── best.pt               # YOLO model weights
├── check_installations.py # Script to check required installations
├── commands.txt          # Commands for the server
├── nohup.out             # Log file for background processes
├── package.json          # Package management for frontend
├── streamlit_app.py      # Main Streamlit application file
└── test.py               # Test script for detecting animals in images
```

## Troubleshooting

- **ModuleNotFoundError**: Ensure that all required dependencies are installed in the virtual environment.
  
  Example:
  ```bash
  pip install -r requirements.txt
  ```

- **No Detection**: If no dogs are detected, ensure that the YOLO model is correctly loaded and that the model weights (`best.pt`) are available in the specified directory.

## Contributing

Feel free to fork this repository and submit pull requests. If you have any feature requests or issues, please open an issue on GitHub.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the [Ultralytics YOLO](https://github.com/ultralytics/yolov5) team for the YOLO model.
- Thanks to the Streamlit team for creating a fantastic framework for rapid app development.
```

