import numpy as np

rml_file_name_bessy2_LoBeta_long_56_errors_on    = 'bessy2lo_56m_PGM_2Perc_coupling_errors_on'
rml_file_name_bessy2_HiBeta_long_56_errors_on    = 'bessy2hi_56m_PGM_2Perc_coupling_errors_on'
rml_file_name_bessy3_long_56_errors_on           = 'bessy3_56m_PGM_2Perc_coupling_errors_on'

rml_file_name_bessy2_LoBeta_long_56_errors_off   = 'bessy2lo_56m_PGM_2Perc_coupling_errors_off'
rml_file_name_bessy2_HiBeta_long_56_errors_off   = 'bessy2hi_56m_PGM_2Perc_coupling_errors_off'
rml_file_name_bessy3_long_56_errors_off          = 'bessy3_56m_PGM_2Perc_coupling_errors_off'


order       = 1
SlitSize    = np.array([.024, .016, .008])
grating     = np.array([1200])
cff         = np.array([2.5])

energy_flux = np.arange(100, 2101,50)
energy_rp   = np.arange(100, 2101,50)

nrays_flux  = 1e5
nrays_rp    = 1e5

round_flux = 10
round_rp   = 10


ncpu = 12
### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]
