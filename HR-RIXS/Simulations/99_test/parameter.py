import numpy as np

# Load in rml file 
# BESSY III:

rml_file_name_bessy3_HRRIXS_91m_errors_off  = 'HRRIXS_91m_no_err_no_refl'
rml_file_name_bessy3_HRRIXS_93m_errors_off  = 'HRRIXS_93m_no_err_no_refl'

# Paramter
order           = 2
SlitSize        = np.array([.0012]) # mm
grating         = np.array([2400])
cff             = np.array([25])
# bandwidth       = np.array([0.1])   # in %
# bandwidth_unit  = '%'               # % or eV

energy_flux = np.arange(100, 3100,5)

nrays_flux  = 1e5
nrays_rp    = 1e5

round_flux = 3

ncpu = 12
### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]