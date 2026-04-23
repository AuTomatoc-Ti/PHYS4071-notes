"""Verify Chapter 7 example results for parts (b) and (c).

This script reproduces the acoustic-scale calculations used in:
- part (b): neighboring-peak separation for two choices of Omega_Lambda,0
- part (c): numerical values of r_s and l_A for the given parameter set

No third-party packages are required.
"""

from __future__ import annotations

import math


def simpson(f, a: float, b: float, n: int = 200_000) -> float:
    """Numerical integral using Simpson's rule."""
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += (4 if i % 2 else 2) * f(x)
    return s * h / 3


def sound_horizon_comoving_mpc(z_rec: float, omega_b: float, omega_gamma: float, omega_r: float, omega_m: float) -> tuple[float, float, float, float]:
    """Return (r_s^c, a_rec, I_s, prefactor) in Mpc units for r_s^c."""
    a_rec = 1.0 / (1.0 + z_rec)
    r_b = 0.75 * (omega_b / omega_gamma)
    r_m = omega_m / omega_r

    integrand = lambda a: 1.0 / math.sqrt(1.0 + r_b * a) / math.sqrt(1.0 + r_m * a)
    i_s = simpson(integrand, 0.0, a_rec)
    prefactor = 3000.0 / math.sqrt(3.0 * omega_r)
    r_s_c = prefactor * i_s
    return r_s_c, a_rec, i_s, prefactor


def d_a_comoving_mpc(z_rec: float, h: float, omega_m0: float, omega_lambda0: float) -> tuple[float, float]:
    """Return (d_A^c, I_d) with d_A^c in Mpc."""
    a_rec = 1.0 / (1.0 + z_rec)
    omega_k0 = 1.0 - omega_m0 - omega_lambda0

    integrand = lambda a: 1.0 / (
        a * a * math.sqrt(omega_m0 * a ** (-3) + omega_lambda0 + omega_k0 * a ** (-2))
    )
    i_d = simpson(integrand, a_rec, 1.0)
    d_a_c = (3000.0 / h) * i_d
    return d_a_c, i_d


def main() -> None:
    # Given/assumed constants from the chapter and question
    z_rec = 1090.0
    omega_d0 = 0.3
    omega_lambda0 = 0.0
    h = 0.7
    omega_b = 0.02

    omega_gamma = 2.4702e-5
    omega_r = 4.1756e-5
    omega_m = omega_d0 * h * h

    print("=== Inputs ===")
    print(f"z_rec = {z_rec}")
    print(f"Omega_d,0 = {omega_d0}")
    print(f"Omega_Lambda,0 = {omega_lambda0}")
    print(f"h = {h}")
    print(f"omega_b = {omega_b}")
    print(f"omega_gamma = {omega_gamma}")
    print(f"omega_r = {omega_r}")
    print(f"omega_m = Omega_d,0 * h^2 = {omega_m}")

    print("\n=== Part (c): r_s and l_A for Omega_Lambda,0 = 0 ===")
    r_s_c, a_rec, i_s, pref_s = sound_horizon_comoving_mpc(
        z_rec=z_rec,
        omega_b=omega_b,
        omega_gamma=omega_gamma,
        omega_r=omega_r,
        omega_m=omega_m,
    )
    r_s_phys = a_rec * r_s_c

    print(f"a_rec = 1/(1+z_rec) = {a_rec:.12e}")
    print(f"R_b = (3/4)(omega_b/omega_gamma) = {0.75 * omega_b / omega_gamma:.6f}")
    print(f"R_m = omega_m/omega_r = {omega_m / omega_r:.6f}")
    print(f"I_s = integral_0^a_rec [...] da = {i_s:.12e}")
    print(f"prefactor = 3000/sqrt(3*omega_r) = {pref_s:.6f}")
    print(f"r_s^c = prefactor * I_s = {r_s_c:.6f} Mpc")
    print(f"r_s = a_rec * r_s^c = {r_s_phys:.6f} Mpc = {r_s_phys * 1e3:.3f} kpc")

    d_open, i_d_open = d_a_comoving_mpc(
        z_rec=z_rec,
        h=h,
        omega_m0=omega_d0,
        omega_lambda0=0.0,
    )
    l_a_open = math.pi * d_open / r_s_c
    print(f"I_d (Omega_Lambda,0=0) = integral_a_rec^1 [...] da = {i_d_open:.6f}")
    print(f"d_A^c (Omega_Lambda,0=0) = (3000/h) * I_d = {d_open:.6f} Mpc")
    print(f"l_A (Omega_Lambda,0=0) = pi * d_A^c / r_s^c = {l_a_open:.6f}")

    print("\n=== Part (b): neighboring-peak separation ===")
    d_flat, i_d_flat = d_a_comoving_mpc(
        z_rec=z_rec,
        h=h,
        omega_m0=omega_d0,
        omega_lambda0=1.0 - omega_d0,
    )
    l_a_flat = math.pi * d_flat / r_s_c

    delta_l_open = l_a_open
    delta_l_flat = l_a_flat

    print(f"I_d (Omega_Lambda,0=0.7) = integral_a_rec^1 [...] da = {i_d_flat:.6f}")
    print(f"d_A^c (Omega_Lambda,0=0.7) = {d_flat:.6f} Mpc")
    print(f"Delta l ~= l_A (Omega_Lambda,0=0)   = {delta_l_open:.6f}")
    print(f"Delta l ~= l_A (Omega_Lambda,0=0.7) = {delta_l_flat:.6f}")
    print(f"relative increase = {(delta_l_flat - delta_l_open) / delta_l_open * 100:.3f}%")

    # Loose sanity checks against values quoted in the notes.
    assert abs(r_s_c - 144.93) < 0.5
    assert abs(r_s_phys - 0.133) < 0.005
    assert abs(l_a_open - 258.4) < 1.5
    assert abs(l_a_flat - 296.8) < 1.5

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
