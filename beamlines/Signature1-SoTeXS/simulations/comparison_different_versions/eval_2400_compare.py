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
from parameter import SlitSize_2400 as SlitSize
from parameter import undulator as undulator_df

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# 3 micron
BL_file_path = os.path.join('RAYPy_Simulation_sotexs_2400_3micron', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_3 = pd.read_csv(BL_file_path)

# 3 micron
BL_file_path = os.path.join('RAYPy_Simulation_sotexs_2400_500nano', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_400 = pd.read_csv(BL_file_path)

# 3 micron
BL_file_path = os.path.join('RAYPy_Simulation_sotexs_2400_200nano', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_200 = pd.read_csv(BL_file_path)

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 25})  # Change 14 to any size you prefer


# Create the Main figure
fig, (ax1) = plt.subplots(1, 1, figsize=(30, 15))
fig.suptitle('SoTeXS, 2400 l/mm, coatings @ 0.4°')
x_range = [500, 8000]

# MIRROR REFLECTIVITY
de = 38.9579-30.0000
table = 'Henke'
theta = 0.4
E = np.arange(480, 8001, de)
Au  = rm.Material('Au',  rho=19.32, kind='mirror',table=table)
Pt  = rm.Material('Pt',  rho=21.45, kind='mirror',table=table)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C',   rho=2.52,  kind='mirror',table=table)
IrCrB4C = rm.Multilayer(tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)

Au, _ = get_reflectivity(Au, E=E, theta=theta)
Pt, _ = get_reflectivity(Pt, E=E, theta=theta)
Ir, _ = get_reflectivity(Ir, E=E, theta=theta)
Cr, _ = get_reflectivity(Cr, E=E, theta=theta)
B4C, _ = get_reflectivity(B4C, E=E, theta=theta)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)

ax1.plot(E, Au, 'gold', label='Au', alpha=0.5)
ax1.plot(E, Pt, 'dimgrey', label='Pt', alpha=0.5)
ax1.plot(E, Ir, 'lime', label='Ir', alpha=0.5)
ax1.plot(E, Cr, 'c', label='Cr', alpha=0.5)
ax1.plot(E, B4C, 'green', label='B4C', alpha=0.5)
ax1.plot(E, IrCrB4C, 'darkmagenta', label='IrCrB4C')

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

plt.tight_layout()
plt.savefig('plot/SoTeXS_2400_coatings.png')
# # FLUX CURVE UNDULATOR
# #Choose the harmonic to plot
# ax2 = axs[0, 1]

# harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

# for harm in harms:
#     ax2.plot(undulator_df[f'Energy{harm}[eV]'], undulator_df[f'Photons{harm}'], label=f'Harm. {harm}')
    
# ax2.set_title('CPMU21 Flux curve')
# ax2.set_xlabel('Energy [eV]')
# ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
# ax2.legend(fontsize=12, loc='best')
# ax2.set_xlim(x_range)
# ax2.minorticks_on()
# ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

# TRANSMITTED BANDWIDTH
fig, (axs) = plt.subplots(2, 2, figsize=(30, 15))
fig.suptitle('SoTeXS, 2400 l/mm')
ax3 = axs[0, 0]

window = 20
for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df_3 = BL_df_3[(BL_df_3['PhotonEnergy'] >= Emin_harm) & (BL_df_3['PhotonEnergy'] <= Emax_harm)]
    filtered_df_400 = BL_df_400[(BL_df_400['PhotonEnergy'] >= Emin_harm) & (BL_df_400['PhotonEnergy'] <= Emax_harm)]
    filtered_df_200 = BL_df_200[(BL_df_200['PhotonEnergy'] >= Emin_harm) & (BL_df_200['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(mov_av(filtered_df_3['PhotonEnergy'], window), 
             mov_av(filtered_df_3['Bandwidth']*1000, window),
             label=f'Harm. {harm}', color='blue')
    ax3.plot(mov_av(filtered_df_400['PhotonEnergy'], window), 
             mov_av(filtered_df_400['Bandwidth']*1000, window),
             label=f'Harm. {harm}', color='red')
    ax3.plot(mov_av(filtered_df_200['PhotonEnergy'], window), 
             mov_av(filtered_df_200['Bandwidth']*1000, window),
             label=f'Harm. {harm}', color='green')

ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
# ax3.legend(loc='best', fontsize=12)
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Manual legend for ax3
custom_lines = [
    Line2D([0], [0], color='blue', lw=2),
    Line2D([0], [0], color='red', lw=2),
    Line2D([0], [0], color='green', lw=2)
]
ax3.legend(custom_lines, ['3 µm²', '400 nm²', '200 nm²'], title='Focus Sze', loc='upper left', fontsize=20, title_fontsize=22)


# BEAMLINE FLUX CURVE
ax4 = axs[0, 1]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df_3 = BL_df_3[(BL_df_3['PhotonEnergy'] >= Emin_harm) & (BL_df_3['PhotonEnergy'] <= Emax_harm)]
    filtered_df_400 = BL_df_400[(BL_df_400['PhotonEnergy'] >= Emin_harm) & (BL_df_400['PhotonEnergy'] <= Emax_harm)]
    filtered_df_200 = BL_df_200[(BL_df_200['PhotonEnergy'] >= Emin_harm) & (BL_df_200['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df_3['PhotonEnergy'], filtered_df_3[f'PhotonFlux{harm}'], color='blue',label=f'Harm. {harm}')
    ax4.plot(filtered_df_400['PhotonEnergy'], filtered_df_400[f'PhotonFlux{harm}'], color='red',label=f'Harm. {harm}')
    ax4.plot(filtered_df_200['PhotonEnergy'], filtered_df_200[f'PhotonFlux{harm}'], color='green',label=f'Harm. {harm}')

ax4.set_title('Flux with CPMU21')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
# ax4.legend(loc='best', fontsize=12)
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.set_yscale('log')
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# RESOLVING POWER
ax5 = axs[1, 0]

for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df_3 = BL_df_3[(BL_df_3['PhotonEnergy'] >= Emin_harm) & (BL_df_3['PhotonEnergy'] <= Emax_harm)]
    filtered_df_400 = BL_df_400[(BL_df_400['PhotonEnergy'] >= Emin_harm) & (BL_df_400['PhotonEnergy'] <= Emax_harm)]
    filtered_df_200 = BL_df_200[(BL_df_200['PhotonEnergy'] >= Emin_harm) & (BL_df_200['PhotonEnergy'] <= Emax_harm)]
    ax5.plot(mov_av(filtered_df_3['PhotonEnergy'], window),
             mov_av(filtered_df_3[f'PhotonEnergy']/filtered_df_3[f'Bandwidth'], window),
             label=f'Harm. {harm}', color='red')
    ax5.plot(mov_av(filtered_df_400['PhotonEnergy'], window),
             mov_av(filtered_df_400[f'PhotonEnergy']/filtered_df_400[f'Bandwidth'], window),
             label=f'Harm. {harm}', color='blue')
    ax5.plot(mov_av(filtered_df_200['PhotonEnergy'], window),
             mov_av(filtered_df_200[f'PhotonEnergy']/filtered_df_200[f'Bandwidth'], window),
             label=f'Harm. {harm}', color='green')
    
ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
# ax5.legend(loc='best', fontsize=12)
ax5.set_xlim(x_range)
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



# Flux Density
ax6 = axs[1, 1]
for harm in harms:
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df_3 = BL_df_3[(BL_df_3['PhotonEnergy'] >= Emin_harm) & (BL_df_3['PhotonEnergy'] <= Emax_harm)]
    filtered_df_400 = BL_df_400[(BL_df_400['PhotonEnergy'] >= Emin_harm) & (BL_df_400['PhotonEnergy'] <= Emax_harm)]
    filtered_df_200 = BL_df_200[(BL_df_200['PhotonEnergy'] >= Emin_harm) & (BL_df_200['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df_3['VerticalFocusFWHM']*filtered_df_3['HorizontalFocusFWHM'])*1000  # in µm²
    ax6.plot(filtered_df_3['PhotonEnergy'],filtered_df_3[f'PhotonFlux{harm}']/foc_area, 
             label=f'Harm. {harm}', color='red')
    ax6.plot(filtered_df_400['PhotonEnergy'],filtered_df_400[f'PhotonFlux{harm}']/foc_area, 
             label=f'Harm. {harm}', color='blue')
    ax6.plot(filtered_df_200['PhotonEnergy'],filtered_df_200[f'PhotonFlux{harm}']/foc_area, 
             label=f'Harm. {harm}', color='green')
    
ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
# ax6.legend(loc='best', fontsize=12)
ax6.set_xlim(x_range)
ax6.set_yscale('log')
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# # Horizontal Focus Size
# ax7 = axs[3, 0]
# ax7.plot(mov_av(BL_df_3['PhotonEnergy'], window),
#          mov_av(BL_df_3['HorizontalFocusFWHM']*1000, window),
#          label='Horizontal Focus Size', color='red')
# ax7.plot(mov_av(BL_df_400['PhotonEnergy'], window),
#          mov_av(BL_df_400['HorizontalFocusFWHM']*1000, window),
#          label='Horizontal Focus Size', color='blue')
# ax7.plot(mov_av(BL_df_200['PhotonEnergy'], window),
#          mov_av(BL_df_200['HorizontalFocusFWHM']*1000, window),
#          label='Horizontal Focus Size', color='green')


# ax7.set_title('Horizontal Focus Size')
# ax7.set_xlabel('Energy [eV]')
# ax7.set_ylabel('[µm]')
# ax7.set_xlim(x_range)
# ax7.minorticks_on()
# ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# # Vertical Focus Size
# ax8 = axs[3, 1]

# ax8.plot(mov_av(BL_df_3['PhotonEnergy'], window),
#          mov_av(BL_df_3['VerticalFocusFWHM']*1000, window),
#          label='Vertical Focus Size', color='red')
# ax8.plot(mov_av(BL_df_400['PhotonEnergy'], window),
#          mov_av(BL_df_400['VerticalFocusFWHM']*1000, window),
#          label='Vertical Focus Size', color='blue')
# ax8.plot(mov_av(BL_df_200['PhotonEnergy'], window),
#          mov_av(BL_df_200['VerticalFocusFWHM']*1000, window),
#          label='Vertical Focus Size', color='green')

# ax8.set_title('Vertical Focus Size')
# ax8.set_xlabel('Energy [eV]')
# ax8.set_ylabel('[µm]')
# ax8.set_xlim(x_range)
# ax8.minorticks_on()
# ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/SoTeXS_2400_compare.png')
# plt.show()
