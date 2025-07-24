import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd


# import simulation parameters
from parameter import energy_rp, energy_flux
from parameter import SlitSize
from parameter import rml_file_name_bessy3_HRRIXS_my, rml_file_name_bessy3_HRRIXS_JV
from parameter import colors, grating

from raypyng.postprocessing import PostProcessAnalyzed
p = PostProcessAnalyzed()
moving_average = p.moving_average

SlitSize = SlitSize*1000
rml_comparison_list = {}
rml_comparison_list[rml_file_name_bessy3_HRRIXS_my]                   = 0
rml_comparison_list[rml_file_name_bessy3_HRRIXS_JV]                   = 0



# set moving average window
window = 10

# prepare figures
fig, (axs) = plt.subplots(3, 2,figsize=(10,10))
fig.suptitle(f"BESSYIII PGM beamline comparison")

# remove plot 0,1
axs[0, 1].axis('off')
# BEAMLINE TRANSMISSION
flux_ax = axs[0,0]
flux_ax.set_xlabel(r'Energy [eV]')
flux_ax.set_ylabel('Transmission [%]')
flux_ax.set_title('Available Flux [in transmitted bandwidth]')
flux_ax.grid(which='both', axis='both')

# BANDWIDTH
bw_ax = axs[1,0]
bw_ax.set_xlabel('Energy [eV]')
bw_ax.set_ylabel('Transmitted Bandwidth [meV]')
bw_ax.set_title('Transmitted Bandwidth (tbw)')
bw_ax.grid(which='both', axis='both')

# RESOLVING POWER
rp_ax = axs[1,1]
rp_ax.set_xlabel('Energy [eV]')
rp_ax.set_ylabel('RP [a.u.]')
rp_ax.set_title('Resolving Power')
rp_ax.grid(which='both', axis='both')

# HORIZONTAL FOCUS
hf_ax = axs[2,0]
hf_ax.set_xlabel('Energy [eV]')
hf_ax.set_ylabel('Focus Size [um]')
hf_ax.set_title('Horizontal Focus')

# VERTICAL FOCUS
vf_ax = axs[2,1]
vf_ax.set_xlabel('Energy [eV]')
vf_ax.set_ylabel('Focus Size [um]')
vf_ax.set_title('Vertical Focus')    

color_index = -1
for rml_file_name, ind in rml_comparison_list.items():
    color_index +=1
    # file/folder/ml index definition
    flux_simulation_folder = 'RAYPy_Simulation_'+rml_file_name+'_FLUX'
    rp_simulation_folder = 'RAYPy_Simulation_'+rml_file_name+'_RP'



    # load Flux simulations results
    folder_name  = flux_simulation_folder
    oe           = 'DetectorAtFocus'
    flux_path    = os.path.join(flux_simulation_folder, oe+'_RawRaysOutgoing.dat')
    flux         = pd.read_csv(flux_path, sep='\t', index_col=None)
    en_flux_path = os.path.join(flux_simulation_folder, 'input_param_SU_photonEnergy.dat')
    energy_flux  = np.loadtxt(en_flux_path)
    ssf          = energy_flux.shape[0]

    # load RP simulations results
    folder_name  = rp_simulation_folder
    oe           = 'DetectorAtFocus'
    rp_path      = os.path.join(rp_simulation_folder, oe+'_RawRaysOutgoing.dat')
    rp           = pd.read_csv(rp_path, sep='\t', index_col=None)
    en_rp_path   = os.path.join(rp_simulation_folder, 'input_param_SU_photonEnergy.dat')
    energy_rp    = np.loadtxt(en_rp_path)
    ssrp         = energy_rp.shape[0]

    energy_flux = moving_average(energy_flux, window)
    energy_rp = moving_average(energy_rp, window)

    # plotting Flux and RP
    # BEAMLINE TRANSMISSION
    flux_plot = flux['PercentageRaysSurvived'][ssf*ind:ssf*(ind+1)]
    flux_plot = moving_average(flux_plot.to_numpy(), window)
    flux_ax.plot(energy_flux,flux_plot, colors[color_index], label=f'{rml_file_name}' )


    # BANDWIDTH
    bw_plot = rp['Bandwidth'][ssrp*ind:ssrp*(ind+1)]
    bw_plot = moving_average(bw_plot, window)
    bw_ax.plot(energy_rp,1000*bw_plot,colors[color_index])


    # RESOLVING POWER
    # plot and deal with bandwidth=0 case.
    try:
        res_p = energy_rp / bw_plot
    except ZeroDivisionError:
        res_p = 0
    inf_indices = np.where(np.isinf(rp))[0]
    rp_ax.plot(energy_rp, res_p, colors[color_index])


    # HORIZONTAL FOCUS
    hor_foc = rp['HorizontalFocusFWHM'][ssrp*ind:ssrp*(ind+1)]
    hor_foc = moving_average(hor_foc.to_numpy(), window)
    hf_ax.plot(energy_rp,1000*hor_foc,colors[color_index])

    # VERTICAL FOCUS
    ver_foc = rp['VerticalFocusFWHM'][ssrp*ind:ssrp*(ind+1)]
    ver_foc = moving_average(ver_foc.to_numpy(), window)
    vf_ax.plot(energy_rp,1000*ver_foc,colors[color_index])



# flux_ax.legend()
handles, labels = flux_ax.get_legend_handles_labels()
axs[0, 1].legend(handles, labels, loc='center', fontsize=16)
plt.tight_layout()
#plt.savefig('plot/FluxRpFocus_comparison.png')
plt.savefig('plot/FluxRpFocus_comparison.pdf')

# plt.show()