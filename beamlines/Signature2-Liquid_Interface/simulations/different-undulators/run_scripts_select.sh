#!/bin/bash


python simulation_2400_UE35.py
git add .
git commit -m 'python simulation_2400_UE35.py'
git push

python simulation_2400_UE65.py
git add .
git commit -m 'python simulation_2400_UE65.py'
git push    

python simulation_2400_IVU42.py
git add .
git commit -m 'python simulation_2400_IVU42.py'
git push