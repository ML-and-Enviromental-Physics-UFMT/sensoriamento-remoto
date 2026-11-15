#!/usr/bin/env python3
"""ex02_1.py — média/std por banda e histograma (Canty Cap. 2)."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Default: exemplo sintético compartilhado (ou cópia local em ../data/)
_HERE = Path(__file__).resolve().parent
_DEFAULT_ASTER = (
    _HERE.parent / "data" / "exemplo_sintetico.tif"
)
_FALLBACK_ASTER = (
    _HERE.parents[3]
    / "data" / "exemplos"
    / "exemplo_sintetico.tif"
)


def load_raster(path: Path) -> np.ndarray:
    """Array (bands, rows, cols). Tenta rasterio, depois GDAL."""
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
            "Instale rasterio ou osgeo.gdal para ler o GeoTIFF.\n"
            f"rasterio: {rio_err}\ngdal: {e_gdal}"
        )


def default_infile() -> Path:
    if _DEFAULT_ASTER.exists():
        return _DEFAULT_ASTER
    if _FALLBACK_ASTER.exists():
        return _FALLBACK_ASTER
    return _DEFAULT_ASTER


def main() -> None:
    parser = argparse.ArgumentParser(description="Estatísticas e histograma por banda")
    parser.add_argument(
        "infile",
        nargs="?",
        type=Path,
        default=None,
        help="GeoTIFF multibanda (default: Exemplo sintético Cap. 1/2)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=_HERE.parent / "figuras" / "histogramas_bandas.png",
        help="PNG de saída",
    )
    parser.add_argument("--bins", type=int, default=64)
    args = parser.parse_args()
    infile = args.infile or default_infile()
    if not infile.exists():
        raise SystemExit(f"Arquivo não encontrado: {infile}")

    image = load_raster(infile)
    nbands = image.shape[0]
    args.output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Arquivo: {infile}")
    print(f"Shape: {image.shape}")
    print(f"{'banda':>6} {'média':>14} {'std':>14}")
    for b in range(nbands):
        band = image[b].ravel()
        print(f"{b+1:6d} {band.mean():14.6f} {band.std(ddof=1):14.6f}")

    ncols = min(3, nbands)
    nrows = int(np.ceil(nbands / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for b in range(nbands):
        axes[b].hist(image[b].ravel(), bins=args.bins, color="steelblue", edgecolor="none")
        axes[b].set_title(f"Banda {b+1}")
        axes[b].set_xlabel("DN")
        axes[b].set_ylabel("contagem")
    for j in range(nbands, len(axes)):
        axes[j].set_axis_off()
    fig.suptitle("Histogramas por banda", y=1.01)
    fig.tight_layout()
    fig.savefig(args.output, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Histograma salvo: {args.output}")


if __name__ == "__main__":
    main()
