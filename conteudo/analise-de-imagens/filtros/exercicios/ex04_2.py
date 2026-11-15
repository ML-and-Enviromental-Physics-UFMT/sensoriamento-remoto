#!/usr/bin/env python3
"""ex04_2 — Detecção de bordas (Sobel e Laplaciano) em uma banda Exemplo sintético.

Salva comparação em figuras/bordas_sobel_laplacian.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


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
    return np.clip((img - lo) / (hi - lo), 0, 1)


def edges_sobel_laplacian(band: np.ndarray):
    """Retorna (magnitude Sobel, |Laplaciano|). Prefere scipy; fallback cv2."""
    try:
        from scipy import ndimage

        sx = ndimage.sobel(band, axis=1)
        sy = ndimage.sobel(band, axis=0)
        sobel_mag = np.hypot(sx, sy)
        lap = np.abs(ndimage.laplace(band))
        return sobel_mag, lap
    except ImportError:
        pass

    try:
        import cv2 as cv
    except ImportError as exc:
        raise ImportError("Instale scipy ou opencv-python (cv2).") from exc

    u8 = percentile_stretch(band)
    u8 = (u8 * 255).astype(np.uint8)
    sx = cv.Sobel(u8, cv.CV_64F, 1, 0, ksize=3)
    sy = cv.Sobel(u8, cv.CV_64F, 0, 1, ksize=3)
    sobel_mag = np.hypot(sx, sy)
    lap = np.abs(cv.Laplacian(u8, cv.CV_64F, ksize=3))
    return sobel_mag, lap


def main():
    repo = Path(__file__).resolve().parents[4]
    default_tif = (
        repo
        / "data" / "exemplos"
        / "exemplo_sintetico.tif"
    )
    out_dir = Path(__file__).resolve().parents[1] / "figuras"

    parser = argparse.ArgumentParser(description="Bordas Sobel / Laplaciano")
    parser.add_argument(
        "infile",
        nargs="?",
        default=str(default_tif),
        help="GeoTIFF de entrada (default: Exemplo sintético Cap. 1)",
    )
    parser.add_argument("-b", "--band", type=int, default=1, help="Índice da banda (1-based)")
    parser.add_argument(
        "-o",
        "--output",
        default=str(out_dir / "bordas_sobel_laplacian.png"),
        help="PNG de saída",
    )
    args = parser.parse_args()

    band = read_band(args.infile, args.band)
    sobel_mag, lap = edges_sobel_laplacian(band)

    panels = [
        ("Original", percentile_stretch(band)),
        ("Sobel |G|", percentile_stretch(sobel_mag)),
        ("|Laplaciano|", percentile_stretch(lap)),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (title, img) in zip(axes, panels):
        ax.imshow(img, cmap="gray")
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    fig.suptitle(f"Detecção de bordas — banda {args.band}", fontsize=12)
    fig.tight_layout()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo: {out}")


if __name__ == "__main__":
    main()
