#!/bin/bash
cd /media/tb-xingliwei/PDE/nuclear-engine
rm -rf precice-run
python openmc_final.py > openmc.log 2>&1 &
python openfoam_final.py
