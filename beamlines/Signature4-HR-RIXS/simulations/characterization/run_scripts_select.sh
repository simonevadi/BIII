#!/bin/bash

python simulation_HRRIXS_6000.py
git add .
git commit -m'add HRRIXS 6000l/mm simulations'
git push

python simulation_HRRIXS_400.py
git add .
git commit -m'add HRRIXS 400l/mm simulations'
git push

python simulation_HRRIXS_1200.py
git add .
git commit -m'add HRRIXS 1200l/mm simulations'
git push