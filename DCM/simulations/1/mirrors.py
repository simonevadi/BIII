import numpy as np

class EllipticalMirror:
    def __init__(self, name, photon_energy_eV, image_distance_m, aperture_m):
        """
        Parameters:
        - name: str, name of the mirror (e.g., "Horizontal" or "Vertical")
        - photon_energy_eV: float, photon energy in electronvolts (eV)
        - image_distance_m: float, distance from mirror to focus (q) in meters
        - aperture_m: float, illuminated length/aperture of mirror in meters (D)
        """
        self.name = name
        self.E_eV = photon_energy_eV
        self.q = image_distance_m
        self.D = aperture_m
        self.lambda_ = self._convert_eV_to_m(photon_energy_eV)

    @staticmethod
    def _convert_eV_to_m(E_eV):
        """
        Convert photon energy in eV to wavelength in meters.
        λ [m] = hc / E, with hc ≈ 1.239841984e-6 eV·m
        """
        hc = 1.239841984e-6  # [eV·m]
        return hc / E_eV

    def spot_size(self):
        """
        Returns the diffraction-limited FWHM spot size at the focus in meters.
        """
        return 1.22 * self.lambda_ * self.q / self.D

    def __repr__(self):
        return (f"{self.name} Mirror:\n"
                f"  Photon Energy = {self.E_eV:.2f} eV\n"
                f"  λ = {self.lambda_ * 1e9:.2f} nm\n"
                f"  Image distance q = {self.q*1000:.1f} mm\n"
                f"  Aperture D = {self.D*1000:.1f} mm\n"
                f"  Spot size ≈ {self.spot_size()*1e9:.1f} nm (FWHM)\n")

# Example usage
if __name__ == "__main__":
    E = 1240      # eV (≈ 1 nm)
    q = 1.0       # m
    D = 0.02      # m

    mirror_x = EllipticalMirror("Horizontal", E, q, D)
    mirror_y = EllipticalMirror("Vertical", E, q, D)

    print(mirror_x)
    print(mirror_y)
