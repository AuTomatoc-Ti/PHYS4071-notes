import numpy as np


def saha_get_ionization_fraction(T):
    r"""
    Calculate the hydrogen ionization fraction using the Saha equation in SI units.

    For x_e = n_p / (n_p + n_H),

    \frac{x_e^2}{1 - x_e} =
    \frac{1}{n_b}
    \left(\frac{m_e k_B T}{2\pi\hbar^2}\right)^{3/2}
    \exp\left(-\frac{\chi}{k_B T}\right),

    where n_b = \eta n_\gamma and
    n_\gamma = \frac{2\zeta(3)}{\pi^2}\left(\frac{k_B T}{\hbar c}\right)^3.
    
    This returns x_e (named Y_p here for compatibility with existing code).
    Parameters:
    T (float): Temperature in Kelvin.
    Returns:
    float: Ionization fraction Y_p.
    """
    if T <= 0.0:
        raise ValueError("T must be positive.")

    # Constants
    eta = 6e-10  # Baryon-to-photon ratio
    m_e = 9.1093837015e-31  # Electron mass in kg
    c = 299792458.0  # Speed of light in m/s
    k_B = 1.380649e-23  # Boltzmann constant in J/K
    hbar = 1.054571817e-34  # Reduced Planck constant in J s
    B = 13.6 * 1.602176634e-19  # Ionization energy of hydrogen in Joules
    zeta_3 = 1.202056903159594  # Riemann zeta function at 3

    n_gamma = (2.0 * zeta_3 / np.pi**2) * (k_B * T / (hbar * c))**3
    n_b = eta * n_gamma

    # x^2/(1-x)=r -> x^2 + r*x - r = 0.
    # Use an algebraically equivalent form that avoids cancellation for large r.
    r = (1.0 / n_b) * (m_e * k_B * T / (2.0 * np.pi * hbar**2))**1.5 * np.exp(-B / (k_B * T))
    if r <= 0.0:
        return 0.0
    Y_p = (2.0 * r) / (r + np.sqrt(r * r + 4.0 * r))
    Y_p = min(float(Y_p), np.nextafter(1.0, 0.0))

    return Y_p

def saha_get_temperature_for_ionization_fraction(Y_p):
    """
    Calculate the temperature for a given ionization fraction using the Saha equation.

    Parameters:
    Y_p (float): Ionization fraction.
    
    Returns:
    float: Temperature in Kelvin.
    """
    if not (0.0 < Y_p < 1.0):
        raise ValueError("Y_p must be in the open interval (0, 1).")

    # Constants
    eta = 6e-10  # Baryon-to-photon ratio
    m_e = 9.1093837015e-31  # Electron mass in kg
    c = 299792458.0  # Speed of light in m/s
    k_B = 1.380649e-23  # Boltzmann constant in J/K
    hbar = 1.054571817e-34  # Reduced Planck constant in J s
    B = 13.6 * 1.602176634e-19  # Ionization energy of hydrogen in Joules
    zeta_3 = 1.202056903159594  # Riemann zeta function at 3

    r_target = (Y_p**2) / (1.0 - Y_p)

    # Combine constants so r(T) = C * T^{-3/2} * exp(-B/(k_B T)).
    C = (
        (np.pi**2 / (2.0 * zeta_3))
        * (1.0 / eta)
        * (m_e * k_B / (2.0 * np.pi * hbar**2))**1.5
        * (hbar * c / k_B) ** 3
    )
    log_r_target = np.log(r_target)

    from scipy.optimize import root_scalar

    def f_log(T):
        log_model = np.log(C) - 1.5 * np.log(T) - (B / (k_B * T))
        return log_model - log_r_target

    T = root_scalar(f_log, bracket=[1.0, 1e6], method='brentq').root
    return T

def mean_free_path(Y_p):
    return mean_free_path_of_photon(Y_p)


def mean_free_path_of_photon(Y_p, comoving=True, unit="Mpc", T0=2.7255):
    r"""
    Calculate the photon mean free path from the ionization fraction.

    Physical mean free path:
    \\lambda_{phys} = \frac{1}{n_e \sigma_T},
    with n_e = x_e n_b, n_b = \eta n_\gamma,
    n_\gamma = \frac{2\zeta(3)}{\pi^2}\left(\frac{k_B T}{\hbar c}\right)^3.

    If comoving=True, return \lambda_{com} = \lambda_{phys}(1+z), where
    1+z = T/T0.

    Parameters:
    Y_p (float): Ionization fraction x_e in (0, 1).
    comoving (bool): Return comoving mean free path when True.
    unit (str): One of "m", "km", "pc", "kpc", "Mpc".
    T0 (float): Present CMB temperature in K, default 2.7255.

    Returns:
    float: Mean free path in requested unit.
    """
    if not (0.0 < Y_p < 1.0):
        raise ValueError("Y_p must be in the open interval (0, 1).")
    if T0 <= 0.0:
        raise ValueError("T0 must be positive.")

    # Constants (SI)
    eta = 6e-10  # Baryon-to-photon ratio
    zeta_3 = 1.202056903159594
    k_B = 1.380649e-23  # J/K
    hbar = 1.054571817e-34  # J s
    c = 299792458.0  # m/s
    sigma_T = 6.6524587321e-29  # Thomson cross section in m^2

    T = saha_get_temperature_for_ionization_fraction(Y_p)
    n_gamma = (2.0 * zeta_3 / np.pi**2) * (k_B * T / (hbar * c))**3
    n_b = eta * n_gamma
    n_e = Y_p * n_b
    #print(f"At T={T:.2f} K, the electron number density n_e is approximately {n_e:.4e} m^-3.")

    if n_e <= 0.0:
        raise ValueError("Computed electron number density is non-positive.")

    lambda_phys_m = 1.0 / (n_e * sigma_T)
    lambda_out_m = lambda_phys_m * (T / T0) if comoving else lambda_phys_m

    unit_scale = {
        "m": 1.0,
        "km": 1e3,
        "pc": 3.085677581491367e16,
        "kpc": 3.085677581491367e19,
        "Mpc": 3.085677581491367e22,
    }
    if unit not in unit_scale:
        raise ValueError("unit must be one of: m, km, pc, kpc, Mpc")

    return lambda_out_m / unit_scale[unit]


def mean_free_path_physical_and_comoving_mpc(Y_p, T0=2.7255):
    """
    Return both physical and comoving photon mean free path in Mpc.

    Parameters:
    Y_p (float): Ionization fraction x_e in (0, 1).
    T0 (float): Present CMB temperature in K, default 2.7255.

    Returns:
    tuple[float, float, float]: (lambda_physical_Mpc, lambda_comoving_Mpc, n_e)
    """
    eta = 6e-10
    zeta_3 = 1.202056903159594
    k_B = 1.380649e-23
    hbar = 1.054571817e-34
    c = 299792458.0

    T = saha_get_temperature_for_ionization_fraction(Y_p)
    n_gamma = (2.0 * zeta_3 / np.pi**2) * (k_B * T / (hbar * c))**3
    n_b = eta * n_gamma
    n_e = Y_p * n_b

    lambda_physical_mpc = mean_free_path_of_photon(Y_p, comoving=False, unit="Mpc", T0=T0)
    lambda_comoving_mpc = mean_free_path_of_photon(Y_p, comoving=True, unit="Mpc", T0=T0)
    return lambda_physical_mpc, lambda_comoving_mpc, n_e


def inverse_mean_free_path_of_photon(lambda_value, comoving=True, unit="Mpc", T0=2.7255):
    """
    Invert mean free path to estimate Y_p.

    Parameters:
    lambda_value (float): Mean free path value in the specified unit.
    comoving (bool): True if lambda_value is comoving, False if physical.
    unit (str): One of "m", "km", "pc", "kpc", "Mpc".
    T0 (float): Present CMB temperature in K, default 2.7255.

    Returns:
    float: Ionization fraction Y_p in (0, 1).
    """
    if lambda_value <= 0.0:
        raise ValueError("lambda_value must be positive.")
    if T0 <= 0.0:
        raise ValueError("T0 must be positive.")

    unit_scale = {
        "m": 1.0,
        "km": 1e3,
        "pc": 3.085677581491367e16,
        "kpc": 3.085677581491367e19,
        "Mpc": 3.085677581491367e22,
    }
    if unit not in unit_scale:
        raise ValueError("unit must be one of: m, km, pc, kpc, Mpc")

    from scipy.optimize import root_scalar

    def f(Y):
        return mean_free_path_of_photon(Y, comoving=comoving, unit=unit, T0=T0) - lambda_value

    # For the relevant regime in this notebook, lambda(Y) is monotonic decreasing.
    y_min = 1e-12
    y_max = 1.0 - 1e-12
    f_min = f(y_min)
    f_max = f(y_max)
    if f_min * f_max > 0.0:
        raise ValueError(
            "lambda_value is outside the invertible range for current model settings."
        )

    return root_scalar(f, bracket=[y_min, y_max], method="brentq").root


if __name__ == "__main__":
    # Example usage
    # Q1a. How large is the mean free path of photons near recombination(Y_p ~ 0.5)?
    print("Q1a. Mean free path of photons near recombination (Y_p ~ 0.5):")
    Y_p_target = 0.5
    T_computed = saha_get_temperature_for_ionization_fraction(Y_p_target)
    print(f"For an ionization fraction of Y_p={Y_p_target}, the corresponding temperature is approximately {T_computed:.2f} K, and the redshift is approximately {T_computed/2.7255 - 1:.0f}.")
    lambda_phys_mpc, lambda_com_mpc, n_e = mean_free_path_physical_and_comoving_mpc(Y_p_target)
    print(f"Electron number density at Y_p={Y_p_target} is approximately {n_e:.4e} m^-3")
    print(f"Physical photon mean free path at Y_p={Y_p_target} is approximately {lambda_phys_mpc:.4f} Mpc")
    print(f"Comoving photon mean free path at Y_p={Y_p_target} is approximately {lambda_com_mpc:.2f} Mpc")
    

    # Q1b. What is the ionization fraction at z=1090, and when \lambda_gamma > 1/H?
    # calculate the n_e first by 1/H = sigma_T * n_e
    print("\nQ1b. Ionization fraction at z=1090, and when lambda_gamma > 1/H:")
    z_target = 1090.0
    T_target = 2.7255 * (1.0 + z_target)
    H_0 = 1/(3/70*(10**5) * 3.085677581491367e22)   # Hubble constant in m^-1
    print("Hubble constant H_0 in m^-1:", H_0)
    H = H_0 * np.sqrt(0.3 * (1 + z_target)**3 )  # Hubble parameter at z
    n_e_target = H / 6.6524587321e-29  # n_e from 1/H = sigma_T * n_e
    print(f"At z={z_target}, the Hubble parameter H is approximately {H:.4e} m^-1, and the corresponding electron number density n_e is approximately {n_e_target:.4e} m^-3.")
    # then calculate the ionization fraction Y_p from n_e = Y_p * n_b, where n_b = eta * n_gamma
    n_gamma_target = (2.0 * 1.202056903159594 / np.pi**2) * (1.380649e-23 * T_target / (1.054571817e-34 * 299792458.0))**3
    n_b_target = 6e-10 * n_gamma_target
    Y_p_target = n_e_target / n_b_target
    print(f"At z={z_target}, the ionization fraction Y_p is approximately {Y_p_target:.4e}.")
    # Lets compare this with the Saha prediction at the same temperature:
    Y_p_saha = saha_get_ionization_fraction(T_target)
    print(f"Saha prediction for ionization fraction at T={T_target:.2f} K (z={z_target}): Y_p={Y_p_saha:.4e}")

    # Q1c. In reionization, when Y_p ~ 1.0, while λ_γ > c/H, what is the redshift?
    # Condition: 1/(n_e σ_T) > c/H  ⟺  n_e * σ_T * c < H(z)
    print("\nQ1c. Redshift when Y_p ~ 1.0 and lambda_gamma > c/H (Hubble distance):")

    from scipy.optimize import brentq

    H0_kmsMpc = 70.0  # Hubble constant in km/s/Mpc
    H0_SI = (H0_kmsMpc * 1e3) / 3.085677581491367e22  # Convert to s^-1
    Omega_m = 0.3
    Y_p_full = 0.9999  # Fully ionized
    sigma_T = 6.6524587321e-29
    T0_cmb = 2.7255
    c = 299792458.0
    
    # Physical constants for coefficient calculation
    k_B = 1.380649e-23  # Boltzmann constant (J/K)
    hbar = 1.054571817e-34  # Reduced Planck constant (J·s)
    zeta_3 = 1.202056903159594  # Riemann zeta(3)
    eta = 6e-10  # Baryon-to-photon ratio
    
    print("\nStep 1: Express n_e coefficient in terms of T")
    print(f"  n_γ(T) = (2ζ(3)/π²) × (k_B T / ℏc)³")
    print(f"  n_γ(T) = {2.0 * zeta_3 / np.pi**2:.4e} × (T / {hbar * c / k_B:.2e})³")
    print(f"  n_e(T) = Y_p × η × n_γ(T)")
    print(f"         = {Y_p_full} × {eta} × n_γ(T)")
    
    # Coefficient for n_e in terms of T
    coeff_n_e = Y_p_full * eta * (2.0 * zeta_3 / np.pi**2) * (k_B / (hbar * c))**3
    T_scale_inv_cubed = (hbar * c / k_B)**3
    print(f"  n_e(T) = {coeff_n_e:.4e} × T³ [m⁻³]")
    
    print("\nStep 2: Express H(z) in terms of T")
    print(f"  T = T₀(1 + z) = {T0_cmb} × (1 + z)")
    print(f"  Since z = T/{T0_cmb} - 1, we have (1 + z) = T/{T0_cmb}")
    print(f"  H(z) = H₀√Ω_m × (1 + z)^1.5")
    print(f"       = H₀√Ω_m × (T/{T0_cmb})^1.5")
    coeff_H = H0_SI * np.sqrt(Omega_m) * (T0_cmb)**(-1.5)
    print(f"  H(T) = {coeff_H:.4e} × T^1.5 [s⁻¹]")
    
    print("\nStep 3: Apply condition σ_T n_e c = H")
    print(f"  σ_T × n_e(T) × c = H(T)")
    print(f"  {sigma_T:.4e} × [{coeff_n_e:.4e} × T³] × {c} = {coeff_H:.4e} × T^1.5")
    
    # Rewrite for solving
    lhs_coeff = sigma_T * coeff_n_e * c
    rhs_coeff = coeff_H
    print(f"  {lhs_coeff:.4e} × T³ = {rhs_coeff:.4e} × T^1.5")
    print(f"  {lhs_coeff:.4e} × T^1.5 = {rhs_coeff:.4e}")
    print(f"  T^1.5 = {rhs_coeff/lhs_coeff:.4e}")
    
    T_solution = (rhs_coeff / lhs_coeff)**(2.0/3.0)
    z_solution = T_solution / T0_cmb - 1.0
    print(f"\nSolving numerically with Brent's method:")

    def condition_q1c(z):
        T = T0_cmb * (1.0 + z)
        n_gamma = (2.0 * zeta_3 / np.pi**2) * (k_B * T / (hbar * c))**3
        n_e = Y_p_full * eta * n_gamma
        H_z = H0_SI * np.sqrt(Omega_m) * (1.0 + z)**1.5
        return n_e * sigma_T * c - H_z  # Transition when this = 0

    z_q1c = brentq(condition_q1c, 10.0, 200.0)
    T_q1c = T0_cmb * (1.0 + z_q1c)
    print(f"At Y_p ~ 1.0, the redshift when λ_γ > c/H is approximately z ≈ {z_q1c:.1f} (T ≈ {T_q1c:.2f} K).")
   