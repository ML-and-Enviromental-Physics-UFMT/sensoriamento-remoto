#!/usr/bin/env python3
"""Generate basic Chapter 01 preview PNGs from the synthetic example raster.

Uses the Agg backend (no display). Skips files that already exist.

  PYTHONPATH=. python scripts/generate_outputs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Repo root on path when run as a script
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from study_utils import example_path, ensure_dir, read_raster


def _stretch01(band: np.ndarray, p_low: float = 2.0, p_high: float = 98.0) -> np.ndarray:
    lo, hi = np.percentile(band.astype(float), (p_low, p_high))
    if hi <= lo:
        lo, hi = float(band.min()), float(band.max())
    if hi <= lo:
        return np.zeros_like(band, dtype=float)
    out = (band.astype(float) - lo) / (hi - lo)
    return np.clip(out, 0.0, 1.0)


def main() -> None:
    path = example_path()
    arr, _, _ = read_raster(path)

    if arr.ndim == 2:
        bands = arr[np.newaxis, ...]
    else:
        bands = arr

    n_bands, rows, cols = bands.shape
    out_dir = ensure_dir(_ROOT / "conteudo/fundamentos/figuras")

    # Per-band stretch previews (only create if missing)
    for i in range(n_bands):
        out = out_dir / f"sintetico_band_{i + 1}_stretch.png"
        if out.exists():
            print(f"skip (exists): {out.name}")
            continue
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(_stretch01(bands[i]), cmap="gray")
        ax.set_title(f"Canal sintético {i + 1}")
        ax.axis("off")
        fig.tight_layout()
        fig.savefig(out, dpi=120, bbox_inches="tight")
        plt.close(fig)
        print(f"wrote {out}")

    # Simple RGB / false-color if enough bands
    if n_bands >= 3:
        rgb_path = out_dir / "sintetico_rgb_falsecolor.png"
        if rgb_path.exists():
            print(f"skip (exists): {rgb_path.name}")
        else:
            # bands 3,2,1 as R,G,B (1-based) — common VNIR false-color style
            r = _stretch01(bands[2] if n_bands > 2 else bands[0])
            g = _stretch01(bands[1] if n_bands > 1 else bands[0])
            b = _stretch01(bands[0])
            rgb = np.dstack([r, g, b])
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.imshow(rgb)
            ax.set_title("Composição sintética (B3,B2,B1)")
            ax.axis("off")
            fig.tight_layout()
            fig.savefig(rgb_path, dpi=120, bbox_inches="tight")
            plt.close(fig)
            print(f"wrote {rgb_path}")
    else:
        print("fewer than 3 bands — skipping RGB composite")


if __name__ == "__main__":
    main()
