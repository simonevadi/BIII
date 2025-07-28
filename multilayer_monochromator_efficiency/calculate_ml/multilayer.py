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
        """
        Initialize the MultilayerBragg object.

        Args:
            mat1 (tuple): Material 1 name and density (name, density).
            t1 (float): Thickness of material 1 in Ångströms.
            mat2 (tuple): Material 2 name and density (name, density).
            t2 (float): Thickness of material 2 in Ångströms.
            N (int): Number of layers.
            save_recap (str, optional): Directory to save recap files.
            individuals (bool, optional): If True, save individual reflectivity plots for each energy.
        """
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
            energy_eV (float): Photon energy in eV.
            max_order (int, optional): Highest Bragg order to compute.
            angle_range (tuple, optional): Angle scan range (deg).
        
        Returns:
            tuple: Angles (theta), s-polarized reflectivity (rs), p-polarized reflectivity (rp), and Bragg angles (bragg_degs).
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
        """
        Plot the reflectivity as a function of incident angle.

        Args:
            energy_eV (float): Photon energy in eV.
            theta (array-like): Array of incident angles.
            rs (array-like, optional): s-polarized reflectivity.
            rp (array-like, optional): p-polarized reflectivity.
            show_plot (bool, optional): If True, display the plot.
        
        Raises:
            ValueError: If neither rs nor rp is provided.
        """
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
            energies (array-like): Iterable of photon energies in eV.
            order (int, optional): Bragg reflection order to analyze.
            window_deg (float, optional): Angular window around Bragg angle to find peak reflectivity.

        Returns:
            pandas.DataFrame: DataFrame with energy, peak reflectivity, and angle information.
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

    def calculate_beta_from_theta(self, theta_deg, energy, grating_density, order=2):
        """
        Calculate the diffraction angle (beta) from the incident angle (theta) using the grating equation.

        Args:
            theta_deg (float or array-like): Incident angle(s) in degrees.
            energy (float or array-like): Photon energy in eV.
            grating_density (float): Grating density in lines per mm.
            order (int, optional): Diffraction order to calculate (default is 2).

        Returns:
            float or array-like: Diffraction angle(s) in degrees.
        """
        # Convert theta from degrees to radians
        energy = np.array(energy, dtype=float)
        theta = np.deg2rad(theta_deg)
        lambdas = 1239.84193 / energy * 1e-9  # Convert eV to meters
        spacing = 1 / (grating_density * 1000)  # Convert lines/mm to lines/m
        beta = np.arcsin(order*lambdas/spacing-np.sin(theta))
        beta_norm_deg = np.rad2deg(beta)
        return beta_norm_deg        
    
    def calculate_c_value(self, alpha_deg, beta_deg):
        """
        Calculate the coupling factor based on the incident and diffraction angles.

        Args:
            alpha_deg (float): Incident angle in degrees.
            beta_deg (float): Diffraction angle in degrees.

        Returns:
            float: Coupling factor (c-value).
        """
        alpha = np.deg2rad(90-alpha_deg)
        beta = np.deg2rad(90+beta_deg)
        c_values = np.sin(beta)/np.sin(alpha)
        return c_values

    def prepare_raypyng_efficiency_table(self, filename, line_density=2400, grating_efficiency_scale=0.85):
        """
        Prepare the RayPyng efficiency table by calculating efficiency values for each energy and angle.

        Args:
            filename (str): Name of the output file to save the table.
            line_density (int, optional): Grating line density in lines/mm.
            grating_efficiency_scale (float, optional): Efficiency scaling factor (default is 0.85).

        Returns:
            pandas.DataFrame: DataFrame containing the efficiency values.
        """
        raypyng_df = self.results_df[['Energy[eV]']].copy()
        alpha_norm_deg = 90-self.results_df['Angle'].values
        energies = self.results_df['Energy[eV]'].values
        beta_norm_deg = self.calculate_beta_from_theta(alpha_norm_deg, energies, line_density, order=2)
        c_values = self.calculate_c_value(alpha_norm_deg, beta_norm_deg)
        raypyng_df['alpha_norm_deg'] = alpha_norm_deg
        raypyng_df['alpha_deg'] = self.results_df['Angle'].values
        raypyng_df['beta_norm_deg'] = beta_norm_deg
        raypyng_df['beta_deg'] = 90 + beta_norm_deg
        raypyng_df['cff'] = c_values
        raypyng_df['Efficiency'] = self.results_df['peak_rs']*self.results_df['peak_rs']*grating_efficiency_scale
        fname = os.path.join(self.save_recap, f"{filename}.csv")
        raypyng_df.to_csv(fname)
        return raypyng_df

    def plot_reflectivity_vs_energy(self, show_plot=True):
        """
        Plot the reflectivity as a function of photon energy.

        Args:
            show_plot (bool, optional): If True, display the plot.
        """
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



