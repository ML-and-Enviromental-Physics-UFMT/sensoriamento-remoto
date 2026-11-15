# Dados de exemplo

A versão pública usa `data/exemplos/exemplo_sintetico.tif`, gerado por [um script próprio](../scripts/gerar_dados_sinteticos.py). O arquivo contém nove canais artificiais de 96 × 96 pixels, em float32, com semente 20261115. Os valores têm unidades arbitrárias. Não representam reflectância, temperatura ou medições de um sensor. A grade não tem CRS nem localização real; sua transformação apenas numera células de tamanho unitário.

O gerador combina gradientes, padrões periódicos e uma região circular com pesos e ruído pseudoaleatórios. Não há classes de cobertura de referência. Índices, agrupamentos e classificações demonstram operações numéricas, sem interpretação ambiental ou validação de acurácia real. Os nomes históricos de bandas nos exercícios não atribuem resposta espectral a estes canais.

Para regenerar o arquivo, execute na raiz, com o ambiente instalado.

```bash
python scripts/gerar_dados_sinteticos.py
```

```python
from study_utils import example_path, read_raster
imagem, transformacao, crs = read_raster(example_path())
```

O raster sintético e sua documentação estão sob CC BY 4.0. O código do gerador segue a licença MIT do projeto. Não há conteúdo extraído do antigo ASTER neste exemplo.

## ASTER histórico

O recorte `AST_20070501.tif` foi retirado da cópia pública, assim como suas figuras derivadas e as saídas dos notebooks. O material histórico permanece no repositório antigo, conforme informado pelo responsável. O backup temporário desta limpeza foi apagado a pedido dele.

A inspeção encontrou 1000 × 1000 pixels, nove bandas float32, CRS declarado EPSG:32632, transformação identidade e ausência de NoData, nomes de bandas e identificação do produto. O CRS declarado não recupera a localização perdida. Os fatores de escala padrão não comprovam calibração. Produto, data de aquisição, unidades, origem e condições de redistribuição não foram confirmados; o nome do arquivo não comprova esses dados.

SHA-256 do recorte retirado: `4378999a4ff5f9e2b8227a829640a2a1d0c3f6b27e4ba307840cf1332a560a92`.

Para trabalhar com observações reais, obtenha um produto de uma fonte oficial, por exemplo o [NASA Earthdata Search](https://search.earthdata.nasa.gov/), e confira as condições específicas do produto. Registre identificador, acesso, licença, data, bandas, unidades, escala, CRS e NoData. Não há instrução de download deste recorte histórico porque sua origem não foi identificada. Dados externos ficam em `referencias/local/`, ignorado pelo Git; passe seu caminho aos exercícios que aceitam um raster ou ajuste a célula de entrada do notebook.
