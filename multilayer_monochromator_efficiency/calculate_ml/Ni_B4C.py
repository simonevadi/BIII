import numpy as np
from multilayer import MultilayerBragg



energies = np.arange(500, 8001, 1)  # 30 to 70 keV

ml = MultilayerBragg(('Ni', 8.9), 21, 
                          ('C', 2.52), 24, 
                          40,
                          save_recap="Ni_B4C - 40 layers - test")

# theta, rs, rp, bragg_degs = ml.calculate_multilayer(energy_eV=500, max_order=1, angle_range=(0, 20))
# ml.plot_reflectivity_vs_theta(1500, theta, rs=rs, show_plot=True)


results_df_mosi = ml.calculate_reflectivity_vs_energy(energies, 
                                                           order=1, 
                                                           window_deg=.5)

ml.prepare_raypyng_efficiency_table('Ni_B4C_efficiency')
ml.plot_reflectivity_vs_energy(show_plot=False)