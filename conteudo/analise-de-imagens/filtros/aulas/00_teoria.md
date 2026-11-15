# Capítulo 4 — Filtros, kernels e campos

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../../data/README.md).

> Referência: Morton J. Canty, *Image Analysis, Classification and Change Detection in Remote Sensing* (4ª ed., 2019), Cap. 4 — *Filters, Kernels and Fields*.  
> Dado padrão neste repositório: `data/exemplos/exemplo_sintetico.tif`.

---

## 0. Para quem é este guia / o que você vai saber ao final

Este texto é para quem já abriu uma banda raster sintético como array NumPy (Caps. 1–2), entende histograma e covariância espectral, e quer passar da ideia de “pixel isolado” para **vizinhança espacial**.

Ao terminar, você deve conseguir:

1. Explicar, com suas palavras, o que é uma **convolução discreta**: soma ponderada local que desliza sobre a imagem.
2. Distinguir filtros de **suavização** (média, Gaussiano, mediana) de filtros de **borda** (Sobel, Laplaciano) e dizer quando usar cada um.
3. Justificar por que, em muitos fluxos, filtramos **antes** de classificar — e também por que filtrar demais apaga informação útil.
4. Separar ruído óptico “aditivo / alta frequência” de **speckle** SAR (multiplicativo) e não aplicar o mesmo filtro cegamente nos dois.
5. Formular a intuição de **campo aleatório** / dependência espacial (MRF “leve”): pixels vizinhos não são amostras i.i.d.
6. Rodar `ex04_1.py` e `ex04_2.py`, ler os PNGs em `figuras/` e relacionar o que aparece na tela com o kernel escolhido.

Não é preciso memorizar todas as máscaras $3\times 3$ de cabeça. O que importa é o mecanismo (vizinhança + pesos) e o efeito visual/estatístico.

---

## 1. Pré-requisitos (o que o livro assume e quase não explica)

O Cap. 4 do Canty entra rápido em kernels e, depois, em linguagem de campos. O livro pressupõe coisas que, na prática, muita gente ainda está consolidando:

**Do Cap. 1**

- Imagem = array; banda = matriz $g(i,j)$; pixel multiespectral = vetor.
- Bordas do array: ao filtrar, a janela “sai” da imagem — precisa de estratégia (reflexão, constante, corte). Bibliotecas fazem isso por você; o conceito não some.

**Do Cap. 2**

- Média e variância **locais** (numa janela) são as mesmas ideias da média/variância global, só que restritas a vizinhos.
- Histograma: filtrar muda a distribuição dos valores (suavização estreita picos de ruído; equalização no Cap. 5 faz outra coisa).

**Matemática mínima**

- Soma dupla $\sum_k\sum_l$ e índice de janela centrada em $(i,j)$.
- Gradiente e segunda derivada em 1D (derivada aproxima diferença; segunda derivada aproxima curvatura) — o Sobel/Laplaciano são versões 2D discretas disso.
- Distribuição Gaussiana 1D/2D só como “peso que cai com a distância”; não precisa da demonstração completa.

**Python útil**

- `numpy` slicing e broadcasting.
- `scipy.ndimage` (`uniform_filter`, `gaussian_filter`, `median_filter`, `sobel`, `laplace`) ou OpenCV equivalente.
- Backend `Agg` do Matplotlib se for gravar PNG sem GUI (como nos exercícios deste repo).

Se “kernel” ainda soa abstrato, pense em **máscara** ou **janela com pesos**. É a mesma ideia.

---

## 2. Intuição do problema (sem equação)

Uma cena de satélite não é um saco de pixels independentes. Um lago, uma floresta ou um bairro ocupam **regiões**. O valor em um pixel costuma se parecer com o dos vizinhos — até encontrar uma margem (rio, estrada, limite de talhão).

Três problemas práticos aparecem o tempo todo:

1. **Ruído e granulação.** Em óptico, flutuações de sensor, atmosfera residual ou compressão geram variação de alta frequência que atrapalha limiares e classificadores. Em SAR, o *speckle* é pior e de natureza diferente (veja §5).
2. **Bordas e estruturas.** Às vezes o que você quer não é a reflectância média, e sim *onde* a imagem muda: limites de uso do solo, drenagem, feições lineares.
3. **Contexto para classificação.** Classificar pixel a pixel como se cada um viesse de uma urna separada ignora o óbvio: a classe “água” tende a vir em manchas. Filtros (e, mais tarde, modelos de Markov) são formas de colocar o espaço no processamento.

A operação central do capítulo é simples de imaginar: escolha um pixel; olhe uma vizinhança $3\times 3$, $5\times 5$, etc.; combine os valores com **pesos**; escreva o resultado no centro; deslize para o próximo pixel. Isso é filtragem por kernel. Se os pesos forem todos iguais e positivos que somam 1, você está fazendo uma média local. Se os pesos forem derivados de uma Gaussiana, a média é “mais macia” no centro. Se, em vez de média, você pegar a **mediana** dos vizinhos, remove outliers sem ser uma soma linear. Se os pesos forem diferenças esquerda/direita e cima/baixo, você está estimando um **gradiente** — ou seja, caçando bordas.

Por que filtrar antes de classificar? Porque ruído local cria pixels “falsos” de outra classe no meio de uma região homogênea. Uma suavização leve reduz esses salpicos. O preço: bordas verdadeiras também amolecem; texturas finas somem; classes estreitas (estradas de 1 pixel) podem desaparecer. Filtrar não é ritual obrigatório — é trade-off.

Campos aleatórios entram na conversa quando você pergunta *por que* a vizinhança importa estatisticamente. Não só “porque o filtro usa vizinhos”, mas porque o processo espacial que gerou a cena tem correlação: $X_{i,j}$ e $X_{i,j+1}$ não são independentes. Filtros são regras determinísticas sobre a vizinhança; campos aleatórios são o modelo probabilístico por trás dessa dependência. No Cap. 4 basta a intuição; MRFs voltam com mais força em classificação contextual.

---

## 3. O que o Canty ensina neste capítulo (mapa das seções + ideias-chave)

O Cap. 4 do livro organiza, em linhas gerais, o seguinte arco (nomes de seção podem variar levemente conforme a edição; o mapa abaixo é o de ideias):

| Bloco no Canty | Ideia-chave | O que ficar |
|----------------|-------------|-------------|
| Convolução / kernels | Operação linear local por máscara | Fórmula da soma ponderada; propriedade de separabilidade quando o kernel permite |
| Suavização | Reduzir alta frequência | Média (box), Gaussiano ($\sigma$), mediana (não linear) |
| Detecção de bordas | Gradiente e curvatura | Sobel ($G_x$, $G_y$, magnitude); Laplaciano; menção a LoG |
| Campos / dependência espacial | Imagem como processo espacial | Vizinhança, correlação espacial, ponte para Markov |
| Ligação com o restante do livro | Pré-processamento | Filtrar alimenta realce (Cap. 5), classificação e detecção de mudança |

Ideias que o Canty quer que você leve adiante:

- **Kernel** define a escala e o tipo de operação (suave vs derivativo).
- Convolução linear é a ferramenta algébrica; mediana mostra que nem todo filtro útil é linear.
- Estrutura espacial não é detalhe cosmético: é parte do sinal.
- Em SAR e em pós-processamento de mapas, a mesma lógica de vizinhança reaparece com estatística adaptativa ou MRF — o capítulo abre a porta.

Neste repositório, o núcleo operacional está em `ex04_1` (suavização) e `ex04_2` (Sobel/Laplaciano), com visualizações já gravadas em `figuras/`.

---

## 4. Desenvolvimento guiado (conceitos do livro, com explicação acessível)

### 4.1 Convolução discreta como soma ponderada local

Seja $g(i,j)$ a imagem (uma banda) e $w(k,l)$ um kernel de tamanho $(2a+1)\times(2b+1)$. A convolução discreta (na forma usual em processamento de imagem) é

```math
(g * w)(i,j)
=
\sum_{k=-a}^{a}
\sum_{l=-b}^{b}
w(k,l)\, g(i-k,\, j-l).
```

Leitura linha a linha: no pixel $(i,j)$, você multiplica cada vizinho pelo peso correspondente e soma. O resultado substitui (ou forma uma nova imagem em) $(i,j)$.

Observações práticas:

- Em SciPy/OpenCV a convenção de índice e de “flip” do kernel pode diferir da fórmula de livro; para kernels **simétricos** (média, Gaussiano) isso raramente muda o resultado de forma perceptível. Para kernels assimétricos de derivada, confira a documentação da função que você chama.
- Na borda, a janela incompleta exige *padding* (reflexão costuma ser razoável em imagens de SR).
- Se $w$ for **separável** ($`w = u\, v^\top`$), a convolução 2D vira duas 1D — mais barata. O Gaussiano clássico é separável.

Em código mental: `out[i,j] = sum(W * g[i-a:i+a+1, j-b:j+b+1])`.

### 4.2 Filtro da média (box)

Kernel uniforme $3\times 3$:

```math
w = \frac{1}{9}
\begin{bmatrix}
1 & 1 & 1 \\
1 & 1 & 1 \\
1 & 1 & 1
\end{bmatrix}.
```

Cada pixel vira a média dos nove. Efeito: reduz ruído aditivo de alta frequência; **borra** bordas e detalhes. Janela maior ($5\times 5$, $7\times 7$) suaviza mais e borra mais. No `ex04_1.py`, isso é `ndimage.uniform_filter`.

Use como primeiro experimento exploratório em óptico. Não espere milagre em SAR.

### 4.3 Filtro Gaussiano

Os pesos decrescem com a distância ao centro, tipicamente

```math
w(k,l)
\propto
\exp\!\left(-\frac{k^2+l^2}{2\sigma^2}\right),
```

depois normalizados para somar 1. O parâmetro $\sigma$ controla a **escala espacial**: $\sigma$ pequeno ≈ pouca suavização; $\sigma$ grande ≈ blur forte. Em relação à média, o Gaussiano costuma parecer menos “em bloco” e preserva um pouco melhor estruturas suaves.

No exercício: `ndimage.gaussian_filter(band, sigma=...)`. Compare visualmente com a média na mesma cena raster sintético: a diferença é sutil em $\sigma$ pequeno e óbvia quando você exagera.

### 4.4 Mediana (filtro não linear)

Na janela, ordene os valores e pegue o do meio. **Não** é convolução linear: não existe um $w$ fixo que reproduza a mediana para qualquer entrada.

Comportamento típico:

- Remove bem *salt-and-pepper* e outliers isolados.
- Preserva bordas **melhor** que a média, em muitos casos.
- Custa mais (ordenar); texturas finas podem sumir; em regiões com poucos níveis distintos, pode criar “plateaus”.

No `ex04_1.py`: `ndimage.median_filter`. Vale olhar o trio média / Gauss / mediana no PNG `figuras/filtros_suavizacao.png`.

### 4.5 Sobel — gradiente discreto

Kernels clássicos $3\times 3$:

```math
G_x =
\begin{bmatrix}
-1 & 0 & 1 \\
-2 & 0 & 2 \\
-1 & 0 & 1
\end{bmatrix},
\quad
G_y =
\begin{bmatrix}
-1 & -2 & -1 \\
0 & 0 & 0 \\
1 & 2 & 1
\end{bmatrix}.
```

$G_x$ responde a mudanças na direção horizontal da imagem (variação em $x$); $G_y$, na vertical. A **magnitude**

$$
|G| = \sqrt{G_x^2 + G_y^2}
$$

(ou a aproximação $|G_x|+|G_y|$) destaca transições: margens de água, estradas, limites de cultivo. O ângulo $\operatorname{atan2}(G_y,G_x)$ dá a orientação da borda, útil em pipelines mais avançados (Canny no Cap. 5).

Sobel já embute um pouco de suavização na direção perpendicular à derivada (pesos 1–2–1), o que o torna um pouco menos sensível a ruído que diferenças puras $[-1,1]$.

No `ex04_2.py`: `ndimage.sobel` nos dois eixos + `np.hypot`. Resultado em `figuras/bordas_sobel_laplacian.png`.

### 4.6 Laplaciano — segunda derivada

Um kernel comum:

```math
\nabla^2 \approx
\begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix}
\quad
\text{(ou variantes $3\times 3$ com cantos).}
```

Responde a curvatura / mudanças bruscas em qualquer direção. É **sensível a ruído**: qualquer granulação vira “borda”. Por isso frequentemente se faz Gaussiano + Laplaciano (*Laplacian of Gaussian*, LoG): suaviza na escala $\sigma$ e depois deriva.

No exercício: `ndimage.laplace` em valor absoluto para visualização.

### 4.7 Por que filtrar antes da classificação (e quando não filtrar)

Fluxo típico em óptico:

1. Calibrar / corrigir o que for necessário (Cap. 5 — cuidado: stretch ≠ calibração).
2. Opcionalmente suavizar bandas ou componentes (PCA) para reduzir salpico.
3. Extrair atributos e classificar (Caps. 6–8).

A suavização reduz a variância dentro de classes homogêneas e diminui pixels isolados mal rotulados. Mas:

- Classes com geometria fina sofrem.
- Diferenças espectrais sutis podem ser diluídas se a janela misturar duas classes na borda (pixel misto piorado).
- Em detecção de mudança, filtrar demais pode apagar mudanças reais pequenas.

Regra prática de estudo: rode a classificação (mais tarde) **com e sem** filtro leve e compare matriz de confusão e aspecto espacial do mapa — não acredite só no “antes fica mais bonito”.

### 4.8 Speckle vs ruído óptico (intuição)

| | Óptico (ex.: raster sintético VNIR) | SAR |
|--|--------------------------|-----|
| Natureza típica do “grain” | Muitas vezes modelado como aditivo / alta frequência | **Speckle** multiplicativo (interferência coerente) |
| Filtro box/Gauss | Às vezes aceitável com parcimônia | Em geral inadequado como primeira escolha |
| O que preservar | Bordas e textura espectral | Bordas + estatística local (ENL) |
| Neste repo | `ex04_*` no raster sintético | `legado/canty/auxil/scripts/gamma_filter.py`, `mmse_filter.py` |

Speckle: o retorno observado é aproximadamente sinal × ruído (em intensidade). Média aritmética em janela fixa reduz speckle, mas borra forte. Filtros adaptativos (Lee, Frost, Gamma MAP, MMSE) estimam média/variância locais e suavizam mais onde a região parece homogênea. O Cap. 4 dá a linguagem de janela; o tratamento sério de SAR fica no “além” e no `legado/canty/auxil/`.

### 4.9 Campos aleatórios e dependência espacial (MRF leve)

Associe a cada sítio $(i,j)$ uma variável aleatória $X_{i,j}$ (valor de DN, reflectância, ou rótulo de classe). O conjunto $`\{X_{i,j}\}`$ é um **campo aleatório**. O que importa:

- **Correlação espacial:** $\mathrm{Corr}(X_{i,j}, X_{i,j+1})$ costuma ser alta no sinal; ruído branco espacial quebra isso.
- **Vizinhança** $\mathcal{N}(i,j)$: 4-vizinhos, 8-vizinhos, ou janela maior — quem “fala” com quem.
- **Markov (ideia):** $P(X_{i,j} \mid \text{todo o resto})$ depende só dos vizinhos. Isso é a ponte para *Markov Random Fields* usados em regularização de mapas classificados.

Kernels de convolução são regras locais determinísticas sobre uma vizinhança. O campo aleatório pergunta pela lei probabilística dessa dependência. Você não precisa, neste ponto, escrever a energia de Gibbs; precisa internalizar: **espaço importa**, e ignorar isso é uma modelagem i.i.d. conveniente, mas incompleta.

Nos Caps. 6–9, a mesma intuição reaparece: amostras de treino espacialmente agrupadas enviesam validação; pós-processamento contextual limpa mapas; mudança isolada de 1 pixel muitas vezes é ruído.

---

## 5. Além do livro (prática moderna, armadilhas, ligação com o mestrado)

**Bibliotecas.** Além de `scipy.ndimage`, OpenCV (`cv2.filter2D`, `GaussianBlur`, `medianBlur`, `Sobel`, `Laplacian`) e scikit-image (`skimage.filters`) são equivalentes didáticos. Em Google Earth Engine, `focal_mean`, `focal_median`, `convolve` com kernel explícito fazem o mesmo papel em escala planetária — a intuição de janela é idêntica.

**Armadilhas**

- Aplicar stretch visual agressivo **antes** de filtrar e achar que “melhorou o dado”: você pode ter saturado e criado bordas falsas.
- Usar mediana $15\times 15$ “porque ficou limpo” e depois tentar medir textura fina.
- Tratar Speckle como Gaussiano aditivo.
- Filtrar cada banda com $\sigma$ diferente sem motivo e depois calcular índices espectrais — o índice herda escalas espaciais misturadas.

**Ligação mestrado / SAR.** O caminho natural neste repo: Cap. 4 (kernels no raster sintético) → `legado/canty/auxil/scripts/gamma_filter.py` e `mmse_filter.py` → cena Sentinel-1 (ponte Cuiabá / notas SAR do Cap. 1). Em séries temporais, filtragem espacial e temporal interagem: excesso de suavização espacial pode mascarar mudança real.

**Deep learning.** CNNs são, em essência, pilhas de filtros aprendidos. Entender convolução clássica torna menos mágico o que a rede faz nas primeiras camadas. Isso não substitui o Cap. 4; ancora.

**MRF / CRF modernos.** Regularização de mapas com potenciais de vizinhança, fully connected CRFs, ou pós-processamento morfológico — todos exploram a mesma hipótese de coerência espacial que o Canty introduz aqui.

---

## 6. Como praticar neste repositório (notebook + exercícios + outputs)

**Dado**

```text
data/exemplos/exemplo_sintetico.tif
```

(os scripts já apontam para esse caminho por padrão.)

**Exercícios**

| Script | O que faz | Saída |
|--------|-----------|--------|
| `exercicios/ex04_1.py` | Média, Gaussiano e mediana numa banda | `figuras/filtros_suavizacao.png` |
| `exercicios/ex04_2.py` | Magnitude Sobel e \|Laplaciano\| | `figuras/bordas_sobel_laplacian.png` |

Comandos típicos (a partir de `conteudo/analise-de-imagens/filtros/`):

```bash
python exercicios/ex04_1.py
python exercicios/ex04_1.py -b 2 --size 7 --sigma 2.0

python exercicios/ex04_2.py
python exercicios/ex04_2.py ../../data/exemplos/exemplo_sintetico.tif -b 1
```

**Notebook**

- `notebooks/04_teoria.ipynb` — intuição, soma de convolução e visualizações (`nb04_*.png` em `figuras/` se você salvar figuras).

**Roteiro sugerido de estudo (≈1–2 h)**

1. Abra `filtros_suavizacao.png` (ou rode `ex04_1`). Sem olhar o código: diga qual painel é mediana e por quê.
2. Varie `--size` e `--sigma`. Anote o que acontece com uma margem de água ou estrada.
3. Rode `ex04_2`. Compare Sobel vs Laplaciano na mesma região ruidosa: o Laplaciano “acende” mais granulação?
4. Leia de novo §4.8–4.9 e escreva em 5 linhas a diferença entre filtro e campo aleatório.
5. (Opcional) Abra `legado/canty/auxil/scripts/gamma_filter.py` só para ver que a janela local reaparece com média/variância — não precisa rodar SAR ainda.

**Dependências:** `numpy`, `matplotlib`, `scipy` (e/ou `opencv-python` no ex04_2), leitor GeoTIFF (`rasterio`, `GDAL`/`osgeo` ou `tifffile`).

---

## 7. Checklist de domínio + dúvidas típicas

### Checklist

- [ ] Consigo explicar convolução como soma ponderada local, sem copiar a fórmula de cor.
- [ ] Sei o efeito qualitativo de média vs Gaussiano vs mediana.
- [ ] Sei que Sobel ≈ gradiente e Laplaciano ≈ segunda derivada; sei que Laplaciano é mais sensível a ruído.
- [ ] Consigo argumentar a favor e contra filtrar antes de classificar.
- [ ] Não confundo speckle SAR com ruído óptico aditivo.
- [ ] Consigo dizer, em uma frase, o que é um campo aleatório espacial e por que pixels não são i.i.d.
- [ ] Rodei `ex04_1` e `ex04_2` e localizei os PNGs em `figuras/`.

### Dúvidas típicas

**“Convolução e correlação cruzada são a mesma coisa?”**  
Em muitos kernels simétricos, o resultado prático coincide. Em kernels assimétricos, a definição (com ou sem flip do kernel) importa. No estudo do Cap. 4, foque no efeito do filtro; ao implementar do zero, seja consistente com a biblioteca.

**“Qual $\sigma$ usar?”**  
Não há valor universal. Comece pequeno ($\sigma \approx 1$ em pixels), compare com a resolução espacial e com o tamanho das feições que você quer preservar. Multiescala = vários $\sigma$.

**“Mediana sempre é melhor que média?”**  
Não. Mediana é ótima contra outliers impulsivos; média/Gauss são mais baratos e suficientes para ruído “suave”. Em texturas, mediana pode apagar estrutura útil.

**“Posso filtrar a composição RGB já esticada?”**  
Para **visualização**, sim. Para **análise quantitativa** (índices, mudança, classificação com significado radiométrico), filtre as bandas na escala de trabalho correta e deixe stretch só para mostrar resultado (Cap. 5 aprofunda essa distinção).

**“MRF cai na prova / no mestrado agora?”**  
Neste capítulo: intuição de vizinhança e dependência. Formalismo de energia, amostragem e ICM/Graph cuts ficam para quando você for regularizar mapas de classe de verdade.

**“O Laplaciano do exercício parece só ruído.”**  
Provável e educativo. Suavize antes (LoG mental: rode Gauss no `ex04_1` e depois pense no Laplaciano sobre a imagem suavizada) ou compare com Sobel, que já tem um pouco de média embutida.

---

*Próximo passo natural:* Cap. 5 — realce visual vs correção física, stretch/equalização, GCPs e feições (Canny, cantos, momentos de Hu), sem confundir “ficar bonito” com “ficar calibrado”.
