import numpy as np

# these must match the name of the rml files in the rml folder that you want to simulate

rml_file_name_bessy3_long_PGM_2Perc_coupling         = 'bessy3_long_52_PGM_out_2Perc_coupling'
rml_file_name_bessy3_long_PGM_10Perc_coupling        = 'bessy3_long_52_PGM_out_10Perc_coupling'

#rml_file_name_bessy3_short                          = 'bessy3_short_37'
#rml_file_name_bessy3_long_52_noRadProtect           = 'bessy3_long_52_noRadProtect'
#rml_file_name_bessy3_long_52_noRadProtect_closer    = 'bessy3_long_52"_noRadProtect_closer'
#rml_file_name_bessy2_HiBeta_short_37                = 'Bessy2_HiBeta_short_37'
#rml_file_name_bessy2_HiBeta_long_52                 = 'Bessy2_HiBeta_long_52'
#rml_file_name_bessy2_LoBeta_short_37                = 'Bessy2_LoBeta_short_37'
#rml_file_name_bessy2_LoBeta_long_52                 = 'Bessy2_LoBeta_long_52'




order       = 1
SlitSize    = np.array([.012, .010, .008])
grating     = np.array([600, 1200, 2400])
cff         = np.array([2.50, 25])

energy_flux = np.arange(100, 2001,50)
energy_rp   = np.arange(100, 2001,50)

nrays_flux  = 1e5
nrays_rp    = 1e5

round_flux = 5
round_rp   = 5

ncpu       = 9

### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]
