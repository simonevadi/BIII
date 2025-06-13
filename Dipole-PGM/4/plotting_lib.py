import os 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



# from helper library
from helper_lib import moving_average



def plot_beamline(hb_1200_energy_flux,
                  hb_1200_energy_rp, 
                  flux_dipole, 
                  flux_percent, 
                  flux_abs, 
                  SlitSize, 
                  bw, 
                  focx, 
                  focy, 
                  title='', 
                  save=False,
                  save_folder='plot', 
                  reflectivity_to_plot=False,
                  source_type = 'Dipole',
                  show_plot=False):
    
    focx *= 1000 # in um
    focy *= 1000 # in um
    en_rp = hb_1200_energy_rp.shape[0]
    en_f = hb_1200_energy_flux.shape[0]

    if reflectivity_to_plot:
        n_rows = 4
        index_row_plot = 0
    else:
        n_rows = 3
        index_row_plot = 1
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(n_rows, 2, figure=fig)

    # MIRROR COATING
    if reflectivity_to_plot:
        ax = plt.subplot(gs[0, 0:2])    
        ax.set_xlabel('Energy [eV]')
        ax.set_ylabel('Reflectivity [a.u.]')
        ax.set_title('Mirror Coating Reflectivity')
        for ref in reflectivity_to_plot:
            E       = ref[0]
            IrCrB4C = ref[1]
            label   = ref[2]
            ax.plot(E, IrCrB4C, label=label)
        ax.legend()


    # Source Flux
    ax = plt.subplot(gs[1-index_row_plot, 0])
    ax.set_title('Dipole Flux')
    ax.grid(which='both', axis='both')
    ax.plot(hb_1200_energy_flux, flux_dipole, label=f'{source_type} Flux')
    ax.set_ylabel('Flux [ph/s/0.1%bw]')

    ax.legend(loc=6)


    # BEAMLINE TRANSMISSION
    ax = plt.subplot(gs[1-index_row_plot, 1])
    for ind, ss in enumerate(SlitSize):
        ss = int(ss*1000) # slit size in um
        window_size = 5
        energy = moving_average(hb_1200_energy_flux, window_size)
        flux = moving_average(flux_percent[ind*en_f:en_f*(ind+1)], window_size)
        ax.plot(energy,flux, label=f'ExitSlit {ss} um' )

    ax.set_xlabel(r'Energy [eV]')
    ax.set_ylabel('Transmission [%]')
    ax.set_title('Available Flux (in transmitted bandwidth)')
    ax.grid(which='both', axis='both')
    ax.legend()


    ax2 = ax.twinx()
    l = ax2.plot(hb_1200_energy_flux,flux_abs[0:en_f], 'r', label='ExitSlit 200 um' )
    ax2.set_xlabel(r'Energy [eV]')
    ax2.set_ylabel('Input Flux [ph/s/tbw]')
    l[0].remove()
    ax2.set_ylabel('Flux [ph/s/tbw]')


    # BANDWIDTH
    ax = plt.subplot(gs[2-index_row_plot, 0])
    for ind, ss in enumerate(SlitSize):
        ss = int(ss*1000) # slit size in um
        ax.plot(hb_1200_energy_rp,bw[ind*en_rp:en_rp*(ind+1)], label=f'ExitSlit {ss} um')

    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Transmitted Bandwidth [eV]')
    ax.set_title('Transmitted bandwidth (tbw)')
    ax.grid(which='both', axis='both')
    # ax.legend()


    # RESOLVING POWER
    ax = plt.subplot(gs[2-index_row_plot, 1])
    for ind, ss in enumerate(SlitSize):
        ss = int(ss*1000) # slit size in um
        ax.plot(hb_1200_energy_rp,hb_1200_energy_rp/bw[ind*en_rp:en_rp*(ind+1)], label=f'ExitSlit {ss} um')


    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('RP [a.u.]')
    ax.set_title('Resolving Power')
    ax.grid(which='both', axis='both')
    ax.legend()

    # HORIZONTAL FOCUS
    ax = plt.subplot(gs[3-index_row_plot, 0])
    focx_plot = 0
    for ind, ss in enumerate(SlitSize):
        ss = int(ss*1000) # slit size in um
        focx_plot += focx[ind*en_rp:en_rp*(ind+1)]
    focx_plot /= (ind+1)
    ax.plot(hb_1200_energy_rp,focx_plot, label=f'ExitSlit {ss} um')

    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Horizontal focus')
    ax.legend()

    # VERTICAL FOCUS
    ax = plt.subplot(gs[3-index_row_plot, 1])
    for ind, ss in enumerate(SlitSize):
        ss = int(ss*1000) # slit size in um
        ax.plot(hb_1200_energy_rp,focy[ind*en_rp:en_rp*(ind+1)], label=f'ExitSlit {ss} um')

    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Vertical focus')

    plt.suptitle(title)
    plt.tight_layout()
    
    plot_folder_exists(folder_path=save_folder)
    if save:
        for s in save:
            save_path = os.path.join(save_folder, s)
            plt.savefig(save_path)
            print(f'Saved: {save_path}')
    # plt.show()

def plot_folder_exists(folder_path='plot'):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")
