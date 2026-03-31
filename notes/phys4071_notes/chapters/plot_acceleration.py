#!/usr/bin/env python3
r"""
Generate a plot of $\ddot{a}$ vs redshift z for LCDM cosmology
with Omega_m0 = 0.315 and Omega_Lambda0 = 0.685
"""

import numpy as np
import matplotlib.pyplot as plt

# Cosmological parameters
H0_kms = 70.0  # H0 in km/s/Mpc (not needed for relative plot)
Omega_m0 = 0.315
Omega_Lambda0 = 0.685

# Redshift range
z = np.linspace(0, 5, 500)

# Normalized Hubble parameter E(z) = H(z)/H0
E_z = np.sqrt(Omega_m0 * (1 + z)**3 + Omega_Lambda0)

# Second acceleration parameter
# ddot{a}/a = -H0^2/2 * [Omega_m0 * (1+z)^3 - 2*Omega_Lambda0]
# Normalize by H0^2: (ddot{a}/a) / H0^2
accel_normalized = -0.5 * (Omega_m0 * (1 + z)**3 - 2 * Omega_Lambda0)

# Transition redshift where ddot{a} = 0
z_trans = (2 * Omega_Lambda0 / Omega_m0)**(1/3) - 1

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# Plot 1: Acceleration parameter vs redshift
ax1.plot(z, accel_normalized, 'b-', linewidth=2.5, label=r'$\frac{\ddot{a}}{aH_0^2}$')
ax1.axhline(y=0, color='k', linestyle='--', linewidth=0.8, alpha=0.5)
ax1.axvline(x=z_trans, color='r', linestyle='--', linewidth=1.5, alpha=0.7, 
            label=f'$z_{{acc}}$ = {z_trans:.3f}')
ax1.fill_between(z, accel_normalized, 0, where=(accel_normalized < 0), 
                  alpha=0.3, color='red', label='Deceleration')
ax1.fill_between(z, accel_normalized, 0, where=(accel_normalized >= 0), 
                  alpha=0.3, color='green', label='Acceleration')
ax1.set_xlabel(r'Redshift $z$', fontsize=12)
ax1.set_ylabel(r'$\frac{\ddot{a}}{aH_0^2}$', fontsize=12)
ax1.set_title(r'Cosmic Acceleration in $\Lambda$CDM: $\ddot{a}/a$ vs $z$', fontsize=13)
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=11, loc='lower right')
ax1.set_xlim(0, 5)

# Plot 2: Absolute value of acceleration (log scale) to see behavior clearly
ax2.semilogy(z, np.abs(accel_normalized), 'b-', linewidth=2.5, label=r'$\left|\frac{\ddot{a}}{aH_0^2}\right|$')
ax2.axvline(x=z_trans, color='r', linestyle='--', linewidth=1.5, alpha=0.7, 
            label=f'$z_{{acc}}$ = {z_trans:.3f}')
ax2.set_xlabel(r'Redshift $z$', fontsize=12)
ax2.set_ylabel(r'$\left|\frac{\ddot{a}}{aH_0^2}\right|$', fontsize=12)
ax2.set_title(r'Magnitude of Acceleration (log scale)', fontsize=13)
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(fontsize=11, loc='upper right')
ax2.set_xlim(0, 5)

plt.tight_layout()

# Save as PDF (for LaTeX inclusion)
output_path = '/Users/automatocti/Documents/ust/course/PHYS4071/notes/phys4071_notes/chapters/images/acceleration_plot.pdf'
plt.savefig(output_path, format='pdf', dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to: {output_path}")

# Also save as PNG for reference
png_path = '/Users/automatocti/Documents/ust/course/PHYS4071/notes/phys4071_notes/chapters/images/acceleration_plot.png'
plt.savefig(png_path, format='png', dpi=150, bbox_inches='tight')
print(f"✓ PNG also saved to: {png_path}")

plt.close()

# Print numerical values for reference
print("\nNumerical Summary:")
print(f"  Omega_m0 = {Omega_m0}, Omega_Lambda0 = {Omega_Lambda0}")
print(f"  Transition redshift z_acc = {z_trans:.4f}")
print(f"\nAcceleration parameter at selected redshifts:")
print(f"  z = 0.0:  (ddot{{a}}/aH_0^2) = {accel_normalized[0]:.6f}")
z_idx_low = np.argmin(np.abs(z - 0.5))
print(f"  z = 0.5:  (ddot{{a}}/aH_0^2) = {accel_normalized[z_idx_low]:.6f}")
z_idx_trans = np.argmin(np.abs(z - z_trans))
print(f"  z = {z_trans:.3f}: (ddot{{a}}/aH_0^2) = {accel_normalized[z_idx_trans]:.6e} (≈0)")
z_idx_high = np.argmin(np.abs(z - 2.0))
print(f"  z = 2.0:  (ddot{{a}}/aH_0^2) = {accel_normalized[z_idx_high]:.6f}")

# Generate TikZ coordinates for reference
print("\nTikZ plot data (first 10 points for reference):")
for i in range(0, min(100, len(z)), 10):
    print(f"  ({z[i]:.3f}, {accel_normalized[i]:.4f})")
