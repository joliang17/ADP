import numpy as np

ValuePart1 = 3
ValuePart2 = 5
Value_N = 10
B_N1 = np.mat([[0, 0], [0, 0]], dtype=float)

# 变动的价值元素:2*1
phi_N = np.mat([[ValuePart1, ValuePart2]], dtype=float)

# 原先的参数: 2*1
theta_N1 = np.mat([[0.3, 0.2]], dtype=float)

# 新价值和原有价值的差：1*1
VSN1 = np.dot(phi_N.T, theta_N1)
esp_N = VSN1-Value_N

# gamma参数： 1*1
Gam_N = 1 + np.dot(np.dot(phi_N.T, B_N1), phi_N)

# H矩阵：2*2 
H_N = B_N1 / Gam_N

# B矩阵：2*2
# B_N1为上次循环获得参数
# 需规定 B_0
B_N = B_N1 - 1/Gam_N*np.dot(np.dot(B_N1), np.dot(B_N1))

# 新参数矩阵：2*1
theta_N = theta_N1 - esp_N*np.dot(H_N, phi_N)
