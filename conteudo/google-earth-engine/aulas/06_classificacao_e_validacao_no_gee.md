# Classificação supervisionada e avaliação no GEE

O Google Earth Engine permite treinar um classificador como Random Forest em poucos segundos. Justamente por ser rápido, fica fácil gerar um mapa colorido com acurácia aparentemente acima de 95% que, na prática, está inflada por autocorrelação espacial ou por rótulos mal conferidos.

A lógica estatística desta aula segue [Classificação supervisionada](../../classificacao/supervisionada/aulas/00_teoria.md) e [Redes e avaliação](../../classificacao/redes-e-avaliacao/aulas/00_teoria.md). Aqui traduzimos esse fluxo para a API Python do GEE.

## 1. Definir classes e amostras em polígonos separados

No GEE, os exemplos rotulados entram como uma `ee.FeatureCollection` de pontos ou polígonos com uma propriedade inteira para a classe (por exemplo, `classe`: `0` = água, `1` = vegetação densa, `2` = solo exposto / pastagem seca).

O erro mais comum nos tutoriais rápidos é extrair todos os pixels dos polígonos com `sampleRegions` e depois sortear pixels aleatoriamente para treino (70%) e teste (30%). Quando você faz isso:

- Dois pixels vizinhos dentro do mesmo polígono quase sempre têm assinaturas espectrais muito parecidas (autocorrelação espacial).
- Um pixel cai no treino e o vizinho imediato cai na avaliação.
- A matriz de confusão mede memorização local, não capacidade de generalizar para o resto da cena.

Uma prática mais honesta já no nível didático é **separar polígonos distintos** em regiões diferentes da cena antes de extrair os pixels: vários polígonos de treino por classe de um lado, vários polígonos de teste separados de outro, sem sobreposição. Ainda assim, vale ser claro sobre o alcance desse teste: centenas de pixels extraídos de poucos polígonos não são amostras probabilísticas independentes, e a matriz resultante não substitui uma avaliação estatística do mapa inteiro.

Antes de treinar, fixe explicitamente `projection` (ou `crs` + `scale`). Como as bandas SWIR (`B11`, `B12`) do Sentinel-2 têm resolução nativa de 20 m, amostrar em `scale=20` na projeção UTM da cena (`EPSG:32721`) mantém coerência entre as bandas:

```python
bandas_preditoras = ["B2", "B3", "B4", "B8", "B11", "B12", "NDVI", "NDWI"]
projecao_20m = ee.Projection("EPSG:32721").atScale(20)

amostras_treino = composta.select(bandas_preditoras).sampleRegions(
    collection=poligonos_treino,
    properties=["classe"],
    projection=projecao_20m,
    scale=20,
)

amostras_teste = composta.select(bandas_preditoras).sampleRegions(
    collection=poligonos_teste,
    properties=["classe"],
    projection=projecao_20m,
    scale=20,
)
```

## 2. Treinar `smileRandomForest` e classificar a imagem

O classificador padrão mais usado no GEE para atributos tabulares (bandas e índices) é o `ee.Classifier.smileRandomForest`:

```python
classificador = ee.Classifier.smileRandomForest(
    numberOfTrees=100,
    seed=42,
).train(
    features=amostras_treino,
    classProperty="classe",
    inputProperties=bandas_preditoras,
)

mapa_classificado = composta.select(bandas_preditoras).classify(classificador)
```

Alguns cuidados importantes:

- `numberOfTrees`: 50 a 200 árvores costumam estabilizar o erro em testes iniciais; `seed` garante reprodutibilidade.
- **Escala na visualização versus na exportação:** o modelo acima foi treinado com pixels de 20 m, mas ao adicionar `mapa_classificado` no `geemap` em zoom baixo (por exemplo, zoom 11), o GEE classifica a imagem na resolução da pirâmide da tela (cerca de 75 m). Para avaliação quantitativa ou geração do produto final, exporte ou reduza informando `crs="EPSG:32721"` e `scale=20` explicitamente.

## 3. Avaliar com matriz de confusão (exemplo resolvido)

Aplique o classificador às amostras dos polígonos de teste e calcule a matriz de confusão no servidor:

```python
teste_predito = amostras_teste.classify(classificador)
matriz = teste_predito.errorMatrix("classe", "classification")

print("Matriz de confusão:", matriz.getInfo())
print("Acurácia global:", matriz.accuracy().getInfo())
print("Acurácia do produtor:", matriz.producersAccuracy().getInfo())
print("Acurácia do usuário:", matriz.consumersAccuracy().getInfo())
```

### Exemplo numérico resolvido

Suponha uma matriz 3x3 devolvida por `errorMatrix("classe", "classification")`, onde as **linhas** são a referência (0 = água, 1 = vegetação, 2 = solo) e as **colunas** são a predição do modelo:

| Referência \ Predito | 0 (Água) | 1 (Vegetação) | 2 (Solo) | Total da linha |
|----------------------|----------|---------------|----------|----------------|
| **0 (Água)** | 90 | 5 | 5 | 100 |
| **1 (Vegetação)** | 0 | 85 | 15 | 100 |
| **2 (Solo)** | 10 | 20 | 20 | 50 |
| **Total da coluna** | 100 | 110 | 40 | **250** |

Calculando à mão:

- **Acurácia global** (diagonal dividida pelo total):
  `(90 + 85 + 20) / 250 = 195 / 250 = 0,78` (78%).
- **Acurácia do produtor** (acerto por linha, complementar ao erro de omissão):
  - Água: `90 / 100 = 0,90` (90%)
  - Vegetação: `85 / 100 = 0,85` (85%)
  - Solo: `20 / 50 = 0,40` (40%)
- **Acurácia do usuário** (acerto por coluna, complementar ao erro de comissão):
  - Água: `90 / 100 = 0,90` (90%)
  - Vegetação: `85 / 110 = 0,773` (77,3%)
  - Solo: `20 / 40 = 0,50` (50%)

Observe o alerta que os números mostram: a acurácia global de 78% parece razoável à primeira vista, mas o classificador acertou apenas 40% dos pixels reais de solo (60% de erro de omissão) e só metade do que marcou como solo era realmente solo (50% de erro de comissão). Por isso, nunca reporte apenas a acurácia global.

## 4. Limites que o GEE não resolve sozinho

Executar `classify()` sem erro não valida um mapa de uso e cobertura da terra. Em um estudo real ou artigo científico, você ainda precisa garantir:

- **Legenda bem definida**: o que separa vegetação arbórea de pastagem alta ou parque urbano?
- **Desenho amostral probabilístico para estimativa de área**: contar pixels do mapa classificado diretamente (`reduceRegion` com `frequencyHistogram`) gera estimativa enviesada quando os erros de omissão e comissão não se cancelam (Olofsson et al., 2014).
- **Transferência temporal e espacial**: um modelo treinado na estação seca de uma região não deve ser aplicado na estação chuvosa ou em outro bioma sem nova avaliação.
- **Referência independente**: polígonos desenhados apenas olhando o próprio mapa de NDVI criam validação circular. Use levantamento de campo, imagens de altíssima resolução ou bases de referência independentes.

## Tente explicar

1. Por que separar treino e avaliação por pixel dentro dos mesmos polígonos costuma inflar a acurácia estimada?
2. No exemplo resolvido acima, o que significa dizer que a classe Solo teve acurácia do produtor de 40% e acurácia do usuário de 50%?
3. Contar pixels classificados como "água" no mapa final fornece automaticamente a área real de água sem viés?

<details>
<summary>Respostas comentadas</summary>

1. Por causa da autocorrelação espacial: pixels vizinhos dentro do mesmo polígono compartilham quase a mesma resposta espectral. Avaliar no pixel ao lado mede memorização local em vez de generalização.
2. Acurácia do produtor de 40% significa que apenas 40% dos pixels de referência da classe Solo foram corretamente classificados como Solo (60% foram omitidos e caíram em outras classes). Acurácia do usuário de 50% significa que, entre todos os pixels que o modelo rotulou como Solo, apenas metade era realmente Solo na referência.
3. Não. Erros de omissão e comissão alteram a contagem de pixels do mapa; estimativas de área com intervalo de confiança exigem amostragem probabilística e ajuste pela matriz de erro.

</details>

Execute agora o notebook [Classificação supervisionada no GEE](../notebooks/03_classificacao_supervisionada_gee.ipynb) e compare o fluxo com as aulas teóricas em [Classificação](../../classificacao/README.md).

Fontes (consultadas em 25/11/2026): Google, [Supervised Classification in Earth Engine](https://developers.google.com/earth-engine/guides/classification); Olofsson et al. (2014), *Good practices for estimating area and assessing accuracy of land change*, Remote Sensing of Environment, 148, 42-57.
