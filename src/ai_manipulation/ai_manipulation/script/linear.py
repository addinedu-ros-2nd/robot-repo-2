import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# JSON 파일로부터 데이터 프레임 A를 읽어옵니다.
file_path_A = '/home/seokwon/deeplearn/src/ai_manipulation/ai_manipulation/datas/way_point_1.json' 
df_A = pd.read_json(file_path_A)

# JSON 파일로부터 데이터 프레임 B를 읽어옵니다.
file_path_B = '/home/seokwon/deeplearn/src/ai_manipulation/ai_manipulation/datas/way_point_2.json' 
df_B = pd.read_json(file_path_B)
df_B.columns = ['output_1', 'output_2', 'output_3', 'output_4', 'output_5', 'output_6']

# 1 번 
# 데이터 프레임 A에서 입력 특성과 데이터 프레임 B에서 예측 대상을 선택
# X = df_A[['input_1', 'input_2', 'input_3', 'input_4', 'input_5']]  # 데이터 프레임 A의 입력 특성
# y = df_B[['output_1', 'output_2', 'output_3', 'output_4', 'output_5']]  # 데이터 프레임 B의 예측 대상

## 2번
# 생각해 보니까  json 데이터의 가로 한줄씩을 넣어서 그 예상값을 받아와야 하는데
# X = df_A
# y = df_B

## 3번
# 생각해 보니까  json 데이터의 가로 한줄씩을 넣어서 그 예상값을 받아와야 하는데
# X = df_A.iloc[i]
# y = df_B.iloc[i]


# 선형 회귀 모델을 정의
model = LinearRegression()

# 데이터 프레임 A의 행을 순차적으로 처리하며 모델을 학습
predicted_rows = []
for i in range(len(df_A)):
    X = df_A.iloc[i:i+1, :]  # 데이터 프레임 A의 i번째 행을 입력으로 선택
    y = df_B.iloc[i:i+1, :]  # 데이터 프레임 B의 i번째 행을 예측 대상으로 선택

    model.fit(X, y)  # 모델 학습

    predicted_row = model.predict(X)  # 해당 행을 예측
    predicted_rows.append(predicted_row)

# 모델 저장
model_filename = '/home/seokwon/deeplearn/src/ai_manipulation/ai_manipulation/datas/linear_model.pkl'
joblib.dump(model, model_filename)


# # 모델을 불러오기
# loaded_model = joblib.load(model_filename)

# # 새로운 입력 데이터
# new_X = df_A.iloc[0:1, :]

# # 저장된 모델을 사용하여 예측
# predicted_y = loaded_model.predict(new_X)

# # 예측값 출력
# print("Predicted Value:", predicted_y)