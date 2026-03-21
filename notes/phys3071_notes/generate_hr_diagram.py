from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def temperature_to_color(temperature: np.ndarray) -> np.ndarray:
    """Map effective temperature to a continuous white→blue→yellow→red spectrum."""
    t_hot = 30000.0
    t_cold = 3000.0
    u = np.clip((t_hot - temperature) / (t_hot - t_cold), 0.0, 1.0)

    cmap = LinearSegmentedColormap.from_list(
        "hr_spectrum",
        [
            (0.00, "#ffffff"),
            (0.30, "#6fa8ff"),
            (0.65, "#ffe680"),
            (1.00, "#d73027"),
        ],
    )
    return cmap(u)


def build_hr_catalog(seed: int = 3071) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)

    n_main = 7500
    n_giants = 1700
    n_dwarfs = 900

    # Main sequence: high T/high L at left-top, down to right-bottom
    logt_main = rng.uniform(np.log10(3200), np.log10(30000), n_main)
    t_main = 10 ** logt_main
    x_main = np.log10(t_main)
    y_main = 6.45 * x_main - 26.0 + rng.normal(0.0, 0.32, n_main)

    # Red giant branch and clump: luminous but cooler
    t_giant = 10 ** rng.uniform(np.log10(3200), np.log10(5600), n_giants)
    x_giant = np.log10(t_giant)
    y_giant = 2.2 + 1.8 * (3.76 - x_giant) + rng.normal(0.0, 0.22, n_giants)

    # White dwarfs: hot but dim
    t_dwarf = 10 ** rng.uniform(np.log10(7000), np.log10(30000), n_dwarfs)
    x_dwarf = np.log10(t_dwarf)
    y_dwarf = -1.8 + 2.2 * (x_dwarf - 4.0) + rng.normal(0.0, 0.18, n_dwarfs)

    return {
        "t_main": t_main,
        "y_main": y_main,
        "t_giant": t_giant,
        "y_giant": y_giant,
        "t_dwarf": t_dwarf,
        "y_dwarf": y_dwarf,
    }


def quality_check(catalog: dict[str, np.ndarray]) -> dict[str, float]:
    x_main = np.log10(catalog["t_main"])
    y_main = catalog["y_main"]
    corr_main = np.corrcoef(x_main, y_main)[0, 1]

    giant_lum_frac = float(np.mean(catalog["y_giant"] > 1.6))
    dwarf_dim_frac = float(np.mean(catalog["y_dwarf"] < 0.2))

    return {
        "main_seq_corr": float(corr_main),
        "giant_luminous_fraction": giant_lum_frac,
        "wd_dim_fraction": dwarf_dim_frac,
    }


def make_figure(catalog: dict[str, np.ndarray], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8.8, 6.2), facecolor="none")
    ax.set_facecolor("none")

    col_main = temperature_to_color(catalog["t_main"])
    ax.scatter(
        catalog["t_main"],
        catalog["y_main"],
        s=8,
        c=col_main,
        alpha=0.62,
        linewidths=0,
        rasterized=False,
    )

    ax.scatter(
        catalog["t_giant"],
        catalog["y_giant"],
        s=14,
        c="#6e0f0f",  # dark red for red giants
        alpha=0.72,
        linewidths=0,
        rasterized=False,
    )

    ax.scatter(
        catalog["t_dwarf"],
        catalog["y_dwarf"],
        s=9,
        c="#9a9a9a",  # grey for white dwarfs
        alpha=0.72,
        linewidths=0,
        rasterized=False,
    )

    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlim(3.2e4, 2.8e3)
    ax.set_ylim(-2.7, 5.8)

    ax.set_xlabel(r"Effective temperature $T_{\mathrm{eff}}$ (K)")
    ax.set_ylabel(r"$\log_{10}(L/L_\odot)$")
    ax.grid(True, which="major", alpha=0.22, linewidth=0.6)

    ax.text(1.35e4, 3.9, "Main sequence", fontsize=10)
    ax.text(4.4e3, 4.7, "Red giants", fontsize=10, color="#6e0f0f")
    ax.text(2.2e4, -1.9, "White dwarfs", fontsize=10, color="#696969")

    fig.tight_layout()

    png_path = out_dir / "hr_diagram_cover.png"
    pdf_path = out_dir / "hr_diagram_cover.pdf"
    svg_path = out_dir / "hr_diagram_cover.svg"

    fig.savefig(png_path, dpi=320, transparent=False)
    fig.savefig(pdf_path, transparent=True)
    fig.savefig(svg_path, transparent=True)
    plt.close(fig)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir / "images"

    catalog = build_hr_catalog(seed=3071)
    checks = quality_check(catalog)
    make_figure(catalog, out_dir)

    print("Generated files:")
    print(f"  - {(out_dir / 'hr_diagram_cover.png').as_posix()}")
    print(f"  - {(out_dir / 'hr_diagram_cover.pdf').as_posix()}")
    print(f"  - {(out_dir / 'hr_diagram_cover.svg').as_posix()}")
    print("\nSanity check against real HR morphology:")
    print(f"  - Main-sequence corr(logT, logL): {checks['main_seq_corr']:.3f} (expect positive)")
    print(f"  - Red-giant luminous fraction    : {checks['giant_luminous_fraction']:.3f} (expect high)")
    print(f"  - White-dwarf dim fraction       : {checks['wd_dim_fraction']:.3f} (expect high)")


if __name__ == "__main__":
    main()
