#!/usr/bin/env python3
"""ex08_2 — GMM (sklearn GaussianMixture) em Exemplo sintético.

Referência do livro: legado/canty/auxil/scripts/em.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

REPO = Path(__file__).resolve().parents[4]
ASTER = REPO / "data" / "exemplos" / "exemplo_sintetico.tif"
OUT = Path(__file__).resolve().parents[1] / "figuras"
OUT.mkdir(parents=True, exist_ok=True)

K = 5
MAX_FIT = 20_000


def main():
    import rasterio

    with rasterio.open(ASTER) as ds:
        img = ds.read().astype(np.float64)
    bands, rows, cols = img.shape
    X = img.reshape(bands, -1).T
    # usa primeiras 4 bandas para acelerar GMM
    X4 = X[:, :4]
    scaler = StandardScaler().fit(X4)
    Xs = scaler.transform(X4)

    rng = np.random.default_rng(1)
    fit_idx = rng.choice(len(Xs), size=min(MAX_FIT, len(Xs)), replace=False)
    gmm = GaussianMixture(
        n_components=K, covariance_type="full", random_state=0, max_iter=120
    )
    gmm.fit(Xs[fit_idx])
    labels = gmm.predict(Xs).reshape(rows, cols)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(labels, cmap="tab10", vmin=0, vmax=9)
    ax.set_title(f"GMM K={K} (4 bandas)")
    ax.axis("off")
    fig.tight_layout()
    out = OUT / "ex08_2_gmm_map.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"BIC (subamostra): {gmm.bic(Xs[fit_idx]):.1f}")
    print(f"Salvo: {out}")
    print("Ver também: legado/canty/auxil/scripts/em.py")


if __name__ == "__main__":
    main()
