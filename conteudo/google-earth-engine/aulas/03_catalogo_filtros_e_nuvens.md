# Catálogo, filtros, fatores de escala e máscaras de nuvens

Buscar uma imagem de satélite no GEE parece simples, mas três descuidos comprometem boa parte das análises iniciantes: escolher a coleção errada, esquecer o fator de escala físico das bandas e ignorar nuvens e sombras de nuvens.

## 1. Como escolher e ler uma entrada do catálogo

O catálogo público fica em [https://developers.google.com/earth-engine/datasets](https://developers.google.com/earth-engine/datasets). Antes de copiar o ID de uma coleção, confira sempre quatro campos na página oficial:

1. **Dataset Availability**: intervalo de datas coberto.
2. **Bands**: nome exato de cada banda, resolução em metros, unidade e **Scale / Offset**.
3. **Image Properties**: nomes das propriedades de metadados (como porcentagem de nuvens e tile MGRS).
4. **Terms of Use**: licença e atribuição exigida (por exemplo, produtos Sentinel-2 exigem o crédito "Contains modified Copernicus Sentinel data [ano]"; Landsat Collection 2 e SRTM são distribuídos pelo USGS/NASA em domínio público).

Produtos de reflectância de superfície (já corrigidos atmosfericamente para nível L2/SR) que servem como ponto de partida:

| Produto | ID no catálogo GEE | Resolução óptica | Conversão para reflectância |
|---------|--------------------|------------------|-----------------------------|
| Sentinel-2 MSI Level-2A (harmonizado) | `COPERNICUS/S2_SR_HARMONIZED` | 10 m e 20 m | `DN * 0.0001` |
| Landsat 8 Collection 2 Level-2 | `LANDSAT/LC08/C02/T1_L2` | 30 m | `DN * 0.0000275 - 0.2` |
| Landsat 9 Collection 2 Level-2 | `LANDSAT/LC09/C02/T1_L2` | 30 m | `DN * 0.0000275 - 0.2` |

Use `COPERNICUS/S2_SR_HARMONIZED` em vez da antiga `COPERNICUS/S2_SR`. A versão harmonizada compensa uma mudança de offset (+1000) introduzida pela ESA em janeiro de 2022, mantendo séries antes e depois dessa data na mesma escala.

## 2. Filtrar no espaço, no tempo e por metadados

Nunca processe uma coleção global inteira. Aplique os filtros na ordem mais restritiva possível: região (`filterBounds`), período (`filterDate`) e propriedades (`filter`).

```python
ponto_cuiaba = ee.Geometry.Point([-56.0967, -15.6014])
regiao = ponto_cuiaba.buffer(15000).bounds()

colecao = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(regiao)
    .filterDate("2024-07-01", "2024-10-01")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30))
)
```

Dois cuidados importantes:

- Em `filterDate(inicio, fim)`, a data inicial é inclusiva e a final é exclusiva. Para incluir todo o mês de setembro de 2024, use `"2024-10-01"` como limite final.
- Uma cena (`ee.Image`) não equivale necessariamente a uma única data na sua área de estudo. Se a região cruza a borda de dois tiles MGRS (como `21LWC` e `21LXC` em Cuiabá), `filterBounds` traz duas cenas para a mesma data. Isso aumenta `colecao.size()` e pode duplicar datas em séries temporais (tratamos isso na Aula 5).

## 3. Aplicar fator de escala antes de qualquer análise

As coleções armazenam reflectância como inteiros para economizar espaço. Sem aplicar o fator de escala e o offset da documentação, os valores perdem o significado físico e até índices de razão podem ficar errados.

### Exemplo numérico resolvido (Landsat Collection 2)

Suponha um pixel de Landsat 8/9 Collection 2 Level-2 com valores inteiros brutos `SR_B4 = 10000` (vermelho) e `SR_B5 = 18000` (NIR).

1. **Cálculo errado, usando os inteiros brutos:**
   `NDVI_bruto = (18000 - 10000) / (18000 + 10000) = 8000 / 28000 = 0,286`
2. **Conversão para reflectância (`DN * 0,0000275 - 0,2`):**
   - `RED = 10000 * 0,0000275 - 0,2 = 0,275 - 0,2 = 0,075`
   - `NIR = 18000 * 0,0000275 - 0,2 = 0,495 - 0,2 = 0,295`
3. **Cálculo correto com reflectância:**
   `NDVI = (0,295 - 0,075) / (0,295 + 0,075) = 0,220 / 0,370 = 0,595`

A diferença passa de `0,30` no NDVI porque o offset aditivo `-0,2` não se cancela na divisão. No Sentinel-2, o fator `0,0001` é puramente multiplicativo (então o NDVI até se cancelaria), mas fórmulas com constantes (como EVI), comparações entre sensores e limiares de reflectância continuam exigindo a escala aplicada.

Funções de escala no GEE:

```python
def escalar_s2(imagem):
    opticas = imagem.select("B.*").multiply(0.0001)
    return imagem.addBands(opticas, overwrite=True)

def escalar_landsat_c2(imagem):
    opticas = imagem.select("SR_B.*").multiply(0.0000275).add(-0.2)
    return imagem.addBands(opticas, overwrite=True)
```

## 4. Mascarar nuvens e sombras de nuvens

Filtrar cenas por `CLOUDY_PIXEL_PERCENTAGE < 30` descarta cenas inteiras muito nubladas, mas mantém os pixels de nuvem dentro das cenas restantes. Para remover esses pixels, usamos `.updateMask(mascara)`: onde a máscara vale `0`, o pixel fica mascarado e é ignorado por médias, medianas e redutores.

### Sentinel-2 com a banda `SCL`

O produto L2A do Sentinel-2 inclui a banda `SCL` (Scene Classification Layer), onde cada código inteiro classifica a qualidade preliminar do pixel. Entre as classes normalmente mascaradas estão:

- `1`: saturado ou defeituoso
- `3`: sombra de nuvem
- `8`: nuvem de probabilidade média
- `9`: nuvem de probabilidade alta
- `10`: cirros finos
- `11`: neve ou gelo

A `SCL` é rápida e não depende de coleção auxiliar, mas tem limitações conhecidas: costuma confundir telhados metálicos muito claros com nuvem ou neve, pode deixar escapar nuvens finas na classe `7` (nuvem de baixa probabilidade) e confunde sombras topográficas com sombras escuras na classe `2`.

```python
def mascarar_s2_scl(imagem):
    scl = imagem.select("SCL")
    mascara = (
        scl.neq(1)
        .And(scl.neq(3))
        .And(scl.neq(8))
        .And(scl.neq(9))
        .And(scl.neq(10))
        .And(scl.neq(11))
    )
    opticas = imagem.select(["B2", "B3", "B4", "B8", "B11", "B12"]).multiply(0.0001)
    return opticas.updateMask(mascara).copyProperties(imagem, ["system:time_start"])
```

### Sentinel-2 com Cloud Score+

Para reduzir erros em bordas de nuvens, sombras finas e alvos urbanos claros, o GEE disponibiliza a coleção auxiliar `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` (Pasquarella et al., 2023), vinculada por `linkCollection`. A banda `cs_cdf` varia de `0` (obstruído) a `1` (céu limpo). A documentação sugere testar limiares entre `0,50` e `0,65`, ajustando conforme a região e a estação:

```python
cs_plus = ee.ImageCollection("GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED")
colecao_ligada = colecao.linkCollection(cs_plus, ["cs_cdf"])

def mascarar_s2_csplus(imagem):
    mascara = imagem.select("cs_cdf").gte(0.60)
    opticas = imagem.select(["B2", "B3", "B4", "B8", "B11", "B12"]).multiply(0.0001)
    return opticas.updateMask(mascara).copyProperties(imagem, ["system:time_start"])
```

### Landsat 8/9 Collection 2 com `QA_PIXEL` e `QA_RADSAT`

No Landsat C2, a qualidade de cada pixel é codificada em bits na banda `QA_PIXEL`:

- bit 0 (`1 << 0`): preenchimento (*fill*)
- bit 1 (`1 << 1`): nuvem dilatada (*dilated cloud*)
- bit 2 (`1 << 2`): cirro (*cirrus*)
- bit 3 (`1 << 3`): nuvem (*cloud*)
- bit 4 (`1 << 4`): sombra de nuvem (*cloud shadow*)

A máscara `0b11111` (decimal `31`) testa esses cinco bits de uma vez. Também convém verificar `QA_RADSAT.eq(0)` para descartar pixels radiometricamente saturados:

```python
def mascarar_landsat_c2(imagem):
    qa = imagem.select("QA_PIXEL")
    radsat = imagem.select("QA_RADSAT")
    mascara = qa.bitwiseAnd(0b11111).eq(0).And(radsat.eq(0))
    opticas = imagem.select("SR_B.*").multiply(0.0000275).add(-0.2)
    return opticas.updateMask(mascara).copyProperties(imagem, ["system:time_start"])
```

Nenhuma máscara automática é perfeita. Inspecione o resultado em RGB (cor verdadeira) antes de confiar em uma composição ou série temporal.

## Tente explicar

1. No exemplo resolvido de Landsat C2, por que o NDVI mudou de `0,286` para `0,595` ao aplicar escala e offset?
2. Qual é a diferença entre filtrar `CLOUDY_PIXEL_PERCENTAGE < 30` e aplicar `updateMask(...)`?
3. Em `filterDate("2024-01-01", "2024-01-31")`, o dia 31 de janeiro entra no filtro?

<details>
<summary>Respostas comentadas</summary>

1. Porque o Landsat Collection 2 possui um offset aditivo (`-0,2`), que não se cancela na razão `(NIR - RED) / (NIR + RED)`. Sem aplicá-lo, o denominador fica artificialmente inflado e o índice cai.
2. O filtro por `CLOUDY_PIXEL_PERCENTAGE` seleciona ou descarta cenas inteiras com base na cobertura média de nuvens. Já `updateMask(...)` remove individualmente os pixels contaminados dentro das cenas mantidas.
3. Não. A data final de `filterDate` é exclusiva; para incluir 31 de janeiro inteiro, use `"2024-02-01"`.

</details>

Agora siga para [Composições temporais, índices espectrais e visualização](04_composicoes_indices_e_visualizacao.md) e depois execute [Primeiros passos no GEE](../notebooks/01_primeiros_passos_gee.ipynb).

Fontes (consultadas em 25/11/2026): Google, [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets), [Sentinel-2 SR Harmonized](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED), [Cloud Score+ for Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_CLOUD_SCORE_PLUS_V1_S2_HARMONIZED) e [Landsat 8 C2 L2](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2); Pasquarella et al. (2023).
