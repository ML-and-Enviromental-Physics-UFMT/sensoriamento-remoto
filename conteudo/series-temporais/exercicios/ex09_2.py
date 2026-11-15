#!/usr/bin/env python3
"""ex09_2 — detecção de mudança com UMA imagem.

Simula mudança alterando uma região da banda 4 (ou última banda),
calcula diferença absoluta + mapa limiarizado e salva PNGs em figuras/.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[3]
ASTER = REPO / "data" / "exemplos" / "exemplo_sintetico.tif"
OUT = Path(__file__).resolve().parents[1] / "figuras"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    import rasterio

    with rasterio.open(ASTER) as ds:
        n_bands = ds.count
        band_idx = 4 if n_bands >= 4 else n_bands  # 1-based
        before = ds.read(band_idx).astype(np.float64)

    rows, cols = before.shape
    after = before.copy()
    # retângulo central: reduz reflectância (~desmatamento / sombra)
    r0, r1 = rows // 3, 2 * rows // 3
    c0, c1 = cols // 3, 2 * cols // 3
    after[r0:r1, c0:c1] *= 0.55
    after[r0:r1, c0:c1] += 0.05 * after.std()

    diff = np.abs(after - before)
    thr = np.percentile(diff, 95)
    change = (diff >= thr).astype(np.uint8)

    fig, axes = plt.subplots(2, 2, figsize=(9, 8))
    im0 = axes[0, 0].imshow(before, cmap="gray")
    axes[0, 0].set_title(f"Antes (banda {band_idx})")
    fig.colorbar(im0, ax=axes[0, 0], fraction=0.046)
    im1 = axes[0, 1].imshow(after, cmap="gray")
    axes[0, 1].set_title("Depois (região alterada)")
    fig.colorbar(im1, ax=axes[0, 1], fraction=0.046)
    im2 = axes[1, 0].imshow(diff, cmap="magma")
    axes[1, 0].set_title("|depois − antes|")
    fig.colorbar(im2, ax=axes[1, 0], fraction=0.046)
    axes[1, 1].imshow(change, cmap="gray")
    axes[1, 1].set_title(f"Mudança (limiar p95={thr:.3g})")
    for ax in axes.ravel():
        ax.axis("off")
    fig.tight_layout()
    panel = OUT / "ex09_2_change_panel.png"
    fig.savefig(panel, dpi=150, bbox_inches="tight")
    plt.close(fig)

    for name, arr, cmap in [
        ("ex09_2_before.png", before, "gray"),
        ("ex09_2_after.png", after, "gray"),
        ("ex09_2_diff.png", diff, "magma"),
        ("ex09_2_threshold_map.png", change, "gray"),
    ]:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(arr, cmap=cmap)
        ax.axis("off")
        fig.savefig(OUT / name, dpi=120, bbox_inches="tight")
        plt.close(fig)

    print(f"Limiar: {thr:.6g} | pixels mudança: {change.sum()} ({100*change.mean():.2f}%)")
    print(f"Salvos em {OUT}")
    print("Para o fluxo MAD/iMAD do livro: legado/canty/auxil/scripts/iMad.py e ex09_1.py (2 datas).")


if __name__ == "__main__":
    main()
