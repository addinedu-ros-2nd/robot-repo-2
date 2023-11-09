import numpy as np

arr = np.array([0, 2, 0, 4, 5, 0, 1, 8])
nonzero_count = np.count_nonzero(arr)
print("0이 아닌 요소의 개수:", nonzero_count)
