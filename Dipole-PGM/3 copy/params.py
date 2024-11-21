import numpy as np
import os

# BESSYIII params

# possible values for coupling
# 2, 10, 50, 75, 100
coupling = 2 
from params_B3 import b3_params as b3_params_all
b3_params = b3_params_all[coupling]

#   PARAMS FOR 1200l/mm GRATING SIMULATIONS
hb_1200_order       = 1
hb_1200_energy_flux = np.arange(50, 2551,10)
hb_1200_energy_rp   = np.arange(50, 2551,10)
hb_1200_SlitSize    = np.array([0.1])
hb_1200_grating     = np.array([1200])
hb_1200_blaze       = np.array([0.9])
hb_1200_cff         = np.array([2.25])
hb_1200_nrays_flux  = 2e5
hb_1200_nrays_rp    = 2e5 
hb_1200_rounds_flux = 50
hb_1200_rounds_rp   = 50
hb_1200_ncpu_flux   = 30
hb_1200_ncpu_rp     = 30

hb_1200_sim_name_flux = '1200_FLUX'
hb_1200_sim_name_rp   = '1200_RP'
hb_1200_rml_file_name = 'Dipole_PGM_1200'

this_file_dir   = os.path.dirname(os.path.realpath(__file__))
hb_1200_file_path   = os.path.join('rml/'+hb_1200_rml_file_name+'.rml')

#   PARAMS FOR 400l/mm GRATING SIMULATIONS
lb_400_order       = 1
lb_400_energy_flux = np.arange(30, 2551,10)
lb_400_energy_rp   = np.arange(30, 2551,10)
lb_400_SlitSize    = np.array([0.1])
lb_400_grating     = np.array([400])
lb_400_cff         = np.array([2.25])
lb_400_nrays_flux  = 2e5
lb_400_nrays_rp    = 2e5 
lb_400_rounds_flux = 50
lb_400_rounds_rp   = 50
lb_400_ncpu_flux   = 30
lb_400_ncpu_rp     = 30

lb_400_sim_name_flux = '400_FLUX'
lb_400_sim_name_rp   = '400_RP'
lb_400_rml_file_name = 'Dipole_PGM_400'

this_file_dir   = os.path.dirname(os.path.realpath(__file__))
lb_400_file_path   = os.path.join('rml/'+lb_400_rml_file_name+'.rml')


#   PARAMS FOR ML 2400l/mm GRATING SIMULATIONS
ml_order        = 2
ml_index        = 'MLBG_mfm_second'
ml_table        = os.path.join('ML_eff', 'grating_eff_5000.xlsx')
ml_energy_flux  = np.arange(500, 5001,500)
ml_energy_rp    = np.arange(500, 5001,500)
ml_SlitSize     = np.array([0.1])
ml_grating      = np.array([2400])
ml_nrays_flux   = 2e5
ml_nrays_rp     = 2e5 
ml_rounds_flux  = 50
ml_rounds_rp    = 50
ml_ncpu_flux    = 30
ml_ncpu_rp      = 30

ml_sim_name_rp     = '2400_RP'
ml_sim_name_flux   = '2400_FLUX'
ml_rml_file_name   = 'Dipole_PGM_2400_ML'

this_file_dir      = os.path.dirname(os.path.realpath(__file__))
ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')