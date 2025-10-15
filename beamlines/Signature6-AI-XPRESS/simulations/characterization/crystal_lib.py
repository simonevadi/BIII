import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials_crystals as rm
# safe import of tqdm
try:
    from tqdm.auto import tqdm
except Exception:
    def tqdm(x, *args, **kwargs):  # minimal fallback
        return x
import warnings
warnings.filterwarnings(
    "ignore",
    message="Reading `.npy` or `.npz` file required additional header parsing as it was created on Python 2. Save the file again to speed up loading and avoid this warning."
)

def calculate_crystal_reflectivity(dtheta, crystal, energy):
    theta = crystal.get_Bragg_angle(energy) + dtheta*1e-6
    theta_deg = np.rad2deg(theta)
    refl_1_crystal = np.abs(crystal.get_amplitude(energy, np.sin(theta))[0])**2  # s-polarization
    refl_2_crystal = refl_1_crystal*refl_1_crystal
    return refl_1_crystal, refl_2_crystal, theta_deg
    
def calculate_dcm_efficiency(crystal, energies, name,
                             savepath=None, save_individuals=True,
                             dtheta=np.linspace(-250, 800, 10000)):

    # create  savepath folder if it does not exist
    if savepath is not None:
        # if savepath has an extension, assume it's a file, else a directory
        path_to_create = os.path.dirname(savepath) if os.path.splitext(savepath)[1] else savepath
        os.makedirs(path_to_create, exist_ok=True)
    
    if save_individuals and savepath is not None:
        os.makedirs(os.path.join(savepath, 'individual'), exist_ok=True)

    # create list to store reflectivity one crystal and two crystal (convolution)    
    reflectivity_1_list = []
    reflectivity_2_list = []
    theta_list = []
    for energy in tqdm(energies, total=len(energies), desc=f"DCM efficiency: {name}"):
        refl_1_crystal, refl_2_crystal, theta = calculate_crystal_reflectivity(dtheta, crystal, energy)
        reflectivity_1_list.append(np.max(refl_1_crystal))
        reflectivity_2_list.append(np.max(refl_2_crystal))
        theta_list.append(theta[np.argmax(refl_2_crystal)])

        if save_individuals:
            # plot 1 crystal
            plt.plot(theta, refl_1_crystal, 'r', 
                     label=u'one crystal') 
            
            #plot second crytal
            plt.plot(theta, refl_2_crystal, 'b',
                     label=u'two crystal (conv)')
            # label and legend
            plt.gca().set_xlabel(u'$\\theta_{B}$ [deg]')
            plt.gca().set_ylabel(r'reflectivity')
            plt.legend(loc='upper right', fontsize=12)
            plt.gca().set_xlim(theta[0], theta[-1])
            # add text
            text = f'RC of {name} at E={energy} eV'
            plt.text(0.5, 1.02, text, transform=plt.gca().transAxes, size=15, ha='center')
            # save figure
            filepath=os.path.join(savepath, 'individual', f'name_{energy}.png')
            plt.savefig(filepath)
            plt.close()

            # build DataFrame
    df = pd.DataFrame({
        "Energy[eV]": energies,
        "ThetaB[deg]": theta_list,
        "Reflectivity_1": reflectivity_1_list,
        "Reflectivity_2": reflectivity_2_list
        })
    # optionally save
    if savepath is not None:
        filepath = os.path.join(savepath, name + '.csv')
        df.to_csv(filepath, index=False)

        plt.figure()
        plt.plot(df['Energy[eV]'], df['Reflectivity_1'], label='one crystal')
        plt.plot(df['Energy[eV]'], df['Reflectivity_2'], label='two crystal (conv)')
        # plt.plot(df['ThetaB[deg]'], df['Reflectivity_2'], label='two crystal (conv)')
        plt.xlabel('Energy [eV]')
        plt.ylabel('Reflectivity [a.u.]')
        plt.title(name)
        plt.legend()
        # minor ticks and grid
        ax = plt.gca()
        ax.minorticks_on()
        ax.grid(which='major', axis='both', linestyle='--', linewidth=0.5, color='lightgrey')
        ax.grid(which='minor', axis='both', linestyle=':', linewidth=0.5, color='lightgrey')

        filepath = os.path.join(savepath, name + '.png')
        plt.savefig(filepath)
        plt.close()
    return df
 