import numpy as np
import os
import pandas as pd
from pathlib import Path

from undulator.ivue31.spectra import ivue31_hl_coherent_flux as undulator_coherent
from undulator.ivue31.spectra import ivue31_hl as undulator


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 29
nrays=5e5
rounds = 20

energy = np.arange(300, 2201,10)
SlitSize = [0.03]
# PARAMS Vertical
energy_vertical = energy
SlitSize_vertical = SlitSize # mm
elisa_vertical_sim_name = 'coherence_vertical'
elisa_vertical_file_name  = 'coherence_vertical'
elisa_vertical_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     elisa_vertical_file_name+'.rml')


# PARAMS Vertical
energy_horizontal = energy
SlitSize_horizontal = SlitSize # mm
elisa_horizontal_sim_name = 'coherence_horizontal'
elisa_horizontal_file_name  = 'coherence_horizontal'
elisa_horizontal_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     elisa_horizontal_file_name+'.rml')






########################################################################################

# Multilayer efficiency
efficiency_path = os.path.join(Path(__file__).resolve().parents[4],
                                'multilayer_monochromator_efficiency',
                                'calculate_ml',
                                'ELISA - CrC - 40 layers', 
                                'CrC_efficiency.csv')


efficiency_2400 = pd.read_csv(efficiency_path)
efficiency_2400 = efficiency_2400[efficiency_2400['Energy[eV]']<=6000]
cff_2400    = efficiency_2400['cff'].to_numpy().flatten()
energy_2400 = efficiency_2400['Energy[eV]'].to_numpy().flatten()

