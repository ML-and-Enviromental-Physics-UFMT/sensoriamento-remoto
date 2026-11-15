# Consulta rápida de matemática

Escolha o [tópico](README.md) para consultar o conceito e um exemplo. As fórmulas abaixo resumem ferramentas usadas nos métodos de análise de imagens.

## Covariância

Para vetores centrados $\mathbf{g}_i \in \mathbb{R}^N$ ($i=1\ldots m$):

$$
\mathbf{S} = \frac{1}{m-1}\sum_{i=1}^{m} \mathbf{g}_i\mathbf{g}_i^\top.
$$

Diagonal = variâncias das bandas; fora da diagonal = covariação entre bandas. Em classificação gaussiana, $\mathbf{S}_k$ entra na distância de Mahalanobis.

## Autovalores / autovetores (PCA)

$$
\mathbf{S}\mathbf{w} = \lambda\mathbf{w}.
$$

Ordenar $\lambda_1 \ge \lambda_2 \ge \cdots$: a 1ª componente principal captura a direção de maior variância. Usado em Cap. 3 (transformações), Cap. 8 (pré-processamento) e Cap. 9 (PCA bitemporal).

## Distância de Mahalanobis

$$
d^2(\mathbf{x},\boldsymbol{\mu}) = (\mathbf{x}-\boldsymbol{\mu})^\top\mathbf{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu}).
$$

Leva em conta a forma elíptica da nuvem (não só a distância euclidiana). É o núcleo do classificador de máxima verossimilhança gaussiana (Cap. 6).


Veja [covariância](estatistica/covariancia.md), [autovalores](algebra-linear/autovalores-e-autovetores.md) e [Mahalanobis](estatistica/mahalanobis.md).
