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
    dt = dtheta[1] - dtheta[0]
    theta = crystal.get_Bragg_angle(energy) + dtheta*1e-6
    refl_1_crystal = np.abs(crystal.get_amplitude(energy, np.sin(theta))[0])**2  # s-polarization
    refl_2_crystal = np.convolve(refl_1_crystal, refl_1_crystal, 'same') / (refl_1_crystal.sum()*dt) * dt
    return refl_1_crystal, refl_2_crystal
    
def calculate_dcm_efficiency(crystal, energies, name,
                             savepath=None, save_individuals=True,
                             dtheta=np.linspace(-250, 500, 10000)):

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

    for energy in tqdm(energies, total=len(energies), desc=f"DCM efficiency: {name}"):
        refl_1_crystal, refl_2_crystal = calculate_crystal_reflectivity(dtheta, crystal, energy)
        reflectivity_1_list.append(np.max(refl_1_crystal))
        reflectivity_2_list.append(np.max(refl_2_crystal))

        if save_individuals:
            try:
                # find the roots for FWHM 1 crystal
                spline = UnivariateSpline(dtheta, refl_1_crystal-refl_1_crystal.max()/2, s=0)
                r11, r12 = spline.roots()  # find the roots
                plt.axvspan(r11, r12, facecolor='r', alpha=0.05)
                # find the roots for FWHM 2 crystal
                spline = UnivariateSpline(dtheta, refl_2_crystal-refl_2_crystal.max()/2, s=0)
                r21, r22 = spline.roots()  # find the roots
                plt.axvspan(r21, r22, facecolor='b', alpha=0.05)
            except ValueError:
                pass
            # plot 1 crystal
            plt.plot(dtheta, refl_1_crystal, 'r', 
                     label=u'one crystal') 
                     #'\nFWHM = {0:.1f} µrad'.format(
                #crystal.get_Darwin_width(energy)*1e6))
            
            #plot second crytal
            plt.plot(dtheta, refl_2_crystal, 'b',
                     label=u'two crystal (conv)')
#                    u'\nFWHM = {0:.1f} µrad'.format(r22-r21))
            # label and legend
            plt.gca().set_xlabel(u'$\\theta - \\theta_{B}$ (µrad)')
            plt.gca().set_ylabel(r'reflectivity')
            plt.legend(loc='upper right', fontsize=12)
            plt.gca().set_xlim(dtheta[0], dtheta[-1])
            # add text
            text = f'Rocking curve of {name} at energy={2:.0f} eV'.format(
                crystal.name, crystal.hkl, energy)
            plt.text(0.5, 1.02, text, transform=plt.gca().transAxes, size=15, ha='center')
            # save figure
            filepath=os.path.join(savepath, 'individual', f'name_{energy}.png')
            plt.savefig(filepath)
            plt.close()

            # build DataFrame
    df = pd.DataFrame({
        "Energy[eV]": energies,
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
 