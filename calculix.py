#!/usr/bin/env python3
import numpy as np
import precice

print("[CalculiX] 启动...")

SIZE = 310  # 必须与 OpenMC/OpenFOAM 一致
n = SIZE**3
print(f"CalculiX: {n:,} 点")

p = precice.Participant("CalculiX", "config_unified.xml", 0, 1)
mesh = "MeshOne"

precice_dt = p.initialize()
dt = precice_dt if precice_dt is not None else 0.01
print(f"dt={dt}")

step = 0
while p.is_coupling_ongoing() and step < 3:
    step += 1
    
    # 读取温度（完整网格）
    temp = p.read_data(mesh, "Temperature", list(range(n)), 0)
    
    # 计算位移（简化：温度升高 → 热膨胀）
    alpha = 1.2e-5  # 热膨胀系数
    T_ref = 300.0
    disp_magnitude = alpha * (temp - T_ref)
    
    print(f"步 {step}: T_avg={temp.mean():.1f}K, max_disp={disp_magnitude.max():.2e}m")
    
    # 写入位移（3 分量）
    displacement = np.zeros((n, 3), dtype=np.float32)
    displacement[:, 0] = disp_magnitude  # x 方向位移
    p.write_data(mesh, "Displacement", list(range(n)), displacement.flatten())
    
    dt = p.advance(dt)
    if dt is None:
        dt = 0.01

p.finalize()
print("[CalculiX] 完成")
