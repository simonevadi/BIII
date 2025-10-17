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

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_AI-XPRESS_Si111', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_si111 = pd.read_csv(BL_file_path)
BL_file_path = os.path.join('RAYPy_Simulation_AI-XPRESS_Si111_LowDiv', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_si111_low = pd.read_csv(BL_file_path)
BL_file_path = os.path.join('RAYPy_Simulation_AI-XPRESS_Si311', 'DetectorAtFocus_RawRaysOutgoing.csv')
BL_df_si311 = pd.read_csv(BL_file_path)

##############################################################
# PLOTTING AND ANALYSIS
plt.rcParams.update({'font.size': 13})  # Change 14 to any size you prefer
# Create the Main figure
fig, (axs) = plt.subplots(4, 2, figsize=(20, 15))
fig.suptitle('Signature6 - AI-XPRESS', size=16)
x_range = [2500, 40000]
colors = ['blue', 'red', 'green', 'orange', 'purple', 'violet']

# MIRROR REFLECTIVITY
ax1 = axs[0, 0]
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
ax1.plot(E, IrRh, 'black', label='IrRh', linewidth=2)

ax1.set_title('Mirror Coating Reflectivity @ 'f'{theta}° incident angle')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel('Reflectivity [a.u.]')
ax1.legend()
ax1.set_xlim(x_range)
ax1.minorticks_on()
ax1.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# FLUX CURVE UNDULATOR
#Choose the harmonic to plot
ax2 = axs[0, 1]


ax2.plot(BL_df_si111[f'PhotonEnergy'],
            BL_df_si111[f'SourcePhotonFlux'])
    
ax2.set_title('Superbend 4T Flux curve')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Photon flux [ph/s/300 mA/0.1% BW]')
ax2.legend(loc='best')
ax2.set_xlim(x_range)
ax2.set_yscale('log')
ax2.minorticks_on()
ax2.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# TRANSMITTED BANDWIDTH
ax3 = axs[1, 0]

window = 5

# Si111
ax3.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['Bandwidth'], window),
            label=f'Si111')    
# Si311
ax3.plot(mov_av(BL_df_si311['PhotonEnergy'], window), 
            mov_av(BL_df_si311['Bandwidth'], window),
            label=f'Si311')    

# Si111 low
ax3.plot(mov_av(BL_df_si111_low['PhotonEnergy'], window), 
            mov_av(BL_df_si111_low['Bandwidth'], window),
            label=f'Si111 low div')  

ax3.set_title(f'Transmitted Bandwidth')
ax3.set_xlabel('Energy [eV]')
ax3.set_ylabel('Transmitted bandwidth [eV]')
ax3.set_xlim(x_range)
ax3.minorticks_on()
ax3.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax3.legend(loc='lower right', ncol=2)


# BEAMLINE FLUX CURVE
ax4 = axs[1, 1]

# Si111
ax4.plot(mov_av(BL_df_si111['PhotonEnergy'], window), 
            mov_av(BL_df_si111['PhotonFlux']*1000, window),
            label=f'Si111')    
# Si311
ax4.plot(mov_av(BL_df_si311['PhotonEnergy'], window), 
            mov_av(BL_df_si311['PhotonFlux']*1000, window),
            label=f'Si311')   

# Si111 low
ax4.plot(mov_av(BL_df_si111_low['PhotonEnergy'], window), 
            mov_av(BL_df_si111_low['PhotonFlux']*1000, window),
            label=f'Si111 low div')  

ax4.set_title('Flux at Focus')
ax4.set_xlabel('Energy [eV]')
ax4.set_ylabel('Photon flux [ph/s/300 mA/TBW]')
ax4.set_xlim(x_range)
ax4.minorticks_on()
ax4.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')
ax4.set_yscale('log')

# RESOLVING POWER
ax5 = axs[2, 0]
window = 20

# Si111
ax5.plot(mov_av(BL_df_si111['PhotonEnergy'], window),
         mov_av(BL_df_si111[f'PhotonEnergy']/BL_df_si111[f'Bandwidth'], window),
         linestyle='solid', label='Si111')

# Si311
ax5.plot(mov_av(BL_df_si311['PhotonEnergy'], window),
         mov_av(BL_df_si311[f'PhotonEnergy']/BL_df_si311[f'Bandwidth'], window),
         linestyle='solid', label='Si311')

# Si111
ax5.plot(mov_av(BL_df_si111_low['PhotonEnergy'], window),
         mov_av(BL_df_si111_low[f'PhotonEnergy']/BL_df_si111_low[f'Bandwidth'], window),
         linestyle='solid', label='Si111 low div')

ax5.set_title(f'Resolving Power')
ax5.set_xlabel('Energy [eV]')
ax5.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
ax5.set_xlim(x_range)
ax5.legend(loc='best')
ax5.minorticks_on()
ax5.set_ylim(0, 50000)
ax5.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


# Flux Density
ax6 = axs[2, 1]


# Si111
foc_area = (BL_df_si111['VerticalFocusFWHM']*BL_df_si111['HorizontalFocusFWHM'])*1000  # in µm²

ax6.plot(BL_df_si111['PhotonEnergy'],
             BL_df_si111[f'PhotonFlux']/foc_area,
             label=f'Si111')
    
# Si311
foc_area = (BL_df_si311['VerticalFocusFWHM']*BL_df_si311['HorizontalFocusFWHM'])*1000  # in µm²

ax6.plot(BL_df_si311['PhotonEnergy'],
             BL_df_si311[f'PhotonFlux']/foc_area,
             label=f'Si311')

# Si111 low
foc_area = (BL_df_si111_low['VerticalFocusFWHM']*BL_df_si111_low['HorizontalFocusFWHM'])*1000  # in µm²
ax6.plot(BL_df_si111_low['PhotonEnergy'],
             BL_df_si111_low[f'PhotonFlux']/foc_area,
             label=f'Si111 low div')

ax6.set_title('Flux Density')
ax6.set_xlabel('Energy [eV]')
ax6.set_ylabel('Photons flux per µm²')
ax6.set_xlim(x_range)
ax6.set_yscale('log')
ax6.minorticks_on()
ax6.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

####################################################
# Focus high div
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
axs[3, 0].set_visible(False)
ax7 = inset_axes(axs[3, 0], width="40%", height="100%", loc="lower left")
ax7_right = inset_axes(axs[3, 0], width="40%", height="100%", loc="lower right")

focus_path = os.path.join('plot', 'DetectorAtFocus-RawRaysOutgoing.csv')
focus = pd.read_csv(
    focus_path,
    sep='\t',        # columns separated by tabs
    decimal='.',     # use comma as decimal separator
    skiprows=1       # skip the first line (the 'sep=' line)
)
x = focus['DetectorAtFocus_OX'] * 1e3
y = focus['DetectorAtFocus_OY'] * 1e3


ax7.scatter(x,y, s=4, color='yellow', alpha=1)

ax7.set_facecolor('#002147')

# # get actual axes width/height in inches
# fig = ax7.figure
# bbox = ax7.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
# width, height = bbox.width, bbox.height

# # compute new symmetric xlim so µm/cm is same horizontally and vertically
# yrange = np.diff(ax7.get_ylim())[0]
# xrange_target = yrange * (width / height)
# x_half = xrange_target / 2
# ax7.set_xlim(-x_half/100*40, x_half/100*40)

ax7.set_xlim(-70, 70)
ax7.set_ylim(-70, 70)

ax7.set_xlabel('µm')
ax7.set_ylabel('µm')
hor_foc = np.mean(BL_df_si111['HorizontalFocusFWHM']*1e3)
ver_foc = np.mean(BL_df_si111['VerticalFocusFWHM']*1e3)
ax7.set_title(f'FWHM(HxV) {50:.0f} x {50:.0f} µm²')

####################################################
# Focus low div
focus_path = os.path.join('plot', 'lowDiv_DetectorAtFocus-RawRaysOutgoing.csv')
focus = pd.read_csv(
    focus_path,
    sep='\t',        # columns separated by tabs
    decimal='.',     # use comma as decimal separator
    skiprows=1       # skip the first line (the 'sep=' line)
)
x = focus['DetectorAtFocus_OX'].to_numpy() * 1e3
y = focus['DetectorAtFocus_OY'].to_numpy() * 1e3

# take only one every ten values
x = x[::10]
y = y[::10]

ax7_right.scatter(x,y, s=4, color='yellow', alpha=1)

ax7_right.set_facecolor('#002147')

# # get actual axes width/height in inches
# fig = ax7_right.figure
# bbox = ax7_right.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
# width, height = bbox.width, bbox.height

# # compute new symmetric xlim so µm/cm is same horizontally and vertically
# yrange = np.diff(ax7_right.get_ylim())[0]
# xrange_target = yrange * (width / height)
# x_half = xrange_target / 2
# ax7_right.set_xlim(-x_half/100*40, x_half/100*40)

ax7_right.set_xlim(-70, 70)
ax7_right.set_ylim(-70, 70)
ax7_right.set_xlabel('µm')
ax7_right.set_ylabel('µm')
hor_foc = np.mean(BL_df_si111['HorizontalFocusFWHM']*1e3)
ver_foc = np.mean(BL_df_si111['VerticalFocusFWHM']*1e3)
ax7_right.set_title(f'FWHM(HxV) {60:.0f} x {50:.0f} µm²')


# DCM efficiency
ax8 = axs[3, 1]
df_111 = pd.read_csv(os.path.join('plot','Si111', 'Si111.csv'))
df_311 = pd.read_csv(os.path.join('plot','Si311', 'Si311.csv'))
ax8.plot(df_111['Energy[eV]'], df_111['Reflectivity_2'], label='Si111: two crystal (conv)')
ax8.plot(df_311['Energy[eV]'], df_311['Reflectivity_2'], label='Si333: two crystal (conv)')
ax8.set_xlabel('Energy [eV]')
ax8.set_ylabel('Reflectivity [a.u.]')
ax8.set_title('Si111 and Si333 monochromator efficiency')
ax8.set_xlim(x_range)
ax8.legend()
# minor ticks and grid
ax8 = plt.gca()
ax8.minorticks_on()
ax8.grid(which='major', axis='both', linestyle='--', linewidth=0.5, color='lightgrey')
ax8.grid(which='minor', axis='both', linestyle=':', linewidth=0.5, color='lightgrey')
##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/AI_XPRESS.png')
# plt.show()
plt.close()


