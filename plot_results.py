import numpy as np
import matplotlib.pyplot as plt

# 加载数据
temp = np.load('temp_field.npy')
power = np.load('power_field.npy')

# 简单绘图（例如，显示温度场的中心切片）
size = int(round(temp.shape[0] ** (1/3)))  # 假设是立方体网格
temp_3d = temp.reshape((size, size, size))

plt.figure(figsize=(10, 4))
plt.subplot(1,2,1)
plt.imshow(temp_3d[:, :, size//2], origin='lower')
plt.colorbar(label='Temperature (K)')
plt.title('Temperature Field (Middle Slice)')

plt.subplot(1,2,2)
# 可类似地绘制功率场
# ...
plt.show()
