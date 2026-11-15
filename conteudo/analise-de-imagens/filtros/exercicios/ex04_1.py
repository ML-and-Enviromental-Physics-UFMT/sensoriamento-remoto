#!/usr/bin/env python3
"""ex04_1 — Filtros de suavização (média, Gaussiano, mediana) em uma banda Exemplo sintético.

Salva comparação lado a lado em figuras/filtros_suavizacao.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- leitura de GeoTIFF (rasterio → GDAL → tifffile) -------------------------

def read_band(path: str | Path, band: int = 1) -> np.ndarray:
    path = Path(path)
    try:
        import rasterio

        with rasterio.open(path) as ds:
            return ds.read(band).astype(np.float64)
    except Exception:
        pass
    try:
        from osgeo import gdal
        from osgeo.gdalconst import GA_ReadOnly

        gdal.AllRegister()
        ds = gdal.Open(str(path), GA_ReadOnly)
        if ds is None:
            raise RuntimeError(f"GDAL não abriu: {path}")
        arr = ds.GetRasterBand(band).ReadAsArray().astype(np.float64)
        ds = None
        return arr
    except Exception:
        pass
    try:
        import tifffile

        data = tifffile.imread(str(path))
        if data.ndim == 2:
            return data.astype(np.float64)
        # (bands, rows, cols) ou (rows, cols, bands)
        if data.shape[0] < data.shape[-1]:
            return data[band - 1].astype(np.float64)
        return data[:, :, band - 1].astype(np.float64)
    except Exception as exc:
        raise ImportError(
            "Instale rasterio, GDAL (osgeo) ou tifffile para ler o GeoTIFF."
        ) from exc


def percentile_stretch(img: np.ndarray, p_low: float = 2, p_high: float = 98) -> np.ndarray:
    lo, hi = np.percentile(img, (p_low, p_high))
    if hi <= lo:
        return np.zeros_like(img, dtype=np.float64)
    out = (img - lo) / (hi - lo)
    return np.clip(out, 0, 1)


def apply_filters(band: np.ndarray, size: int = 5, sigma: float = 1.5):
    try:
        from scipy import ndimage
    except ImportError as exc:
        raise ImportError("scipy é necessário (scipy.ndimage).") from exc

    mean = ndimage.uniform_filter(band, size=size)
    gauss = ndimage.gaussian_filter(band, sigma=sigma)
    median = ndimage.median_filter(band, size=size)
    return mean, gauss, median


def main():
    repo = Path(__file__).resolve().parents[4]
    default_tif = (
        repo
        / "data" / "exemplos"
        / "exemplo_sintetico.tif"
    )
    out_dir = Path(__file__).resolve().parents[1] / "figuras"

    parser = argparse.ArgumentParser(description="Filtros média / Gaussiano / mediana")
    parser.add_argument(
        "infile",
        nargs="?",
        default=str(default_tif),
        help="GeoTIFF de entrada (default: Exemplo sintético Cap. 1)",
    )
    parser.add_argument("-b", "--band", type=int, default=1, help="Índice da banda (1-based)")
    parser.add_argument("--size", type=int, default=5, help="Tamanho da janela (média/mediana)")
    parser.add_argument("--sigma", type=float, default=1.5, help="Sigma do Gaussiano")
    parser.add_argument(
        "-o",
        "--output",
        default=str(out_dir / "filtros_suavizacao.png"),
        help="PNG de saída",
    )
    args = parser.parse_args()

    band = read_band(args.infile, args.band)
    mean, gauss, median = apply_filters(band, size=args.size, sigma=args.sigma)

    panels = [
        ("Original", band),
        (f"Média {args.size}×{args.size}", mean),
        (f"Gaussiano σ={args.sigma}", gauss),
        (f"Mediana {args.size}×{args.size}", median),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    for ax, (title, img) in zip(axes, panels):
        ax.imshow(percentile_stretch(img), cmap="gray")
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    fig.suptitle(f"Filtros de suavização — banda {args.band}", fontsize=12)
    fig.tight_layout()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo: {out}")


if __name__ == "__main__":
    main()
