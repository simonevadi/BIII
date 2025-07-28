#!/bin/bash

# Ask for sudo password upfront
sudo -v



# python simulation_2400_nano_b.py
# python simulation_2400_nano.py
# python simulation_2400.py

# python simulation_1200.py
# python simulation_1200_nano.py


python simulation_2400_nano_b_multi_inc.py
git add .
git commit -m 'sim'
git push

sudo reboot