import numpy as np
import matplotlib.pyplot as plt
from scipy import special

from xrt.backends.raycing.sources_sybase import SourceBase
from xrt.backends.raycing.physconsts import E0, C, M0, SIE0, SIM0, FINE_STR, SQ3, E2W


class BendingMagnet(SourceBase):
    def __init__(self, B0=1.0, rho=None, eE=2.5, **kwargs):
        super().__init__(eE=eE, **kwargs)
        self.Np = 0.5
        self.B = B0
        self.ro = rho
        if self.ro:
            if not self.B:
                self.B = M0 * C**2 * self.gamma / self.ro / E0 / 1e6
        elif self.B:
            self.ro = M0 * C**2 * self.gamma / self.B / E0 / 1e6
        self.isMPW = False
        self.needReset = False

    @property
    def B0(self):
        return self.B

    @B0.setter
    def B0(self, B):
        self.B = float(B)
        self.ro = M0 * C**2 * self.gamma / B / E0 / 1e6
        self.needReset = True

    @property
    def rho(self):
        return self.ro

    @rho.setter
    def rho(self, rho):
        self.ro = rho
        self.B = M0 * C**2 * self.gamma / rho / E0 / 1e6
        self.needReset = True

    def build_I_map(self, dde, ddtheta, ddpsi, harmonic=None, dg=None):
        gamma = self.gamma
        gamma2 = self.gamma2

        w_cr = 1.5 * gamma2 * self.B * SIE0 / SIM0
        gammapsi = gamma * ddpsi
        gamma2psi2p1 = gammapsi**2 + 1
        eta = 0.5 * dde * E2W / w_cr * gamma2psi2p1**1.5

        ampSP = -0.5j * SQ3 / np.pi * gamma * dde * E2W / w_cr * gamma2psi2p1
        ampS = ampSP * special.kv(2. / 3., eta)
        ampP = 1j * gammapsi * ampSP * special.kv(1. / 3., eta) / np.sqrt(gamma2psi2p1)

        ampS = np.where(np.isfinite(ampS), ampS, 0.)
        ampP = np.where(np.isfinite(ampP), ampP, 0.)

        bwFact = 1. / dde
        Amp2Flux = FINE_STR * bwFact * self.eI / SIE0 * 2 * self.Np

        return (Amp2Flux * (np.abs(ampS)**2 + np.abs(ampP)**2),
                np.sqrt(Amp2Flux) * ampS,
                np.sqrt(Amp2Flux) * ampP)

    def __repr__(self):
        lambda_c_A = 5.59 * self.ro / self.eE**3
        E_crit_keV = 12.398 / lambda_c_A

        return (
            f"BendingMagnet(\n"
            f"  Magnetic field     = {self.B:.3f} T\n"
            f"  Bending radius     = {self.ro:.3f} m\n"
            f"  Beam energy        = {self.eE:.3f} GeV\n"
            f"  Gamma (γ)          = {self.gamma:.2f}\n"
            f"  Critical energy    = {E_crit_keV:.3f} keV\n"
            f"  Critical wavelength= {lambda_c_A:.3f} Å\n"
            f")"
        )

    def plot_spectrum(self, energy_range_keV=(0.1, 20), npoints=500,
                      theta=0.0, psi=0.0):
        energy_keV = np.linspace(*energy_range_keV, npoints)
        flux, _, _ = self.build_I_map(energy_keV, theta, psi)

        plt.figure(figsize=(8, 5))
        plt.plot(energy_keV, flux)
        plt.xlabel("Photon Energy [keV]")
        plt.ylabel("Flux [photons/s/eV/0.1% BW/A]")
        plt.title("Synchrotron Spectrum from Bending Magnet")
        plt.grid(True)
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    # bm = BendingMagnet(B0=1.3)
    # print(bm)
    # bm.plot_spectrum()

    # Create the bending magnet source
    bm = BendingMagnet(B0=1.3, eE=2.5)  # Tesla, GeV

    # Energy range (in eV)
    energies = np.linspace(-1000, 30000, 2000)  # e.g., from 100 eV to 30 keV

    # On-axis angles: theta = 0, psi = 0
    theta = np.zeros_like(energies)
    psi = np.zeros_like(energies)

    # Get on-axis spectral flux
    flux, _, _ = bm.build_I_map(energies, theta, psi)

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(energies, flux)
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Spectral Flux [ph/s/0.1%BW]")
    plt.title("On-axis Spectral Flux from Bending Magnet")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
