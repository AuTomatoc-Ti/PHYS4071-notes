import numpy as np
import matplotlib.pyplot as plt

from saha import saha_get_ionization_fraction


def main():
    temperatures = np.geomspace(1500.0, 3.0e5, 900)
    ionization_fraction = np.array([
        saha_get_ionization_fraction(float(t)) for t in temperatures
    ])

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    ax = axes[0]
    ax.semilogx(temperatures, ionization_fraction, linewidth=2)
    ax.set_xlabel("Temperature T (K)")
    ax.set_ylabel("Ionization Fraction x_e")
    ax.set_title("Saha x_e(T): Wide Range")
    ax.set_ylim(0.0, 1.02)
    ax.grid(True, which="both", linestyle="--", alpha=0.5)

    ax = axes[1]
    t_zoom = np.linspace(2500.0, 6000.0, 700)
    x_zoom = np.array([saha_get_ionization_fraction(float(t)) for t in t_zoom])
    ax.plot(t_zoom, x_zoom, linewidth=2)
    ax.axhline(0.5, color="tab:gray", linestyle=":", linewidth=1.2)
    ax.axvline(3758.6, color="tab:red", linestyle="--", linewidth=1.2)
    ax.text(3785, 0.53, "x_e=0.5", fontsize=9, color="tab:red")
    ax.set_xlabel("Temperature T (K)")
    ax.set_ylabel("Ionization Fraction x_e")
    ax.set_title("Zoom Near Recombination")
    ax.set_xlim(2500.0, 6000.0)
    ax.set_ylim(0.0, 1.02)
    ax.grid(True, linestyle="--", alpha=0.5)

    output_path = "../images/saha_ionization_fraction_vs_temperature.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    print(f"Saved plot to: {output_path}")


if __name__ == "__main__":
    main()
