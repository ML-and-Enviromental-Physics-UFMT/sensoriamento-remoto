# Capítulo 5 — Realce e correção de imagens

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../data/README.md).

> Referência: Morton J. Canty, *Image Analysis, Classification and Change Detection in Remote Sensing* (4ª ed., 2019), Cap. 5 — *Image Enhancement and Correction*.  
> Dado padrão neste repositório: `data/exemplos/exemplo_sintetico.tif`.

---

## Antes do realce: qual problema você quer resolver?

Se uma banda parece escura porque os valores ocupam uma faixa estreita, um realce pode ajudar a enxergar seus padrões. Se há fumaça entre o sensor e o alvo, o sinal pode ter mudado pela interação com a atmosfera. Esticar o contraste resolve a primeira necessidade, mas não estima a contribuição atmosférica da segunda.

Imagine duas cenas iguais no terreno, exibidas com mínimos e máximos próprios. Um valor intermediário pode ganhar cores diferentes nas duas figuras. Portanto, não interprete diferença de cor como diferença física sem conferir a composição e a escala de exibição.

Outro caso é a posição. Se a margem de um rio aparece deslocada entre as datas, uma correção radiométrica não alinha as grades. O problema geométrico exige registro e avaliação do alinhamento. Confira esses pontos antes de interpretar uma diferença temporal.

Fonte complementar: Moraes, [Fundamentos](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_1.pdf), seção 1.3, sobre a atmosfera; Albuquerque, [Cartografia](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_10.pdf), PDF pp. 6–8, sobre representação espacial. A aplicação desses princípios ao realce e ao registro prepara o conteúdo do Canty. Veja também [Da imagem ao mapa](../../fundamentos/aulas/05_da_imagem_ao_mapa.md).

## 0. Para quem é este guia / o que você vai saber ao final

Este guia é para quem já lê bandas como arrays (Cap. 1), entende histogramas (Cap. 2) e viu filtros espaciais (Cap. 4). O Cap. 5 muda o foco: nem toda operação é “análise estatística” — muita coisa existe para **enxergar melhor** ou para **alinhar / calibrar** o dado antes da análise.

Ao terminar, você deve conseguir:

1. Separar com clareza **realce visual** (contrast stretch, equalização de histograma) de **correção física / geométrica** (radiância, reflectância, registro com GCPs).
2. Explicar o stretch linear (e por percentis) e a equalização de histograma — o que cada um faz no histograma e quando distorcem o significado radiométrico.
3. Enunciar a regra de ouro: **stretch ≠ calibração**. Deixar a imagem “bonita” não transforma DN em reflectância.
4. Descrever correção radiométrica (valor do pixel) versus geométrica (lugar do pixel).
5. Entender o papel de **cantos**, **Canny** e **momentos de Hu** como feições locais para interpretação e registro — e ligar isso aos scripts `ex05_*` / `ex05_viz`.
6. Rodar o fluxo versionável deste repo (PNGs em `figuras/`) sem gravar GeoTIFFs de 34 MB ao lado do raster sintético por acidente.

Comece pela diferença entre exibir, corrigir os valores e alinhar a grade. Depois acompanhe os métodos e os exercícios correspondentes.

---

## 1. Pré-requisitos (o que o livro assume e quase não explica)

**Do Cap. 1**

- DN (digital number) ≠ grandeza física automaticamente. O sensor entrega números em uma escala; fatores de calibração e modelos atmosféricos transformam esses números.
- GeoTIFF carrega georreferência (geotransform / CRS). “Corrigir geometricamente” mexe nessa relação pixel ↔ mapa.

**Do Cap. 2**

- Histograma e CDF (função de distribuição acumulada empírica): a equalização de histograma é essencialmente um remapeamento via CDF.
- Percentis: o stretch 2%–98% usa estatística robusta para não deixar outliers ditarem o contraste.

**Do Cap. 4**

- Gradiente / Sobel: Canny é um pipeline de bordas que começa em ideias de gradiente + suavização + histerese.
- Vizinhança: cantos são lugares onde a variação é forte em **duas** direções (não só uma, como numa borda retilínea).

**Matemática / geometria leve**

- Transformação linear no plano: rotação, escala, translação (RST). Matriz $3\times 3$ homogênea aparece no `ex05_3.py`.
- Mínimos quadrados: ajustar parâmetros RST a partir de vários pares de pontos (GCPs) — o exercício monta o sistema $A\mathbf{x}\approx\mathbf{y}$.

**Python útil**

- NumPy para stretch e histograma; OpenCV (`cornerMinEigenVal`, `Canny`, `findContours`, `HuMoments`) nos exercícios de feições; GDAL nos scripts “originais” do livro.
- Matplotlib com `Agg` para PNG headless (`ex05_4`, `ex05_viz`).

Se você ainda mistura “abrir a imagem no QGIS e esticar” com “gerar NDVI comparável entre datas”, este capítulo existe exatamente para desfazer essa confusão.

---

## 2. Intuição do problema (sem equação)

Imagine a mesma cena raster sintético de duas maneiras.

**Modo A — apresentação.** Você quer mostrar vegetação, água e cidade numa figura de relatório. Os DNs brutos ocupam uma faixa estreita ou têm caudas longas; a imagem parece “lavada” ou escura. Você estica o contraste ou equaliza o histograma. Pronto: o olho enxerga estrutura. Você **não** inventou informação nova — só redistribuiu a escala de cinza (ou de cada banda) para o display.

**Modo B — medida.** Você quer comparar reflectância entre junho e setembro, ou alimentar um classificador com valores comparáveis aos de outro sensor. Aí esticar por percentis **por cena** pode ser desastroso: cada data ganha uma escala diferente; a “mesma” floresta muda de número sem mudar no chão. O que você precisa é **correção radiométrica** (calibração, atmosfera, talvez topografia) e, se for empilhar ou cruzar mapas, **correção / registro geométrico**.

Há ainda um terceiro fio no capítulo: **feições locais**. Cantos e bordas não “corrigem” a radiometria; ajudam a achar pontos estáveis para amarrar duas imagens (GCPs), a segmentar contornos e a descrever formas (momentos de Hu). No Cap. 4 você já viu Sobel/Laplaciano; aqui o Canty coloca essas ideias no contexto de realce, registro e descrição de objetos.

Resumo mental em uma frase: **realce muda como você vê; correção muda o que o número (ou a posição) significa; feições localizam estrutura.**

---

## 3. O que o Canty ensina neste capítulo (mapa das seções + ideias-chave)

| Bloco no Canty | Ideia-chave | Levar para o laboratório |
|----------------|-------------|---------------------------|
| Realce radiométrico / contraste | Stretch e equalização | Ferramentas de visualização; cuidado em pipelines quantitativos |
| Correção radiométrica | DN → grandeza física (visão geral) | Calibração e atmosfera como pré-requisito de comparação |
| Correção geométrica | Posição no mapa; GCPs | RST / polinômios; RMS dos resíduos |
| Feições (bordas, cantos, momentos) | Estrutura espacial local | Canny, cantos, Hu; insumos para registro e interpretação |

Ideias-chave que atravessam o capítulo:

- Histogram shaping (stretch, EQ) opera na **distribuição dos valores**, não no modelo físico do sensor.
- Correção radiométrica e geométrica respondem a perguntas diferentes (*quanto?* vs *onde?*).
- Feições de canto/borda são pontos e curvas estáveis o bastante para amarrar geometria — daí o exercício com GCPs e o com momentos de Hu.
- O livro não substitui um manual de calibração raster sintético/Landsat; ele dá o enquadramento e a prática computacional.

Neste repo: `ex05_4` (stretch vs EQ), `ex05_1`/`ex05_viz` (canto/Canny), `ex05_2`/`ex05_viz` (Hu), `ex05_3` (RST via GCPs).

---

## 4. Desenvolvimento guiado (conceitos do livro, com explicação acessível)

### 4.1 Realce visual versus correção física

| | Realce (enhancement) | Correção |
|--|----------------------|----------|
| Objetivo | Legibilidade, contraste, interpretação visual | Comparabilidade física ou alinhamento espacial |
| Mexe em | Escala de display / histograma | Valor calibrado ou coordenadas |
| Reversível / cosmético? | Em geral cosmético para análise | Deve ser documentado e, se possível, rastreável |
| Exemplo | Percentile stretch 2–98%; hist. eq. | DN→radiância→reflectância; ortorretificação; registro RST |

Você pode realçar **depois** de corrigir, para mostrar o produto. O erro clássico é realçar **no lugar** de corrigir e seguir o processamento como se os números fossem reflectância.

### 4.2 Estiramento de contraste (contrast stretch)

Ideia: mapear um intervalo de valores de entrada $[x_{\mathrm{low}}, x_{\mathrm{high}}]$ para $[0,1]$ ou $[0,255]$:

```math
x'
=
\mathrm{clip}
\left(
\frac{x - x_{\mathrm{low}}}{x_{\mathrm{high}} - x_{\mathrm{low}}},\,
0,\, 1
\right).
```

Escolhas comuns para $x_{\mathrm{low}}$ e $x_{\mathrm{high}}$:

- mínimo e máximo da imagem (sensível a outliers e a pixels ruins);
- percentis $p_{\mathrm{low}}$, $p_{\mathrm{high}}$ (ex.: 2% e 98%) — o que `ex05_4.py` e os stretches dos Caps. 4–5 usam.

Efeito: pixels abaixo de $x_{\mathrm{low}}$ saturam no preto; acima de $x_{\mathrm{high}}$, no branco; o miolo do histograma ganha contraste. **Não cria informação nova.** Em RGB, esticar cada banda separadamente é o caminho usual para composição colorida legível — e também o caminho para cores “irreais” se os percentis forem agressivos.

### 4.3 Equalização de histograma

Objetivo aproximado: redistribuir os níveis de cinza para que o histograma fique mais **uniforme**, usando a CDF empírica. Em discretização com $L$ níveis (ex.: 256),

$$
x' \propto F_{\hat{}}(x),
$$

onde $F_{\hat{}}$ é a CDF estimada dos valores (após quantização). Intuição: níveis raros “ganham espaço”; o contraste global sobe.

Cuidados:

- Em regiões homogêneas, o ruído também é amplificado.
- A relação ordinal local se preserva de forma grosseira, mas a **relação radiométrica** entre cenas ou sensores se perde se cada imagem for equalizada à parte.
- Para análise quantitativa (índices, detecção de mudança, classificação com significado físico), equalização global costuma ser má ideia como pré-processamento dos *features*.

No `ex05_4.py`, a função `histogram_equalization` quantiza a banda, acumula o histograma, monta a LUT via CDF e remapeia. Compare no PNG `figuras/realce_stretch_histeq.png` o stretch por percentis (previsível) com a EQ (mais agressiva).

### 4.4 “Stretch ≠ calibração” — a regra que evita meses de confusão

**Calibração radiométrica** usa coeficientes do sensor (gain/offset), eventualmente irradiance solar, ângulo zenital, e modelos atmosféricos, para transformar DN em radiância ($L$) ou reflectância ($\rho$). O histograma muda, mas por um motivo físico documentado.

**Stretch** escolhe percentis *desta* imagem e espalha os valores no monitor. Amanhã outra cena da mesma órbita terá outros percentis; o stretch será outro.

Checklist rápido:

- Vou calcular NDVI e comparar datas? → trabalhe em reflectância (ou pelo menos DN calibrado de forma consistente); stretch só no mapa final para figura.
- Vou só interpretar visualmente uma composição 3-2-1? → stretch por banda é adequado.
- Vou treinar um classificador e reportar acurácia? → seja explícito se os atributos foram esticados; em geral prefira escala calibrada ou padronização *com parâmetros fixos* (média/std do treino), não percentis por cena.

### 4.5 Correção radiométrica — intuição DN → radiância → reflectância

Cadeia típica (óptico passivo), em espírito — constantes e fórmulas exatas dependem do sensor e do produto:

1. **DN → radiância** no sensor: $L = g\cdot\mathrm{DN} + b$ (gain/offset; às vezes tabelas por banda).
2. **Radiância → reflectância aparente / TOA**: normaliza pela irradância solar e geometria sol-sensor.
3. **Correção atmosférica** (DOS, modelos baseados em física, produtos Surface Reflectance prontos): tenta aproximar reflectância de superfície.
4. **Efeitos de iluminação / topografia** (ex.: C-correction em `legado/canty/auxil/scripts/c_corr.py`): em relevo forte, a mesma cobertura parece mais clara ou escura conforme a face da encosta.

O Canty apresenta o enquadramento; produtos modernos (Landsat Collection 2 SR, Sentinel-2 L2A, etc.) muitas vezes já entregam um passo adiantado. O ponto didático permanece: saiba **em que nível radiométrico** está o seu array antes de interpretar números.

### 4.6 Correção geométrica e GCPs

Aqui o objeto de interesse é a **posição**. Exemplos:

- georreferenciar um raster sem CRS confiável;
- registrar imagem–imagem (mesma área, datas ou sensores diferentes);
- ortorretificar com DEM (além do RST simples).

**GCP** (*ground control point*): par de coordenadas (pixel na imagem A ↔ mapa ou pixel na imagem B). Com vários GCPs, ajusta-se um modelo (afim, RST, polinomial). O `ex05_3.py` implementa um **RST** (rotação–escala–translação) por mínimos quadrados:

- lê pares de pontos de um arquivo de GCPs;
- monta sistema linear nas incógnitas $a,b,x_0,y_0$;
- imprime a matriz da transformação e o **RMS** dos resíduos.

RMS alto ⇒ GCPs ruins, modelo insuficiente (precisa de afim completo / polinômio / warping local), ou distorção residual (relevo, óptica). RMS baixo não garante qualidade se todos os pontos estiverem num canto da cena — espalhe GCPs.

### 4.7 Cantos, Canny e momentos de Hu (como nos `ex05_*`)

**Cantos (ex.: `cv.cornerMinEigenVal`).**  
Uma borda tem gradiente forte numa direção; um canto tem variação forte em duas. O menor autovalor da estrutura local de gradientes (janela $7\times 7$ no `ex05_1`) é alto em cantos. Cantos bons são candidatos a GCP: estáveis, localizáveis, repetíveis entre datas (com ressalvas: sombra, inundação, obras).

**Canny.**  
Pipeline clássico: suavizar → gradiente → supressão não máxima → histerese com dois limiares. Produz bordas finas e conectadas melhor que um Sobel cru. No `ex05_1` (`-a 2`) e no `ex05_viz`, Canny vira mapa de bordas; no `ex05_2`, Canny alimenta `findContours`.

**Contornos + momentos de Hu.**  
Momentos geométricos resumem a forma de uma região. Os **momentos de Hu** são combinações projetadas para serem invariantes a certas transformações (translação, escala, rotação — no sentido clássico da literatura). O `ex05_2` calcula Hu por contorno e plota histogramas de $\log\mu$ dos primeiros momentos; o `ex05_viz` grava isso em `figuras/ex05_hu_moments.png` sem `plt.show()` interativo.

Uso típico em SR: descrever manchas / objetos segmentados, casar formas, ou só explorar a estatística de contornos da cena. Não substituem atributos espectrais; complementam.

### 4.8 Ligação Cap. 4 → Cap. 5

| Cap. 4 | Cap. 5 |
|--------|--------|
| Sobel / Laplaciano | Canny (pipeline de borda) |
| Suavização | Prefácio comum antes de Canny / cantos |
| Campo / vizinhança | Coerência espacial de GCPs e de objetos |
| Filtrar antes de classificar | Realçar para ver classes; corrigir para medir classes |

---

## 5. Além do livro (prática moderna, armadilhas, ligação com o mestrado)

**Produtos prontos vs faça-você-mesmo.** Em muitos fluxos atuais você baixa Surface Reflectance e gasta energia em máscaras de nuvem, índice e classificação — não em reinventar calibração. Ainda assim, precisa saber o que o produto *já* corrigiu (e o que não corrigiu: BRDF, topografia, sazonalidade fenológica).

**Google Earth Engine.** `image.unitScale`, `visualize({min,max})` e `image.aside` são realces de display. Compostos `median()` em coleções e `normalizedDifference` operam na escala do produto. Misturar `visualize` com cálculo de índice é o mesmo erro stretch/calibração, só que na API.

**scikit-image / OpenCV.** `exposure.rescale_intensity`, `equalize_hist`, `equalize_adapthist` (CLAHE). CLAHE equaliza por azulejos e limita amplificação de contraste — útil em visualização, ainda cosmético para física.

**Armadilhas**

- Equalizar cada data de uma série e depois detectar “mudança”.
- Esticar PC1–PC3 de formas diferentes e interpretar cores como se fossem bandas físicas.
- Gerar GCPs só em regiões fáceis (costa reta) e declarar RMS baixo como sucesso global.
- Rodar `ex05_1` no raster sintético de 34 MB e versionar o GeoTIFF vizinho no Git — use `ex05_viz.py` para PNG em `figuras/`.
- Confiar em Canny com limiares default em DN brutos sem olhar o histograma: limiares 50/150 em `uint8` assumem uma escala; stretch prévio (como em `ex05_viz`) muda o jogo.

**Mestrado / SAR.** Correção geométrica e coregistro rigoroso são críticos em detecção de mudança e em interferometria. Realce de speckle (Cap. 4 + filtros adaptativos) é outra família: não equalize histograma de intensidade SAR achando que “atmosférico”. Para óptico em relevo, `legado/canty/auxil/scripts/c_corr.py` é a ponte topológica mencionada no README do Cap. 5 / ecossistema `legado/canty/auxil/`.

**Deep learning.** Redes de super-resolução e de realce aprendido também são, em espírito, mapeamentos cosméticos ou task-specific — não calibradores físicos, a menos que treinadas com esse alvo. A disciplina do Cap. 5 (saber *qual* pergunta a operação responde) continua válida.

---

## 6. Como praticar neste repositório (notebook + exercícios + outputs)

**Dado padrão**

```text
data/exemplos/exemplo_sintetico.tif
```

**Mapa dos scripts**

| Script | Papel | Saída recomendada |
|--------|--------|-------------------|
| `exercicios/ex05_4.py` | Stretch vs equalização | `figuras/realce_stretch_histeq.png` |
| `exercicios/ex05_viz.py` | Canto + Canny + Hu (wrapper headless) | `figuras/ex05_corner_canny.png`, `ex05_hu_moments.png` |
| `exercicios/ex05_1.py` | Script do livro: canto ou Canny | GeoTIFF **ao lado do input** (local) |
| `exercicios/ex05_2.py` | Contornos + Hu com `plt.show()` | Interativo; prefira `ex05_viz` para PNG |
| `exercicios/ex05_3.py` | RST a partir de arquivo de GCPs | Impressão da matriz + RMS no terminal |
| `notebooks/05_teoria.ipynb` | Realce + demos de feições | PNGs em `figuras/` |

Comandos (a partir de `conteudo/pre-processamento/`):

```bash
# realce (versionável)
python exercicios/ex05_4.py
python exercicios/ex05_4.py -b 2 --p-low 5 --p-high 95

# feições → figuras/ (recomendado)
python exercicios/ex05_viz.py

# scripts originais do livro (requerem GDAL/OpenCV; ex05_1 grava ao lado do TIF)
python exercicios/ex05_1.py -b 1 -a 1 ../../data/exemplos/exemplo_sintetico.tif
python exercicios/ex05_1.py -b 1 -a 2 ../../data/exemplos/exemplo_sintetico.tif
python exercicios/ex05_2.py -b 1 ../../data/exemplos/exemplo_sintetico.tif
python exercicios/ex05_3.py caminho/para/gcps.txt
```

**Roteiro sugerido (≈1–2 h)**

1. Rode `ex05_4` e abra `realce_stretch_histeq.png`. Descreva em duas frases a diferença visual stretch vs EQ.
2. Mude `--p-low` / `--p-high`. O que satura? O histograma “miolo” melhora?
3. Rode `ex05_viz`. Relacione cantos densos com áreas texturadas da cena; Canny com limites água/solo.
4. Leia o código do `ex05_3` (mesmo sem arquivo de GCPs): identifique onde entram $a,b,x_0,y_0$ e o RMS.
5. Escreva num caderno: três exemplos do seu fluxo de mestrado que são realce e três que são correção.

**Dependências:** `numpy`, `matplotlib`; `opencv-python` para feições; `rasterio` / `GDAL` / `tifffile` para ler o GeoTIFF; GDAL obrigatório nos scripts originais `ex05_1`–`ex05_2`.

---

## 7. Checklist de domínio + dúvidas típicas

### Checklist

- [ ] Distingo realce visual de correção radiométrica e de correção geométrica.
- [ ] Explico stretch linear/percentil e equalização de histograma e seus riscos em séries temporais.
- [ ] Nunca chamo stretch de “calibração”.
- [ ] Sei que radiométrica mexe no valor e geométrica no lugar.
- [ ] Relaciono cantos / Canny / Hu aos scripts `ex05_1`, `ex05_2`, `ex05_viz`.
- [ ] Sei por que `ex05_viz` / `ex05_4` existem além dos scripts do livro (PNG em `figuras/`, Git amigo).
- [ ] Consigo ler a saída RST + RMS do `ex05_3` como qualidade de ajuste de GCPs.

### Dúvidas típicas

**“Equalização ficou mais legível que o stretch — posso usar sempre?”**  
Para *figura*, sim, com gosto. Para *atributos* de classificação ou mudança, em geral não. Prefira stretch controlado só no display final.

**“Percentis 2–98% são obrigatórios?”**  
São um default robusto, não uma lei. Em cenas com água escura dominante ou nuvens brilhantes, ajuste. O importante é documentar os limites.

**“Preciso corrigir atmosfera no raster sintético deste repo para estudar o Cap. 5?”**  
Não para entender stretch, feições e RST. Sim quando for comparar datas ou sensores de verdade no mestrado.

**“Canny não parece com o Sobel do Cap. 4.”**  
Esperado: Canny afina bordas e usa histerese. Sobel entrega magnitude contínua; Canny entrega mapa binário (ou quase) de bordas.

**“Momentos de Hu para quê se eu só classfico por espectro?”**  
Forma e espectro contam histórias diferentes. Hu entra quando objetos (talhões, lagos, construções) importam; classificação pixel a pixel espectral pode ignorá-los.

**“Meu RMS no RST está baixo, mas o mosaicamento falha.”**  
GCPs localizados, modelo rígido demais para a distorção, ou erro de unidade (pixel vs mapa). Espalhe pontos, tente modelo afim completo, inspecione resíduos por ponto.

**“Posso versionar o `*_corner.tif` do ex05_1?”**  
Melhor não (tamanho). Use `ex05_viz.py` e mantenha PNGs em `figuras/`.

---

*Capítulo anterior:* filtros e campos (Cap. 4). *Próximos:* classificação supervisionada (Caps. 6–7), onde realce demais vira viés e correção bem feita vira comparabilidade.
