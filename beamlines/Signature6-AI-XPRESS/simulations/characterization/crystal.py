import numpy as np
# path to xrt:
# import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials_crystals as rm
# safe import of tqdm

import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
)

from crystal_lib import calculate_dcm_efficiency
from parameter import energy_si111, energy_si311        
crystal = rm.Si(hkl=(1, 1, 1))
# calculate_dcm_efficiency(rm.Si(hkl=(1, 1, 1)),
#                          energy_si111,
#                          'Si111',
#                          savepath='plot/Si111',
#                          save_individuals=False,
#                          dtheta=np.linspace(-250, 500, 10000))

calculate_dcm_efficiency(rm.Si(hkl=(3, 1, 1)),
                         np.arange(1500, 10000, 100),
                         'Si311',
                         savepath='plot/Si311',
                         save_individuals=True,
                         dtheta=np.linspace(-250, 500, 10000))
