import os
import numpy as np
import pandas as pd
from pathlib import Path

# Standard Simulation Parameters
this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu    = 12
nrays   = 1e6
rounds  = 2
HRRIXS_energy = np.arange(150, 2101, 5)  # eV
HRRIXS_order   = 2  # diffraction order
HRRIXS_cff     = 25
HRRIXS_SlitSize = np.array([.0012])  # mm   #NOTE: each BL has its own slit size, where the RP is max without reducing FLUX
HRRIXS_grating  = np.array([3000])  # lines/mm


#   PARAMS HRRIXS 91 m Version #1 SIMULATIONS
HRRIXS_V1_rml_file_name     = 'HRRIXS_91m_1'
HRRIXS_V1_sim_name                           = HRRIXS_V1_rml_file_name
HRRIXS_V1_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_V1_rml_file_name+'.rml')

#   PARAMS HRRIXS 91 m Version #2 SIMULATIONS
HRRIXS_V2_rml_file_name     = 'HRRIXS_91m_2'
HRRIXS_V2_sim_name                           = HRRIXS_V2_rml_file_name
HRRIXS_V2_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_V2_rml_file_name+'.rml')

#   PARAMS HRRIXS 91 m Version #3 SIMULATIONS
HRRIXS_V3_hor_rml_file_name     = 'HRRIXS_91m_3hor'
HRRIXS_V3_hor_sim_name                           = HRRIXS_V3_hor_rml_file_name
HRRIXS_V3_hor_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_V3_hor_rml_file_name+'.rml')

#   PARAMS HRRIXS 91 m Version #3_1 SIMULATIONS
HRRIXS_V4_hor_rml_file_name     = 'HRRIXS_91m_4hor'
HRRIXS_V4_hor_sim_name                           = HRRIXS_V4_hor_rml_file_name
HRRIXS_V4_hor_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_V4_hor_rml_file_name+'.rml')


#   PARAMS HRRIXS 100 m Version SIMULATIONS
HRRIXS_100m_1_rml_file_name     = 'HRRIXS_100m_1'
HRRIXS_100m_1_sim_name                           = HRRIXS_100m_1_rml_file_name
HRRIXS_100m_1_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_1_rml_file_name+'.rml')


#   PARAMS HRRIXS 100 m with short grating (250 mm) Version SIMULATIONS
HRRIXS_100m_1_SG_rml_file_name     = 'HRRIXS_100m_1_shortgrating'
HRRIXS_100m_1_SG_sim_name                           = HRRIXS_100m_1_SG_rml_file_name
HRRIXS_100m_1_SG_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_1_SG_rml_file_name+'.rml')


#   PARAMS HRRIXS 100 m with blaze grating (250 mm) Version SIMULATIONS
HRRIXS_100m_1_blaze_rml_file_name     = 'HRRIXS_100m_blaze'
HRRIXS_100m_1_blaze_sim_name                           = HRRIXS_100m_1_blaze_rml_file_name
HRRIXS_100m_1_blaze_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_1_blaze_rml_file_name+'.rml')

#   PARAMS HRRIXS 100 m with blaze grating (250 mm) Version SIMULATIONS
HRRIXS_100m_Wolter1_rml_file_name     = 'HRRIXS_100m_Wolter_1'
HRRIXS_100m_Wolter1_sim_name                           = HRRIXS_100m_Wolter1_rml_file_name
HRRIXS_100m_Wolter1_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_Wolter1_rml_file_name+'.rml')

#   PARAMS HRRIXS 100 m with blaze grating (250 mm) Version SIMULATIONS
HRRIXS_100m_Wolter1wovKP_rml_file_name     = 'HRRIXS_100m_Wolter_1_wo_vKB'
HRRIXS_100m_Wolter1wovKP_sim_name                           = HRRIXS_100m_Wolter1wovKP_rml_file_name
HRRIXS_100m_Wolter1wovKP_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_Wolter1wovKP_rml_file_name+'.rml')


#   PARAMS HRRIXS 108 m KB swaped (hor) SIMULATIONS
HRRIXS_108m_1hor_rml_file_name     = 'HRRIXS_108m_1hor'
HRRIXS_108m_1hor_sim_name                           = HRRIXS_108m_1hor_rml_file_name
HRRIXS_108m_1hor_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_108m_1hor_rml_file_name+'.rml')


###################################################################################
#   PARAMS FOR Undulator BESSY III UE42.5 by smalerz
HRRIXS_undulator_file_path  = os.path.abspath(
                            os.path.join(Path(__file__).resolve().parents[4], 
                            'undulators',
                            'UndulatorFiles_BESSY_III',
                            'Signature2-ELISA',
                            'Elisa-IVUE42-HL-1.csv')
                            )
HRRIXS_undulator = pd.read_csv(HRRIXS_undulator_file_path)



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