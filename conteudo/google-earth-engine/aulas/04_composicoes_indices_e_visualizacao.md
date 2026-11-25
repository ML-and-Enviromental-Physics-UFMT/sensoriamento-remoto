# Composições temporais, índices espectrais e visualização

Depois de filtrar uma coleção e mascarar nuvens, você tem várias imagens sobre a mesma região em datas diferentes. O passo seguinte quase sempre envolve combinar essas cenas em uma imagem limpa (composição) e calcular índices espectrais.

Esta aula reforça uma regra que atravessa todo o repositório (veja [Pré-processamento](../../pre-processamento/aulas/00_teoria.md)): o que você ajusta para enxergar melhor na tela não deve entrar nos cálculos físicos.

## 1. Composições temporais

Uma `ImageCollection` pode ser reduzida ao longo do tempo para uma única `ee.Image`. Cada método muda o significado físico do resultado:

| Método | Como combina cada pixel no tempo | Quando faz sentido | Cuidados |
|--------|----------------------------------|--------------------|----------|
| `.median()` | Valor mediano por banda, ignorando pixels mascarados | Mosaico sem nuvens em janelas sazonais | Mistura datas diferentes entre pixels e até entre bandas do mesmo pixel |
| `.mean()` | Média aritmética por banda | Resumo médio quando a máscara de nuvem é muito limpa | Mais sensível a nuvens ou sombras que escaparam da máscara |
| `.mosaic()` | Coloca a última imagem da coleção por cima | Quando a ordem da coleção foi definida deliberadamente | Pode deixar costuras bruscas entre cenas |
| `.qualityMosaic("NDVI")` | Escolhe, por pixel, toda a observação da data com maior valor na banda indicada | Pico de vigor vegetativo no ciclo agrícola | Exagera valores extremos se houver ruído residual |

Na prática, `.median()` é o primeiro ponto de teste para reduzir resíduos de nuvem e sombra. Registre sempre a janela temporal usada: uma mediana de três meses na estação seca de Mato Grosso representa um estado bem diferente de uma mediana anual. Lembre também que a composição perde a projeção UTM nativa das cenas individuais e passa a usar `EPSG:4326` como projeção padrão até você especificar `crs` e `scale` nas etapas seguintes.

## 2. Calcular índices espectrais

Há duas formas principais de calcular índices no GEE.

### Razão normalizada direta com `normalizedDifference`

Para índices do tipo `(A - B) / (A + B)`:

```python
ndvi = composta.normalizedDifference(["B8", "B4"]).rename("NDVI")
ndwi_mcfeeters = composta.normalizedDifference(["B3", "B8"]).rename("NDWI")
nbr = composta.normalizedDifference(["B8", "B12"]).rename("NBR")
```

Dois cuidados técnicos essenciais aqui:

1. **Ordem e definição das bandas:** `["B8", "B4"]` calcula `(B8 - B4) / (B8 + B4)`. No caso do NDWI, `(B3 - B8) / (B3 + B8)` (verde e NIR) é o **NDWI de McFeeters (1996)**, voltado a destacar corpos d'água superficiais; ele é diferente do **NDWI de Gao (1996)** (`(B8 - B11) / (B8 + B11)`, NIR e SWIR), usado para avaliar conteúdo de água na vegetação.
2. **Entradas negativas são mascaradas:** conforme a documentação do GEE, `normalizedDifference` descarta automaticamente qualquer pixel onde uma das duas bandas de entrada seja negativa. Em produtos com offset aditivo como Landsat Collection 2 Level-2, água muito escura ou sombras podem gerar reflectâncias levemente negativas; com `normalizedDifference`, esses pixels somem (e `sampleRegions` descarta as amostras correspondentes). Quando isso ocorrer, prefira `.expression()` com proteção contra denominador zero:

```python
ndvi_expr = composta.expression(
    "(NIR - RED) / (NIR + RED)",
    {"NIR": composta.select("B8"), "RED": composta.select("B4")},
).rename("NDVI")
```

### Fórmulas gerais com `expression`

Para índices com constantes ou mais de duas bandas, como o EVI, use `.expression()`:

```python
evi = composta.expression(
    "2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))",
    {
        "NIR": composta.select("B8"),
        "RED": composta.select("B4"),
        "BLUE": composta.select("B2"),
    },
).rename("EVI")
```

A constante `+ 1` no denominador pressupõe reflectância na escala `0` a `1`. Se as bandas não tivessem sido multiplicadas por `0.0001` antes, a fórmula produziria valores distorcidos.

Para manter bandas e índices juntos em um único objeto `ee.Image`, use `addBands`:

```python
composta_com_indices = composta.addBands([ndvi, ndwi_mcfeeters])
```

## 3. Visualizar com `geemap` sem confundir tela com medição

No `geemap`, os parâmetros de visualização controlam apenas como os valores numéricos são convertidos em cores RGB de 8 bits para o navegador:

```python
import geemap

mapa = geemap.Map()
mapa.centerObject(regiao, 11)

vis_rgb = {
    "bands": ["B4", "B3", "B2"],
    "min": 0.02,
    "max": 0.30,
    "gamma": 1.2,
}

vis_ndvi = {
    "min": -0.2,
    "max": 0.8,
    "palette": ["#8c510a", "#f6e8c3", "#80cdc1", "#01665e"],
}

mapa.addLayer(composta_com_indices.clip(regiao), vis_rgb, "Sentinel-2 RGB")
mapa.addLayer(composta_com_indices.select("NDVI").clip(regiao), vis_ndvi, "NDVI")
mapa
```

Três cuidados práticos:

1. **Nunca calcule índices sobre `imagem.visualize(...)`.** O método `visualize()` converte a imagem em canais RGB de exibição (0 a 255) e descarta a grandeza física.
2. **Use `.clip(regiao)` no final, para exibir ou exportar.** Recortar cada imagem individual antes de compor costuma ser desnecessário e mais lento do que filtrar com `filterBounds(regiao)` e recortar só o resultado final.
3. **Paleta de cor não define classe.** Um pixel verde-escuro no mapa de NDVI apenas tem contraste alto entre NIR e vermelho; confirmar se é floresta nativa, pastagem vigorosa ou cultura irrigada exige contexto e referência.

## Tente explicar

1. Por que uma composição `.median()` pode combinar bandas de datas diferentes no mesmo pixel?
2. Por que `normalizedDifference` pode fazer sumir pixels de água escura em imagens Landsat Collection 2?
3. Por que você não deve passar o resultado de `imagem.visualize(vis_rgb)` para `normalizedDifference`?

<details>
<summary>Respostas comentadas</summary>

1. Porque `.median()` calcula a mediana de forma independente em cada banda. Em uma pilha de 10 datas, a mediana de `B4` pode vir da data 3 e a mediana de `B8` pode vir da data 7.
2. Porque o offset `-0,2` do Landsat C2 pode produzir valores levemente negativos sobre água escura ou sombras, e `normalizedDifference` mascara automaticamente pixels com qualquer banda de entrada negativa.
3. Porque `visualize()` transforma medições físicas em canais de exibição RGB (0 a 255) já esticados por `min`, `max` e `gamma`, destruindo a relação quantitativa original das bandas.

</details>

Agora abra e execute o notebook [Primeiros passos no GEE](../notebooks/01_primeiros_passos_gee.ipynb) para colocar em prática as aulas 1 a 4. Depois, avance para [Redutores espaciais, séries temporais e exportação](05_redutores_series_e_exportacao.md).

Fontes (consultadas em 25/11/2026): Google, [Compositing and Mosaicking](https://developers.google.com/earth-engine/guides/ic_composite_mosaic), [Image Visualization](https://developers.google.com/earth-engine/guides/image_visualization) e [Mathematical Operations](https://developers.google.com/earth-engine/guides/image_math).
