import numpy as np
from multilayer import MultilayerBragg



# ml = MultilayerBragg(('Cr', 7.19), 23, 
#                      ('C', 2.3), 27, 
#                      40, 
#                      save_recap="ELISA - CrC - 40 layers - test")

# theta, rs, rp, bragg_degs = ml.calculate_multilayer(1500,
#                                                     max_order=1,
#                                                     angle_range=(0, 20))  # up to 3rd Bragg order

# ml.plot_reflectivity_vs_theta(1500, theta, rs, rp, show_plot=False)

energies = np.arange(500, 8001, 500)  # 30 to 70 keV
# results_df = ml.calculate_reflectivity_vs_energy(energies, 
#                                                 order=1, 
#                                                 window_deg=0.5)

# ml.plot_reflectivity_vs_energy(show_plot=False)


# # W/Si multilayer
# ml_wsi = MultilayerBragg(('W', 19.3), 20, 
#                          ('Si', 2.33), 20, 
#                          40,
#                          save_recap="ELISA - WSi - 40 layers - test")

# results_df_wsi = ml_wsi.calculate_reflectivity_vs_energy(energies, 
#                                                          order=1, 
#                                                          window_deg=0.5)
# ml_wsi.plot_reflectivity_vs_energy(show_plot=False)

# Mo/Si multilayer
ml_mosi = MultilayerBragg(('Mo', 10.2), 20, 
                          ('Si', 2.33), 20, 
                          40,
                          save_recap="ELISA - MoSi - 40 layers - test")

results_df_mosi = ml_mosi.calculate_reflectivity_vs_energy(energies, 
                                                           order=1, 
                                                           window_deg=0.5)

ml_mosi.prepare_raypyng_efficiency_table('MoSi_efficiency')
ml_mosi.plot_reflectivity_vs_energy(show_plot=False)