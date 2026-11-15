# Classificação Não Supervisionada (Agrupamento)

> Stub. Teoria didática completa: [`00_teoria.md`](00_teoria.md).  
> Referência: Canty (2019), Cap. 8.

## Quando o não supervisionado ajuda em SR

- Não há (ainda) amostras de campo suficientes.
- Quer-se **explorar** quantas coberturas espectrais distintas existem na cena.
- Pré-processamento / redução de complexidade antes da classificação supervisionada.
- Segmentação espectral para gerar candidatos a classes.

O resultado são **clusters**, não nomes de cobertura: a interpretação (legenda) é etapa posterior.

## k-means

1. Escolha $K$ centróides iniciais.
2. Atribua cada pixel ao centróide mais próximo (distância euclidiana no espaço espectral).
3. Recalcule centróides; repita até estabilizar.

Simples e rápido; assume clusters esféricos de tamanho similar. Sensível à escala das bandas — normalize ou use PCA antes se as bandas tiverem amplitudes muito diferentes.

Referência do livro: `legado/canty/auxil/scripts/kmeans.py`, `legado/canty/auxil/scripts/ekmeans.py` (variante estendida).

## EM / mistura de gaussianas (GMM)

Modela $`p(\mathbf{x}) = \sum_{k=1}^{K} \pi_k\,\mathcal{N}(\mathbf{x};\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)`$.

O algoritmo **Expectation–Maximization** alterna:

- **E**: responsabilidades (soft assignment) de cada pixel a cada componente;
- **M**: atualização de $\pi_k$, $\boldsymbol{\mu}_k$, $\boldsymbol{\Sigma}_k$.

Mais flexível que k-means (elipses, soft labels), mais caro computacionalmente. No sklearn: `GaussianMixture`. No livro: `legado/canty/auxil/scripts/em.py`.

## SOM (Self-Organizing Map)

Mapa neural 2D que preserva topologia: pixels espectralmente próximos tendem a neurônios vizinhos. Útil para visualização e agrupamento exploratório. Referência: `legado/canty/auxil/scripts/som.py`.

## Exercícios

- `ex08_1.py` — k-means em vetores espectrais raster sintético (subamostra para velocidade).
- `ex08_2.py` — GMM/sklearn opcional, mesmo fluxo de mapa.
