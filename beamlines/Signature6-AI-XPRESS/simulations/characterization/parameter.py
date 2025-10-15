import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=5e5
rounds = 1


# Si111
medium_step = 500
big_step=500
e1   = np.arange(2500, 4500,big_step)
e1_b = np.arange(4500, 23100,big_step)
e2   = np.arange(23100, 23450,medium_step) # Rh edge
e3   = np.arange(23450, 40000,big_step)
energy_si111 = np.concatenate((e1, e1_b, e2, e3))
energy_si311 = np.concatenate((e1, e1_b, e2, e3))

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