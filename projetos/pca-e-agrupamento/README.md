# PCA e agrupamento de uma imagem

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../data/README.md).

Este piloto padroniza as bandas do raster sintético, calcula componentes principais e aplica k-means aos escores. O objetivo é observar como uma transformação espectral muda a representação dos pixels antes do agrupamento.

Abra o [notebook](notebooks/aplicacao_piloto.ipynb) no ambiente do repositório. Ele encontra a raiz tanto quando iniciado nesta pasta quanto pela raiz e usa `data/exemplos/exemplo_sintetico.tif`. As figuras são gravadas em `figuras/` deste projeto.

O material veio de `mestrado/`, mas não usa dados de uma dissertação. O raster sintético é o exemplo compartilhado. Para trocar a imagem, ajuste `RASTER_PATH` e confira a compatibilidade das bandas e o tratamento dos pixels inválidos.

Os grupos não foram avaliados como classes de cobertura. Este piloto não demonstra acurácia de um mapa nem substitui um protocolo de pesquisa. Compare a composição dos componentes com o agrupamento e explique onde os grupos parecem seguir brilho ou sombra, em vez de uma cobertura identificada.

Pré-requisitos: [transformações](../../conteudo/analise-de-imagens/transformacoes/README.md) e [agrupamento](../../conteudo/classificacao/agrupamento/README.md). Dependências: NumPy, Matplotlib, rasterio e scikit-learn.
