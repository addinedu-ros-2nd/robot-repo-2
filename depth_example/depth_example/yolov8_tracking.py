import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
video_path = "walk1.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        person_tracking = model.track(frame, persist=True, conf=0.5, classes=0)[0]

        tracking_info = []

        # 박스를 사용하여 원본 이미지에 "person" 객체를 그리기
        if person_tracking.boxes.id==None:
            continue
        for box in person_tracking.boxes:
            x1, y1, x2, y2 = box.data.tolist()[0][:4]
            x1, y1, x2, y2 = map(round, [x1, y1, x2, y2])
            tracking_info.extend([int(box.id[0]), x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
            # 텍스트를 박스 위에 추가 (배경을 빨간색으로, 글자를 흰색으로)
            text = "ID: " + str(int(box.id[0])) + ", Acc: " + str(float(box.data[0][-2]))[:4]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
            text_x = x1 - 2  # 텍스트를 그릴 x 좌표
            text_y = y1 - 2  # 텍스트를 그릴 y 좌표 (박스 위에 위치)
            # 텍스트 배경 박스를 그리기
            cv2.rectangle(frame, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), (0, 0, 255), cv2.FILLED)
            # 텍스트를 흰색으로 그리기
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
        cv2.imshow("YOLOv8 Tracking", frame)
        cv2.waitKey(1)
        print("=============================================================================")
        print(tracking_info)
        print("=============================================================================")

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()