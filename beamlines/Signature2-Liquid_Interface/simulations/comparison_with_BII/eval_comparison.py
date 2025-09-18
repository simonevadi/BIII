import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import pandas as pd

from parameter3 import SlitSize_2400 as SlitSize
from parameter3 import undulator as undulator_3

from raypyng.postprocessing import PostProcessAnalyzed

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('../characterization/RAYPy_Simulation_elisa_2400', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df = pd.read_csv(BL_file_path)

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_2400', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_2 = pd.read_csv(BL_file_path)
# define energy regions
BL_df_2 = BL_df_2[(BL_df_2['Dipole.photonEnergy'] >= 50) & (BL_df_2['Dipole.photonEnergy'] <= 3500)]

harms=[1,3,5]
##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 15})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(3, 2, figsize=(20, 15))
fig.suptitle('Comparison ELISA @ BESSY II and BESSY III, 2400 l/mm')
x_range = [500, 8000]


# TRANSMITTED BANDWIDTH
ax3 = axs[0, 0]

window = 20
colors = ['red', 'blue', 'green']
color_B2 = ['salmon', 'skyblue', 'lightgreen']
for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax3.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df['Bandwidth']*1000, window),
             color=colors[ind], linestyle='solid',
             label=f'B3-Harm. {harm}')
ax3.plot(mov_av(BL_df_2['PhotonEnergy'], window), 
            mov_av(BL_df_2['Bandwidth']*1000, window),
            color=color_B2[ind], linestyle='dashed',
            label=f'B2')


ax3.set_title(f'Transmitted Bandwidth @{int(SlitSize[0]*1000)} µm ExitSlit')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
ax3.legend(loc='best')
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[0, 1]
window = 1
for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(mov_av(filtered_df['PhotonEnergy'], window), 
             mov_av(filtered_df[f'PhotonFlux{harm}'], window),
             color=colors[ind], linestyle='solid',
             label=f'B3-Harm. {harm}')
ax4.plot(mov_av(BL_df_2['PhotonEnergy'], window), 
            mov_av(BL_df_2[f'PhotonFlux'], window),
            color=color_B2[ind], linestyle='dashed',
            label=f'B2')
    

ax4.set_title('Flux with CPMU21 at B3 and Dipole at B2')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.legend(loc='best')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_yscale('log')

# RESOLVING POWER
ax5 = axs[1, 0]
window = 20
for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    ax5.plot(mov_av(filtered_df['PhotonEnergy'], window),
             mov_av(filtered_df[f'PhotonEnergy']/filtered_df[f'Bandwidth'], window),
             color=colors[ind], linestyle='solid',
             label=f'B3-Harm. {harm}')
ax5.plot(mov_av(BL_df_2['PhotonEnergy'], window),
            mov_av(BL_df_2[f'PhotonEnergy']/BL_df_2[f'Bandwidth'], window),
            color=color_B2[ind], linestyle='dashed',
            label=f'B2')

ax5.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
ax5.legend(loc='best')
ax5.set_xlim(x_range)
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax6 = axs[1, 1]

for ind,harm in enumerate(harms):
    Emin_harm = undulator_3[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_3[f'Energy{harm}[eV]'].max()
    filtered_df = BL_df[(BL_df['PhotonEnergy'] >= Emin_harm) & (BL_df['PhotonEnergy'] <= Emax_harm)]
    foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000
    ax6.plot(filtered_df['PhotonEnergy'],
             filtered_df[f'PhotonFlux{harm}']/foc_area,
             color=colors[ind], linestyle='solid',
             label=f'B3-Harm. {harm}')
foc_area = (BL_df_2['VerticalFocusFWHM']*BL_df_2['HorizontalFocusFWHM'])*1000
ax6.plot(BL_df_2['PhotonEnergy'],
            BL_df_2[f'PhotonFlux']/foc_area,
            color=color_B2[ind], linestyle='dashed',
            label=f'B2')
    
ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
ax6.legend(loc='best')
ax6.set_xlim(x_range)
ax6.minorticks_on()
ax6.set_yscale('log')
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# Horizontal Focus Size
ax7 = axs[2, 0]
ax7.plot(mov_av(BL_df['PhotonEnergy'], window),
         mov_av(BL_df['HorizontalFocusFWHM']*1000, window),
         label='B3', color='red', linestyle='solid')

ax7.plot(mov_av(BL_df_2['PhotonEnergy'], window),
         mov_av(BL_df_2['HorizontalFocusFWHM']*1000, window),
         label='B2', color='lightgreen', linestyle='dashed')

ax7.set_title('Horizontal Focus Size')
ax7.set_xlabel('Energy [eV]')
ax7.set_ylabel('[µm]')
maxy=BL_df_2['HorizontalFocusFWHM'].max()*1000*1.1
miny=BL_df['HorizontalFocusFWHM'].min()*1000*0.9
ax7.set_ylim(miny, maxy)
# ax7.set_yscale('log')
ax7.set_xlim(x_range)
ax7.minorticks_on()
ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax7.yaxis.set_major_formatter(ScalarFormatter())
ax7.ticklabel_format(style='plain', axis='y')
ax7.legend(loc='best')
# Vertical Focus Size
ax8 = axs[2, 1]

ax8.plot(mov_av(BL_df['PhotonEnergy'], window),
         mov_av(BL_df['VerticalFocusFWHM']*1000, window),
         label='B3', color='red', linestyle='solid')

ax8.plot(mov_av(BL_df_2['PhotonEnergy'], window),
         mov_av(BL_df_2['VerticalFocusFWHM']*1000, window),
         label='B2', color='lightgreen', linestyle='dashed')

ax8.set_title('Vertical Focus Size')
ax8.set_xlabel('Energy [eV]')
ax8.set_ylabel('[µm]')
ax8.set_xlim(x_range)
maxy=BL_df_2['VerticalFocusFWHM'].max()*1000*1.1
miny=BL_df['VerticalFocusFWHM'].min()*1000*0.9
ax8.set_ylim(miny, maxy)
# ax8.set_ylim(0.01, 10.5)
# ax8.set_yscale('log')
ax8.minorticks_on()
ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax8.yaxis.set_major_formatter(ScalarFormatter())
ax8.ticklabel_format(style='plain', axis='y')
ax8.legend(loc='best')


##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/LiquidInterface_2400_comparison.png')
plt.show()
plt.close()

