# Capítulo 2 — Image Statistics

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../../data/README.md).

> Baseado em Canty (2019), Cap. 2. Leitura principal deste capítulo no repositório. Notas anteriores foram fundidas aqui.

## Antes da distribuição: quais pixels entraram na conta?

Um histograma descreve os valores selecionados. Para interpretá-lo como informação sobre o terreno, precisamos saber o que entrou nessa seleção. Uma cena com solo, vegetação, água e sombras mistura respostas físicas diferentes. Dois picos não demonstram, por si só, duas classes de cobertura.

Imagine três valores válidos de uma banda: `0,10`, `0,20` e `0,30`. A média é `0,20`. Se um pixel sem dado for representado por zero e incluído indevidamente, a média dos quatro números cai para `0,15`. O terreno não mudou; mudou a seleção usada no resumo. Este exemplo é inventado para mostrar o efeito da máscara.

Ao comparar histogramas de duas datas, confira também área, produto e época do ano. Uma mudança na distribuição pode envolver vegetação sazonal, iluminação ou atmosfera. A estatística detecta a diferença, mas não escolhe sua causa.

A interpretação física vem de Moraes, [Fundamentos](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_1.pdf), PDF pp. 15–20, e Ponzoni, [Vegetação](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_8.pdf), seção 3. A conta e sua ligação à seleção amostral são um desenvolvimento didático deste repositório. Para uma entrada sem fórmulas, veja [Interpretar imagens](../../../fundamentos/aulas/04_interpretar_imagens.md).

## 0. Para quem é este guia / o que você vai saber ao final

No Capítulo 1 você passou a tratar a imagem como array e o pixel como vetor. Aqui entramos na pergunta seguinte: **como resumir e relacionar esses números** de forma que classificação, PCA e detecção de mudança façam sentido?

Você não precisa dominar probabilidade formal. Precisa de intuição sólida de variável aleatória, histograma, média, variância, covariância e correlação — sempre colada ao raster sintético em `data/exemplos/exemplo_sintetico.tif` (o exemplo compartilhado entre os módulos).

Ao final você deve conseguir:

- Modelar o DN (ou reflectância) de uma banda como variável aleatória e o pixel multibanda como vetor aleatório.
- Ler um histograma e dizer o que ele sugere (saturação, multimodalidade, contraste).
- Calcular média e variância por banda e interpretar.
- Montar e ler matrizes de covariância e correlação $N\times N$.
- Explicar por que essas matrizes importam para classificação e PCA.
- Distinguir amostra vs população e reconhecer o caveat da autocorrelação espacial.
- Rodar `ex02_1` / `ex02_2` e o notebook com confiança.

## 1. Pré-requisitos (o que o livro assume e quase não explica)

1. **Pixel-vetor (Cap. 1).** $\mathbf{g}\in\mathbb{R}^N$ com uma coordenada por banda.
2. **Média aritmética e dispersão.** Saber que “média” puxa para o centro e “variância” mede espalhamento já basta para começar.
3. **Histograma escolar.** Contar quantas observações caem em cada intervalo.
4. **Independência vs correlação (intuição).** Duas grandezas podem tender a subir juntas sem uma “causar” a outra.
5. **Notação de esperança.** $\mathbb{E}[X]$ = valor esperado (média populacional). No computador quase sempre estimamos com médias amostrais.

O Canty formaliza depressa; este guia alonga a intuição antes das fórmulas.

## 2. Intuição do problema (sem equação)

Pegue a banda 3 do raster sintético. Cada pixel tem um número. Se você sorteasse um pixel ao acaso na cena, que valor esperaria? Quão espalhados estão os valores? Há um pico só (cena homogênea) ou vários (água + vegetação + solo)?

Agora pegue duas bandas. Quando a banda vermelha sobe, a NIR sobe junto ou faz o contrário? Em vegetação densa, vermelho baixo e NIR alto é típico — correlação negativa entre esses canais em certas regiões, positiva em outras. Na imagem inteira, bandas vizinhas do óptico quase sempre andam juntas: a cena “brilha” ou “escurece” de forma parecida em canais próximos. Essa redundância é exatamente o que a PCA (Cap. 3) vai compactar.

Estatística de imagem, neste capítulo, é: **tratar os pixels como amostra de um fenômeno aleatório** e estimar resumos (média, variância, covariâncias) que depois viram insumos de algoritmos. Não é estatística espacial completa (variogramas, krigagem): o livro, na maior parte, trata pixels como observações no espaço espectral, muitas vezes fingindo independência espacial para estimar $\boldsymbol{\mu}$ e $\boldsymbol{\Sigma}$. Essa mentira útil tem preço — discutimos no final.

## 3. O que o Canty ensina neste capítulo (mapa das seções + ideias-chave)

| Tema | Ideia-chave |
|------|-------------|
| Variável aleatória | DN/reflectância como realização de $X$ |
| Distribuição | PDF/CDF (população) vs histograma (amostra) |
| Momentos univariados | Média, variância por banda |
| Vetor aleatório | Pixel multibanda $\mathbf{X}$ |
| Segunda ordem | $\boldsymbol{\Sigma}$ (covariância), $R$ (correlação) |
| Estimação amostral | $\bar{\mathbf{g}}$, $\mathbf{S}$ a partir dos pixels |
| Uso posterior | Classificadores (Caps. 6–7), PCA/MNF (Cap. 3), mudança (Cap. 9) |

Mensagens duráveis:

1. Histograma descreve **uma** banda; covariância descreve **relações entre** bandas.
2. Correlação alta ≈ informação quase duplicada (linearmente).
3. Estimamos com a amostra de pixels; a “população” é o modelo idealizado da cena/sensor.
4. Pixels vizinhos não são independentes — a covariância espectral global ainda é útil, mas não conte a história espacial toda.

## 4. Desenvolvimento guiado (conceitos do livro, com derivação/explicação acessível)

### 4.1 Variável aleatória e o pixel

Uma **variável aleatória** $X$ é um número cujo valor não fixamos de antemão: depende do alvo, da iluminação, da atmosfera e do ruído do sensor. O DN numa posição é uma **realização** de $X$.

Uma imagem (uma banda) é uma grade de realizações. Se ignorarmos a dependência espacial por um momento, pensamos nos $m$ pixels como $m$ observações de $X$. Isso permite falar em média amostral, histograma e desvio padrão da banda.

### 4.2 PDF e CDF (intuição, sem terror)

A **função densidade de probabilidade** (PDF) $f(x)$ descreve, no modelo contínuo, onde a probabilidade se concentra: a área sob $f$ entre $a$ e $b$ é $P(a\le X\le b)$. A **função de distribuição acumulada** (CDF) é

```math
F(x)=P(X\le x)=\int_{-\infty}^{x} f(t)\,dt.
```

Você quase nunca conhece $f$ de verdade para uma cena raster sintético. O que você tem é o **histograma**: uma estimativa empírica, em barras, de como a massa de probabilidade se distribui nos valores observados. PDF/CDF são o ideal teórico; histograma é o instrumento de laboratório.

### 4.3 Histograma de uma banda

Divida a faixa $[g_{\min}, g_{\max}]$ em $B$ intervalos (bins). Conte quantos pixels caem em cada bin. O gráfico dessas contagens (ou densidades normalizadas) é o histograma.

O que procurar no raster sintético:

- **Pico único estreito:** pouco contraste; stretch ajuda na visualização.
- **Vários picos:** misturas de classes (ex.: água vs terra).
- **Massa colada no teto/chão:** saturação ou corte de no-data mal tratado.
- **Cauda longa:** poucos pixels muito claros/escuros — min–max absoluto pode ser enganoso (Cap. 1).

Em Python: `np.histogram` + plot; o `ex02_1.py` gera `figuras/histogramas_bandas.png`.

### 4.4 Média e variância (univariadas)

Para $m$ pixels da banda $k$:

$$
\bar{g}_k=\frac{1}{m}\sum_{i=1}^{m} g_{k,i},
\qquad
s_k^2=\frac{1}{m-1}\sum_{i=1}^{m}(g_{k,i}-\bar{g}_k)^2.
$$

- $\bar{g}_k$: nível radiométrico “típico” da banda na cena (ou na região).
- $s_k=\sqrt{s_k^2}$: contraste/espalhamento.

O denominador $m-1$ (Bessel) deixa $s_k^2$ não viesado para a variância populacional sob amostragem i.i.d. Em imagens enormes, $m$ vs $m-1$ quase não muda o número; a convenção importa quando você compara com `np.cov(..., ddof=1)`.

**Média populacional** $\mu=\mathbb{E}[X]$ e **variância** $\sigma^2=\mathbb{E}[(X-\mu)^2]$ são propriedades do modelo. $\bar{g}$ e $s^2$ são estimativas a partir da amostra de pixels.

### 4.5 Pixel como vetor aleatório

Com $N$ bandas,

```math
\mathbf{X}=\begin{pmatrix}X_1\\ \vdots\\ X_N\end{pmatrix},\qquad
\boldsymbol{\mu}=\mathbb{E}[\mathbf{X}]=\begin{pmatrix}\mu_1\\ \vdots\\ \mu_N\end{pmatrix}.
```

Cada realização $\mathbf{g}_i$ é um ponto no $\mathbb{R}^N$. A nuvem de todos os pixels da imagem (ou de uma classe de treinamento) é o objeto geométrico que classificadores gaussianos e PCA enxergam.

### 4.6 Matriz de covariância

A covariância populacional entre bandas $j$ e $k$ é

$$
\Sigma_{jk}=\mathrm{Cov}(X_j,X_k)=\mathbb{E}[(X_j-\mu_j)(X_k-\mu_k)].
$$

Na forma matricial,

$$
\boldsymbol{\Sigma}=\mathbb{E}\bigl[(\mathbf{X}-\boldsymbol{\mu})(\mathbf{X}-\boldsymbol{\mu})^\top\bigr].
$$

Estimativa amostral com $m$ pixels e média $\bar{\mathbf{g}}$:

$$
\mathbf{S}=\frac{1}{m-1}\sum_{i=1}^{m}
(\mathbf{g}_i-\bar{\mathbf{g}})(\mathbf{g}_i-\bar{\mathbf{g}})^\top.
$$

Se $G$ é a matriz $m\times N$ de pixels **já centrados** (colunas com média zero),

$$
\mathbf{S}=\frac{1}{m-1}G^\top G.
$$

Leitura:

| Entrada | Significado |
|---------|-------------|
| $S_{kk}$ | Variância da banda $k$ |
| $S_{jk}>0$ grande | Bandas $j$ e $k$ tendem a variar no mesmo sentido |
| $S_{jk}<0$ | Tendem a variar em sentidos opostos |
| $S_{jk}\approx 0$ | Pouca associação linear (ainda pode haver relação não linear) |

**Exemplo mental raster sintético.** Bandas VNIR adjacentes: $S_{jk}$ alto e positivo. Isso não é “bug”: sensores ópticos medem a mesma paisagem sob o mesmo Sol; a estrutura espacial comum vaza para todos os canais.

### 4.7 Matriz de correlação

A covariância mistura escala: uma banda com DN grandes domina numericamente. A correlação padroniza:

```math
R_{jk}=\frac{S_{jk}}{s_j\, s_k},\qquad -1\le R_{jk}\le 1.
```

- $R_{jk}\approx 1$: quase a mesma informação linear.
- $R_{jk}\approx -1$: contraste linear forte.
- $R_{jk}\approx 0$: pouca associação linear.

O heatmap de correlação (`ex02_2.py` → `figuras/correlacao_heatmap.png`) costuma ser mais legível que o de covariância bruta (`covariancia_heatmap.png`), porque todas as entradas compartilham a mesma escala.

### 4.8 Por que isso importa para classificação e PCA

**Classificação supervisionada (Caps. 6–7).** Muitos classificadores (máxima verossimilhança gaussiana, QDA, etc.) estimam, por classe, um $\hat{\boldsymbol{\mu}}_c$ e um $\hat{\boldsymbol{\Sigma}}_c$. A forma da elipsoide de covariância diz como a classe se espalha no espaço espectral. Se você só olhar médias e ignorar $\boldsymbol{\Sigma}$, perde a geometria da confusão entre classes.

**PCA (Cap. 3).** A PCA diagonaliza $\mathbf{S}$: encontra eixos ortogonais onde a variância se ordena. Sem $\mathbf{S}$, não há PCA clássica. Correlação alta entre bandas ⇒ poucos autovalores grandes e muitos pequenos (redundância).

**MNF.** Além de $\mathbf{S}$ (sinal+ruído), estima-se $\mathbf{S}_N$ (ruído). O Cap. 2 entrega $\mathbf{S}$; o Cap. 3.5 usa a ideia espacial para $\mathbf{S}_N$.

**Detecção de mudança (Cap. 9).** Comparar estatísticas entre datas (ou transformar diferenças) parte do mesmo vocabulário de momentos e covariâncias.

### 4.9 Amostra vs população

| | População (modelo) | Amostra (o que calculamos) |
|--|--------------------|----------------------------|
| Média | $\boldsymbol{\mu}$ | $\bar{\mathbf{g}}$ |
| Covariância | $\boldsymbol{\Sigma}$ | $\mathbf{S}$ |
| Distribuição | PDF $f$ | Histograma |

A população pode ser “todos os pixels possíveis daquela classe sob aquele sensor” — uma abstração. A amostra é o que está no GeoTIFF (ou num ROI). Quanto maior $m$, em geral melhor a estimativa — **se** as observações forem representativas. Uma cena só de floresta não estima bem a covariância de área urbana.

### 4.10 Caveat: autocorrelação espacial

Pixels vizinhos se parecem. Isso viola a hipótese i.i.d. usada na intuição “$m$ amostras independentes”. Consequências práticas:

- O **tamanho amostral efetivo** é menor que $m$: erros-padrão “ingênuos” são otimistas demais.
- $\mathbf{S}$ espectral global ainda é um resumo válido da nuvem de pontos no espaço das bandas; só não interprete $m=n_{\mathrm{lin}}n_{\mathrm{col}}$ como $m$ experimentos independentes.
- Para ruído (MNF), o livro **explora** a diferença entre vizinhos: o sinal muda devagar, o ruído não — Cap. 3.

No notebook e nos exercícios deste capítulo, seguimos a prática do livro: estatísticas globais no espaço espectral, cientes do caveat.

## 5. Além do livro (prática moderna, armadilhas, ligação com sklearn/GEE/SAR/mestrado)

**sklearn.** `StandardScaler`, `EmpiricalCovariance`, classificadores que usam covariância (`QuadraticDiscriminantAnalysis`) — todos comem a mesma ideia. `np.corrcoef` nas bandas achatadas reproduz $R$.

**GEE.** `ee.Reducer.mean`, `ee.Reducer.covariance` em uma região: mesma estatística, amostragem por scale/tile. Cuidado com escala: covariância a 10 m ≠ a 100 m se você misturar resoluções.

**SAR.** Backscatter em dB tem distribuição diferente de DN óptico; speckle infla variância local. Correlação entre VV e VH ainda é informativa, mas histogramas e $\mathbf{S}$ pedem pré-processamento (multilook, filtro) antes de copiar o pipeline do raster sintético.

**Armadilhas**

- Incluir no-data (zeros, negativos sentinela) na média/covariância.
- Comparar covariâncias entre bandas com unidades/escalas diferentes sem olhar $R$.
- Estimar $\boldsymbol{\Sigma}$ por classe com poucos pixels de treinamento → matriz singular ou instável (regularização / pooled covariance nos Caps. 6–7).
- Interpretar $R_{jk}=0$ como “bandas independentes” (só implica ausência de correlação **linear**).

## 6. Como praticar neste repositório (notebook + exercícios + outputs)

**Dado:** `data/exemplos/aster-capitulo-2.tif` (fallback automático para o raster sintético do Cap. 1 nos scripts).

**Notebook:** `notebooks/02_teoria.ipynb`.

**Exercícios**

```bash
cd conteudo/analise-de-imagens/estatistica/exercicios
python ex02_1.py
python ex02_2.py
# opcional:
python ex02_1.py ../../../../data/exemplos/exemplo_sintetico.tif -o ../figuras/histogramas_bandas.png
python ex02_2.py ../../../../data/exemplos/exemplo_sintetico.tif -o ../figuras
```

| Script | Saída típica |
|--------|----------------|
| `ex02_1.py` | Média/std por banda + `histogramas_bandas.png` |
| `ex02_2.py` | Matrizes + `covariancia_heatmap.png`, `correlacao_heatmap.png` |

**Roteiro sugerido.** (1) Rode `ex02_1` e descreva em uma frase o histograma de duas bandas contrastantes. (2) Rode `ex02_2` e localize o par de bandas com maior $|R_{jk}|$. (3) Antecipe: esse par será fortemente misturado na PC1 do Cap. 3.

## 7. Checklist de domínio + dúvidas típicas

**Checklist**

- [ ] Defino variável aleatória com um exemplo de pixel raster sintético.
- [ ] Distingo PDF/CDF (modelo) de histograma (dados).
- [ ] Calculo $\bar{g}_k$ e $s_k^2$ e interpreto.
- [ ] Escrevo $\mathbf{S}$ e leio diagonal vs fora da diagonal.
- [ ] Passo de $\mathbf{S}$ para $R$ e digo por que $R$ é mais comparável.
- [ ] Ligo $\mathbf{S}$ a classificação e a PCA em uma frase cada.
- [ ] Explico amostra vs população e o caveat espacial.
- [ ] Sei o que `ex02_1` e `ex02_2` geram.

**Dúvidas típicas**

1. *“Histograma de qual região?”*  
   Cena inteira = mistura de classes. Para assinatura de um alvo, recorte um ROI.

2. *“Usar covariância ou correlação na PCA?”*  
   PCA clássica no Canty usa covariância (após centrar). Se bandas tiverem escalas muito diferentes, padronizar (PCA na correlação) muda os pesos — escolha consciente.

3. *“Por que $m-1$?”*  
   Correção de Bessel para variância amostral. Com milhões de pixels, o efeito numérico é ínfimo; a consistência com `ddof=1` importa.

4. *“Pixels são i.i.d.?”*  
   Não. Mesmo assim $\mathbf{S}$ descreve a nuvem espectral; só calibra mal a incerteza se você fingir independência.

5. *“Isso vale para SAR VV/VH?”*  
   A álgebra vale; a interpretação do histograma e o tratamento de ruído mudam. Filtre/speckle-aware antes de cravar conclusões.
