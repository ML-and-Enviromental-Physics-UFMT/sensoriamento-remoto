# Modelo cliente-servidor e objetos `ee`

O erro mais frequente de quem já sabe Python e começa no Google Earth Engine é tentar manipular imagens e listas do GEE como se fossem arrays NumPy na memória do computador. Quando você faz isso, o código falha com mensagens pouco intuitivas, trava ou estoura cotas.

Esta aula concentra-se em uma distinção fundamental: existe código que roda no seu computador (cliente) e existe código que descreve operações para rodar nos servidores do Google (servidor).

## 1. Objetos locais versus objetos `ee.*`

No Python comum, `x = 2 + 3` calcula `5` imediatamente na sua máquina. No GEE, quando você escreve:

```python
a = ee.Number(2)
b = ee.Number(3)
c = a.add(b)
```

O servidor ainda não somou nada. A variável `c` guarda apenas uma **receita** (um grafo de execução) dizendo "some `2` com `3` quando alguém pedir o resultado". Isso se chama avaliação preguiçosa (*lazy evaluation*).

Se você rodar `print(c)`, o Python imprime a descrição do objeto proxy, não o número `5`. O cálculo só acontece no servidor quando você solicita explicitamente uma saída:

- chamando `.getInfo()` (traz um valor pequeno para o Python local);
- adicionando uma camada ao mapa (`mapa.addLayer(...)`);
- iniciando uma exportação (`ee.batch.Export...`).

## 2. Por que `for` local, `if` Python e `getInfo()` são armadilhas

Imagine uma coleção com 120 imagens Sentinel-2. Se você escrever um laço `for` em Python chamando `.getInfo()` em cada iteração, o computador faz 120 requisições síncronas pela rede, uma de cada vez. Em coleções maiores, o script leva minutos ou falha por limite de tempo.

Além disso, dentro de uma função passada para `.map()`, o argumento recebido é um símbolo abstrato do servidor, ainda sem valor concreto avaliado. Chamar `.getInfo()` ou `if` nativo do Python sobre esse argumento **gera erro de execução**, porque o cliente não consegue inspecionar um valor que ainda não foi computado.

As regras práticas recomendadas pelo guia oficial de boas práticas do GEE são:

- Não misture operadores de controle do cliente (`if`, `for`, `len`) com objetos do servidor (`ee.Number`, `ee.Image`, `ee.ImageCollection`).
- Prefira `.map()`, `.filter()`, máscaras booleanas com `.updateMask()` e substituições condicionais em raster com `.where()`.
- Evite também `ee.Algorithms.If`: a documentação do GEE desaconselha seu uso porque ambos os ramos costumam ser avaliados antes da escolha e o código fica mais lento e difícil de otimizar. Na maioria dos casos, `.filter()` ou `.where()` resolvem o problema de forma mais limpa.
- Use `.getInfo()` apenas no final, para inspecionar um número, uma lista curta de metadados ou uma tabela já agregada.

Exemplo de função mapeada inteiramente no servidor:

```python
def escalar_s2(imagem):
    bandas = imagem.select(["B2", "B3", "B4", "B8"]).multiply(0.0001)
    return bandas.copyProperties(imagem, ["system:time_start"])

colecao_escalada = colecao.map(escalar_s2)
```

Repare em dois detalhes importantes dessa função:

1. Ela usa apenas métodos `ee.*`, sem `print()` nem `.getInfo()`. O servidor consegue serializar a função e aplicá-la em paralelo em todas as imagens.
2. `copyProperties(imagem, ["system:time_start"])` preserva o timestamp de aquisição da imagem original. Operações matemáticas no GEE criam uma nova imagem sem os metadados de tempo e sensor, a menos que você os copie de volta.

## 3. Os cinco objetos principais do GEE

Quase todo script em GEE combina cinco tipos de objetos:

| Objeto | O que representa | Exemplo de uso |
|--------|------------------|----------------|
| `ee.Geometry` | Ponto, linha ou polígono geográfico | Definir a área de estudo em Cuiabá |
| `ee.Feature` | Uma geometria combinada com atributos (dicionário de propriedades) | Um talhão com nome da cultura e data |
| `ee.FeatureCollection` | Conjunto de feições (análogo a um shapefile ou GeoJSON) | Limites municipais ou polígonos de treino |
| `ee.Image` | Raster com uma ou mais bandas e metadados | Uma cena Sentinel-2 ou um mapa de NDVI |
| `ee.ImageCollection` | Pilha ou série de imagens | Todas as cenas Landsat 8 de 2024 em uma região |

## 4. Projeção e escala só são decididas na saída

Em arquivos locais com `rasterio`, você abre uma matriz com número fixo de linhas e colunas e um sistema de coordenadas definido no cabeçalho. No GEE, uma `ee.Image` pode juntar bandas de 10 m, 20 m e 60 m, ou nascer de uma composição de cenas em zonas UTM diferentes.

O GEE trabalha com pirâmides de resolução e decide a grade de cálculo **sob demanda** (*pull model*):

- Ao exibir no mapa, ele calcula na escala aproximada do zoom atual da tela.
- Composições como `.median()` ou `.mean()` perdem a projeção UTM nativa das cenas individuais e assumem `EPSG:4326` como projeção padrão até você especificar outra.
- Ao rodar `reduceRegion`, `sampleRegions` ou `Export`, ele usa o `crs` e o `scale` (ou `projection`) informados na chamada.

Por isso, sempre informe `crs` e `scale` explicitamente em cálculos quantitativos sobre composições. Confiar no zoom do mapa ou em padrões implícitos pode produzir números diferentes para a mesma região.

## Tente explicar

1. Por que `print(ee.Number(2).add(3))` não imprime `5` diretamente?
2. O que acontece se você chamar `.getInfo()` sobre o argumento `imagem` dentro de uma função passada para `.map()`?
3. O que muda na projeção de uma imagem Sentinel-2 quando você calcula `.median()` sobre a coleção?

<details>
<summary>Respostas comentadas</summary>

1. Porque `ee.Number(2).add(3)` cria apenas a descrição de uma operação no servidor. Sem `.getInfo()`, o valor não é trazido para o Python local.
2. Ocorre erro de execução, porque o argumento `imagem` dentro de `.map()` é um símbolo do servidor ainda sem valor concreto para ser inspecionado pelo cliente.
3. A imagem resultante perde a projeção UTM nativa das cenas individuais e passa a ter `EPSG:4326` como projeção padrão, exigindo que você informe `crs` e `scale` nas operações quantitativas seguintes.

</details>

Siga agora para [Catálogo, filtros, fatores de escala e máscaras de nuvens](03_catalogo_filtros_e_nuvens.md).

Fontes (consultadas em 25/11/2026): Google, [Client vs. Server](https://developers.google.com/earth-engine/guides/client_server), [Scale in Earth Engine](https://developers.google.com/earth-engine/guides/scale), [Projections](https://developers.google.com/earth-engine/guides/projections) e [Best Practices](https://developers.google.com/earth-engine/guides/best_practices).
