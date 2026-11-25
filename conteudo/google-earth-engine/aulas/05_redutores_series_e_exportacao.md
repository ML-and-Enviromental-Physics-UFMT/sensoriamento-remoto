# Redutores espaciais, séries temporais e exportação

Ver um mapa interativo ajuda a inspecionar nuvens e padrões visuais, mas uma análise científica precisa de números reproduzíveis: médias e desvios por polígono, séries temporais em tabela e arquivos GeoTIFF ou CSV exportados para análise posterior.

No GEE, quase toda agregação numérica passa por objetos `ee.Reducer`.

## 1. Estatística em uma região: `reduceRegion`

Para resumir uma imagem (por exemplo, a banda `NDVI` de uma composta `composta_com_indices` dentro de um polígono `poligono`), usamos `reduceRegion`:

```python
poligono = ee.Geometry.Point([-56.11032, -15.57505]).buffer(100)
ndvi = composta_com_indices.select("NDVI")

redutor = (
    ee.Reducer.mean()
    .combine(ee.Reducer.stdDev(), sharedInputs=True)
    .combine(ee.Reducer.count(), sharedInputs=True)
)

estatisticas = ndvi.reduceRegion(
    reducer=redutor,
    geometry=poligono,
    crs="EPSG:32721",
    scale=10,
    maxPixels=1e8,
)

print(estatisticas.getInfo())
```

Cada parâmetro tem um motivo concreto:

- `crs="EPSG:32721"` e `scale=10`: como `.median()` perde a projeção nativa e cai para `EPSG:4326`, informar `crs` (aqui `WGS 84 / UTM zona 21S`, a grade nativa do Sentinel-2 em Cuiabá) junto com `scale` em metros fixa exatamente a grade de cálculo. Mudar `scale` (por exemplo, de 10 m para 100 m) faz o GEE ler um nível mais grosso da pirâmide de resolução, alterando média, desvio-padrão e covariância.
- `mean` versus `count` na borda do polígono: por padrão, o `ee.Reducer.mean()` pondera os pixels parcialmente interceptados pela borda do polígono conforme a fração de sobreposição; já `count()` conta quantos pixels válidos contribuíram com peso positivo.
- `maxPixels=1e8`: teto de segurança contra requisições acidentais em áreas gigantes (o padrão do GEE é `1e7`).
- `bestEffort=True` (opcional): se a área ultrapassar `maxPixels`, o GEE engrossa a escala automaticamente para terminar a conta. Evite ligar `bestEffort=True` sem registrar isso no relatório, pois ele muda silenciosamente a resolução efetiva da estatística.

## 2. Estatística em vários polígonos: `reduceRegions`

Se você tem uma `ee.FeatureCollection` com vários polígonos (`meus_poligonos`, por exemplo, cinco parques ou dez talhões), use `reduceRegions` (no plural) em vez de um laço `for` em Python:

```python
meus_poligonos = ee.FeatureCollection([
    ee.Feature(poligono, {"nome": "area_1"}),
])

tabela_poligonos = ndvi.reduceRegions(
    collection=meus_poligonos,
    reducer=ee.Reducer.mean(),
    crs="EPSG:32721",
    scale=10,
)
```

O resultado é uma nova `ee.FeatureCollection` em que cada feição ganha a coluna `mean` com o valor calculado.

## 3. Séries temporais: tiles, lacunas e limite de `getInfo()`

Antes de extrair uma série temporal, há duas armadilhas importantes:

1. **Datas duplicadas entre tiles MGRS:** se o polígono cruza a borda de dois tiles Sentinel-2 (como `21LWC` e `21LXC` em Cuiabá), `filterBounds` traz duas cenas na mesma data, uma cobrindo 100% do polígono e outra cobrindo apenas parte dele. Filtrar explicitamente por `.filter(ee.Filter.eq("MGRS_TILE", "21LWC"))` (ou compor cenas da mesma data) evita linhas duplicadas na tabela e no CSV.
2. **Não apague as datas sem observação válida na tabela:** se em uma data o polígono inteiro estava coberto por nuvens, `stats.get("NDVI_mean")` retorna nulo (`None`) e `pixels_validos` vale `0`. Preservar todos os registros na tabela deixa explícito quais passagens falharam por nuvem (como recomenda a aula de observação em [Fundamentos](../../fundamentos/aulas/03_satelites_e_observacao.md)). Filtre os nulos apenas no momento de traçar o gráfico, usando marcadores ou quebrando a linha nas lacunas para não inventar interpolação visual na estação chuvosa.

```python
def extrair_ndvi_medio(imagem):
    stats = imagem.select("NDVI").reduceRegion(
        reducer=ee.Reducer.mean().combine(ee.Reducer.count(), sharedInputs=True),
        geometry=poligono,
        crs="EPSG:32721",
        scale=10,
        maxPixels=1e7,
    )
    return ee.Feature(
        None,
        {
            "data": imagem.date().format("YYYY-MM-dd"),
            "ndvi_medio": stats.get("NDVI_mean"),
            "pixels_validos": stats.get("NDVI_count"),
        },
    )

serie_fc = colecao_ndvi.map(extrair_ndvi_medio)
```

Para converter uma tabela pequena para `pandas` no cliente:

```python
import pandas as pd

registros = [f["properties"] for f in serie_fc.getInfo()["features"]]
df = pd.DataFrame(registros)
df["data"] = pd.to_datetime(df["data"])
df = df.sort_values("data")
```

Atenção ao limite do cliente: `.getInfo()` em uma `FeatureCollection` tem limite prático de **5.000 elementos** (além de limite de tamanho de resposta). Para séries longas com muitos polígonos, exporte direto como CSV com `ee.batch.Export.table.toDrive`.

## 4. Exportação assíncrona (`ee.batch.Export`)

Requisições interativas (`getInfo()`, `mapa.addLayer()`) têm limite rígido de tempo e memória. Quando você precisa baixar um GeoTIFF completo ou uma tabela grande, use tarefas em lote (`ee.batch.Export`). Elas rodam em segundo plano nos servidores do Google e gravam no Google Drive, Google Cloud Storage ou como Asset do Earth Engine.

Exportando um raster para o Google Drive:

```python
tarefa_imagem = ee.batch.Export.image.toDrive(
    image=composta_com_indices.select(["B4", "B3", "B2", "B8", "NDVI"]).toFloat(),
    description="sentinel2_cuiaba_seca_2024",
    folder="gee_estudos",
    fileNamePrefix="s2_cuiaba_seca_2024",
    region=regiao,
    scale=10,
    crs="EPSG:32721",
    maxPixels=1e9,
)
tarefa_imagem.start()
```

Exportando a tabela completa (incluindo datas com `pixels_validos == 0`) em CSV:

```python
tarefa_tabela = ee.batch.Export.table.toDrive(
    collection=serie_fc,
    description="serie_ndvi_cuiaba_2024",
    folder="gee_estudos",
    fileNamePrefix="serie_ndvi_cuiaba_2024",
    fileFormat="CSV",
)
tarefa_tabela.start()
```

Para acompanhar o andamento pelo Python:

```python
print(tarefa_imagem.status())
```

Dois cuidados evitam falhas comuns na exportação:

1. `.toFloat()` garante que todas as bandas tenham o mesmo tipo numérico. O GeoTIFF falha se misturar `Int16` e `Float64`.
2. Escolha o `crs` de forma consciente: `EPSG:32721` (WGS 84 / UTM zona 21S) preserva a grade nativa do Sentinel-2 em Cuiabá sem reamostragem extra; `EPSG:31981` (SIRGAS 2000 / UTM zona 21S) atende ao padrão cartográfico brasileiro oficial, com diferença centimétrica em relação ao WGS 84, mas envolve reamostragem da grade nativa pelo GEE.

## Tente explicar

1. O que `bestEffort=True` faz em `reduceRegion` e por que ele exige cuidado em análises científicas?
2. Por que convém manter as datas com `pixels_validos == 0` na tabela da série temporal e filtrar os nulos só na hora do gráfico?
3. Por que chamamos `.toFloat()` antes de exportar uma imagem que mistura bandas originais e índices calculados?

<details>
<summary>Respostas comentadas</summary>

1. Se o cálculo ultrapassar `maxPixels`, `bestEffort=True` aumenta automaticamente o tamanho do pixel (`scale`) para caber no limite. Sem registrar isso, você pode achar que calculou estatísticas a 10 m quando o servidor usou uma grade mais grossa.
2. Porque remover os nulos da tabela apaga o registro das datas em que a passagem do satélite ocorreu mas ficou encoberta por nuvens. Guardar todas as datas com `pixels_validos` preserva o histórico completo de lacunas e evita mascarar vieses sazonais.
3. Porque `Export.image` exige que todas as bandas da imagem exportada compartilhem o mesmo tipo de dado compatível no GeoTIFF.

</details>

Pratique esta etapa no notebook [Séries temporais e exportação](../notebooks/02_series_temporais_e_exportacao.ipynb). Em seguida, avance para [Classificação supervisionada e avaliação no GEE](06_classificacao_e_validacao_no_gee.md).

Fontes (consultadas em 25/11/2026): Google, [Reducers Overview](https://developers.google.com/earth-engine/guides/reducers_intro), [Reduce Region](https://developers.google.com/earth-engine/guides/reducers_reduce_region) e [Exporting Data](https://developers.google.com/earth-engine/guides/exporting).
