#!/usr/bin/env python3
"""ex02_2.py — covariância e correlação espectral + heatmap (Canty Cap. 2)."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = Path(__file__).resolve().parent
_DEFAULT_ASTER = _HERE.parent / "data" / "exemplo_sintetico.tif"
_FALLBACK_ASTER = (
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
            "Instale rasterio ou osgeo.gdal para ler o GeoTIFF.\n"
            f"rasterio: {rio_err}\ngdal: {e_gdal}"
        )


def default_infile() -> Path:
    if _DEFAULT_ASTER.exists():
        return _DEFAULT_ASTER
    if _FALLBACK_ASTER.exists():
        return _FALLBACK_ASTER
    return _DEFAULT_ASTER


def cov_corr(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """image: (bands, rows, cols) → S e R (N×N)."""
    nbands = image.shape[0]
    G = image.reshape(nbands, -1)  # N × m
    S = np.cov(G, ddof=1)
    std = np.sqrt(np.diag(S))
    # evita divisão por zero
    denom = np.outer(std, std)
    R = np.divide(S, denom, out=np.zeros_like(S), where=denom > 0)
    return S, R


def heatmap(mat: np.ndarray, title: str, path: Path, cmap: str = "coolwarm") -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(mat, cmap=cmap)
    ax.set_title(title)
    ax.set_xlabel("banda")
    ax.set_ylabel("banda")
    n = mat.shape[0]
    ticks = np.arange(n)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(ticks + 1)
    ax.set_yticklabels(ticks + 1)
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Covariância e correlação espectral")
    parser.add_argument("infile", nargs="?", type=Path, default=None)
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=_HERE.parent / "figuras",
    )
    args = parser.parse_args()
    infile = args.infile or default_infile()
    if not infile.exists():
        raise SystemExit(f"Arquivo não encontrado: {infile}")

    image = load_raster(infile)
    S, R = cov_corr(image)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    np.set_printoptions(precision=3, suppress=True, linewidth=120)
    print(f"Arquivo: {infile}")
    print("Covariância S:")
    print(S)
    print("\nCorrelação R:")
    print(R)

    heatmap(S, "Matriz de covariância", out / "covariancia_heatmap.png", cmap="viridis")
    heatmap(R, "Matriz de correlação", out / "correlacao_heatmap.png", cmap="coolwarm")
    print(f"Heatmaps em: {out}")


if __name__ == "__main__":
    main()
