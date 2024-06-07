import cv2
import argparse
import numpy as np
from ultralytics import YOLO

ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

def annotate_frame(frame, detections, labels):
    for detection, label in zip(detections, labels):
        x, y, w, h = detection[:4]
        class_id = int(detection[5])
        confidence = detection[4]

        # Draw bounding box
        cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)

        # Put label
        cv2.putText(frame, label, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    return frame

def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov5nu.pt")

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        detections = result.boxes[0].cpu().numpy()
        labels = [
            f"{model.names[int(class_id)]} {confidence:.2f}"
            for _, _, _, confidence, class_id in detections
        ]

        frame = annotate_frame(frame, detections, labels)
        
        cv2.imshow("YOLOv8", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
