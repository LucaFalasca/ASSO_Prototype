import cv2
import os
from ultralytics import YOLO
from flask import Flask, Response
from confluent_kafka import Consumer, Producer

app = Flask(__name__)

@app.route('/video')
def video_feed():
    return Response(get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_stream():
    model = YOLO('yolo11n-pose.pt')

    body_parts = {
        "Nose": 0,
        "Left Eye": 1,
        "Right Eye": 2,
        "Left Ear": 3,
        "Right Ear": 4,
        "Left Shoulder": 5,
        "Right Shoulder": 6,
        "Left Elbow": 7,
        "Right Elbow": 8,
        "Left Wrist": 9,
        "Right Wrist": 10,
        "Left Hip": 11,
        "Right Hip": 12,
        "Left Knee": 13,
        "Right Knee": 14,
        "Left Ankle": 15,
        "Right Ankle": 16
    }


    # Usiamo 0.0.0.0 per ascoltare su tutte le interfacce interne del container
    udp_url = "udp://0.0.0.0:5000"

    print("Tentativo di connessione...")
    cap = cv2.VideoCapture(udp_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print("Errore: OpenCV non riesce ancora ad aprire lo stream.")
        exit()

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_size = (width, height)
    output_filename = 'output_video.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_writer = cv2.VideoWriter(output_filename, fourcc, 10, frame_size)

    conf = {
        'bootstrap.servers': 'kafka_broker:9092', 
        'client.id': 'vision_alarm_producer',
    }

    producer = Producer(conf)
    alarm_topic = 'alarms'

    c = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Frame finiti")
            break

        print(f"Processing frame of shape: {frame.shape}")
        print(f"Frame {c}")
        c += 1
        # 0 se gpu e cpu se non c'è gpu
        device = "cuda" if os.getenv("USE_GPU", "0") == "1" else "cpu"

        results = model(frame, device=device, classes=[0], conf=0.4, save=False)  # Classe 0 corrisponde a "person" nel COCO dataset

        #print(f"Detections: {results}")
        keypoints = results[0].keypoints
        #print(f"Keypoints: {keypoints.xy.cpu().numpy()[0] if keypoints is not None else 'None'}")
        coords = keypoints.xy.cpu().numpy() if keypoints is not None else []
        annotated_frame = results[0].plot()
        status = "Not Fallen"
        for res in results:
            keypoints = results[0].keypoints
            coords = keypoints.xy.cpu().numpy() if keypoints is not None else []
            for k, box in enumerate(res.boxes):
                #print(f"Box: {box.xyxy}, Confidence: {box.conf}, Class: {box.cls}")

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                width = x2 - x1
                height = y2 - y1

                if height > 0:
                    aspect_ratio = width / height
                    #print(f"Aspect Ratio: {aspect_ratio}")
                else:
                    aspect_ratio = 0

                fallen_threshold = 0.8
                sight_threshold = 0.6

                if aspect_ratio > fallen_threshold:
                    status = "Fallen by aspect ratio"
                    color = (0, 0, 255)  # Red
                elif aspect_ratio > sight_threshold:
                    body_parts_coords = coords[k]

                    leg1_lenght = ((body_parts_coords[body_parts["Left Hip"]][0] - body_parts_coords[body_parts["Left Knee"]][0])**2 + (body_parts_coords[body_parts["Left Hip"]][1] - body_parts_coords[body_parts["Left Knee"]][1])**2) ** 0.5

                    leg2_lenght = ((body_parts_coords[body_parts["Right Hip"]][0] - body_parts_coords[body_parts["Right Knee"]][0])**2 + (body_parts_coords[body_parts["Right Hip"]][1] - body_parts_coords[body_parts["Right Knee"]][1])**2) ** 0.5

                    torso_lenght = ((body_parts_coords[body_parts["Left Shoulder"]][0] - body_parts_coords[body_parts["Left Hip"]][0])**2 + (body_parts_coords[body_parts["Left Shoulder"]][1] - body_parts_coords[body_parts["Left Hip"]][1])**2) ** 0.5

                    ratio_legs_torso = (leg1_lenght) / torso_lenght if torso_lenght != 0 else float('inf')

                    nose_y = body_parts_coords[body_parts["Nose"]][1]

                    left_ankle_y = body_parts_coords[body_parts["Left Ankle"]][1]
                    right_ankle_y = body_parts_coords[body_parts["Right Ankle"]][1]
                    ankle_y = min(left_ankle_y, right_ankle_y)

                    box_height = y2 - y1
                    percentage_ratio_box = 0.1 * box_height

                    if nose_y > ankle_y - percentage_ratio_box:  # Soglia per determinare se la persona è caduta
                        status = "Fallen by nose"
                        color = (0, 0, 255)  # Red
                    elif ratio_legs_torso > 1.5:  # Soglia per determinare se la persona è caduta
                        status = "Fallen by legs"
                        color = (0, 0, 255)  # Red
                    else:
                        status = "Not Fallen"
                        color = (0, 255, 0)  # Green
                else:
                    status = "Not Fallen"
                    color = (0, 255, 0)

                confidence = box.conf[0] 
                label = f"{status}"

                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        print(f"Status: {status}")
        if status != "Not Fallen":
            print("Fall detected, sending alarm...")
            producer.produce(alarm_topic, f'Alarm: Fall detected! Status: {status}')
            producer.flush()

        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        #video_writer.write(annotated_frame)

    #cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)