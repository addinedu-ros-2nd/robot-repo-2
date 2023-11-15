import cv2
import numpy as np
import torch
import torch.nn as nn
from ultralytics import YOLO
from tensorflow import keras

# LSTM 모델 아키텍처 정의
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

# LSTM 모델 초기화
input_size = 34 # 입력 크기 정의
hidden_size = 64 # 숨겨진 상태 크기 정의
num_layers =  2# LSTM 레이어 수 정의
num_classes = 2 # 클래스 수 정의
lstm_model = LSTMModel(input_size, hidden_size, num_layers, num_classes)
lstm_model.load_state_dict(torch.load("/home/seokwon/dev_ws/final_models/lstm_model_v1.pth"))
lstm_model.eval()



# 하이퍼파라미터 설정
# input_size = 34  # 데이터의 차원 (예: x와 y 좌표)
# hidden_size = 64  # LSTM의 은닉 상태 크기
# num_layers = 2  # LSTM 레이어 수
# num_classes = 2  # 분류할 클래스 수 (0 또는 1)
# num_epochs = 10
# batch_size = 16
# learning_rate = 0.001

# YOLOv8-pose 모델 초기화
yolo_model = YOLO("yolov8n-pose.pt")

# 웹캠 스트림 열기
cap = cv2.VideoCapture("/home/seokwon/Desktop/RNN_data/2023-11-06_16-06-45.avi")  # 0은 기본 웹캠을 나타냅니다. 다른 카메라를 사용하려면 1, 2 등을 사용할 수 있습니다.

while True:
    # 현재 프레임 가져오기
    ret, frame = cap.read()

    # YOLOv8-pose 모델을 사용하여 스켈레톤 좌표를 가져오는 코드
    results = yolo_model(frame)
    frame_keypoints_xyn = []

    # Keypoint 정보를 가져와서 리스트에 저장
    for result in results:
        for keypoints in result.keypoints:
            xyn = keypoints.xyn.cpu().numpy()
            xyn_list = xyn.tolist()
            flattened_xyn = [point for sublist in xyn_list[0] for point in sublist]
            frame_keypoints_xyn.append(flattened_xyn)

        # LSTM 모델을 사용하여 예측
        if len(frame_keypoints_xyn) > 0:
            new_data = np.array(frame_keypoints_xyn)  # 예측하고자 하는 새로운 데이터

            # 3-D 텐서로 입력 데이터 조정
            new_data = torch.FloatTensor(new_data)  # (sequence_length, input_size)
            new_data = new_data.unsqueeze(0)  # (1, sequence_length, input_size)

            lstm_prediction = lstm_model(new_data)

            # 예측 결과를 클래스 확률로 변환
            softmax = torch.nn.Softmax(dim=1)
            class_probabilities = softmax(lstm_prediction)
            class_0_probability = class_probabilities[0][0].item()
            class_1_probability = class_probabilities[0][1].item()

            # 예측 결과를 0 또는 1로 변환
            threshold = 0.5  # 임계값 설정
            if class_1_probability > threshold:
                binary_prediction = 1 # 앉아있을때가 1로 나옴
            else : 
                binary_prediction = 0 # 서있을때가 0으로 나옴

            # 예측 결과 출력
            print("LSTM 모델 예측 결과 (0 또는 1로 변환):", binary_prediction)


    # 웹캠 화면에 프레임 표시 (선택 사항)
    # cv2.imshow("Webcam", frame) # 그냥 아무것도 없는 일반 화면 
    cv2.imshow("Results", results[0].plot()) # yolo로 사람인식, skeleton keypoint값 받아온 화면

    # # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# VideoCapture 객체 해제
cap.release()
cv2.destroyAllWindows()
