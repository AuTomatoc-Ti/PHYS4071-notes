#!/usr/bin/env python3
r"""
Plot the scale factor evolution a(t) for a dust-dominated flat universe
with Omega_d = 0.3 (and Omega_Lambda = 0.7), compared to Einstein-de Sitter.
"""

import numpy as np
import matplotlib.pyplot as plt

# Cosmological parameters
H0 = 70.0  # km/s/Mpc
Omega_d0 = 0.3
Omega_L0 = 0.7

# Hubble time in Gyr
H0_inv_Gyr = 977.8 / H0  # H0^-1 in Gyr

# Time array (normalized to H0^-1)
t_norm = np.linspace(0.001, 1.2, 1000)

# ── LambdaCDM: Omega_d=0.3, Omega_L=0.7 ──────────────────────────────────────
# t(a) = 2/(3*H0*sqrt(Omega_L)) * asinh(sqrt(Omega_L/Omega_d) * a^(3/2))
# Invert numerically to get a(t)
a_lcdm = np.zeros_like(t_norm)
for i, t_val in enumerate(t_norm):
    # Solve for a given t using the analytical inverse
    # sinh(3/2 * sqrt(Omega_L) * H0 * t) = sqrt(Omega_L/Omega_d) * a^(3/2)
    arg = 1.5 * np.sqrt(Omega_L0) * t_val
    a_lcdm[i] = (Omega_d0 / Omega_L0)**(1/3) * np.sinh(arg)**(2/3)

# ── Einstein-de Sitter: Omega_d=1.0, Omega_L=0 ──────────────────────────────
# a(t) = (t/t0)^(2/3), with t0 = 2/(3*H0)
a_ed = (t_norm / (2/3))**(2/3)

# ── Present age for LambdaCDM ────────────────────────────────────────────────
t0_lcdm_norm = 2/(3*np.sqrt(Omega_L0)) * np.arcsinh(np.sqrt(Omega_L0/Omega_d0))
t0_ed_norm = 2/3

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(t_norm, a_lcdm, 'b-', linewidth=2.5, label=r'$\Lambda$CDM: $\Omega_d=0.3,\ \Omega_\Lambda=0.7$')
ax.plot(t_norm, a_ed, 'r--', linewidth=2, label=r'Einstein-de Sitter: $\Omega_d=1$')

# Mark present day (a=1)
ax.axhline(y=1.0, color='k', linestyle=':', linewidth=1, alpha=0.5)
ax.axvline(x=t0_lcdm_norm, color='b', linestyle='--', linewidth=1.2, alpha=0.6,
           label=f'$t_0^{{\Lambda\mathrm{{CDM}}}}$ = {t0_lcdm_norm:.3f} $H_0^{{-1}}$')
ax.axvline(x=t0_ed_norm, color='r', linestyle='--', linewidth=1.2, alpha=0.6,
           label=f'$t_0^{{\mathrm{{EdS}}}}$ = {t0_ed_norm:.3f} $H_0^{{-1}}$')

# Mark transition redshift (deceleration to acceleration)
z_acc = (2 * Omega_L0 / Omega_d0)**(1/3) - 1
a_acc = 1 / (1 + z_acc)
t_acc_arg = 1.5 * np.sqrt(Omega_L0) * np.arcsinh(np.sqrt(Omega_L0 / Omega_d0) * a_acc**(1.5))
# Actually compute t at a_acc directly
t_acc_norm = 2/(3*np.sqrt(Omega_L0)) * np.arcsinh(np.sqrt(Omega_L0/Omega_d0) * a_acc**(1.5))
ax.axvline(x=t_acc_norm, color='g', linestyle='-.', linewidth=1.2, alpha=0.6,
           label=f'$t_{{\mathrm{{acc}}}}$ = {t_acc_norm:.3f} $H_0^{{-1}}$')

ax.set_xlabel(r'Time $t$ (in units of $H_0^{-1}$)', fontsize=13)
ax.set_ylabel(r'Scale Factor $a(t)$', fontsize=13)
ax.set_title(r'Scale Factor Evolution: Dust-Dominated $\Omega_d=0.3$ vs Einstein-de Sitter', fontsize=13)
ax.set_xlim(0, 1.2)
ax.set_ylim(0, 2.5)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()

# Save
output_pdf = '/Users/automatocti/Documents/ust/course/PHYS4071/notes/phys4071_notes/chapters/images/dust_dominated_at.pdf'
output_png = '/Users/automatocti/Documents/ust/course/PHYS4071/notes/phys4071_notes/chapters/images/dust_dominated_at.png'
plt.savefig(output_pdf, format='pdf', dpi=300, bbox_inches='tight')
plt.savefig(output_png, format='png', dpi=150, bbox_inches='tight')
print(f"✓ Plot saved to: {output_pdf}")
print(f"✓ PNG saved to: {output_png}")

# Print summary
print(f"\nNumerical Summary:")
print(f"  Omega_d0 = {Omega_d0}, Omega_L0 = {Omega_L0}")
print(f"  Present age (LCDM): t0 = {t0_lcdm_norm:.4f} H0^-1 = {t0_lcdm_norm * H0_inv_Gyr:.2f} Gyr")
print(f"  Present age (EdS):  t0 = {t0_ed_norm:.4f} H0^-1 = {t0_ed_norm * H0_inv_Gyr:.2f} Gyr")
print(f"  Acceleration onset: z_acc = {z_acc:.3f}, a_acc = {a_acc:.3f}")
print(f"  Acceleration time:  t_acc = {t_acc_norm:.4f} H0^-1 = {t_acc_norm * H0_inv_Gyr:.2f} Gyr")
