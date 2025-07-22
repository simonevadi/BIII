import numpy as np

# Load in rml file 
# BESSY II:
rml_file_name_bessy2_LoBeta_37m    = 'bessy2lo_37m_PGM_2Perc_coupl_1p5deg_1200l'
rml_file_name_bessy2_HiBeta_37m    = 'bessy2hi_37m_PGM_2Perc_coupl_1p5deg_1200l'


# Paramter
order       = 1
SlitSize    = np.array([.020]) # mm
grating     = np.array([1200])
cff         = np.array([2.25])

energy_flux = np.arange(100, 2101,5)

nrays_flux  = 1e5
nrays_rp    = 1e5

round_flux = 10

ncpu = 12
### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]