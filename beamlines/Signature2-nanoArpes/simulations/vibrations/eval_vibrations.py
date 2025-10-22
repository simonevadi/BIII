import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xrt.backends.raycing.materials as rm
 
from raypyng.postprocessing import PostProcessAnalyzed
from helper_lib import get_reflectivity
from parameter import SlitSize

##############################################################
# LOAD IN DATA

for amp in [0.0003, 0.003, 0.03]:

    this_file_dir=os.path.dirname(os.path.realpath(__file__))

    # Read Undulator CSV-File BESSY III
    undulator_table_filename = os.path.join(this_file_dir, 'undulator_flux_curves','b3_ue42_5_ver_300mA_flux.csv')
    undulator_df = pd.read_csv(undulator_table_filename)

    # BESSY III vert_PGM:
    BL_file_path = os.path.join(f'RAYPy_Simulation_vertical_PGM_vibration_{amp}', 'DetectorAtFocus_RawRaysOutgoing.csv')
    PGM_vert = pd.read_csv(BL_file_path)
    PGM_vert['PhotonEnergy'] +=50 # shift for visualization
    # BESSY III hor_PGM_M3Para:
    BL2_file_path = os.path.join(f'RAYPy_Simulation_horizontal_PGM_vibration_{amp}', 'DetectorAtFocus_RawRaysOutgoing.csv')
    PGM_hor = pd.read_csv(BL2_file_path)



    ##############################################################
    # PLOTTING AND ANALYSIS
    # Create the Main figure
    fig, (axs) = plt.subplots(2, 2, figsize=(20, 15))
    fig.suptitle(f'Comparison vibration for vertical/horizontal PGM, amplitude: {amp}', size=14)
    x_range = [50, 2150]

    # Smoothing the data
    window = 10
    step = 1






    harms = [1,3,5] # The Harmonics from the ID. Typically 1,3,5, rather higher. Depends on the FluxSims of the ID.

    # TRANSMITTED BANDWIDTH
    ax = axs[0, 0]


    ax.scatter(PGM_vert['PhotonEnergy'],
            PGM_vert['Bandwidth']*1000,
            label='Vertical PGM')

    ax.scatter(PGM_hor['PhotonEnergy'],
            PGM_hor['Bandwidth']*1000,
                label='Horizontal PGM')


    ax.set_title(f'Transmitted Bandwidth @ {int(SlitSize[0]*1000)} µm ExitSlit')
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Transmitted bandwidth [meV]')
    ax.legend(loc='best', fontsize=12)
    ax.set_xlim(x_range)
    ax.minorticks_on()
    ax.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



    # RESOLVING POWER
    ax = axs[0,1]


    ax.scatter(PGM_vert['PhotonEnergy'],
            (PGM_vert[f'PhotonEnergy']/PGM_vert[f'Bandwidth']))
    ax.scatter(PGM_hor['PhotonEnergy'],
            (PGM_hor[f'PhotonEnergy']/PGM_hor[f'Bandwidth']))

    ax.set_title(f'Resolving Power @ {int(SlitSize[0]*1000)} µm ExitSlit')
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel(r'$\frac{E}{\Delta E}$ [a.u.]')
    # ax.legend(loc='best', fontsize=12)
    ax.set_xlim(x_range)
    ax.minorticks_on()
    ax.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


    # Horizontal Focus Size
    ax = axs[1, 0]
    ax.scatter(PGM_vert['PhotonEnergy'], 
                PGM_vert['HorizontalCenter']*1000,
                label='Vertical PGM')
    ax.scatter(PGM_hor['PhotonEnergy'], 
                PGM_hor['HorizontalCenter']*1000,
                label='Horizontal PGM')

    ax.set_title('Horizontal Focus Size')
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('[µm]')
    ax.set_xlim(x_range)
    ax.minorticks_on()
    ax.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')

    ax.legend()
    # Vertical Focus Size
    ax = axs[1, 1]

    ax.scatter(PGM_vert['PhotonEnergy'], 
            PGM_vert['VerticalFocusFWHM']*1000)
    ax.scatter(PGM_hor['PhotonEnergy'],
            PGM_hor['VerticalFocusFWHM']*1000)

    ax.set_title('Vertical Focus Size')
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('[µm]')
    ax.set_xlim(x_range)
    ax.minorticks_on()
    ax.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')



    ##############################################################
    # SAVING
    # Ensure the "plot" folder exists
    plot_folder = 'plot'
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)

    # Save the the figure
    plt.tight_layout()
    plt.savefig(f'plot/vibrations_comparison_{amp}.pdf')
    plt.show()