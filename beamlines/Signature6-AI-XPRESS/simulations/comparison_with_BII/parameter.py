import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=1e6
rounds = 5


# Si111
fine_step = 1000
medium_step = 1000
big_step=1000
e1   = np.arange(2000, 10000,medium_step)
e1_b = np.arange(3900, 10000,medium_step)
e2   = np.arange(10000, 33000+1,big_step) # Rh edge
# e2   = np.arange(23100, 23450,fine_step) # Rh edge
energy_si111 = np.concatenate((e1, e2))
energy_si311 = np.concatenate((e1_b, e2))

si111_sim_name = 'MySpot_Si111_noM2'
si111_file_name  = 'mySpot_Si111_noM2_original'
si111_file_path  = os.path.join('rml',
                                     si111_file_name+'.rml')

si111_noPin_sim_name = 'MySpot_Si111_noM2_no_pinhole'
si111_noPin_file_name  = 'mySpot_Si111_noM2_no_pinhole'
si111_noPin_file_path  = os.path.join('rml',
                                     si111_file_name+'.rml')


# si311_sim_name = 'AI-XPRESS_Si311'
# si311_file_name  = 'AI-XPRESS_Si311'
# si311_file_path  = os.path.join(Path(__file__).resolve().parents[2],
#                                      'rml',
#                                      si311_file_name+'.rml')
