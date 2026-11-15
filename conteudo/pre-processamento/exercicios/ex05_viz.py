#!/usr/bin/env python3
"""ex05_viz — Visualizações versionáveis dos exercícios 5.1 / 5.2.

Os scripts originais do livro gravam GeoTIFF ao lado do input (ex05_1) ou
abrem janela interativa (ex05_2). Este wrapper só escreve PNGs em figuras/,
sem duplicar o TIF de ~34 MB.
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


def to_uint8(band: np.ndarray) -> np.ndarray:
    lo, hi = np.percentile(band, (2, 98))
    if hi <= lo:
        return np.zeros(band.shape, dtype=np.uint8)
    scaled = np.clip((band - lo) / (hi - lo), 0, 1)
    return (scaled * 255).astype(np.uint8)


def stretch_display(arr: np.ndarray) -> np.ndarray:
    lo, hi = np.percentile(arr, (2, 98))
    if hi <= lo:
        return np.zeros_like(arr, dtype=np.float64)
    return np.clip((arr - lo) / (hi - lo), 0, 1)


def main():
    repo = Path(__file__).resolve().parents[3]
    default_tif = (
        repo
        / "data" / "exemplos"
        / "exemplo_sintetico.tif"
    )
    out_dir = Path(__file__).resolve().parents[1] / "figuras"

    parser = argparse.ArgumentParser(
        description="PNGs de cantos/Canny/Hu em figuras/ (wrapper ex05_1/ex05_2)"
    )
    parser.add_argument("infile", nargs="?", default=str(default_tif))
    parser.add_argument("-b", "--band", type=int, default=1)
    parser.add_argument(
        "--outdir",
        default=str(out_dir),
        help="Diretório de PNGs (default: Chapter_05/.../figuras)",
    )
    args = parser.parse_args()

    try:
        import cv2 as cv
    except ImportError as exc:
        raise ImportError("opencv-python (cv2) é necessário para ex05_viz.") from exc

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    band = read_band(args.infile, args.band)
    u8 = to_uint8(band)

    corners = cv.cornerMinEigenVal(u8, 7)
    canny = cv.Canny(u8, 50, 150)

    # --- painel cantos / Canny ---
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(stretch_display(band), cmap="gray")
    axes[0].set_title("Original")
    axes[1].imshow(stretch_display(corners), cmap="inferno")
    axes[1].set_title("Cantos (min eigenvalue)")
    axes[2].imshow(canny, cmap="gray")
    axes[2].set_title("Canny")
    for ax in axes:
        ax.axis("off")
    fig.suptitle(f"Feições locais — banda {args.band}")
    fig.tight_layout()
    p1 = out_dir / "ex05_corner_canny.png"
    fig.savefig(p1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo: {p1}")

    # --- momentos de Hu (como ex05_2, headless) ---
    edges = cv.Canny(u8, 20, 80)
    contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if hierarchy is None or len(contours) == 0:
        print("nenhum contorno; PNG de Hu omitido")
        return

    num = len(hierarchy[0])
    hus = np.zeros((num, 7), dtype=np.float32)
    arr = np.zeros(u8.shape, dtype=np.uint8)
    for i in range(num):
        arr[:] = 0
        cv.drawContours(arr, contours, i, 1)
        m = cv.moments(arr)
        hus[i, :] = cv.HuMoments(m).ravel()

    fig, ax = plt.subplots(figsize=(7, 4))
    for i in range(3):
        idx = hus[:, i] > 0
        if not np.any(idx):
            continue
        hist, edges_h = np.histogram(np.log(hus[idx, i]), 50)
        ax.plot(edges_h[1:], hist, label=f"Hu moment {i + 1}")
    ax.legend()
    ax.set_xlabel(r"log($\mu$)")
    ax.set_ylabel("contagem")
    ax.set_title("Histograma dos primeiros momentos de Hu")
    fig.tight_layout()
    p2 = out_dir / "ex05_hu_moments.png"
    fig.savefig(p2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"salvo: {p2}")


if __name__ == "__main__":
    main()
