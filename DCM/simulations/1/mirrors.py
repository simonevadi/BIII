import numpy as np

class EllipticalMirror:
    def __init__(self, name, photon_energy_eV, image_distance_m, aperture_m,
                 object_distance_m=None, source_size_m=None):
        """
        Parameters:
        - name: str
        - photon_energy_eV: float
        - image_distance_m (q): float
        - aperture_m (D): float
        - object_distance_m (p): float or None → if None, assumes parallel beam
        - source_size_m: float or None → optional, required for geometrical spot estimation
        """
        self.name = name
        self.energy = photon_energy_eV
        self.q = image_distance_m
        self.D = aperture_m
        self.p = object_distance_m
        self.source_size = source_size_m
        self.lambda_ = self._convert_eV_to_m(photon_energy_eV)

    @staticmethod
    def _convert_eV_to_m(E_eV):
        hc = 1.239841984e-6  # [eV·m]
        return hc / E_eV

    def spot_size_diffraction(self):
        return 1.22 * self.lambda_ * self.q / self.D

    def spot_size_geometrical(self):
        if self.p is None or self.source_size is None:
            return None
        M = self.q / self.p
        return self.source_size * M

    def spot_size_combined(self):
        """
        Return total spot size considering both geometrical and diffraction effects.
        Added in quadrature (Gaussian assumption).
        """
        w_d = self.spot_size_diffraction()
        w_g = self.spot_size_geometrical()
        if w_g is None:
            return w_d
        return np.sqrt(w_d**2 + w_g**2)

    def __repr__(self):
        text = (f"{self.name} Mirror:\n"
                f"  Photon Energy = {self.energy:.2f} eV\n"
                f"  λ = {self.lambda_ * 1e9:.2f} nm\n"
                f"  Image distance q = {self.q*1000:.1f} mm\n"
                f"  Aperture D = {self.D*1000:.1f} mm\n")

        if self.p is None:
            text += f"  [Parallel beam]\n"
        else:
            text += (f"  Object distance p = {self.p*1000:.1f} mm\n"
                     f"  Source size = {self.source_size*1e6:.1f} µm\n"
                     f"  Geometrical spot ≈ {self.spot_size_geometrical()*1e9:.1f} nm\n")

        text += f"  Diffraction spot ≈ {self.spot_size_diffraction()*1e9:.1f} nm\n"
        text += f"  Total estimated spot ≈ {self.spot_size_combined()*1e9:.1f} nm (FWHM)\n"
        return text


if __name__ == "__main__":
    mirror_parallel = EllipticalMirror(
        name="KB-X", photon_energy_eV=8000, image_distance_m=1.0, aperture_m=0.02
    )

    mirror_finite = EllipticalMirror(
        name="KB-Y", photon_energy_eV=8000, image_distance_m=1.0,
        aperture_m=0.02, object_distance_m=10.0, source_size_m=10e-6
    )

    print(mirror_parallel)
    print(mirror_finite)
