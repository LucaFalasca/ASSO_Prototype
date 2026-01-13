# ASSO Prototype - Monitoring and Fall Detection System

This project is an advanced prototype for environmental sensor monitoring and automated fall detection using Computer Vision, integrating microservices that communicate through a message broker.

## 🏗️ System Architecture

The system is built on a containerized microservices architecture using Docker, with **Apache Kafka** acting as the backbone for message exchange:

1.  **Kafka Broker**: Manages communication channels (`sensors_data` and `alarms`). It uses KRaft for cluster management.
2.  **Sensor Producer**: A Python simulator that generates random data (simulating physical sensors) and publishes it to Kafka.
3.  **Data Sensor Manager**: Analyzes sensor data streams. If a value exceeds a critical threshold, it publishes a message to the alarms topic.
4.  **Video Streamer**: A GStreamer-based module that broadcasts a video file (simulating a camera feed) via UDP protocol.
5.  **Vision Detector**: The core of the video analysis. It receives the UDP stream, utilizes the **YOLOv11-pose** model for human pose estimation, and detects falls based on geometric logic (aspect ratio and keypoint positioning).
6.  **Alarm Reader**: A Flask Web App serving as a dashboard. It consumes messages from the `alarms` topic and updates the user interface in real-time.

<img width="701" height="526" alt="high_level_architecture" src="https://github.com/user-attachments/assets/33339bf1-30b4-4b25-8bd0-2969eb1edf77" />

## 🚀 General Workflow

The system operates in real-time following these steps:
- The **Producer** and **Streamer** constantly send data (numerical and video).
- The **Sensor Manager** and **Vision Detector** act as consumers and analyzers:
    - If the sensor detects a value > 9, a sensor alarm is triggered.
    - If the vision algorithm detects a body in a horizontal position or meeting specific fall parameters, a fall alarm is triggered.
- Alarms are sent to a centralized topic on Kafka.
- The **Alarm Reader** retrieves these alarms and turns the corresponding UI indicators red to alert the operator.

## 📋 Prerequisites

To run the entire ecosystem, ensure you have the following installed on your system:
- **Docker**
- **Docker Compose**

## 🛠️ How to Use

The entire process is automated. Follow these steps from your terminal in the project root:

1. **Start the system**:
   ```bash
   docker compose up
   ```
   *Note: The first run may take some time to download images and the YOLO model weights.*

2. **Access the Dashboard**:
   Open your browser and navigate to:
   [http://localhost:8081](http://localhost:8081)

3. **Vision Monitoring (Optional)**:
   To view the real-time video analysis with bounding boxes and keypoints:
   [http://localhost:8080](http://localhost:8080)

4. **Video Stream reset (if needed)**:
   If you want to restart the video stream without stopping the entire system, open a new terminal and run:
   ```bash
   docker compose restart video_streamer
   ```

5. **Sensor data view (Optional)**:
   You can monitor the sensor data being produced by accessing the container:
   ```bash
   docker logs -f sensor_producer
   ```

6. **Shutdown**:
   To stop all services:
   ```bash
   docker compose down
   ```
## Example of system in use

https://github.com/user-attachments/assets/b3f3b152-5d92-436e-b4d4-4966f1ba13df


