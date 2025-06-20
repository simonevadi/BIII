import numpy as np
import matplotlib.pyplot as plt
from scipy.special import kv
from scipy.integrate import quad

class DipoleSynchrotronSpectrum:
    def __init__(self, bending_radius_m=None, magnetic_field_T=None, 
                 beam_energy_GeV=2.5, current_A=0.1):
        self.beam_energy_GeV = beam_energy_GeV
        self.current_A = current_A

        if (bending_radius_m is None) == (magnetic_field_T is None):
            raise ValueError("Specify either 'bending_radius_m' or 'magnetic_field_T', but not both.")

        if bending_radius_m is not None:
            self.bending_radii = np.atleast_1d(bending_radius_m)
            self.fields = 3.335 * beam_energy_GeV / self.bending_radii
        else:
            self.fields = np.atleast_1d(magnetic_field_T)
            self.bending_radii = 3.335 * beam_energy_GeV / self.fields

        self.lambda_critical_A = 5.59 * self.bending_radii / beam_energy_GeV**3
        self.energy_critical_keV = 12.398 / self.lambda_critical_A
        self.gamma = 1957 * self.energy_critical_keV

    def __repr__(self):
        out = "DipoleSynchrotronSpectrum(\n"
        for i, (B, R, Ec, lam, g) in enumerate(zip(self.fields, self.bending_radii, self.energy_critical_keV, self.lambda_critical_A, self.gamma)):
            out += f"  Case {i+1}:\n"
            out += f"    Magnetic field     = {B:.3f} T\n"
            out += f"    Bending radius     = {R:.3f} m\n"
            out += f"    Critical energy    = {Ec:.3f} keV\n"
            out += f"    Critical wavelength= {lam:.3f} Å\n"
            out += f"    γ (Gamma)          = {g:.2f}\n"
            out += f"    Beam energy         = {self.beam_energy_GeV} GeV\n"
            out += f"    Beam current        = {self.current_A:.3f} A\n"
            out += ")"
        return out

    def F_exact(self, x_array):
        """Spectral function F(x) = x * ∫_x^∞ K_{5/3}(z) dz"""
        return np.array([
            x * quad(lambda z: kv(5.0 / 3.0, z), x, np.inf)[0]
            for x in x_array
        ])

    def compute_flux(self, energy_keV_range):
        """Compute absolute photon flux for all cases over the given energy range (in keV)
        Returns:
            np.ndarray: shape (n_cases, len(energy_keV_range)), flux in [photons/s/keV]
        """
        fluxes = []
        for Ec, gamma in zip(self.energy_critical_keV, self.gamma):
            x = energy_keV_range / Ec
            F_vals = self.F_exact(x)

            # Empirical normalization factor for total dipole flux around Ec
            # 1.3e13 photons/s/0.1% BW * current [A] * Ec [keV]
            norm = 1.3e13 * self.current_A * Ec  # [photons/s/0.1% BW]

            # Convert to per-keV units:
            delta_E_keV = energy_keV_range * 0.001  # 0.1% of E
            flux = norm * F_vals / delta_E_keV  # [photons/s/keV]

            fluxes.append(flux)
        return np.array(fluxes)

    def plot_spectrum(self, energy_min=0.001, energy_max=10, energy_step=0.1):
        """Plot synchrotron spectra for all field/radius cases"""
        energy_keV = np.arange(energy_min, energy_max + energy_step, energy_step)
        fluxes = self.compute_flux(energy_keV)

        plt.figure(figsize=(8, 5))
        for i, flux in enumerate(fluxes):
            label = f"{self.fields[i]:.1f} T"
            plt.plot(energy_keV, flux, label=label)

        plt.xlabel("Photon Energy [keV]")
        plt.ylabel(f"Photon Flux [photons/s/0.1%BW/{self.current_A:.1f} A]")
        plt.xscale('log')
        plt.yscale('log')
        plt.title("Synchrotron Radiation Spectrum for Different Fields")
        plt.legend(title="Magnetic Field")
        plt.grid(True)
        plt.tight_layout()
        return plt

if __name__ == "__main__":
    import pandas as pd
    import os

    spectrum = DipoleSynchrotronSpectrum(magnetic_field_T=[1.3, 2.0, 3.0])
    print(spectrum)
    plt = spectrum.plot_spectrum()
    magnetic_fields = np.array([0.6, 1.3, 2.0, 3.0])  # Tesla
    bending_radii = 3.335 * 2.5 / magnetic_fields
    for index, radius in enumerate(bending_radii): 
        flux = pd.read_csv(os.path.join('RAYPy_Simulation_Dipole', 'Dipole_RawRaysOutgoing.csv'))
        print(radius)
        filtered_flux = flux[np.abs(flux['Dipole.bendingRadius'] - radius) <= 0.1]
        print(flux)
        filtered_flux['PhotonEnergy']
        filtered_flux['PhotonFlux']

        plt.plot(filtered_flux['PhotonEnergy']/1000, filtered_flux['PhotonFlux'], label=f'B = {magnetic_fields[index]} T')
    plt.legend(title="Magnetic Field")
    plt.savefig('Dipole.png')
