#!/bin/bash

# Ask for sudo password upfront
# sudo -v



python simulation_2400.py
git add .
git commit -m 'sim sotexs 2400'
git push
python simulation_1200.py
git add .
git commit -m 'sim sotexs 1200'
git push
# python simulation_2400_multi_inc.py
# git add .
# git commit -m 'sim sotexs 2400 multi inc'
# git push


# git add .
# git commit -m 'sim'
# git push

# sudo reboot