import cv2
from ultralytics import YOLO
from database import create_table,log_detection
from collections import defaultdict

create_table()

model = YOLO("yolov8n.pt")

TARGET_OBJECTS = [
    'bottle', 'book', 'laptop', 'phone', 'cup', 'keyboard',
    'mouse', 'backpack', 'chair', 'tv', 'clock', 'remote', 'handbag','toy'
]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    counts = defaultdict(int)

    for result in results:
        for box in result.boxes:
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            if label in TARGET_OBJECTS and conf > 0.5:
                counts[label] += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


                log_detection(label)

    y_offset = 30
    for obj,count in counts.items():
        cv2.putText(frame,f'{obj}:{count}', (10, y_offset),cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 0, 255), 2)
        y_offset += 25


    cv2.imshow('Object Recognition mini-system',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()