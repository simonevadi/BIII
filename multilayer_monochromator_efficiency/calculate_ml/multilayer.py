import os
import numpy as np
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import xrt.backends.raycing.materials as rm

import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

class MultilayerBragg:
    def __init__(self, mat1: tuple, t1: float, mat2: tuple, t2: float, N: int, save_recap: str =None, individuals: bool=True):
        self.mat1_name, self.rho1 = mat1
        self.mat2_name, self.rho2 = mat2
        self.t1 = t1  # Å
        self.t2 = t2  # Å
        self.N = N
        self.period_nm = (t1 + t2) * 0.1  # convert Å to nm
        self.stack = None
        self.bragg_degs = []  # list of Bragg angles
        self.save_recap = save_recap
        self.individuals = individuals
        self.individuals_folder = os.path.join(self.save_recap, 'individuals') if save_recap else None
        if self.save_recap is not None:
            os.makedirs(self.save_recap, exist_ok=True)
        if self.save_recap and self.individuals:
            os.makedirs(self.individuals_folder, exist_ok=True)

    def calculate_multilayer(self, energy_eV: float, max_order: int = 1, angle_range=(0, 20)):
        """
        Build multilayer and compute Bragg angles up to max_order.

        Args:
            energy_eV: Photon energy in eV.
            max_order: Highest Bragg order to compute.
            angle_range: Angle scan range (deg).
        """
        m1 = rm.Material(self.mat1_name, rho=self.rho1)
        m2 = rm.Material(self.mat2_name, rho=self.rho2)
        self.stack = rm.Multilayer(m1, self.t1, m2, self.t2, self.N, m1)

        self.bragg_degs = []
        for order in range(1, max_order + 1):
            theta_rad = self.stack.get_Bragg_angle(energy_eV, order)
            theta_deg = np.rad2deg(theta_rad)
            self.bragg_degs.append((order, theta_deg))

        theta = np.linspace(*angle_range, 1001)
        sin_theta = np.sin(np.deg2rad(theta))
        rs, rp = self.stack.get_amplitude(energy_eV, sin_theta)[0:2]
        return theta, rs, rp, self.bragg_degs

    def plot_reflectivity_vs_theta(self, energy_eV: float, theta, rs=None, rp=None, show_plot=True):
        if rs is None and rp is None:
            raise ValueError("At least one of rs or rp must be provided.")

        fig, ax = plt.subplots(figsize=(6, 4))

        if rs is not None:
            ax.plot(theta, abs(rs)**2, 'r', label='s-polarization')
        if rp is not None:
            ax.plot(theta, abs(rp)**2, 'b', label='p-polarization')

        for order, theta_B in self.bragg_degs:
            ax.axvline(theta_B, color='k', linestyle='--', label=f'Bragg {order}: {theta_B:.3f}°')

        ax.set_xlabel('Incident angle (deg)')
        ax.set_ylabel('Reflectivity')
        ax.set_title(f'Multilayer Reflectivity at {energy_eV / 1000:.1f} keV')
        ax.legend()
        ax.grid(True)
        fig.tight_layout()
        if show_plot:
            plt.show()
        plt.close(fig)
    
    def calculate_reflectivity_vs_energy(self, energies, order=1, window_deg=0.1):
        """
        Compute peak reflectivity near the Bragg angle as a function of energy.

        Args:
            energies: Iterable of photon energies in eV.
            order: Bragg reflection order to analyze.
            window_deg: Angular window around Bragg angle to find peak reflectivity.

        Returns:
            energy_list: list of energies
            peak_rs_list: list of max |rs|^2 near Bragg peak
            peak_rp_list: list of max |rp|^2 near Bragg peak
        """
        energy_list = []
        peak_rs_list = []
        peak_rp_list = []
        self.results_df = pd.DataFrame(columns=['Energy[eV]', 'Reflectivity', 'Angle'])

        for energy in tqdm(energies, desc="Calculating reflectivity"):
            theta, rs, rp, bragg_degs = self.calculate_multilayer(energy, max_order=order)
            bragg_deg = None
            for o, deg in bragg_degs:
                if o == order:
                    bragg_deg = deg
                    break

            if bragg_deg is None:
                continue  # Skip if this order doesn't exist at this energy

            # Find indices within the window around the Bragg angle
            mask = (theta >= bragg_deg - window_deg) & (theta <= bragg_deg + window_deg)
            if not np.any(mask):
                continue

            rs2 = np.abs(rs)**2
            rp2 = np.abs(rp)**2

            peak_rs = np.max(rs2[mask]) if rs is not None else None
            peak_rp = np.max(rp2[mask]) if rp is not None else None

            # Find peak position for rs
            if peak_rs is not None:
                peak_idx = np.where(rs2 == peak_rs)[0][0]
                peak_theta = theta[peak_idx]
            else:
                peak_theta = None

            energy_list.append(energy)
            peak_rs_list.append(peak_rs)
            peak_rp_list.append(peak_rp)
            
            new_results_row = {'Energy[eV]': energy, 'peak_rs': peak_rs,
                       'peak_rp': peak_rp, 'Angle': peak_theta}
            
            self.results_df = pd.concat([self.results_df,
                                    pd.DataFrame([new_results_row])],
                                    ignore_index=True)
            
            


            # Save plot if required
            if self.individuals:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.plot(theta, rs2, label='|rs|²', color='red')
                if peak_theta is not None:
                    ax.plot(peak_theta, peak_rs, 'ro', label='Peak in window')
                ax.axvline(bragg_deg, color='k', linestyle='--', label=f'Bragg {order}: {bragg_deg:.3f}°')
                ax.set_xlabel("Incident angle (deg)")
                ax.set_ylabel("Reflectivity |rs|²")
                ax.set_title(f"{energy/1000:.1f} keV Reflectivity")
                ax.legend()
                ax.grid(True)
                fig.tight_layout()
                fname = os.path.join(self.individuals_folder, f"{energy}_eV.png")
                fig.savefig(fname)
                plt.close(fig)
        
            if self.save_recap is not None:
                fname = os.path.join(self.save_recap, f"results.csv")
                self.results_df.to_csv(fname, index=False)
            
        return self.results_df
    
    def prepare_raypyng_efficiency_table(self, filename):
            raypyng_df = self.results_df[['Energy[eV]', 'peak_rs']].copy()
            # we take arbitrarly 85% efficiency for the grating
            raypyng_df['peak_rs'] *= raypyng_df['peak_rs']*0.85
            fname = os.path.join(self.save_recap, f"{filename}.csv")
            raypyng_df.to_csv(fname)
            return raypyng_df

    def plot_reflectivity_vs_energy(self, show_plot=True):
        # Plot s-polarized peak reflectivity
        plt.plot(self.results_df['Energy[eV]'], self.results_df['peak_rs'], label='s-polarized')
        plt.plot(self.results_df['Energy[eV]'], self.results_df['peak_rp'], label='p-polarized')
        plt.xlabel('Photon energy (eV)')
        plt.ylabel('Peak Reflectivity near Bragg')
        plt.grid(True)
        plt.legend()
        if self.save_recap is not None:
            fname = os.path.join(self.save_recap, "reflectivity_vs_energy.png")
            plt.savefig(fname)
        if show_plot:
            plt.show() 
        plt.close()



