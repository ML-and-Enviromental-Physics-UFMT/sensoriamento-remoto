#!/usr/bin/env python3
"""ex03_3.py — grava as 3 primeiras PCs (PNG; GeoTIFF se GDAL/rasterio disponível)."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = Path(__file__).resolve().parent
_DEFAULT = (
    _HERE.parents[3]
    / "data" / "exemplos"
    / "exemplo_sintetico.tif"
)
_OUT = _HERE.parent / "figuras"


def load_raster(path: Path):
    """Retorna (array bands×rows×cols, meta dict para escrita opcional)."""
    try:
        import rasterio

        with rasterio.open(path) as src:
            data = src.read().astype(np.float64)
            meta = {
                "backend": "rasterio",
                "profile": src.profile.copy(),
                "transform": src.transform,
                "crs": src.crs,
            }
            return data, meta
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
        meta = {
            "backend": "gdal",
            "projection": ds.GetProjection(),
            "geotransform": ds.GetGeoTransform(),
        }
        ds = None
        return data, meta
    except Exception as e_gdal:
        raise SystemExit(
            "Instale rasterio ou osgeo.gdal.\n"
            f"rasterio: {rio_err}\ngdal: {e_gdal}"
        )


def pca_components(image: np.ndarray, n_comp: int = 3) -> tuple[np.ndarray, np.ndarray]:
    bands, rows, cols = image.shape
    G = image.reshape(bands, -1).copy()
    mean = G.mean(axis=1, keepdims=True)
    G -= mean
    S = np.cov(G, ddof=1)
    lamda, W = np.linalg.eigh(S)
    idx = np.argsort(lamda)[::-1]
    lamda = lamda[idx]
    W = W[:, idx]
    n_comp = min(n_comp, bands)
    pcs = (W[:, :n_comp].T @ G).reshape(n_comp, rows, cols)
    return pcs, lamda


def stretch01(band: np.ndarray) -> np.ndarray:
    mn, mx = band.min(), band.max()
    if mx <= mn:
        return np.zeros_like(band)
    return (band - mn) / (mx - mn)


def save_pngs(pcs: np.ndarray, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, pc in enumerate(pcs):
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.imshow(stretch01(pc), cmap="gray")
        ax.set_title(f"PC{i+1}")
        ax.set_axis_off()
        path = out_dir / f"pc{i+1}.png"
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        print(f"Salvo {path}")


def save_geotiff(pcs: np.ndarray, meta: dict, path: Path) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    n, rows, cols = pcs.shape
    if meta.get("backend") == "rasterio":
        try:
            import rasterio

            profile = meta["profile"]
            profile.update(
                count=n,
                dtype="float32",
                compress="lzw",
            )
            with rasterio.open(path, "w", **profile) as dst:
                dst.write(pcs.astype(np.float32))
            print(f"GeoTIFF salvo: {path}")
            return True
        except Exception as e:
            print(f"Aviso: não gravou GeoTIFF com rasterio ({e})")
            return False

    if meta.get("backend") == "gdal":
        try:
            from osgeo import gdal
            from osgeo.gdalconst import GDT_Float32

            driver = gdal.GetDriverByName("GTiff")
            ds = driver.Create(str(path), cols, rows, n, GDT_Float32)
            if meta.get("projection"):
                ds.SetProjection(meta["projection"])
            if meta.get("geotransform"):
                ds.SetGeoTransform(meta["geotransform"])
            for k in range(n):
                ds.GetRasterBand(k + 1).WriteArray(pcs[k].astype(np.float32))
            ds = None
            print(f"GeoTIFF salvo: {path}")
            return True
        except Exception as e:
            print(f"Aviso: não gravou GeoTIFF com GDAL ({e})")
            return False
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Exporta PC1–PC3 como PNG e opcionalmente GeoTIFF")
    parser.add_argument("infile", nargs="?", type=Path, default=_DEFAULT)
    parser.add_argument("-o", "--output-dir", type=Path, default=_OUT)
    parser.add_argument("--n-comp", type=int, default=3)
    parser.add_argument(
        "--geotiff",
        type=Path,
        default=None,
        help="Caminho opcional do GeoTIFF multibanda (default: figuras/pcs_top3.tif)",
    )
    args = parser.parse_args()
    if not args.infile.exists():
        raise SystemExit(f"Arquivo não encontrado: {args.infile}")

    image, meta = load_raster(args.infile)
    pcs, lamda = pca_components(image, args.n_comp)
    print(f"Arquivo: {args.infile}")
    print("Autovalores (todos):", np.round(lamda, 4))
    save_pngs(pcs, args.output_dir)
    gt_path = args.geotiff or (args.output_dir / "pcs_top3.tif")
    save_geotiff(pcs, meta, gt_path)


if __name__ == "__main__":
    main()
