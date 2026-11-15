#!/usr/bin/env python3
"""ex07_1 — compara dois classificadores no mesmo conjunto de rótulos.

GaussianNB vs RandomForest (fallback SVM). Dados: Exemplo sintético + limiar NDVI
ou gaussianas 2D. Referência: legado/canty/auxil/scripts/classify.py, crossvalidate.py, mcnemar.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

REPO = Path(__file__).resolve().parents[4]
ASTER = REPO / "data" / "exemplos" / "exemplo_sintetico.tif"
OUT = Path(__file__).resolve().parents[1] / "figuras"
OUT.mkdir(parents=True, exist_ok=True)


def load_aster():
    import rasterio

    with rasterio.open(ASTER) as ds:
        img = ds.read().astype(np.float64)
    bands, rows, cols = img.shape
    ndvi = (img[2] - img[1]) / (img[2] + img[1] + 1e-6)
    y = np.zeros(ndvi.shape, dtype=int)
    y[ndvi >= 0.35] = 2
    y[(ndvi >= 0.1) & (ndvi < 0.35)] = 1
    X = img.reshape(bands, -1).T
    return X, y.ravel(), rows, cols, ndvi


def synthetic():
    rng = np.random.default_rng(1)
    means = [(-1.2, -0.8), (1.5, 0.4), (0.1, 2.0)]
    Xs, ys = [], []
    for k, mu in enumerate(means):
        Xs.append(rng.normal(mu, 0.55, size=(700, 2)))
        ys.append(np.full(700, k))
    return np.vstack(Xs), np.concatenate(ys), None, None, None


def main():
    if ASTER.is_file():
        print(f"ASTER: {ASTER}")
        X_all, y_all, rows, cols, ndvi = load_aster()
        rng = np.random.default_rng(7)
        idx = rng.choice(len(y_all), size=min(15000, len(y_all)), replace=False)
        X, y = X_all[idx], y_all[idx]
    else:
        print("Exemplo sintético ausente — dados sintéticos 2D")
        X, y, rows, cols, ndvi = synthetic()
        X_all, y_all = X, y

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0, stratify=y
    )
    scaler = StandardScaler().fit(X_train)
    X_train_s = scaler.transform(X_train)
    X_test_s = scaler.transform(X_test)

    models = {
        "GaussianNB": GaussianNB(),
        "RandomForest": RandomForestClassifier(
            n_estimators=80, max_depth=12, random_state=0, n_jobs=-1
        ),
    }
    # SVM só no subconjunto de teste/treino já reduzido; se for lento, ainda é ok
    if X_train_s.shape[1] <= 4 or X_train_s.shape[0] <= 5000:
        models["SVM_RBF"] = SVC(kernel="rbf", C=2.0, gamma="scale")

    preds = {}
    best_name, best_acc = None, -1.0
    for name, clf in models.items():
        clf.fit(X_train_s, y_train)
        yp = clf.predict(X_test_s)
        preds[name] = yp
        acc = accuracy_score(y_test, yp)
        kappa = cohen_kappa_score(y_test, yp)
        print(f"\n=== {name} ===")
        print(f"acurácia={acc:.3f}  kappa={kappa:.3f}")
        print(confusion_matrix(y_test, yp))
        print(classification_report(y_test, yp, digits=3))
        if acc > best_acc:
            best_acc, best_name = acc, name

    # McNemar simplificado entre NB e o melhor outro
    names = list(preds.keys())
    if len(names) >= 2:
        a, b = names[0], names[1]
        correct_a = preds[a] == y_test
        correct_b = preds[b] == y_test
        n01 = int(np.sum(~correct_a & correct_b))
        n10 = int(np.sum(correct_a & ~correct_b))
        # estatística de McNemar com correção de continuidade
        if n01 + n10 > 0:
            chi2 = (abs(n01 - n10) - 1) ** 2 / (n01 + n10)
            print(f"\nMcNemar ({a} vs {b}): n01={n01}, n10={n10}, chi2≈{chi2:.3f}")
            print("(ver legado/canty/auxil/scripts/mcnemar.py para o fluxo completo do livro)")

    # mapa com o melhor modelo
    best = models[best_name]
    if rows is not None:
        pred_map = best.predict(scaler.transform(X_all)).reshape(rows, cols)
        fig, axes = plt.subplots(1, 2, figsize=(9, 4))
        axes[0].imshow(ndvi, cmap="RdYlGn", vmin=-0.2, vmax=0.8)
        axes[0].set_title("NDVI-like")
        axes[1].imshow(pred_map, cmap="tab10", vmin=0, vmax=9)
        axes[1].set_title(f"Melhor: {best_name}")
        for ax in axes:
            ax.axis("off")
    else:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.scatter(X_test[:, 0], X_test[:, 1], c=preds[best_name], s=10, cmap="tab10")
        ax.set_title(f"Predições {best_name}")
    fig.tight_layout()
    out = OUT / "ex07_1_comparison_map.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nMelhor hold-out: {best_name} ({best_acc:.3f})")
    print(f"Salvo: {out}")


if __name__ == "__main__":
    main()
