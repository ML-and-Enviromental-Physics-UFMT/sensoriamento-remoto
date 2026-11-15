#!/usr/bin/env python3
"""ex03_2.py — estimativa da covariância de ruído via diferenças espaciais (MNF)."""
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


def noisecovar(image: np.ndarray) -> np.ndarray:
    """Σ_N ≈ Cov(pixel - vizinho_vertical) / 2 (Canty / ex3_2)."""
    bands, rows, cols = image.shape
    D = np.empty((bands, rows * cols), dtype=np.float64)
    for b in range(bands):
        tmp = image[b]
        D[b, :] = (tmp - np.roll(tmp, 1, axis=0)).ravel()
    return (D @ D.T) / (2 * (rows * cols - 1))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estima matriz de covariância de ruído (diferenças espaciais)"
    )
    parser.add_argument(
        "infile",
        nargs="?",
        type=Path,
        default=_DEFAULT,
        help="GeoTIFF multibanda (default: Exemplo sintético Cap. 1)",
    )
    args = parser.parse_args()
    if not args.infile.exists():
        raise SystemExit(f"Arquivo não encontrado: {args.infile}")

    image = load_raster(args.infile)
    S_N = noisecovar(image)
    np.set_printoptions(precision=2, suppress=True, linewidth=120)
    print(f"Noise covariance, file {args.infile}")
    print(S_N)


if __name__ == "__main__":
    main()
