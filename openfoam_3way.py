#!/usr/bin/env python3
import numpy as np
import precice

print("[OpenFOAM] 三场耦合启动...")

SIZE = 350
n = SIZE**3

p = precice.Participant("OpenFOAM", "config_3way.xml", 0, 1)
mesh = "MeshOne"

bounds = [0.0, 1.0, -0.5, 0.5, 0.0, 1.0]
p.set_mesh_access_region(mesh, bounds)

precice_dt = p.initialize()
dt = precice_dt if precice_dt is not None else 0.01
print(f"dt={dt}")

temp = np.ones(n, dtype=np.float32) * 300.0
step = 0

while p.is_coupling_ongoing() and step < 5:
    if p.requires_writing_checkpoint():
        print("  [OpenFOAM] 写入检查点")
    
    step += 1
    
    power = p.read_data(mesh, "Power", list(range(n)), 0)
    p.write_data(mesh, "Temperature", list(range(n)), temp)
    
    print(f"步 {step}: P={power.mean():.2e}")
    
    if p.requires_reading_checkpoint():
        print("  [OpenFOAM] 读取检查点")
    
    dt = p.advance(dt)
    if dt is None:
        dt = 0.01

p.finalize()
print("OpenFOAM 完成")
