import numpy as np
from multilayer import MultilayerBragg



ml = MultilayerBragg(('Cr', 7.19), 23, 
                     ('C', 2.3), 27, 
                     40, 
                     save_recap="ELISA - CrC - 40 layers - test")

energies = np.arange(500, 8001, 500)  # 30 to 70 keV


results_df_mosi = ml.calculate_reflectivity_vs_energy(energies, 
                                                           order=1, 
                                                           window_deg=0.5)

ml.prepare_raypyng_efficiency_table('CrC_efficiency', line_density=2400)
ml.plot_reflectivity_vs_energy(show_plot=False)