import numpy as np

# n개의 (640, 480) 모양의 배열 생성 (예시)
n = 10  # 배열의 개수
arrays = np.random.randint(2, size=(n, 640, 480))  # 1 또는 0으로 구성된 무작위 배열

# 모든 배열에 대한 OR 연산 수행
result = np.logical_or.reduce(arrays, axis=0)

print(result.shape)