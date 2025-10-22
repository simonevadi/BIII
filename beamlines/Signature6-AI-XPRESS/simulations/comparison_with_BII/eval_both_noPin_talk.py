import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm
import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
)
from helper_lib import get_reflectivity

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

current_factor = 3
mrad_scale = 200
# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('..','characterization','RAYPy_Simulation_AI-XPRESS_Si111', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_si111 = pd.read_csv(BL_file_path)
BL_df_si111[f'SourcePhotonFlux'] = BL_df_si111[f'SourcePhotonFlux']*current_factor # for 300 mA
BL_df_si111[f'PhotonFlux'] = BL_df_si111[f'PhotonFlux']*current_factor # for 300 mA

myspot_Si111_path = os.path.join('RAYPy_Simulation_MySpot_Si111_noM2_no_pinhole', 'DetectorAtFocus_RawRaysOutgoing.csv')
myspot_Si111 = pd.read_csv(myspot_Si111_path)
myspot_Si111[f'SourcePhotonFlux'] = myspot_Si111[f'SourcePhotonFlux']*current_factor/mrad_scale # for 300 mA
myspot_Si111[f'PhotonFlux'] = myspot_Si111[f'PhotonFlux']*current_factor # for 300 mA

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 13})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison: AI-XPRESS @ BESSY III and MySPot @ BESSY II', size=16)
x_range = [2500, 40000]
colors = ['blue', 'red', 'green', 'orange', 'purple', 'violet']

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
de = 0.1
table = 'Chantler'
theta = 0.1
E = np.arange(500, x_range[-1], de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Rh  = rm.Material('Rh',  rho=12.423,  kind='mirror',table=table)
IrRh = rm.Multilayer(tLayer=Rh, tThickness=40, 
                        bLayer=Rh, bThickness=0, 
                        nPairs=1, substrate=Ir)

Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
Rh, _ = get_reflectivity(Rh, E=E, theta=theta)
IrRh, _ = get_reflectivity(IrRh, E=E, theta=theta)

ax1.plot(E, Ir, 'grey', label='Ir', alpha=0.5, linewidth=1.5)
ax1.plot(E, Rh, 'blue', label='Rh', alpha=0.5, linewidth=1.5)
ax1.plot(E, IrRh, 'black', label='IrRh', linewidth=5)

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# FLUX CURVE DIPOLE
#Choose the harmonic to plot
ax2 = axs[1]


ax2.plot(BL_df_si111[f'PhotonEnergy'],
            BL_df_si111[f'SourcePhotonFlux'],
            label='BIII SB 4T', 
            color='blue',
            linewidth=5)

ax2.plot(myspot_Si111[f'PhotonEnergy'],
            myspot_Si111[f'SourcePhotonFlux'],
            label='BII WS 7T',
            color='royalblue', 
            linestyle='dashed',
)


    
ax2.set_title('Source, Superbend 4T BIII vs Wavelength Shifter 7T BII')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax2.legend(loc='best')
ax2.set_xlim(x_range)
ax2.set_yscale('log')
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/AI_XPRESS_MySpot_comparison_noPinhole_1.png')
# plt.show()
plt.close()

fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison: AI-XPRESS @ BESSY III and MySPot @ BESSY II', size=16)
# TRANSMITTED BANDWIDTH
ax3 = axs[0]

window = 2

# Si111 BIII
ax3.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['Bandwidth'], window),
            label=f'BIII Si111', 
            color='blue', linewidth=5)    
# Si111 BII
ax3.plot(mov_av(myspot_Si111['PhotonEnergy'], window), 
            mov_av(myspot_Si111['Bandwidth'], window),
            label=f'BII Si111', 
            color='royalblue', 
            linestyle='dashed')    
 

ax3.set_title(f'Transmitted Bandwidth')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [eV]')
ax3.set_xlim(x_range)
ax3.minorticks_on()
# ax3.set_yscale('log')
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax3.legend(loc='lower right', ncol=2)


# BEAMLINE FLUX CURVE
ax4 = axs[1]

# BIII Si111
ax4.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['PhotonFlux'], window),
            label=f'BIII Si111', 
            color='blue', linewidth=5)    
# BII Si111
ax4.plot(mov_av(myspot_Si111['PhotonEnergy'], window), 
            mov_av(myspot_Si111['PhotonFlux'], window),
            label=f'BII Si111', 
            color='royalblue', linewidth=1, 
            linestyle = 'dashed')   

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_yscale('log')

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/AI_XPRESS_MySpot_comparison_noPinhole_2.png')
# plt.show()
plt.close()

fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison: AI-XPRESS @ BESSY III and MySPot @ BESSY II', size=16)





##############################################################
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('Comparison: AI-XPRESS @ BESSY III and MySPot @ BESSY II', size=16)
# RESOLVING POWER
ax3 = axs[0]

window = 2

# Si111 BIII
ax3.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['PhotonEnergy']/BL_df_si111['Bandwidth'], window),
            label=f'BIII Si111', 
            color='blue', linewidth=5)    
# Si111 BII
ax3.plot(mov_av(myspot_Si111['PhotonEnergy'], window), 
            mov_av(myspot_Si111['PhotonEnergy']/myspot_Si111['Bandwidth'], window),
            label=f'BII Si111', 
            color='royalblue', 
            linestyle='dashed')    
 

ax3.set_title(f'Resolving Power')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Resolving Power [a.u.]')
ax3.set_xlim(x_range)
ax3.minorticks_on()
# ax3.set_yscale('log')
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax3.legend(loc='lower right', ncol=2)


# BEAMLINE FLUX CURVE
ax4 = axs[1]

# BIII Si111
ax4.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['PhotonFlux'], window),
            label=f'BIII Si111', 
            color='blue', linewidth=5)    
# BII Si111
ax4.plot(mov_av(myspot_Si111['PhotonEnergy'], window), 
            mov_av(myspot_Si111['PhotonFlux'], window),
            label=f'BII Si111', 
            color='royalblue', linewidth=1, 
            linestyle = 'dashed')   

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_yscale('log')

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/AI_XPRESS_MySpot_comparison_noPinhole_3.png')
# plt.show()
plt.close()

