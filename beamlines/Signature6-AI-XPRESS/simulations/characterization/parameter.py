import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=1e5
rounds = 1


# Si111
fine_step = 50#0.1
medium_step = 50#10
big_step=50
e1   = np.arange(1950, 2150,fine_step) # iridium edge
e2   = np.arange(1800, 2000,50)
e3   = np.arange(23100, 23450,medium_step) # rhodium edge
e4   = np.arange(23450, 40000,big_step)
energy = np.concatenate((e1, e2, e3, e4))

si111_sim_name = 'AI-XPRESS_Si111'
si111_file_name  = 'AI-XPRESS_Si111'
si111_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     si111_file_name+'.rml')

si311_sim_name = 'AI-XPRESS_Si311'
si311_file_name  = 'AI-XPRESS_Si311'
si311_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     si311_file_name+'.rml')