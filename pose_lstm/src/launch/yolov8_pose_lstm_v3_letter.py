import cv2
import numpy as np
import torch
import torch.nn as nn
from ultralytics import YOLO
from tensorflow import keras
import time



# LSTM 모델 정의
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.lstm1 = nn.LSTM(input_size, hidden_size, num_layers=1, batch_first=True)
        self.lstm2 = nn.LSTM(hidden_size, hidden_size * 2, num_layers=1, batch_first=True)
        self.lstm3 = nn.LSTM(hidden_size * 2, hidden_size * 4, num_layers=1, batch_first=True)
        self.dropout1 = nn.Dropout(0.1)
        self.lstm4 = nn.LSTM(hidden_size * 4, hidden_size * 2, num_layers=1, batch_first=True)
        self.lstm5 = nn.LSTM(hidden_size * 2, hidden_size, num_layers=1, batch_first=True)
        self.lstm6 = nn.LSTM(hidden_size, hidden_size // 2, num_layers=1, batch_first=True)
        self.dropout2 = nn.Dropout(0.1)
        self.lstm7 = nn.LSTM(hidden_size // 2, hidden_size // 4, num_layers=1, batch_first=True)
        self.fc = nn.Linear(hidden_size // 4, num_classes)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)

        out, _ = self.lstm1(x, (h0, c0))
        out, _ = self.lstm2(out)
        out, _ = self.lstm3(out)
        out = self.dropout1(out)
        out, _ = self.lstm4(out)
        out, _ = self.lstm5(out)
        out, _ = self.lstm6(out)
        out = self.dropout2(out)
        out, _ = self.lstm7(out)
        out = self.fc(out[:, -1, :])
        return out



## 하이퍼파라미터 설정
input_size = 34  # 데이터의 차원 (예: x와 y 좌표)
hidden_size = 64  # LSTM의 은닉 상태 크기
num_layers = 2  # LSTM 레이어 수
num_classes = 2  # 분류할 클래스 수 (0 또는 1)



# LSTMModel 생성
loaded_model = LSTMModel(input_size, hidden_size, num_layers, num_classes)

# 불러온 모델의 가중치 로드
loaded_model.load_state_dict(torch.load('lstm_long_data_model_v1.pth'))
loaded_model.eval()



# YOLOv8-pose 모델 초기화
yolo_model = YOLO("yolov8n-pose.pt")

# 웹캠 스트림 열기
# cap = cv2.VideoCapture("/home/seokwon/Desktop/RNN_data/2023-11-06_16-13-31.avi")
# cap = cv2.VideoCapture("/home/seokwon/Desktop/RNN_data/2023-11-09_14-02-22.avi")
cap = cv2.VideoCapture(6)



while True:
    start_time = time.time()
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
    if len(frame_keypoints_xyn):
        if len(frame_keypoints_xyn) > 0:
            new_data = np.array(frame_keypoints_xyn)  # 예측하고자 하는 새로운 데이터

            # 3-D 텐서로 입력 데이터 조정
            new_data = torch.FloatTensor(new_data)  # (sequence_length, input_size)
            new_data = new_data.unsqueeze(0)  # (1, sequence_length, input_size)


            if new_data.size(-1) == input_size: # 입력 데이터의 차원이 맞는지 확인
                lstm_prediction = loaded_model(new_data)

                # 예측 결과를 클래스 확률로 변환
                softmax = torch.nn.Softmax(dim=1)
                class_probabilities = softmax(lstm_prediction)
                class_probabilities_numpy = class_probabilities.cpu().detach().numpy()

                # 예측 결과 출력
                print("LSTM 모델 예측 결과 (클래스 확률):", class_probabilities_numpy)
                if (class_probabilities_numpy[0][1] > 0.65).any():
                    cv2.putText(frame, "stand", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "sit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 웹캠 화면에 프레임 표시 (선택 사항)
    cv2.imshow("Results", results[0].plot())  # yolo로 사람인식, skeleton keypoint값 받아온 화면

    end_time = time.time()
    inference_time = end_time - start_time
    print("모델 추론 속도 : {:2f} 초".format(inference_time))
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# VideoCapture 객체 해제
cap.release()
cv2.destroyAllWindows()
