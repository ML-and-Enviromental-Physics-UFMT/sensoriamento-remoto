# Capítulo 1 — Images, Arrays, and Matrices

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../data/README.md).

> Baseado em Canty (2019), Cap. 1. Este guia é a leitura principal do capítulo neste repositório. Notas antigas foram fundidas aqui; o satélite de radar continua em [SAR.md](../../radar-sar/aulas/01-introducao.md).

## Antes das matrizes: o que cada componente mede

Se a notação ainda atrapalha, leia [Da paisagem ao número](01_da_paisagem_ao_numero.md) e [Energia e resposta dos alvos](02_energia_e_alvos.md). Um vetor de pixel reúne medições de bandas diferentes. Seus componentes não são números intercambiáveis: cada um corresponde à resposta do alvo, da atmosfera e do instrumento naquela faixa.

Por exemplo, `[0,10; 0,50]` pode representar reflectâncias hipotéticas no vermelho e NIR. A diferença entre os componentes tem uma explicação física. O baixo vermelho pode estar associado à absorção por pigmentos, enquanto o alto NIR pode envolver espalhamento na estrutura foliar. A geometria do dossel, o solo e a sombra também participam. O vetor não é uma identificação de espécie.

Antes de calcular estatísticas, anote o significado das bandas, a unidade ou escala e a regra de validade dos pixels. Dois arrays com o mesmo formato podem conter grandezas incompatíveis.

Fonte complementar: Moraes, [Fundamentos](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_1.pdf), PDF pp. 15–21; Ponzoni, [Vegetação](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_8.pdf), PDF pp. 8–14. Os números do exemplo são autorais. O [catálogo](../../../referencias/inpe/README.md) registra a procedência e os links de download.

## 0. Para quem é este guia / o que você vai saber ao final

Este texto é para quem já consegue abrir um script Python, importar NumPy e plotar algo com Matplotlib, mas ainda não “pensa” em imagem de satélite como objeto matemático. Você não precisa ter lido o PDF do Canty antes: a ideia é que, ao terminar, consiga abrir o raster sintético em `data/exemplos/exemplo_sintetico.tif`, dizer o que cada eixo do array significa, explicar por que um pixel é um vetor, e saber a diferença entre esticar contraste para ver a cena e calibrar radiometricamente para medir.

Ao final você deve ser capaz de:

- Distinguir sensores **passivos** (ópticos/termais) de **ativos** (SAR, LiDAR) e saber quando cada um importa.
- Representar uma imagem multiespectral como array $g_k(i,j)$ e cada pixel como vetor $\mathbf{g}(i,j)$.
- Relacionar formatos de armazenamento BSQ / BIL / BIP com o `shape` típico no NumPy `(bandas, linhas, colunas)`.
- Usar o mínimo de álgebra linear (produto, covariância, autovalores) suficiente para entender a PCA do Exercício 1.2.
- Aplicar stretch min–max com consciência: visualização ≠ calibração.
- Ligar essa base ao notebook, aos scripts `ex01_1` / `ex01_2` e à ponte Sentinel-1 (Cuiabá) do mestrado.

## 1. Pré-requisitos (o que o livro assume e quase não explica)

O Canty entra rápido em arrays e matrizes. Quase sem aviso, ele assume que você já viu:

1. **Pixel e resolução espacial.** Uma cena digital é uma grade: cada célula (pixel) cobre uma área no terreno (ex.: 15 m × 15 m no VNIR do raster sintético). O valor numérico na célula é o que o sensor registrou naquela posição e naquela banda.
2. **Banda espectral.** Um sensor óptico não grava “uma foto colorida” no sentido de câmera de celular. Ele grava várias camadas, cada uma sensível a um intervalo de comprimentos de onda (azul, verde, vermelho, infravermelho próximo, SWIR, etc.). Essas camadas são as **bandas**.
3. **DN vs grandeza física.** Muitos arquivos chegam em *digital numbers* (DN): inteiros brutos do instrumento. Reflectância de superfície, radiância ou backscatter (em SAR) já são grandezas calibradas. O livro trabalha com arrays numéricos; a interpretação física depende do produto.
4. **Vetor e matriz.** Um vetor coluna $\mathbf{x}\in\mathbb{R}^N$ é uma lista ordenada de $N$ números. Uma matriz $A\in\mathbb{R}^{m\times n}$ é uma tabela. O produto $A\mathbf{x}$ combina linhas de $A$ com $\mathbf{x}$.
5. **GeoTIFF / GDAL.** Na prática, o arquivo `.tif` do raster sintético carrega bandas + georreferência. No Python usamos `rasterio` ou `osgeo.gdal`; o Canty ilustra com GDAL.

Se algo disso for novo, não trave: as seções seguintes constroem o vocabulário com o raster sintético na mão.

## 2. Intuição do problema (sem equação)

Imagine que você abre `exemplo_sintetico.tif` e “vê” uma paisagem. Por baixo, o computador só tem uma pilha de números. Cada banda é uma fotografia em tons de cinza da mesma área, mas em uma fatia diferente do espectro. A vegetação brilha no infravermelho próximo e absorve no vermelho; a água absorve quase tudo no NIR; o solo se comporta de outro jeito. Por isso **a mesma posição geográfica** tem vários números — um por banda.

Há duas maneiras de olhar esses números:

- **Olhar espacial:** “esta banda é uma imagem 2D; quero ver a cena.”
- **Olhar espectral:** “neste pixel, o conjunto de bandas é a assinatura do alvo.”

Quase todo o livro (classificação, PCA, detecção de mudança) vive no segundo olhar: o pixel vira um ponto (vetor) num espaço de $N$ dimensões. O Capítulo 1 fixa essa representação e o ferramental mínimo para manipulá-la — inclusive a ideia de que bandas vizinhas costumam ser redundantes (variam juntas), o que a covariância e a PCA vão explorar.

Há ainda o contraste entre **ver** e **medir**. Esticar os valores da banda 1 para o intervalo $[0,1]$ deixa o `imshow` legível. Isso não transforma DN em reflectância. Confundir os dois é um erro clássico no início.

Por fim, sensores **ativos** (radar) não dependem do Sol: o satélite emite micro-ondas e registra o retorno. O brilho do pixel conta outra história (rugosidade, umidade, geometria), mas a estrutura de dados — array multibanda / multipolarização, pixel como vetor — é a mesma. Por isso Sentinel-1 VV/VH em Cuiabá entra neste capítulo como ponte, não como desvio.

## 3. O que o Canty ensina neste capítulo (mapa das seções + ideias-chave)

| Bloco do Cap. 1 (ideia) | Ideia-chave |
|-------------------------|-------------|
| Imagens como arrays | $g_k(i,j)$: banda $k$, linha $i$, coluna $j$ |
| Pixel como vetor | $\mathbf{g}(i,j)\in\mathbb{R}^N$ — base da análise multivariada |
| Armazenamento | BSQ, BIL, BIP — ordem dos bytes no disco/memória |
| Algebra linear útil | Produto, inversa, autovalores; ponte ao Apêndice A |
| Extremos e stretch | Min/max por banda; normalização para exibição |
| PCA introdutória | Diagonalizar a covariância; Exercício 1.2 no livro |

Ideias que você deve sair carregando:

1. **Uma imagem multiespectral é um cubo** (ou um stack de matrizes), não um RGB “mágico”.
2. **O objeto de análise quantitativa costuma ser o vetor de pixel**, não a “foto”.
3. **Formato de arquivo ≠ layout mental.** GDAL/rasterio abstraem BSQ/BIL/BIP; no NumPy você escolhe o eixo das bandas.
4. **Álgebra linear não é enfeite:** covariância e autodecomposição já aparecem no Cap. 1 e dominam o Cap. 3.
5. **Stretch min–max é cosmética controlada**, não calibração.

## 4. Desenvolvimento guiado (conceitos do livro, com derivação/explicação acessível)

### 4.1 Sensores passivos e ativos

**Passivos.** O sensor não ilumina a cena: mede radiação solar refletida ou emissão térmica da superfície. Landsat, Sentinel-2, CBERS, raster sintético (parte óptica) entram aqui. Limitação óbvia: nuvens e noite (no óptico).

**Ativos.** O sensor emite energia e mede o retorno. SAR (micro-ondas) e LiDAR (laser) são os exemplos centrais. Sentinel-1 opera em banda C, com polarizações como VV e VH. Vantagem: imageamento com nuvens e à noite. O preço: interpretação diferente (espalhamento, speckle) — detalhada em [SAR.md](../../radar-sar/aulas/01-introducao.md).

| | Multiespectral (passivo) | SAR (ativo) |
|--|--------------------------|-------------|
| Fonte | Sol / emissão térmica | Pulso do próprio radar |
| “Bandas” | Intervalos de $\lambda$ | Frequência + polarização |
| Nuvens | Bloqueiam (óptico) | Em geral atravessam |
| Pixel brilhante | Alta reflectância/emissão naquela banda | Muito retroespalhamento |

### 4.2 Imagem multiespectral como array

O livro formaliza a imagem como

$$
g_k(i,j),\qquad k=1,\ldots,N,\quad i=1,\ldots,n_{\mathrm{lin}},\quad j=1,\ldots,n_{\mathrm{col}}.
$$

No raster sintético deste repositório, $N$ é o número de bandas do GeoTIFF; $n_{\mathrm{lin}}$ e $n_{\mathrm{col}}$ são as dimensões espaciais. Em NumPy, após `rasterio.open(...).read()` ou o loop GDAL do `ex01_1.py`, o layout convencional neste projeto é:

```text
image.shape == (bands, rows, cols)
```

Assim, `image[0]` é a primeira banda (matriz 2D); `image[:, i, j]` é o vetor espectral do pixel na linha $i$, coluna $j`.

**Cuidado com eixos.** Algumas bibliotecas usam `(rows, cols, bands)` (estilo “imagem HWC”). Sempre confira `shape` e a documentação do leitor. Misturar os dois sem converter quebra covariância, PCA e classificação.

### 4.3 Pixel como vetor

Na posição $(i,j)$,

```math
\mathbf{g}(i,j)=\begin{pmatrix}g_1(i,j)\\ g_2(i,j)\\ \vdots\\ g_N(i,j)\end{pmatrix}\in\mathbb{R}^N.
```

Intuição: cada eixo do $\mathbb{R}^N$ é uma banda. Dois pixels de vegetação densa tendem a ficar próximos nesse espaço; água e solo ocupam outras regiões. Classificadores (Caps. 6–8) estimam nuvens de pontos por classe nesse espaço. PCA (Caps. 1 e 3) gira os eixos para alinhar com as direções de maior variância.

No código do `ex01_2.py`, todos os pixels são empilhados numa matriz de dados centrada:

$$
G\in\mathbb{R}^{m\times N},\qquad m=n_{\mathrm{lin}}\cdot n_{\mathrm{col}},
$$

onde cada linha é um pixel (média da banda já subtraída). Isso é só o cubo “achatado” no espaço — passo padrão antes de covariância.

### 4.4 BSQ, BIL e BIP

No disco, os mesmos números podem estar ordenados de três jeitos clássicos:

| Formato | Ordem (ideia) | Analogia |
|---------|---------------|----------|
| **BSQ** (*Band Sequential*) | Banda 1 inteira, depois banda 2, … | Pilha de mapas completos |
| **BIL** (*Band Interleaved by Line*) | Linha 1 de todas as bandas, linha 2 de todas, … | Intercala por linha |
| **BIP** (*Band Interleaved by Pixel*) | Pixel $(i,j)$ com todas as bandas juntas, depois o próximo pixel | Vetor espectral contíguo |

Por que importa? Performance de leitura e compatibilidade com software legado. Para o estudante: **GDAL/rasterio escondem o formato**; o que importa é o array que você monta. O Canty menciona os três para você não se surpreender com documentação de sensores antigos.

### 4.5 Álgebra linear mínima para PCA (nível introdutório)

#### Produto matricial

Se $A$ é $p\times q$ e $B$ é $q\times r$, o produto $AB$ tem entradas

$$
(AB)_{ik}=\sum_{j=1}^{q} A_{ij}B_{jk}.
$$

No Cap. 1, o uso mais frequente é: dados centrados $G$ ($m\times N$) e matriz de pesos $U$ ($N\times N$) → projeção $GU$ (pixels nas novas coordenadas).

#### Covariância (intuição; formalismo no Cap. 2)

Com pixels centrados (média zero por banda), a covariância amostral $N\times N$ é

$$
C=\frac{1}{m-1}G^\top G.
$$

- Diagonal $C_{kk}$: variância da banda $k$ (quanto a banda “oscila” na cena).
- Fora da diagonal $C_{k\ell}$: se as bandas $k$ e $\ell$ sobem e descem juntas ($>0$) ou em sentidos opostos ($<0$).

Bandas ópticas vizinhas quase sempre têm $C_{k\ell}$ grande → **redundância**. A PCA remove essa correlação linear.

#### Autovalores e autovetores (só o necessário)

Resolvemos

$$
C\mathbf{v}=\lambda\mathbf{v}.
$$

- $\mathbf{v}$: direção no espaço das bandas (combinação linear das bandas originais).
- $\lambda$: variância ao longo dessa direção.

Ordenamos $\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_N$. A primeira direção captura o máximo de variância; a segunda, o máximo sob a restrição de ser ortogonal à primeira; e assim por diante. Em NumPy: `np.linalg.eigh(C)` (matriz simétrica) e `argsort` decrescente — exatamente o fluxo do `ex01_2.py`.

Ortogonalidade dos autovetores (para $C$ simétrica):

$$
U^\top U=I,
$$

ou seja, as componentes principais são linearmente não correlacionadas (na amostra, sob o modelo da PCA).

**Leitura física (exemplo esquemático).** Se um autovetor tem pesos grandes e de sinais opostos em vermelho e NIR, a componente correspondente se parece com um contraste de vegetação. Se todos os pesos têm o mesmo sinal, a componente se parece com “brilho geral”. Interpretação fina depende da cena e das bandas; o ponto didático é: **os coeficientes do autovetor são pesos das bandas originais**.

### 4.6 Mínimo, máximo e stretch

Para uma banda $g$ (matriz 2D),

$$
g_{\min}=\min_{i,j} g(i,j),\qquad g_{\max}=\max_{i,j} g(i,j).
$$

O stretch linear para $[0,1]$ (como no `ex01_1.py`) é

$$
g'=\frac{g-g_{\min}}{g_{\max}-g_{\min}}.
$$

Para exibir em 8 bits:

$$
g_{8}=\left\lfloor 255\cdot g'\right\rfloor.
$$

**O que isso faz bem:** usa toda a faixa dinâmica do display; revela contraste que o olho não via em uma banda “escura”.

**O que isso não faz:** não remove atmosfera, não converte DN em reflectância, não equaliza histogramas entre datas. Outliers (um pixel saturado) podem “achatar” o restante da cena — daí, na prática moderna, muita gente usa percentis (2%–98%) em vez do min/max absolutos.

**Perda de qualidade?** A transformação linear em si preserva ordem e razões relativas. A perda aparece se você quantizar para `uint8` e jogar fora o float original. Para análise, mantenha `float64`/`float32`; use 8 bits só para PNG de visualização. Com `NaN`/máscaras, use `np.nanmin` / `np.nanmax`.

### 4.7 Calibração radiométrica (contraste com o stretch)

Calibração (resumo conceitual):

```math
L = g\cdot a + b
\quad\text{ou}\quad
\rho = f(\mathrm{DN},\,\text{ângulo solar},\,\text{atmosfera},\,\ldots)
```

dependendo do produto (radiância $L$, reflectância $\rho$, etc.). É um modelo físico/sensor. O stretch min–max é uma mudança de escala **ad hoc** para o monitor. No mestrado e em séries temporais, misturar os dois gera artefatos: você acha que detectou mudança quando só mudou o contraste da visualização.

### 4.8 Do cubo à PCA em poucas linhas (o que o Exercício 1.2 faz)

1. Ler bandas → `image` com shape `(N, rows, cols)`.
2. Achatar e centrar → $G$ ($m\times N$).
3. $C=G^\top G/(m-1)$.
4. Autodecomposição; ordenar; projetar $P=GU$.
5. Remoldar para `(rows, cols, N)` (ou `(N, rows, cols)`) e gravar GeoTIFF.

Isso é o Cap. 1 “fechando o ciclo”: representação → álgebra → produto derivado. O Cap. 3 aprofunda scree, erro de reconstrução e MNF.

### 4.9 SVD e a ligação com a PCA

Para $m\ge N$ (caso de imagem: muito mais pixels que bandas), a matriz centrada $G$ ($m\times N$) pode ser escrita como

$$
G = W S V^\top,
$$

com $W$ ($m\times N$) de colunas ortonormais, $S$ diagonal com os valores singulares $s_1\ge s_2\ge\cdots\ge s_N\ge 0$, e $V$ ($N\times N$) ortogonal. Essa é a decomposição em valores singulares (SVD), na forma reduzida.

Ligação com a covariância. Substituindo na definição de $C$:

$$
C=\frac{1}{m-1}G^\top G=\frac{1}{m-1}V S^2 V^\top.
$$

Logo as colunas de $V$ são autovetores de $C$ e

$$
\lambda_k=\frac{s_k^2}{m-1}.
$$

As componentes principais saem direto: $P = GV = WS$.

Comparação com a matriz $U$ de autovetores da seção 4.5:

- Se os autovalores são distintos, cada autovetor é único a menos do sinal. Então $V$ e $U$ podem diferir por $\pm 1$ em cada coluna. Fixar uma convenção (por exemplo, a maior componente em módulo positiva) torna a comparação direta.
- Se há autovalores repetidos, a liberdade é maior: qualquer base ortonormal do autoespaço serve. $V$ e $U$ podem diferir por uma rotação dentro desse autoespaço, e o que se compara é o autoespaço (o projetor), não cada coluna.

Na prática, a SVD evita formar $G^\top G$ e é numericamente mais estável. O `sklearn` oferece os dois caminhos e o parâmetro `svd_solver` decide. Desde a versão 1.5, com `svd_solver="auto"` e muito mais amostras que variáveis (o caso de imagem), ele usa a autodecomposição da covariância (`covariance_eigh`).

Implementação própria e verificação numérica em `notebooks/01_pca_propria.ipynb`. Se a SVD fica aqui ou no Apêndice A é uma das perguntas em [duvidas_orientador.md](duvidas_orientador.md).

## 5. Além do livro (prática moderna, armadilhas, ligação com sklearn/GEE/SAR/mestrado)

**rasterio vs GDAL.** O livro é GDAL-centrico. Hoje `rasterio` é mais idiomático em Python; o notebook tenta os dois. O contrato mental é o mesmo: array + perfil geográfico.

**sklearn.** `sklearn.decomposition.PCA` faz a mesma geometria (com detalhes de API: `fit` em matriz $m\times N$). Entender $C\mathbf{v}=\lambda\mathbf{v}$ evita tratar PCA como caixa-preta.

**Google Earth Engine.** Em GEE, `Image` também é um stack de bandas; `ee.Image.principalComponents` existe, mas o custo e a amostragem (região vs imagem inteira) mudam. O conceito de pixel-vetor é idêntico.

**SAR / mestrado.** Produtos Sentinel-1 em Cuiabá (`figuras/cuiaba_sentinel1_2025_VV.png`, `..._VH.png`) mostram duas “bandas” de polarização. Trate VV e VH como eixos do vetor $\mathbf{g}$; estatística (Cap. 2) e transformações (Cap. 3) se aplicam, com o caveat do **speckle** (ruído multiplicativo) — não ignore ao copiar receitas ópticas.

**Armadilhas frequentes**

- Assumir que banda 1 do arquivo = “azul” sem ler metadados.
- Fazer PCA sem centrar (ou sem padronizar quando as escalas diferem muito).
- Usar stretch min–max em composição RGB e achar que a cor é comparável entre datas.
- Esquecer máscara de nuvem / no-data e contaminar min, max e covariância.
- Misturar `(bands, rows, cols)` com `(rows, cols, bands)` no meio do pipeline.

## 6. Como praticar neste repositório (notebook + exercícios + outputs)

**Dado central:** `data/exemplos/exemplo_sintetico.tif`.

**Notebook:** `notebooks/01_teoria.ipynb` — leitura do raster sintético, visualização de bandas, discussão de shape e stretch. Rode a partir de `notebooks/`.

**Implementação própria:** `notebooks/01_pca_propria.ipynb`. PCA e SVD do zero com NumPy numa imagem sintética 3x50x50. Não depende de dado externo.

**Dúvidas em aberto:** [duvidas_orientador.md](duvidas_orientador.md).

**Exercícios**

```bash
python conteudo/fundamentos/exercicios/ex01_1.py data/exemplos/exemplo_sintetico.tif 1
python conteudo/fundamentos/exercicios/ex01_2.py data/exemplos/exemplo_sintetico.tif conteudo/fundamentos/figuras/aster_pca.tif
```

`figuras/aster_pca.tif` é gerado localmente e não é versionado (`.gitignore` ignora `conteudo/**/figuras/*.tif`).

- `ex01_1.py`: abre o GeoTIFF, monta `(bands, rows, cols)`, aplica min–max na banda pedida e exibe.
- `ex01_2.py`: PCA completa e grava GeoTIFF das componentes.

**Outputs de referência:** `figuras/aster_band_*_stretch.png`, `grid_bandas.png`, `aster_rgb_falsecolor.png`, e os pares Sentinel-1 Cuiabá VV/VH. Use-os para checar se o que você gera “parece” a mesma família visual (não precisa ser bit-a-bit idêntico se o backend de plot diferir).

**Leitura satélite:** [SAR.md](../../radar-sar/aulas/01-introducao.md) — espalhamento, abertura sintética, bandas de frequência e polarização.

## 7. Checklist de domínio + dúvidas típicas

**Checklist**

- [ ] Explico passivo vs ativo com um exemplo de satélite cada.
- [ ] Escrevo $g_k(i,j)$ e $\mathbf{g}(i,j)$ sem consultar o livro.
- [ ] Sei o `shape` do array neste repo e como pegar uma banda vs um pixel.
- [ ] Distingo BSQ/BIL/BIP em uma frase cada.
- [ ] Relaciono $C=G^\top G/(m-1)$ com “bandas que variam juntas”.
- [ ] Digo o que $\lambda$ e $\mathbf{v}$ significam na PCA introdutória.
- [ ] Aplico stretch min–max e digo por que não é calibração.
- [ ] Sei o que `ex01_1` e `ex01_2` fazem e onde está o raster sintético.

**Dúvidas típicas**

1. *“Por que o pixel é um vetor se a imagem é 2D?”*  
   A imagem é 2D no espaço; em cada célula há $N$ medidas. O vetor vive no espaço **espectral**, não no mapa.

2. *“Posso fazer PCA em RGB de 8 bits baixado da internet?”*  
   Pode, como exercício numérico. Para ciência, prefira produtos calibrados e bandas com significado espectral conhecido.

3. *“Min–max por banda ou global?”*  
   Para visualizar uma banda sozinha: por banda. Para RGB falso-color: em geral min–max (ou percentis) **por banda** usada no R, G e B do display.

4. *“SAR também tem ‘bandas’?”*  
   Sim, no sentido de canais (frequência/polarização). O mecanismo físico muda; a estrutura de array, não. Ver [SAR.md](../../radar-sar/aulas/01-introducao.md).

5. *“Preciso decorar BSQ?”*  
   Não. Precisa reconhecer o termo e saber que o NumPy `shape` é o contrato do seu código.

6. *“Onde a covariância volta?”*  
   Cap. 2 (estimativa formal, histograma, correlação) e Cap. 3 (PCA/MNF com scree e erro de reconstrução).
