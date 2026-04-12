import numpy as np
import matplotlib.pyplot as plt

from saha import saha_get_ionization_fraction


def main():
    # CMB temperature today in Kelvin.
    t0 = 2.7255

    z = np.linspace(0.0, 2000.0, 1600)
    temperatures = t0 * (1.0 + z)
    x_e = np.array([saha_get_ionization_fraction(float(t)) for t in temperatures])

    z_ref = 1000.0
    x_ref = saha_get_ionization_fraction(t0 * (1.0 + z_ref))

    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    ax.plot(z, x_e, linewidth=2)
    ax.axvline(z_ref, color="tab:red", linestyle="--", linewidth=1.3)
    ax.axhline(x_ref, color="tab:gray", linestyle=":", linewidth=1.2)
    ax.scatter([z_ref], [x_ref], color="tab:red", zorder=3)
    ax.text(z_ref + 25.0, min(0.97, x_ref + 0.03), f"z=1000, x_e={x_ref:.3f}", color="tab:red")

    ax.set_xlim(0.0, 2000.0)
    ax.set_ylim(0.0, 1.02)
    ax.set_xlabel("Redshift z")
    ax.set_ylabel("Ionization Fraction x_e")
    ax.set_title("Saha Ionization Fraction x_e(z), with T = T0(1+z)")
    ax.grid(True, linestyle="--", alpha=0.5)

    output_path = "../images/saha_ionization_fraction_vs_redshift.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    print(f"Saved plot to: {output_path}")


if __name__ == "__main__":
    main()
