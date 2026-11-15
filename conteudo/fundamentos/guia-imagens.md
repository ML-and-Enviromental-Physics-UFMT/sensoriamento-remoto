# Imagens, arrays e matrizes

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../data/README.md).

Depois das seis [aulas iniciais](README.md), leia [Imagens, arrays e matrizes](aulas/07-imagens-arrays-matrizes.md). Esse material veio do Capítulo 1 de Canty. O foco é representar bandas, interpretar os eixos e distinguir visualização de medição.

## Práticas

- [Primeira leitura de um raster](notebooks/01_teoria.ipynb), com o raster sintético compartilhado.
- [PCA e SVD em imagem sintética](notebooks/01_pca_propria.ipynb), sem dados externos.
- [Introdução a SAR](../radar-sar/README.md), agora em percurso próprio.

Os scripts `ex01_1.py` e `ex01_2.py` em `exercicios/` usam GDAL. Execute da raiz, no ambiente completo.

```bash
python conteudo/fundamentos/exercicios/ex01_1.py data/exemplos/exemplo_sintetico.tif 1
python conteudo/fundamentos/exercicios/ex01_2.py data/exemplos/exemplo_sintetico.tif conteudo/fundamentos/figuras/aster_pca.tif
```

O GeoTIFF resultante fica ignorado pelo Git. As figuras selecionadas ficam em `figuras/`. Os PDFs de referência são materiais de consulta local; veja o [catálogo](../../referencias/canty.md).
