#!/usr/bin/env python3
import numpy as np
import precice
import time

print("[OpenMC] 500³ 优化版启动...")

SIZE = 390
n = SIZE**3
print(f"OpenMC: {n:,} 点")

p = precice.Participant("OpenMC", "config_unified.xml", 0, 1)
mesh = "MeshOne"

print("生成网格...")
x = np.linspace(0, 1, SIZE, dtype=np.float32)
y = np.linspace(-0.5, 0.5, SIZE, dtype=np.float32)
z = np.linspace(0, 1, SIZE, dtype=np.float32)
xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
vertices = np.column_stack([xv.ravel(), yv.ravel(), zv.ravel()]).astype(np.float32)
del xv, yv, zv

p.set_mesh_vertices(mesh, vertices)
print(f"顶点: {vertices.nbytes/1e6:.1f} MB")
del vertices

# OpenMC 是提供网格的一方，不需要 set_mesh_access_region！

precice_dt = p.initialize()
dt = precice_dt if precice_dt is not None else 0.01
print(f"dt={dt}")

step = 0
while p.is_coupling_ongoing() and step < 5:
    if p.requires_writing_checkpoint():
        print("  [OpenMC] 写入检查点")
    
    step += 1
    
    temp = p.read_data(mesh, "Temperature", list(range(n)), 0)
    if temp.mean() < 10:
        temp = np.ones(n, dtype=np.float32) * 300.0
    
    power = np.ones(n, dtype=np.float32) * 1000.0
    
    print(f"步 {step}: T={temp.mean():.1f}K")
    p.write_data(mesh, "Power", list(range(n)), power)
    
    if p.requires_reading_checkpoint():
        print("  [OpenMC] 读取检查点")
    
    dt = p.advance(dt)
    if dt is None:
        dt = 0.01

p.finalize()
print("OpenMC 完成")
