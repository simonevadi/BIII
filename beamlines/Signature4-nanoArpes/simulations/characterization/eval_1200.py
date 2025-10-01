import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm
import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
) 
from helper_lib import get_reflectivity
from parameter import SlitSize_300 as SlitSize
from parameter import undulator as undulator_df

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_nanoARPES_300', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)
cff = 2.5
BL_df = BL_df[BL_df['PG.cFactor']==cff]  
##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
fig, (axs) = plt.subplots(4, 2, figsize=(20, 15))
fig.suptitle(f'Signature4 - nanoARPES, 300 l/mm, cff={cff}', size=16)
x_range = [100,1000]

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
# Coatings:
de = 0.01
table = 'Henke'
theta = 0.75
E = np.arange(100, 1000, de)
Pt  = rm.Material('Pt',  rho=21.45, kind='mirror',table=table)

Pt, _ = get_reflectivity(Pt, E=E, theta=theta)

ax1.plot(E, Pt, 'r', label='Pt')

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
# ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



# FLUX CURVE UNDULATOR
#Choose the harmonic to plot
ax2 = axs[0, 1]

harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

for harm in harms:
    ax2.plot(undulator_df[f'Energy{harm}[eV]'], undulator_df[f'Photons{harm}'], label=f'Harm. {harm}')
    
ax2.set_title('UE65 HL Flux curve')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.01% BW]')
ax2.legend(fontsize=12, loc='best')
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# TRANSMITTED BANDWIDTH
ax3 = axs[1, 0]
window = 20
for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(mov_av(filtered_df['PhotonEnergy'], window),
             mov_av(filtered_df['Bandwidth']*1000, window),
             label=f'Harm. {harm}')

ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
ax3.legend(loc='best', fontsize=12)
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[1, 1]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'], label=f'Harm. {harm}')

ax4.set_title('Flux with UE65 HL')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.legend(loc='best', fontsize=12)
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.set_yscale('log')
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# RESOLVING POWER
ax5 = axs[2, 0]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax5.plot(mov_av(filtered_df['PhotonEnergy'],window),
             mov_av(filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth'],window),
             label=f'Harm. {harm}')

ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
ax5.legend(loc='best', fontsize=12)
ax5.set_xlim(x_range)
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax6 = axs[2, 1]
for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df['PhotonEnergy'],filtered_df[f'PhotonFlux{harm}']/foc_area, label=f'Harm. {harm}')

ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
ax6.legend(loc='best', fontsize=12)
ax6.set_xlim(x_range)
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Horizontal Focus Size
ax7 = axs[3, 0]

ax7.plot(mov_av(BL_df['PhotonEnergy'], window),
         mov_av(BL_df['HorizontalFocusFWHM']*1e6, window),
         label='Horizontal Focus Size', color='red')

ax7.set_title('Horizontal Focus Size')
ax7.set_xlabel('Energy [eV]')
ax7.set_ylabel('[nm]')
ax7.set_xlim(x_range)
ax7.minorticks_on()
ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Vertical Focus Size
ax8 = axs[3, 1]

ax8.plot(mov_av(BL_df['PhotonEnergy'], window),
         mov_av(BL_df['VerticalFocusFWHM']*1e6, window),
         label='Vertical Focus Size', color='limegreen')

ax8.set_title('Vertical Focus Size')
ax8.set_xlabel('Energy [eV]')
ax8.set_ylabel('[nm]')
ax8.set_xlim(x_range)
ax8.minorticks_on()
ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig(f'plot/nanoARPES_300_{cff}.png')
# plt.show()
