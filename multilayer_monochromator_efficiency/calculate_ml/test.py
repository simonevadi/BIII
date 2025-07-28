import numpy as np

def calculate_beta_and_cff(alpha_deg, energy_eV, grating_density_lmm):
    """
    Calculate the diffraction angle (beta) and the coupling factor (cff) for a grating.

    Args:
        alpha_deg (float): Incident angle (alpha) in degrees.
        energy_eV (float): Photon energy in eV.
        grating_density_lmm (float): Grating density in lines per mm.

    Returns:
        beta_deg (float): Diffraction angle (beta) in degrees.
        cff (float): Coupling factor (cff).
    """
    
    # Constants
    hc = 1239.84187  # Planck constant * speed of light in eV*nm
    
    # Convert alpha from degrees to radians
    alpha_rad = np.deg2rad(alpha_deg)
    
    # Convert grating density from lines/mm to lines/m
    grating_density = grating_density_lmm * 1e3  # in lines/m
    
    # Calculate grating spacing (d)
    d = 1 / grating_density  # in meters
    
    # Calculate wavelength (lambda) from energy
    wavelength = hc / energy_eV*1e-9  # in m
    # Solve grating equation: m * lambda = d * (sin(alpha) + sin(beta))
    # For first order diffraction (m = 1):
    m = 2
    # Grating equation: lambda = d * (sin(alpha) + sin(beta))
    # Rearranging for sin(beta): sin(beta) = (lambda / d) - sin(alpha)
    sin_alpha = np.sin(alpha_rad)
    sin_beta = (m*wavelength / d) - sin_alpha
    
    if sin_beta < -1 or sin_beta > 1:
        raise ValueError("No physical solution for beta. Check your inputs.")
    
    # Calculate beta (diffraction angle)
    beta_rad = np.arcsin(sin_beta)
    beta_deg = np.degrees(beta_rad)
    
    # Calculate the coupling factor (cff) based on the grating equation:
    # cff = lambda / (2 * d * sin(alpha)) for first-order diffraction
    cff = np.cos(beta_rad)/np.cos(alpha_rad)
    
    return beta_deg+90, cff

# Example usage:
alpha = 75.82364478  # Incident angle in degrees (converted from 90 - 75.82)
energy = 500    # Photon energy in eV
grating_density = 2400  # Grating density in lines/mm

beta, cff = calculate_beta_and_cff(alpha, energy, grating_density)
print(f"Diffraction angle (beta): {beta:.6f}°")
print(f"Coupling factor (cff): {cff:.6e}")
