#!/bin/bash




python simulation_1200_Pt.py
git add .
git commit -m "sotexs BII simulation_1200_Pt"
git push origin main

python simulation_2400.py
git add .
git commit -m "sotexs BII simulation_2400"
git push origin main

