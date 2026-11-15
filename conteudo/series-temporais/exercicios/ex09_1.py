#!/usr/bin/env python3
# Name:  ex9_1.py
"""PCA iterada + EM no 2º PC (exercício do livro, Cap. 9).

Requer duas imagens, GDAL e a instalação externa descrita em legado/canty/README.md.

Uso:
  python ex09_1.py imagem_t1.tif imagem_t2.tif

Se não houver segundo arquivo real, use ex09_2.py (simulação com uma imagem).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def main():
    if len(sys.argv) < 3:
        print("Uso: python ex09_1.py <imagem_t1> <imagem_t2>")
        print("Sem par bitemporal? Rode exercicios/ex09_2.py")
        print(f"Repo root no path: {REPO}")
        sys.exit(1)

    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    canty_src = Path(os.environ.get("CANTY_SRC", REPO / "referencias/local/CRC4Docker/src"))
    if not (canty_src / "auxil/auxil1.py").is_file():
        raise SystemExit("Instale o software externo conforme legado/canty/README.md e configure CANTY_SRC.")
    sys.path.insert(0, str(canty_src))
    scripts = canty_src / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from osgeo import gdal
    from osgeo.gdalconst import GA_ReadOnly

    import auxil.auxil1 as auxil
    import em

    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    inDataset = gdal.Open(infile1, GA_ReadOnly)
    cols = inDataset.RasterXSize
    rows = inDataset.RasterYSize
    band = inDataset.GetRasterBand(min(4, inDataset.RasterCount))
    G1 = band.ReadAsArray(0, 0, cols, rows).flatten()
    inDataset = gdal.Open(infile2, GA_ReadOnly)
    band = inDataset.GetRasterBand(min(4, inDataset.RasterCount))
    G2 = band.ReadAsArray(0, 0, cols, rows).flatten()

    G = np.zeros((rows * cols, 2))
    G[:, 0] = G1 - np.mean(G1)
    G[:, 1] = G2 - np.mean(G2)

    cpm = auxil.Cpm(2)
    cpm.update(G)
    eivs, w = np.linalg.eigh(cpm.covariance())
    eivs = eivs[::-1]
    w = w[:, ::-1]
    pcs = G @ w
    plt.plot([-1, 1], [-np.abs(w[0, 1] / w[0, 0]), np.abs(w[0, 1] / w[0, 0])])

    itr = 0
    U = None
    while itr < 5:
        sigma = np.sqrt(eivs[1])
        U = np.random.rand(2, rows * cols)
        unfrozen = np.where(np.abs(pcs[:, 1]) >= sigma)[0]
        frozen = np.where(np.abs(pcs[:, 1]) < sigma)[0]
        U[0, frozen] = 1.0
        U[1, frozen] = 0.0
        for j in range(2):
            U[j, :] = U[j, :] / np.sum(U, 0)
        U = em.em(G, U, 0, 0, rows, cols, unfrozen=unfrozen)[0]
        cpm.update(G, U[0, :])
        cov = cpm.covariance()
        eivs, w = np.linalg.eigh(cov)
        eivs = eivs[::-1]
        w = w[:, ::-1]
        pcs = G @ w
        plt.plot(
            [-1, 1],
            [-np.abs(w[0, 1] / w[0, 0]), np.abs(w[0, 1] / w[0, 0])],
            dashes=[4, 4],
        )
        itr += 1

    out_dir = Path(__file__).resolve().parents[1] / "figuras"
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.title("Eixos PCA / iPCA")
    plt.savefig(out_dir / "ex09_1_pca_axes.png", dpi=150, bbox_inches="tight")
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(np.reshape(U[1, :], (rows, cols)), cmap="gray")
    ax.set_title("Componente de mudança (EM)")
    ax.axis("off")
    fig.savefig(out_dir / "ex09_1_change_component.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Figuras em {out_dir}")


if __name__ == "__main__":
    main()
