#!/usr/bin/env python3
"""ex08_1 — k-means em vetores espectrais Exemplo sintético (subamostra + predição completa).

Referência do livro: legado/canty/auxil/scripts/kmeans.py, ekmeans.py, som.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

REPO = Path(__file__).resolve().parents[4]
ASTER = REPO / "data" / "exemplos" / "exemplo_sintetico.tif"
OUT = Path(__file__).resolve().parents[1] / "figuras"
OUT.mkdir(parents=True, exist_ok=True)

K = 5
MAX_FIT = 30_000


def main():
    import rasterio

    with rasterio.open(ASTER) as ds:
        img = ds.read().astype(np.float64)
    bands, rows, cols = img.shape
    X = img.reshape(bands, -1).T
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)

    rng = np.random.default_rng(0)
    fit_idx = rng.choice(len(Xs), size=min(MAX_FIT, len(Xs)), replace=False)
    km = KMeans(n_clusters=K, n_init=10, random_state=0)
    km.fit(Xs[fit_idx])
    labels = km.predict(Xs).reshape(rows, cols)

    rgb = np.stack([img[2], img[1], img[0]], axis=-1)
    rgb = (rgb - np.percentile(rgb, 2)) / (np.percentile(rgb, 98) - np.percentile(rgb, 2) + 1e-6)
    rgb = np.clip(rgb, 0, 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(rgb)
    axes[0].set_title("Exemplo sintético RGB (b3,b2,b1)")
    axes[1].imshow(labels, cmap="tab10", vmin=0, vmax=9)
    axes[1].set_title(f"k-means K={K}")
    for ax in axes:
        ax.axis("off")
    fig.tight_layout()
    out = OUT / "ex08_1_kmeans_map.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Inércia (subamostra): {km.inertia_:.1f}")
    print(f"Salvo: {out}")
    print("Ver também: legado/canty/auxil/scripts/kmeans.py, ekmeans.py, som.py")


if __name__ == "__main__":
    main()
