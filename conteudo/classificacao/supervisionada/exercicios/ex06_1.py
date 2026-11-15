#!/usr/bin/env python3
"""ex06_1 — classificação supervisionada simples (GaussianNB / QDA).

Usa Exemplo sintético (bandas VNIR) com rótulos sintéticos por limiar NDVI-like,
ou cai em classes gaussianas 2D sintéticas se o raster não estiver disponível.

Referência completa do livro: legado/canty/auxil/scripts/classify.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

REPO = Path(__file__).resolve().parents[4]
ASTER = REPO / "data" / "exemplos" / "exemplo_sintetico.tif"
OUT = Path(__file__).resolve().parents[1] / "figuras"
OUT.mkdir(parents=True, exist_ok=True)


def load_aster_features(path: Path):
    """Retorna (X, rows, cols, ndvi) com X shape (n_pixels, n_bands)."""
    import rasterio

    with rasterio.open(path) as ds:
        img = ds.read().astype(np.float64)  # (bands, rows, cols)
    bands, rows, cols = img.shape
    # ASTER VNIR: b2≈vermelho, b3≈NIR (1-indexados)
    red = img[1]
    nir = img[2]
    ndvi = (nir - red) / (nir + red + 1e-6)
    X = img.reshape(bands, -1).T
    return X, rows, cols, ndvi


def synthetic_gaussians(n_per_class: int = 800, seed: int = 0):
    rng = np.random.default_rng(seed)
    means = [np.array([-1.5, -1.0]), np.array([1.8, 0.5]), np.array([0.0, 2.2])]
    covs = [
        np.array([[0.4, 0.1], [0.1, 0.3]]),
        np.array([[0.35, -0.15], [-0.15, 0.5]]),
        np.array([[0.5, 0.05], [0.05, 0.25]]),
    ]
    Xs, ys = [], []
    for k, (mu, cov) in enumerate(zip(means, covs)):
        Xs.append(rng.multivariate_normal(mu, cov, size=n_per_class))
        ys.append(np.full(n_per_class, k, dtype=int))
    X = np.vstack(Xs)
    y = np.concatenate(ys)
    # grade para mapa 2D
    xx, yy = np.meshgrid(
        np.linspace(X[:, 0].min() - 0.5, X[:, 0].max() + 0.5, 200),
        np.linspace(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5, 200),
    )
    grid = np.c_[xx.ravel(), yy.ravel()]
    return X, y, grid, xx.shape


def labels_from_ndvi(ndvi: np.ndarray) -> np.ndarray:
    """3 classes sintéticas: baixa / média / alta vegetação."""
    y = np.zeros(ndvi.shape, dtype=int)
    y[ndvi >= 0.35] = 2
    y[(ndvi >= 0.1) & (ndvi < 0.35)] = 1
    # 0 = NDVI baixo
    return y


def main():
    use_aster = ASTER.is_file()
    clf_name = "QDA"
    if use_aster:
        print(f"Lendo ASTER: {ASTER}")
        X_all, rows, cols, ndvi = load_aster_features(ASTER)
        y_map = labels_from_ndvi(ndvi)
        y_all = y_map.ravel()
        # subamostra para treino (rótulos sintéticos existem para todos os pixels)
        rng = np.random.default_rng(42)
        idx = rng.choice(len(y_all), size=min(20000, len(y_all)), replace=False)
        X_s, y_s = X_all[idx], y_all[idx]
        X_train, X_test, y_train, y_test = train_test_split(
            X_s, y_s, test_size=0.3, random_state=0, stratify=y_s
        )
        scaler = StandardScaler().fit(X_train)
        X_train_s = scaler.transform(X_train)
        X_test_s = scaler.transform(X_test)
        # QDA precisa de amostras suficientes por classe; fallback NB
        try:
            clf = QuadraticDiscriminantAnalysis().fit(X_train_s, y_train)
        except Exception as exc:  # noqa: BLE001
            print(f"QDA falhou ({exc}); usando GaussianNB")
            clf = GaussianNB().fit(X_train_s, y_train)
            clf_name = "GaussianNB"
        y_pred_test = clf.predict(X_test_s)
        print(f"Acurácia hold-out ({clf_name}): {accuracy_score(y_test, y_pred_test):.3f}")
        cm = confusion_matrix(y_test, y_pred_test)
        print("Matriz de confusão:\n", cm)

        # mapa na imagem completa (pode ser pesado — classifica em blocos)
        X_scaled = scaler.transform(X_all)
        pred = clf.predict(X_scaled).reshape(rows, cols)

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        axes[0].imshow(ndvi, cmap="RdYlGn", vmin=-0.2, vmax=0.8)
        axes[0].set_title("NDVI-like (b3,b2)")
        axes[1].imshow(y_map, cmap="tab10", vmin=0, vmax=9)
        axes[1].set_title("Rótulos sintéticos")
        axes[2].imshow(pred, cmap="tab10", vmin=0, vmax=9)
        axes[2].set_title(f"Mapa {clf_name}")
        for ax in axes:
            ax.axis("off")
        fig.tight_layout()
        map_path = OUT / "ex06_1_classification_map.png"
        fig.savefig(map_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        fig_cm, ax_cm = plt.subplots(figsize=(4, 4))
        ConfusionMatrixDisplay(cm).plot(ax=ax_cm, colorbar=False)
        ax_cm.set_title(f"Confusão — {clf_name}")
        cm_path = OUT / "ex06_1_confusion_matrix.png"
        fig_cm.savefig(cm_path, dpi=150, bbox_inches="tight")
        plt.close(fig_cm)
        print(f"Salvo: {map_path}\nSalvo: {cm_path}")
    else:
        print("Exemplo sintético não encontrado — usando gaussianas 2D sintéticas")
        X, y, grid, shape2d = synthetic_gaussians()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=0, stratify=y
        )
        clf = GaussianNB().fit(X_train, y_train)
        clf_name = "GaussianNB"
        y_pred = clf.predict(X_test)
        print(f"Acurácia: {accuracy_score(y_test, y_pred):.3f}")
        cm = confusion_matrix(y_test, y_pred)
        print("Matriz de confusão:\n", cm)
        zz = clf.predict(grid).reshape(shape2d)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.contourf(grid[:, 0].reshape(shape2d), grid[:, 1].reshape(shape2d), zz, alpha=0.35, cmap="tab10")
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, s=8, cmap="tab10", edgecolors="none")
        ax.set_title(f"Fronteiras {clf_name} (sintético)")
        map_path = OUT / "ex06_1_classification_map.png"
        fig.savefig(map_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        fig_cm, ax_cm = plt.subplots(figsize=(4, 4))
        ConfusionMatrixDisplay(cm).plot(ax=ax_cm, colorbar=False)
        cm_path = OUT / "ex06_1_confusion_matrix.png"
        fig_cm.savefig(cm_path, dpi=150, bbox_inches="tight")
        plt.close(fig_cm)
        print(f"Salvo: {map_path}\nSalvo: {cm_path}")


if __name__ == "__main__":
    main()
