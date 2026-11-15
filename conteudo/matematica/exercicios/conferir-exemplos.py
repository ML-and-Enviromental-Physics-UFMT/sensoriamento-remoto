"""Recalcula exemplos matemáticos do percurso, sem imagens externas.

Execute da raiz com Python e NumPy instalados. As asserções conferem identidades
numéricas e resultados analíticos; não avaliam o domínio do estudante.
"""
import numpy as np


def main():
    X = np.array([[0.12, 0.30], [0.20, 0.25], [0.05, 0.10]])
    np.testing.assert_allclose(X.mean(axis=0), [0.37/3, 0.65/3])
    A = np.array([[1., 2., 3.], [4., 5., 6.]])
    np.testing.assert_array_equal(A.T.T, A)
    x, y = np.array([1., 2.]), np.array([3., 4.])
    np.testing.assert_allclose(x @ y, 11)
    np.testing.assert_allclose(np.outer(x, y), [[3, 4], [6, 8]])
    W = np.array([[-1., 1.], [0.5, 0.5]])
    np.testing.assert_allclose(W @ [0.2, 0.6], [0.4, 0.4])
    print('Vetores, matrizes e produtos: conferidos.')

    A = np.array([[2., 1.], [1., -1.]])
    solution = np.linalg.solve(A, [5., 1.])
    np.testing.assert_allclose(solution, [2, 1])
    np.testing.assert_allclose(A @ solution, [5, 1])
    np.testing.assert_allclose(np.linalg.det([[1., 2.], [2., 4.]]), 0)
    np.testing.assert_allclose(np.linalg.cond(np.diag([1e8, 1e-8])), 1e16)
    A = np.array([[1., 0.], [1., 1.], [1., 2.]])
    beta, *_ = np.linalg.lstsq(A, [1., 2., 2.], rcond=None)
    np.testing.assert_allclose(beta, [7/6, 1/2])
    residual = np.array([1., 2., 2.]) - A @ beta
    np.testing.assert_allclose(residual @ residual, 1/6)
    np.testing.assert_allclose(A.T @ residual, [0, 0], atol=1e-14)
    print('Sistemas, determinantes e mínimos quadrados: conferidos.')

    basis = np.array([[1., 1.], [1., -1.]])
    np.testing.assert_allclose(basis @ [2.5, 0.5], [3, 2])
    u = np.array([1., 1.]) / np.sqrt(2)
    P = np.outer(u, u)
    projection = P @ [3., 2.]
    np.testing.assert_allclose(projection, [2.5, 2.5])
    np.testing.assert_allclose(u @ (np.array([3., 2.]) - projection), 0, atol=1e-14)
    np.testing.assert_allclose(P @ P, P)
    S = np.array([[2., 1.], [1., 2.]])
    values, vectors = np.linalg.eigh(S)
    np.testing.assert_allclose(values, [1, 3])
    np.testing.assert_allclose(S @ vectors, vectors * values)
    np.testing.assert_allclose(values[-1] / values.sum(), 0.75)
    X = np.array([[2., 0.], [-2., 0.]])
    U, singular, Vt = np.linalg.svd(X, full_matrices=False)
    np.testing.assert_allclose(U @ np.diag(singular) @ Vt, X)
    np.testing.assert_allclose(singular**2 / (len(X)-1), [8, 0])
    U_explicit = np.array([[1., 1.], [-1., 1.]]) / np.sqrt(2)
    np.testing.assert_allclose(U_explicit @ np.diag([2*np.sqrt(2), 0]), X)
    print('Bases, projeções, autovalores e SVD: conferidos.')

    posterior = 0.9*0.2 / (0.9*0.2 + 0.1*0.8)
    np.testing.assert_allclose(posterior, 180/260)
    np.testing.assert_allclose(0.9*0.01/(0.9*0.01+0.1*0.99), 1/12)
    data = np.array([0.1, 0.2, 0.3])
    np.testing.assert_allclose([data.mean(), data.var(ddof=1), data.std(ddof=1)], [0.2, 0.01, 0.1])
    X = np.array([[1., 2.], [2., 4.], [3., 6.]])
    Xc = X - X.mean(axis=0)
    covariance = Xc.T @ Xc / (len(X)-1)
    np.testing.assert_allclose(covariance, [[1, 2], [2, 4]])
    np.testing.assert_allclose(covariance, np.cov(X, rowvar=False, ddof=1))
    np.testing.assert_allclose(np.linalg.det(covariance), 0)
    delta = np.array([2., 2.])
    np.testing.assert_allclose(delta @ np.linalg.solve(np.diag([4., 1.]), delta), 5)
    S = np.array([[2., 1.], [1., 2.]])
    np.testing.assert_allclose([v @ np.linalg.solve(S, v) for v in [np.array([1., 1.]), np.array([1., -1.])]], [2/3, 2])
    print('Bayes, dispersão, covariância e Mahalanobis: conferidos.')

    loss = lambda w: (2*w - 3)**2
    gradient = lambda w: 4*(2*w - 3)
    h = 1e-5
    for w in [0., 1., 1.5, 3.]:
        difference = (loss(w+h)-loss(w-h))/(2*h)
        np.testing.assert_allclose(difference, gradient(w), atol=1e-8)
    w = 0.
    trace = []
    for _ in range(4):
        trace.append((w, loss(w)))
        w -= 0.1*gradient(w)
    np.testing.assert_allclose(trace, [[0, 9], [1.2, 0.36], [1.44, 0.0144], [1.488, 0.000576]])
    np.testing.assert_allclose(np.array([1., 1.]) @ (np.array([1., 1.])/np.sqrt(2)), np.sqrt(2))
    for i, eigenvalue in enumerate([4., 1.]):
        w = np.eye(2)[:, i]
        np.testing.assert_allclose(np.diag([4., 1.]) @ w, eigenvalue*w)
        np.testing.assert_allclose(w @ w, 1)
    print('Derivadas, gradiente descendente e candidatos de Lagrange: conferidos.')


if __name__ == '__main__':
    main()
