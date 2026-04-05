#!/usr/bin/env python3
import numpy as np
import precice
import time

print("[OpenFOAM] 500³ 优化版启动...")

SIZE = 390
n = SIZE**3
print(f"OpenFOAM: {n:,} 点")

p = precice.Participant("OpenFOAM", "config_unified.xml", 0, 1)
mesh = "MeshOne"

# OpenFOAM 是接收网格的一方，需要设置访问区域
bounds = [0.0, 1.0, -0.5, 0.5, 0.0, 1.0]
p.set_mesh_access_region(mesh, bounds)
print(f"设置网格访问区域: {bounds}")

precice_dt = p.initialize()
dt = precice_dt if precice_dt is not None else 0.01
print(f"dt={dt}")

temp = np.ones(n, dtype=np.float32) * 300.0
step = 0

while p.is_coupling_ongoing() and step < 5:
    if p.requires_writing_checkpoint():
        print("  [OpenFOAM] 写入检查点")
    
    step += 1
    step_start = time.time()
    
    power = p.read_data(mesh, "Power", list(range(n)), 0)
    print(f"步 {step}: P={power.mean():.2e}")
    p.write_data(mesh, "Temperature", list(range(n)), temp)
    
    if p.requires_reading_checkpoint():
        print("  [OpenFOAM] 读取检查点")
    
    dt = p.advance(dt)
    if dt is None:
        dt = 0.01

p.finalize()
print("OpenFOAM 完成")
