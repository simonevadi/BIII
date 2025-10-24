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

from parameter import HRRIXS_undulator as undulator_df


##############################################################
# LOAD IN DATA

# 1200 flux
BL_file_path = os.path.join('RAYPy_Simulation_HRRIXS_100m_c5_1200lpmm_Wolter_1_mono', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_f_1200 = pd.read_csv(BL_file_path)
BL_f_1200_18 = BL_f_1200[(BL_f_1200['PG.cFactor'] == 1.8)].copy()
BL_f_1200_5 = BL_f_1200[(BL_f_1200['PG.cFactor'] == 5)].copy()
BL_f_1200_10 = BL_f_1200[(BL_f_1200['PG.cFactor'] == 10)].copy()

# 1200 rp
BL_file_path = os.path.join('RAYPy_Simulation_HRRIXS_100m_c5_1200lpmm_Wolter_1_mono', 'ExitSlit_RawRaysOutgoing.csv')
BL_rp_1200 = pd.read_csv(BL_file_path)
BL_rp_1200_18 = BL_rp_1200[(BL_rp_1200['PG.cFactor'] == 1.8)].copy()
BL_rp_1200_5 = BL_rp_1200[(BL_rp_1200['PG.cFactor'] == 5)].copy()
BL_rp_1200_10 = BL_rp_1200[(BL_rp_1200['PG.cFactor'] == 10)].copy()

# 400 flux
BL_file_path = os.path.join('RAYPy_Simulation_HRRIXS_100m_c5_400lpmm_Wolter_1_mono', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_f_400 = pd.read_csv(BL_file_path)

# 400 rp
BL_file_path = os.path.join('RAYPy_Simulation_HRRIXS_100m_c5_400lpmm_Wolter_1_mono', 'ExitSlit_RawRaysOutgoing.csv')
BL_rp_400 = pd.read_csv(BL_file_path)

# 6000 flux
BL_file_path = os.path.join('RAYPy_Simulation_HRRIXS_100m_c20_6000lpmm_Wolter_1_mono', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_f_6000 = pd.read_csv(BL_file_path)

# 6000 rp
BL_file_path = os.path.join('RAYPy_Simulation_HRRIXS_100m_c20_6000lpmm_Wolter_1_mono', 'ExitSlit_RawRaysOutgoing.csv')
BL_rp_6000 = pd.read_csv(BL_file_path)


# Normalize the data Bandwidth to 0.1 %
norm_BW = 0.1   # in %
sim_BW_400 = 0.002  # in %
sim_BW_1200 = 0.002  # in %
sim_BW_6000 = 0.0002  # in %

bw_correction_400 = norm_BW / sim_BW_400  #Factor to normalize the Flux regarding the Bandwidth which used to accelaret the simulation
bw_correction_1200 = norm_BW / sim_BW_1200  #Factor to normalize the Flux regarding the Bandwidth which used to accelaret the simulation
bw_correction_6000 = norm_BW / sim_BW_6000  #Factor to normalize the Flux regarding the Bandwidth which used to accelaret the simulation

for harm in [1,3,5,7,9]:
    BL_rp_1200_18.loc[:, f'PhotonFlux{harm}'] = BL_rp_1200_18[f'PhotonFlux{harm}']/bw_correction_1200
    BL_rp_1200_5.loc[:, f'PhotonFlux{harm}'] = BL_rp_1200_5[f'PhotonFlux{harm}']/bw_correction_1200
    BL_rp_1200_10.loc[:, f'PhotonFlux{harm}'] = BL_rp_1200_10[f'PhotonFlux{harm}']/bw_correction_1200
    BL_rp_400.loc[:, f'PhotonFlux{harm}'] = BL_rp_400[f'PhotonFlux{harm}']/bw_correction_400
    BL_rp_6000.loc[:, f'PhotonFlux{harm}'] = BL_rp_6000[f'PhotonFlux{harm}']/bw_correction_6000

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 15})  # Change 14 to any size you prefer
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 3

# Create the Main figure
fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('HR-RIXS @ BESSY III', size=16)
x_range = [50, 2150]
colors = ['red', 'magenta', 'orange', 'blue', 'green']
colors_harm = ['red', 'blue', 'green']

ls = ['solid', 'dashed', 'dotted']

# Smoothing the data
window = 1
step = 1

BL_f_1200_18  = BL_f_1200_18.rolling(window=window, step=step).mean()   
BL_f_1200_5   = BL_f_1200_5.rolling(window=window, step=step).mean()   
BL_f_1200_10  = BL_f_1200_10.rolling(window=window, step=step).mean()   
BL_rp_1200_18  = BL_f_1200_18.rolling(window=window, step=step).mean()   
BL_rp_1200_5   = BL_f_1200_5.rolling(window=window, step=step).mean()   
BL_rp_1200_10  = BL_f_1200_10.rolling(window=window, step=step).mean() 
BL_rp_400  = BL_rp_400.rolling(window=window, step=step).mean() 

# MIRROR REFLECTIVITY
ax1 = axs[0]
# Coatings:
de = 38.9579-30.0000
table = 'Henke'
theta = 0.75
E = np.arange(50, 5001, de)
Au  = rm.Material('Au',  rho=19.32, kind='mirror',table=table)
Pt  = rm.Material('Pt',  rho=21.45, kind='mirror',table=table)


Au, _ = get_reflectivity(Au, E=E, theta=theta)
Pt, _ = get_reflectivity(Pt, E=E, theta=theta)

# ax1.plot(E, Au, 'b', label='Au')
ax1.plot(E, Pt, 'r', 'silver', label='Pt', linewidth=5)

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



# FLUX CURVE UNDULATOR
#Choose the harmonic to plot
ax2 = axs[1]

harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

for ind,harm in enumerate(harms):
    ax2.plot(undulator_df[f'Energy{harm}[eV]'], undulator_df[f'Photons{harm}'],
             linestyle=ls[ind], color=colors_harm[ind],
             label=f'Harm. {harm}', linewidth=3)
    
ax2.set_title('IVUE42')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax2.legend(fontsize=12, loc='best')
ax2.set_xlim(x_range)
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/HRRIXS_1.pdf')
plt.savefig('plot/talk/HRRIXS_1.png', dpi=600)


fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('HR-RIXS @ BESSY III', size=16)

# TRANSMITTED BANDWIDTH
ax3 = axs[0]

# 1200 1.8 20
ax3.plot(BL_rp_1200_18['PhotonEnergy'],BL_rp_1200_18['Bandwidth']*1000,
         label=f'1200l/mm, cff 1.8, ES=20µm',
         color=colors[0])
# 1200 5 5
ax3.plot(BL_rp_1200_5['PhotonEnergy'],BL_rp_1200_5['Bandwidth']*1000,
         label=f'1200l/mm, cff 5, ES=5µm',
         color=colors[1])
# 1200 10 2.5
ax3.plot(BL_rp_1200_10['PhotonEnergy'],BL_rp_1200_10['Bandwidth']*1000,
         label=f'1200l/mm, cff 10, ES=2.5µm',
         color=colors[2])
# 400 1.6 20
ax3.plot(BL_rp_400['PhotonEnergy'],BL_rp_400['Bandwidth']*1000,
         label=f'400l/mm, cff 1.6, ES=20µm',
         color=colors[3], linestyle='dashed')

# 6000 20 1
ax3.plot(BL_rp_6000['PhotonEnergy'],BL_rp_6000['Bandwidth']*1000,
         label=f'6000l/mm, cff 25, ES=1',
         color=colors[4])

ax3.set_title(f'Transmitted Bandwidth')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [meV]')
ax3.legend(loc='best', fontsize=12)
ax3.set_xlim(x_range)
# ax3.set_yscale('log')
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# BEAMLINE FLUX CURVE
ax4 = axs[1]

# 1200 1.8 20
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_1200_18[(BL_f_1200_18['PhotonEnergy'] >= Emin_harm) & (BL_f_1200_18['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[0],
             label=f'1200l/mm, cff 1.8, ES=20µm')

# 1200 5 5
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_1200_5[(BL_f_1200_5['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_1200_5['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[1],
             label=f'1200l/mm, cff 5, ES=5µm')
# 1200 10 2.5
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_1200_10[(BL_f_1200_10['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_1200_10['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[2],
             label=f'1200l/mm, cff 10, ES=2.5µm')

# 400 1.6 20
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_400[(BL_f_400['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_400['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[3],
             label=f'400l/mm, cff 1.6, ES=20µm')
    
# 6000 20 1
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_6000[(BL_f_6000['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_6000['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[4],
             label=f'6000l/mm, cff 25, ES=1')
    
ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA in TBW]')
ax4.set_yscale('log')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/HRRIXS_2.pdf')
plt.savefig('plot/talk/HRRIXS_2.png', dpi=600)




fig, (axs) = plt.subplots(1, 2, figsize=(20, 7))
fig.suptitle('HR-RIXS @ BESSY III', size=16)

# RESOLVING POWER
ax5 = axs[0]

# 1200 1.8 20
ax5.plot(BL_rp_1200_18['PhotonEnergy'],
         BL_rp_1200_18['PhotonEnergy']/BL_rp_1200_18['Bandwidth'],
         label=f'1200l/mm, cff 1.8, ES=20µm',
         color=colors[0])
# 1200 5 5
ax5.plot(BL_rp_1200_5['PhotonEnergy'],
         BL_rp_1200_5['PhotonEnergy']/BL_rp_1200_5['Bandwidth'],
         label=f'1200l/mm, cff 5, ES=5µm',
         color=colors[1])
# 1200 10 2.5
ax5.plot(BL_rp_1200_10['PhotonEnergy'],
         BL_rp_1200_10['PhotonEnergy']/BL_rp_1200_10['Bandwidth'],
         label=f'1200l/mm, cff 10, ES=2.5µm',
         color=colors[2])

# 400 1.6 20
ax5.plot(BL_rp_400['PhotonEnergy'],
         BL_rp_400['PhotonEnergy']/BL_rp_400['Bandwidth'],
         label=f'400l/mm, cff 1.6, ES=20µm',
         color=colors[3], linestyle='dashed')

# 6000 20 1
ax5.plot(BL_rp_6000['PhotonEnergy'],
         BL_rp_6000['PhotonEnergy']/BL_rp_6000['Bandwidth'],
         label=f'6000l/mm, cff 25, ES=1',
         color=colors[4])

ax5.set_title(f'Resolving Power')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
ax5.legend(loc='best', fontsize=12)
ax5.set_xlim(x_range)
# ax5.set_yscale('log')
ax5.minorticks_on()
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



# BEAMLINE FLUX CURVE
ax4 = axs[1]

# 1200 1.8 20
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_1200_18[(BL_f_1200_18['PhotonEnergy'] >= Emin_harm) & (BL_f_1200_18['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[0],
             label=f'1200l/mm, cff 1.8, ES=20µm')

# 1200 5 5
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_1200_5[(BL_f_1200_5['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_1200_5['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[1],
             label=f'1200l/mm, cff 5, ES=5µm')
# 1200 10 2.5
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_1200_10[(BL_f_1200_10['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_1200_10['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[2],
             label=f'1200l/mm, cff 10, ES=2.5µm')

# 400 1.6 20
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_400[(BL_f_400['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_400['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[3],
             label=f'400l/mm, cff 1.6, ES=20µm')
    
# 6000 20 1
for ind, harm in enumerate(harms):
    Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
    Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
    filtered_df = BL_f_6000[(BL_f_6000['PhotonEnergy'] >= Emin_harm) & 
                              (BL_f_6000['PhotonEnergy'] <= Emax_harm)]
    ax4.plot(filtered_df['PhotonEnergy'], filtered_df[f'PhotonFlux{harm}'],
             linestyle=ls[ind], color=colors[4],
             label=f'6000l/mm, cff 25, ES=1')
    
ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA in TBW]')
ax4.set_yscale('log')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/talk/HRRIXS_3.pdf')
plt.savefig('plot/talk/HRRIXS_3.png', dpi=600)



# # RESOLVING POWER
# ax5 = axs[2, 0]

# # 1200 1.8 20
# ax5.plot(BL_rp_1200_18['PhotonEnergy'],
#          BL_rp_1200_18['PhotonEnergy']/BL_rp_1200_18['Bandwidth'],
#          label=f'1200l/mm, cff 1.8, ES=20µm',
#          color=colors[0])
# # 1200 5 5
# ax5.plot(BL_rp_1200_5['PhotonEnergy'],
#          BL_rp_1200_5['PhotonEnergy']/BL_rp_1200_5['Bandwidth'],
#          label=f'1200l/mm, cff 5, ES=5µm',
#          color=colors[1])
# # 1200 10 2.5
# ax5.plot(BL_rp_1200_10['PhotonEnergy'],
#          BL_rp_1200_10['PhotonEnergy']/BL_rp_1200_10['Bandwidth'],
#          label=f'1200l/mm, cff 10, ES=2.5µm',
#          color=colors[2])

# # 400 1.6 20
# ax5.plot(BL_rp_400['PhotonEnergy'],
#          BL_rp_400['PhotonEnergy']/BL_rp_400['Bandwidth'],
#          label=f'400l/mm, cff 1.6, ES=20µm',
#          color=colors[3])

# # 6000 20 1
# ax5.plot(BL_rp_6000['PhotonEnergy'],
#          BL_rp_6000['PhotonEnergy']/BL_rp_6000['Bandwidth'],
#          label=f'6000l/mm, cff 25, ES=1',
#          color=colors[4])

# ax5.set_title(f'Resolving Power')
# ax5.set_xlabel('Energy [eV]')
# ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
# ax5.legend(loc='best', fontsize=12)
# ax5.set_xlim(x_range)
# # ax5.set_yscale('log')
# ax5.minorticks_on()
# ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# # Flux Density
# ax6 = axs[2, 1]

# # 1200 1.8 20
# for ind, harm in enumerate(harms):
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_f_1200_18[(BL_f_1200_18['PhotonEnergy'] >= Emin_harm) & (BL_f_1200_18['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
#     ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}'])/foc_area,
#              linestyle=ls[ind], color=colors[0],
#              label=f'1200l/mm, cff 1.8, ES=20µm')

# # 1200 5 5
# for ind, harm in enumerate(harms):
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_f_1200_5[(BL_f_1200_5['PhotonEnergy'] >= Emin_harm) & 
#                               (BL_f_1200_5['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
#     ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}'])/foc_area,
#              linestyle=ls[ind], color=colors[1],
#              label=f'1200l/mm, cff 5, ES=5µm')
# # 1200 10 2.5
# for ind, harm in enumerate(harms):
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_f_1200_10[(BL_f_1200_10['PhotonEnergy'] >= Emin_harm) & 
#                               (BL_f_1200_10['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
#     ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}'])/foc_area,
#              linestyle=ls[ind], color=colors[2],
#              label=f'1200l/mm, cff 10, ES=2.5µm')
# # 400 1.6 20
# for ind, harm in enumerate(harms):
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_f_400[(BL_f_400['PhotonEnergy'] >= Emin_harm) & 
#                               (BL_f_400['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
#     ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}'])/foc_area,
#              linestyle=ls[ind], color=colors[3],
#              label=f'400l/mm, cff 1.6, ES=20µm')

# # 6000 20 1
# for ind, harm in enumerate(harms):
#     Emin_harm = undulator_df[f'Energy{harm}[eV]'].min()
#     Emax_harm = undulator_df[f'Energy{harm}[eV]'].max()
#     filtered_df = BL_f_6000[(BL_f_6000['PhotonEnergy'] >= Emin_harm) & 
#                               (BL_f_6000['PhotonEnergy'] <= Emax_harm)]
#     foc_area = (filtered_df['VerticalFocusFWHM']*filtered_df['HorizontalFocusFWHM'])*1000  # in µm²
#     ax6.plot(filtered_df['PhotonEnergy'],(filtered_df[f'PhotonFlux{harm}'])/foc_area,
#              linestyle=ls[ind], color=colors[4],
#              label=f'6000l/mm, cff 25, ES=1')

# ax6.set_title('Flux Density on sample')
# ax6.set_xlabel('Energy [eV]')
# ax6.set_ylabel('Photons flux per µm²')
# ax6.set_yscale('log')
# ax6.set_xlim(x_range)
# ax6.minorticks_on()
# ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# # Horizontal Focus Size
# ax7 = axs[3, 0]

# ax7.plot(BL_f_1200_18['PhotonEnergy'],BL_f_1200_18['HorizontalFocusFWHM']*1000, 
#          color=colors[0], label=f'1200l/mm, cff 1.8, ES=20µm')

# ax7.plot(BL_f_1200_5['PhotonEnergy'],BL_f_1200_5['HorizontalFocusFWHM']*1000, 
#          color=colors[1], label=f'1200l/mm, cff 5, ES=5µm')

# ax7.plot(BL_f_1200_10['PhotonEnergy'],BL_f_1200_10['HorizontalFocusFWHM']*1000, 
#          color=colors[2], label=f'1200l/mm, cff 10, ES=2.5µm')

# # 400 1.6 20
# ax7.plot(BL_f_400['PhotonEnergy'],BL_f_400['HorizontalFocusFWHM']*1000, 
#          color=colors[3], label=f'400l/mm, cff 1.6, ES=20µm')

# # 6000 20 1
# ax7.plot(BL_f_6000['PhotonEnergy'],BL_f_6000['HorizontalFocusFWHM']*1000, 
#          color=colors[4], label=f'6000l/mm, cff 25, ES=1')

# ax7.set_title('Horizontal Focus Size')
# ax7.set_xlabel('Energy [eV]')
# ax7.set_ylabel('[µm]')
# ax7.set_xlim(x_range)
# ax7.minorticks_on()
# ax7.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

# # Vertical Focus Size
# ax8 = axs[3, 1]

# ax8.plot(BL_f_1200_18['PhotonEnergy'],BL_f_1200_18['VerticalFocusFWHM']*1000, 
#          color=colors[0], label=f'1200l/mm, cff 1.8, ES=20µm')

# ax8.plot(BL_f_1200_5['PhotonEnergy'],BL_f_1200_5['VerticalFocusFWHM']*1000, 
#          color=colors[1], label=f'1200l/mm, cff 5, ES=5µm')

# ax8.plot(BL_f_1200_10['PhotonEnergy'],BL_f_1200_10['VerticalFocusFWHM']*1000, 
#          color=colors[2], label=f'1200l/mm, cff 10, ES=2.5µm')

# # 400 1.6 20
# ax8.plot(BL_f_400['PhotonEnergy'],BL_f_400['VerticalFocusFWHM']*1000, 
#          color=colors[3], label=f'400l/mm, cff 1.6, ES=20µm')

# # 6000 20 1
# ax8.plot(BL_f_6000['PhotonEnergy'],BL_f_6000['VerticalFocusFWHM']*1000, 
#          color=colors[4], label=f'6000l/mm, cff 25, ES=1')

# ax8.set_title('Vertical Focus Size')
# ax8.set_xlabel('Energy [eV]')
# ax8.set_ylabel('[µm]')
# ax8.set_xlim(x_range)
# ax8.minorticks_on()
# ax8.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# ##############################################################
# # SAVING
# # Ensure the "plot" folder exists
# plot_folder = 'plot'
# if not os.path.exists(plot_folder):
#     os.makedirs(plot_folder)

# # Save the the figure
# plt.tight_layout()
# plt.savefig('plot/HRRIXS_100m_1.pdf')
# plt.savefig('plot/HRRIXS_100m_1.png', dpi=600)
# # plt.show()
