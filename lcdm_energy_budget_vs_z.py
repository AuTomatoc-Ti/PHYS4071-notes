import numpy as np
import matplotlib.pyplot as plt

# Present-day density parameters (Planck 2018 values)
Omega_r0 = 9.4e-5   # radiation (photons + neutrinos)
Omega_d0 = 0.315    # matter (dark matter + baryons)
Omega_L0 = 1.0 - Omega_r0 - Omega_d0  # dark energy (flat universe)

# Redshift range: focus on z from 0 to 5 for better visibility
z = np.linspace(0, 5, 1000)

# Hubble function squared: E^2(z) = H^2(z)/H0^2
E2 = Omega_r0 * (1 + z)**4 + Omega_d0 * (1 + z)**3 + Omega_L0

# Density parameters as functions of z
Omega_r = Omega_r0 * (1 + z)**4 / E2
Omega_d = Omega_d0 * (1 + z)**3 / E2
Omega_L = Omega_L0 / E2

# Find crossing redshifts
# 1. Omega_d = Omega_L  (matter-dark energy equality)
diff_dL = Omega_d - Omega_L
idx_dL = np.argmin(np.abs(diff_dL))
z_dL = z[idx_dL]

print(f"Matter-Dark Energy equality:  z ≈ {z_dL:.3f}")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))

ax.plot(z, Omega_r, color='firebrick',  lw=2.2, label=r'$\Omega_r(z)$  (Radiation)')
ax.plot(z, Omega_d, color='steelblue',  lw=2.2, label=r'$\Omega_d(z)$  (Matter)')
ax.plot(z, Omega_L, color='darkorange', lw=2.2, label=r'$\Omega_\Lambda(z)$  (Dark Energy)')

# Mark crossing point
ax.axvline(z_dL, color='gray', ls='--', lw=1.2, alpha=0.7)

ax.annotate(fr'$\Omega_d = \Omega_\Lambda$'+f'\n$z = {z_dL:.2f}$',
            xy=(z_dL, 0.5), xytext=(z_dL + 0.8, 0.65),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=11, ha='left', color='gray')

ax.set_xlabel(r'Redshift $z$', fontsize=13)
ax.set_ylabel(r'$\Omega_i(z)$', fontsize=13)
ax.set_title(r'Cosmic Energy Budget vs Redshift in $\Lambda$CDM', fontsize=14)
ax.set_xlim(0, 5)
ax.set_ylim(-0.02, 1.05)
ax.legend(fontsize=12, loc='right')
ax.grid(True, ls=':', alpha=0.4)

# Add era labels
ax.text(0.5, 0.92, 'Present Era\n(Dark Energy\ndominated)', fontsize=10, color='darkorange', ha='center')
ax.text(2.5, 0.92, 'Matter\ndominated', fontsize=10, color='steelblue', ha='center')

plt.tight_layout()
plt.savefig('/Users/automatocti/Documents/ust/course/PHYS4071/lcdm_energy_budget_vs_z.png', dpi=150)
plt.show()
print("Plot saved.")
