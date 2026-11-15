#!/usr/bin/env python3
"""ex05_4 — Contrast stretch vs equalização de histograma.

Salva comparação em figuras/realce_stretch_histeq.png
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


def contrast_stretch(img: np.ndarray, p_low: float = 2, p_high: float = 98) -> np.ndarray:
    lo, hi = np.percentile(img, (p_low, p_high))
    if hi <= lo:
        return np.zeros_like(img, dtype=np.float64)
    return np.clip((img - lo) / (hi - lo), 0, 1)


def histogram_equalization(img: np.ndarray) -> np.ndarray:
    """Equalização em 256 bins sobre a faixa [min, max] da banda."""
    flat = img.ravel()
    vmin, vmax = float(np.min(flat)), float(np.max(flat))
    if vmax <= vmin:
        return np.zeros_like(img, dtype=np.float64)

    # quantiza para 0..255
    scaled = np.clip((flat - vmin) / (vmax - vmin) * 255.0, 0, 255).astype(np.uint8)
    hist, _ = np.histogram(scaled, bins=256, range=(0, 256))
    cdf = hist.cumsum().astype(np.float64)
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_min = cdf_masked.min()
    cdf_max = cdf_masked.max()
    if cdf_max == cdf_min:
        return np.zeros_like(img, dtype=np.float64)
    lut = ((cdf_masked - cdf_min) / (cdf_max - cdf_min)).filled(0)
    eq = lut[scaled].reshape(img.shape)
    return eq


def main():
    repo = Path(__file__).resolve().parents[3]
    default_tif = (
        repo
        / "data" / "exemplos"
        / "exemplo_sintetico.tif"
    )
    out_dir = Path(__file__).resolve().parents[1] / "figuras"

    parser = argparse.ArgumentParser(description="Stretch vs equalização de histograma")
    parser.add_argument(
        "infile",
        nargs="?",
        default=str(default_tif),
        help="GeoTIFF de entrada (default: Exemplo sintético Cap. 1)",
    )
    parser.add_argument("-b", "--band", type=int, default=1, help="Banda (1-based)")
    parser.add_argument("--p-low", type=float, default=2.0, help="Percentil inferior do stretch")
    parser.add_argument("--p-high", type=float, default=98.0, help="Percentil superior do stretch")
    parser.add_argument(
        "-o",
        "--output",
        default=str(out_dir / "realce_stretch_histeq.png"),
        help="PNG de saída",
    )
    args = parser.parse_args()

    band = read_band(args.infile, args.band)
    stretched = contrast_stretch(band, args.p_low, args.p_high)
    equalized = histogram_equalization(band)

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))

    axes[0, 0].imshow(contrast_stretch(band, 0, 100), cmap="gray")
    axes[0, 0].set_title("Original (min–max)")
    axes[0, 1].imshow(stretched, cmap="gray")
    axes[0, 1].set_title(f"Stretch {args.p_low:g}–{args.p_high:g}%")
    axes[0, 2].imshow(equalized, cmap="gray")
    axes[0, 2].set_title("Equalização de histograma")

    for ax in axes[0]:
        ax.axis("off")

    axes[1, 0].hist(band.ravel(), bins=64, color="gray", density=True)
    axes[1, 0].set_title("Hist. original")
    axes[1, 1].hist(stretched.ravel(), bins=64, color="steelblue", density=True)
    axes[1, 1].set_title("Hist. stretch")
    axes[1, 2].hist(equalized.ravel(), bins=64, color="darkorange", density=True)
    axes[1, 2].set_title("Hist. equalizado")
    for ax in axes[1]:
        ax.set_xlabel("valor")
        ax.set_ylabel("densidade")

    fig.suptitle(f"Realce radiométrico — banda {args.band}", fontsize=12)
    fig.tight_layout()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo: {out}")


if __name__ == "__main__":
    main()
