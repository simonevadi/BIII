import os
import numpy as np
import pandas as pd
from pathlib import Path

# Standard Simulation Parameters
this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu    = 12
nrays   = 1e5
rounds  = 10

#   PARAMS FOR BESSY III 56 m PGM-Standard Beamline SIMULATIONS
B3_energy                             = np.arange(100, 2101,5)
B3_SlitSize                           = np.array([.020]) # mm
B3_cff                                = np.array([2.25])
B3_Standard_PGM_56m_rml_file_name     = 'bessy3_56m_PGM_2Perc_coupl_0p75deg_1200l'
B3_sim_name                           = B3_Standard_PGM_56m_rml_file_name
B3_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     B3_Standard_PGM_56m_rml_file_name+'.rml')

#   PARAMS FOR Undulator BESSY III 56 m PGM-Standard Beamline SIMULATIONS
B3_undulator_file_path         = os.path.join(Path(__file__).resolve().parents[4],
                                           'undulators', 
                                           'UndulatorFiles_BESSY_III', 
                                           'undulator_flux_curves_SPECTRA',
                                           'UE42p5_b3_2PercCoupl_2025_smalerz_ver_300mA.csv')
B3_undulator = pd.read_csv(B3_undulator_file_path)


###################################################################################
# MultiLayer Simulation Parameters
#   PARAMS FOR BESSY III 56 m PGM-Standard Beamline with ML

B3_ML_order                              = 2
B3_ML_SlitSize                           = np.array([.020]) # mm
B3_ML_grating                            = np.array([2400])
B3_ML_Standard_PGM_56m_rml_file_name     = 'bessy3_56m_PGM_2Perc_coupl_0p75deg_2400l_ML'
B3_ML_sim_name                           = B3_ML_Standard_PGM_56m_rml_file_name
B3_ML_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                    'rml',
                                                    B3_ML_Standard_PGM_56m_rml_file_name+'.rml')


#   PARAMS FOR Undulator BESSY III 56 m PGM-Standard Beamline SIMULATIONS
B3_ML_undulator_file_path         = os.path.join(Path(__file__).resolve().parents[4],
                                           'undulators', 
                                           'UndulatorFiles_BESSY_III', 
                                           'undulator_flux_curves_SPECTRA',
                                           'IVUE28_b3_2PercCoupl_2025_smalerz_300mA.txt')
B3_ML_undulator = pd.read_csv(B3_ML_undulator_file_path, sep='\t')

# read grating and premirror efficiency for ML
grating_eff_path = os.path.join(Path(__file__).resolve().parents[4],
                                'multilayer_monochromator_efficiency',
                                'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat')
mirror_eff_path = os.path.join(Path(__file__).resolve().parents[4], 
                               'multilayer_monochromator_efficiency',
                               'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat')

grating = pd.read_csv(grating_eff_path,
                      sep='\s+')
mirror = pd.read_csv(mirror_eff_path,
                      sep='\s+')

# combine grating and pre-mirror efficiency, 
# interpolating if necessary, and save it in new dataframe called efficiency
ml_cff = grating['Cff'].to_numpy().flatten()
ml_energy = grating['Energy'].to_numpy().flatten()
if grating['Energy'].equals(mirror['Energy']):
    # If energy columns match, directly multiply
    efficiency = pd.DataFrame({
        'Energy[eV]': grating['Energy'],
        'Efficiency': grating['Efficiency(GR)'] * mirror['Efficiency(PM)']
    })
else:
    # Interpolate to a common energy range
    min_energy = max(grating['Energy'].min(), mirror['Energy'].min())
    max_energy = min(grating['Energy'].max(), mirror['Energy'].max())
    common_energy = np.linspace(min_energy, max_energy, num=1000)  # Define a common range

    grating_eff = np.interp(common_energy, grating['Energy'], grating['Efficiency(GR)'])
    mirror_eff = np.interp(common_energy, mirror['Energy'], mirror['Efficiency(PM)'])

    # Create a new DataFrame with interpolated values
    efficiency = pd.DataFrame({
        'Energy[eV]': common_energy,
        'Efficiency': grating_eff * mirror_eff
    })