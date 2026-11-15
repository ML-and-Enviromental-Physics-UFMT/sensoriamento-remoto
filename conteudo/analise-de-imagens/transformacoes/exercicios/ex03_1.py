#!/usr/bin/env python3
"""ex03_1.py — PCA: erro de reconstrução vs fórmula com autovalores (Canty ~3.45)."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_DEFAULT = (
    _HERE.parents[3]
    / "data" / "exemplos"
    / "exemplo_sintetico.tif"
)


def load_raster(path: Path) -> np.ndarray:
    try:
        import rasterio

        with rasterio.open(path) as src:
            return src.read().astype(np.float64)
    except Exception as e_rio:
        rio_err = e_rio
    try:
        from osgeo import gdal
        from osgeo.gdalconst import GA_ReadOnly

        gdal.AllRegister()
        ds = gdal.Open(str(path), GA_ReadOnly)
        if ds is None:
            raise RuntimeError(f"GDAL não abriu: {path}")
        bands, rows, cols = ds.RasterCount, ds.RasterYSize, ds.RasterXSize
        data = np.empty((bands, rows, cols), dtype=np.float64)
        for b in range(bands):
            data[b] = ds.GetRasterBand(b + 1).ReadAsArray().astype(np.float64)
        ds = None
        return data
    except Exception as e_gdal:
        raise SystemExit(
            "Instale rasterio ou osgeo.gdal.\n"
            f"rasterio: {rio_err}\ngdal: {e_gdal}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compara covariância do erro de reconstrução PCA com a fórmula teórica"
    )
    parser.add_argument(
        "infile",
        nargs="?",
        type=Path,
        default=_DEFAULT,
        help="GeoTIFF multibanda (default: Exemplo sintético Cap. 1)",
    )
    parser.add_argument(
        "-r",
        "--retain",
        type=int,
        default=2,
        help="Número de PCs retidas na reconstrução (default: 2)",
    )
    args = parser.parse_args()
    if not args.infile.exists():
        raise SystemExit(f"Arquivo não encontrado: {args.infile}")

    image = load_raster(args.infile)
    bands, rows, cols = image.shape
    m = rows * cols
    G = image.reshape(bands, m).copy()
    G -= G.mean(axis=1, keepdims=True)

    S = (G @ G.T) / (m - 1)
    lamda, W = np.linalg.eigh(S)
    idx = np.argsort(lamda)[::-1]
    lamda = lamda[idx]
    W = W[:, idx]

    r = max(0, min(args.retain, bands))
    Y = W.T @ G
    G_r = W[:, :r] @ Y[:r, :]

    err_emp = ((G - G_r) @ (G - G_r).T) / (m - 1)
    err_th = W[:, r:] @ np.diag(lamda[r:]) @ W[:, r:].T

    np.set_printoptions(precision=4, suppress=True)
    print(f"Arquivo: {args.infile}")
    print(f"PCs retidas r={r}")
    print("Autovalores:", lamda)
    print("\nCovariância do erro (empírica) [:3,:3]:")
    print(err_emp[:3, :3])
    print("\nCovariância do erro (eq. 3.45) [:3,:3]:")
    print(err_th[:3, :3])
    print("\n||empírica - teórica||_F =", np.linalg.norm(err_emp - err_th))


if __name__ == "__main__":
    main()
