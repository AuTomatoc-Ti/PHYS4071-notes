import numpy as np
import matplotlib.pyplot as plt

# Present-day density parameters (Planck 2018 values)
Omega_r0 = 9.4e-5   # radiation (photons + neutrinos)
Omega_d0 = 0.315    # matter (dark matter + baryons)
Omega_L0 = 1.0 - Omega_r0 - Omega_d0  # dark energy (flat universe)

# Redshift range: log scale from z=0.001 to z=1e6
z = np.logspace(-3, 6, 10000)

# Hubble function squared: E^2(z) = H^2(z)/H0^2
E2 = Omega_r0 * (1 + z)**4 + Omega_d0 * (1 + z)**3 + Omega_L0

# Density parameters as functions of z
Omega_r = Omega_r0 * (1 + z)**4 / E2
Omega_d = Omega_d0 * (1 + z)**3 / E2
Omega_L = Omega_L0 / E2

# Find crossing redshifts
# 1. Omega_r = Omega_d  (matter-radiation equality)
diff_rd = Omega_r - Omega_d
idx_rd = np.argmin(np.abs(diff_rd))
z_rd = z[idx_rd]

# 2. Omega_d = Omega_L  (matter-dark energy equality)
diff_dL = Omega_d - Omega_L
idx_dL = np.argmin(np.abs(diff_dL))
z_dL = z[idx_dL]

print(f"Radiation-Matter equality:    z ≈ {z_rd:.1f}")
print(f"Matter-Dark Energy equality:  z ≈ {z_dL:.3f}")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))

ax.semilogx(1 + z, Omega_r, color='firebrick',  lw=2.2, label=r'$\Omega_r(z)$  (Radiation)')
ax.semilogx(1 + z, Omega_d, color='steelblue',  lw=2.2, label=r'$\Omega_d(z)$  (Matter)')
ax.semilogx(1 + z, Omega_L, color='darkorange', lw=2.2, label=r'$\Omega_\Lambda(z)$  (Dark Energy)')

# Mark crossing points
ax.axvline(1 + z_rd, color='steelblue', ls='--', lw=1.2, alpha=0.7)
ax.axvline(1 + z_dL, color='darkorange', ls='--', lw=1.2, alpha=0.7)

ax.annotate(fr'$\Omega_r = \Omega_d$'+f'\n$z \\approx {z_rd:.0f}$',
            xy=(1 + z_rd, 0.5), xytext=(1 + z_rd * 10, 0.62),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=11, ha='left', color='gray')

ax.annotate(fr'$\Omega_d = \Omega_\Lambda$'+f'\n$z \\approx {z_dL:.2f}$',
            xy=(1 + z_dL, 0.5), xytext=(1 + z_dL * 0.05, 0.62),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=11, ha='right', color='gray')

ax.set_xlabel(r'$1 + z$', fontsize=13)
ax.set_ylabel(r'$\Omega_i(z)$', fontsize=13)
ax.set_title(r'Cosmic Energy Budget in $\Lambda$CDM (flat universe)', fontsize=14)
ax.set_xlim(1e-3 * (1 + z[-1]), 1 + z[-1])   # show full range
ax.set_xlim(1, 1e7)
ax.set_ylim(-0.02, 1.05)
ax.legend(fontsize=12, loc='center right')
ax.grid(True, which='both', ls=':', alpha=0.4)

# Add era labels
ax.text(3, 0.92, 'Dark-Energy\ndominated', fontsize=10, color='darkorange', ha='center')
ax.text(50, 0.92, 'Matter\ndominated', fontsize=10, color='steelblue', ha='center')
ax.text(3e5, 0.92, 'Radiation\ndominated', fontsize=10, color='firebrick', ha='center')

plt.tight_layout()
plt.savefig('/Users/automatocti/Documents/ust/course/PHYS4071/lcdm_energy_budget.png', dpi=150)
plt.show()
print("Plot saved.")
