# Capítulo 3 — Transformations

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../../data/README.md).

> Baseado em Canty (2019), Cap. 3 (ênfase em PCA e ponte para MNF, §3.5). Leitura principal deste capítulo no repositório.

## 0. Para quem é este guia / o que você vai saber ao final

Nos Caps. 1–2 você montou o cubo espectral, o pixel-vetor e a matriz de covariância $\mathbf{S}$. Aqui a pergunta é operacional: **como girar o espaço das bandas** para concentrar informação útil em poucas componentes e, se possível, empurrar ruído para as últimas?

Este guia assume Python/NumPy básicos e as ideias do Cap. 2 (média, $\mathbf{S}$, correlação). Não exige ter aberto o PDF: seguimos PCA passo a passo no raster sintético (`data/exemplos/exemplo_sintetico.tif`), depois contrastamos com MNF.

Ao final você deve:

- Explicar o problema das bandas correlacionadas sem jargão.
- Executar PCA do zero: centrar → $\mathbf{S}$ → autodecomposição → projeção → scree.
- Interpretar autovalores/autovetores e o gráfico de scree.
- Relacionar erro de reconstrução truncada aos autovalores descartados (eq. ~3.45 do Canty).
- Contrastear PCA (maximiza variância) com MNF (maximiza razão sinal/ruído após branquear o ruído).
- Saber quando preferir cada uma e onde estão `ex03_1`–`ex03_3`, o notebook e `legado/canty/auxil/scripts/pca.py` / `mnf.py`.

## 1. Pré-requisitos (o que o livro assume e quase não explica)

1. **Covariância amostral $\mathbf{S}$** (Cap. 2) e o fato de bandas ópticas vizinhas serem fortemente correlacionadas.
2. **Autovalores:** $A\mathbf{v}=\lambda\mathbf{v}$; para $A$ simétrica, autovetores ortogonais e $\lambda$ reais.
3. **Centrar dados:** subtrair a média de cada banda antes da PCA por covariância.
4. **Shape NumPy:** neste repo, imagens `(bands, rows, cols)`; pixels achatados em matriz $N\times m$ ou $m\times N$ (seja consistente).
5. **Ruído vs sinal (intuição):** sinal muda suavemente no espaço; ruído de sensor oscila de pixel a pixel — base da estimativa de $\mathbf{S}_N$ na MNF.

## 2. Intuição do problema (sem equação)

Abra o heatmap de correlação do Cap. 2. Se várias bandas carregam quase a mesma paisagem, guardar todas é caro e confuso: classificadores sofrem com dimensão e multicolinearidade; visualização satura de canais redundantes.

A PCA responde: *existe uma rotação do espaço espectral em que o primeiro eixo captura o máximo de variância possível, o segundo o máximo do que sobrou sem se correlacionar com o primeiro, e assim por diante?* Sim. Depois da rotação, as primeiras componentes costumam mostrar estrutura da cena (rios, blocos de vegetação, contraste solo/urbano); as últimas parecem granulação.

Há um porém: **variância não é sinônimo de informação**. Um canal muito ruidoso pode ter variância alta e dominar a PC1 “errada”. A MNF tenta corrigir isso estimando a covariância do ruído, branqueando o ruído e só então ordenando por qualidade (razão sinal/ruído). Quando o ruído é parecido em todas as bandas, PCA e MNF se parecem; quando o ruído é colorido (diferente por banda) ou fortemente correlacionado, a MNF tende a separar melhor o que é estrutural do que é artefato.

## 3. O que o Canty ensina neste capítulo (mapa das seções + ideias-chave)

| Tema | Ideia-chave |
|------|-------------|
| Motivação | Bandas correlacionadas ⇒ redundância |
| PCA | Autodecomposição de $\mathbf{S}$; componentes ortogonais por variância |
| Scree / retenção | Quantas PCs guardar? |
| Reconstrução | Truncar PCs; erro ↔ autovalores descartados (~eq. 3.45) |
| MNF (§3.5) | Estimar $\mathbf{S}_N$; branquear ruído; ordenar por SNR |
| Prática | Transformar imagem; inspecionar PC1–PC3 |

Ideias duráveis:

1. PCA = mudança de base alinhada às direções de variância de $\mathbf{S}$.
2. Autovalor = variância da componente; autovetor = pesos das bandas originais.
3. Reconstrução com $r$ PCs perde a energia das $\lambda$ descartadas.
4. MNF não substitui PCA “sempre”: exige estimativa de ruído e hipóteses espaciais.

## 4. Desenvolvimento guiado (conceitos do livro, com derivação/explicação acessível)

### 4.1 O problema das bandas correlacionadas

Se $R_{jk}\approx 1$ para vários pares, a nuvem de pixels no $\mathbb{R}^N$ é alongada: quase um “cigarro” em vez de uma bola. Coordenadas originais (bandas) são eixos diagonais a esse cigarro — ruins para comprimir e, às vezes, para classificar. Queremos eixos ao longo do cigarro (máxima variância) e transversais (variâncias menores).

### 4.2 PCA passo a passo

**Passo 1 — Organizar e centrar.**  
Seja a imagem `image` com shape $(N, n_{\mathrm{lin}}, n_{\mathrm{col}})$. Ache $m=n_{\mathrm{lin}}n_{\mathrm{col}}$ e forme

$$
G\in\mathbb{R}^{N\times m}
$$

(empilhando pixels nas colunas). Subtraia a média de cada banda:

$$
G \leftarrow G - \bar{\mathbf{g}}\mathbf{1}^\top.
$$

**Passo 2 — Covariância.**

$$
\mathbf{S}=\frac{1}{m-1}GG^\top.
$$

($\mathbf{S}$ é $N\times N$. Se você preferir pixels nas linhas, $G$ vira $m\times N$ e $\mathbf{S}=\frac{1}{m-1}G^\top G$ — equivalente.)

**Passo 3 — Autodecomposição.**

$$
\mathbf{S}\mathbf{w}=\lambda\mathbf{w}.
$$

Use `np.linalg.eigh(S)` (simétrica). Ordene $\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_N$ e alinhe as colunas de $W=[\mathbf{w}_1|\cdots|\mathbf{w}_N]$ na mesma ordem.

**Passo 4 — Projetar.**

$$
\mathbf{y}=W^\top(\mathbf{g}-\bar{\mathbf{g}}).
$$

Em forma matricial (com $G$ já centrada, bandas×pixels): $Y=W^\top G$. Remolde cada linha de $Y$ para uma imagem 2D: essas são as componentes principais.

**Passo 5 — Interpretar.**

| Objeto | Significado |
|--------|-------------|
| $\lambda_k$ | Variância da PC $k$ |
| $\mathbf{w}_k$ | Carga (loading) de cada banda na PC $k$ |
| PC1 | Em geral contraste/brilho global da cena |
| PCs médias | Contrastes espectrais (ex.: vegetação vs solo) |
| Últimas PCs | Baixa variância; frequentemente ruído e artefatos |

Os sinais dos pesos são arbitrários a menos de uma multiplicação por $-1$ (autovetor $-\mathbf{w}$ também serve): uma PC pode “inverter” o contraste sem mudar a geometria.

### 4.3 Gráfico de scree

Plote $\lambda_k$ versus $k$ (ou a fração acumulada $\sum_{i=1}^{r}\lambda_i/\sum_{i=1}^{N}\lambda_i$). Procure um “cotovelo”: depois dele, autovalores caem e se estabilizam. Regras práticas:

- Reter componentes até X% da variância total (ex.: 95%) — heurística, não lei.
- Inspecionar as imagens das PCs: se a PC $r$ ainda mostra estrutura espacial coerente, talvez mereça ficar; se só granulação, candidata a descarte.

No raster sintético deste repo, poucas primeiras PCs costumam dominar — típico de óptico com bandas correlacionadas. O notebook `03_teoria.ipynb` plota o scree e as PC1–PC3.

### 4.4 Reconstrução e erro (eq. ~3.45)

Com as $r$ primeiras componentes, $`\mathbf{y}_{1:r}=W_{:,1:r}^\top(\mathbf{g}-\bar{\mathbf{g}})`$,

```math
\hat{\mathbf{g}}=\bar{\mathbf{g}}+W_{:,1:r}\,\mathbf{y}_{1:r}.
```

O erro $\mathbf{e}=\mathbf{g}-\hat{\mathbf{g}}$ vive no subespaço das PCs descartadas. O Canty relaciona a covariância desse erro aos autovalores $\lambda_{r+1},\ldots,\lambda_N$ (fórmula ~3.45 no livro). Intuição energética:

$$
\text{variância total}=\sum_{k=1}^{N}\lambda_k,
\qquad
\text{variância retida}=\sum_{k=1}^{r}\lambda_k,
\qquad
\text{variância descartada}=\sum_{k=r+1}^{N}\lambda_k.
$$

O `ex03_1.py` compara a covariância empírica do erro de reconstrução com a previsão teórica a partir dos autovalores — exercício de sanidade: se a implementação da PCA estiver certa, os dois lados batem.

### 4.5 MNF vs PCA (intuição de branqueamento de ruído)

**PCA** maximiza variância total (sinal + ruído misturados).  
**MNF** (*Maximum Noise Fraction*) ordena componentes por razão sinal/ruído estimada.

Ingredientes:

1. $\boldsymbol{\Sigma}$ (ou $\mathbf{S}$): covariância da imagem observada (sinal + ruído).
2. $\boldsymbol{\Sigma}_N$ (ou $\mathbf{S}_N$): covariância do **ruído**.

$\boldsymbol{\Sigma}_N$ não vem de um arquivo “só ruído”. O Canty (§3.5) explora autocorrelação espacial: o sinal de pixels vizinhos é parecido; o ruído, não. Uma receita prática (implementada em `ex03_2.py`) é

$$
\mathbf{S}_N\approx\frac{1}{2}\mathrm{Cov}\bigl(\mathbf{g}(i,j)-\mathbf{g}(i-1,j)\bigr),
$$

ou seja: diferenças verticais entre vizinhos; o fator $1/2$ entra sob hipóteses de ruído i.i.d. de média zero e sinal quase constante entre vizinhos. É aproximação — útil, não milagre.

**Branqueamento de ruído (ideia).** Se você transformar os dados de modo que o ruído fique esférico (covariância identidade no espaço branqueado), maximizar variância nesse espaço fica alinhado a maximizar SNR. A MNF realiza (em espírito) essa sequência: usar $\mathbf{S}_N$ para branquear, depois decompor a covariância branqueada. Componentes finais ordenam do “mais limpo” ao “mais ruidoso”.

Esclarecimento importante (vindo das notas antigas da §3.5): $\mathbf{S}$ e $\mathbf{S}_N$ são estimados **na imagem observada** (já ruidosa). Não há necessidade de um par “antes/depois do ruído”. $\mathbf{S}$ = tudo; $\mathbf{S}_N$ = pedaço atribuído ao ruído via hipótese espacial.

### 4.6 Quando usar qual

| Situação | Preferência típica |
|----------|-------------------|
| Exploração rápida, compressão, RGB de PCs | PCA |
| Bandas com níveis de ruído muito diferentes | MNF (se $\mathbf{S}_N$ for crível) |
| Hiperespectral com ruído estruturado | MNF / variantes (NAPC, etc.) |
| Poucos pixels / cena não estacionária | Cuidado com ambas; ROI importa |
| SAR com speckle | Nenhuma das duas “crua”; pré-processar |

Regra de bolso: comece com PCA no raster sintético deste curso; use MNF quando o exercício ou o problema pedir estimativa de ruído (`ex03_2`) ou quando a PCA claramente empurrar artefato para as primeiras componentes.

## 5. Além do livro (prática moderna, armadilhas, ligação com sklearn/GEE/SAR/mestrado)

**sklearn.** `PCA(n_components=r).fit_transform(X)` com $X$ de shape $(m,N)$ — mesma geometria. `explained_variance_` ≈ autovalores. Entender $W$ evita surpresas com sinal invertido e com `whiten=True` (branqueamento de variância unitária, **não** é MNF).

**GEE.** `principalComponents` amostrando uma região: o $\mathbf{S}$ é o da amostra, não necessariamente o da imagem global. Documente a região de treino da transformação.

**auxil.** Scripts de referência do ecossistema Canty/CRC:

- `legado/canty/auxil/scripts/pca.py` — PCA em linha de comando / fluxo do livro.
- `legado/canty/auxil/scripts/mnf.py` — MNF.
- `legado/canty/auxil/scripts/kpca.py` — PCA kernel (além do Cap. 3 linear).

Os exercícios `ex03_*` deste capítulo são versões didáticas focadas no raster sintético; o `auxil` é o ferramental mais completo do pacote.

**SAR / mestrado.** PCA em VV/VH (e outras polarizações) pode condensar contraste, mas speckle é multiplicativo: log/dB e filtragem mudam $\mathbf{S}$. MNF com diferenças espaciais assume modelo de ruído que pode falhar sob speckle forte — valide visualmente.

**Armadilhas**

- Esquecer de centrar.
- Ordenar autovalores em ordem crescente (`eigh` não ordena sozinho).
- Tratar PC1 como “vegetação” sem olhar os loadings e a cena.
- Estimar $\mathbf{S}_N$ em bordas/nuvens sem máscara → ruído “espacial” falso.
- Comparar PCs entre datas sem a mesma matriz $W$ (ou sem procedimento comum) e achar mudança temática.

## 6. Como praticar neste repositório (notebook + exercícios + outputs)

**Dado:** não há cópia local obrigatória no Cap. 3; scripts apontam para

`../../data/exemplos/exemplo_sintetico.tif`.

**Notebook:** `notebooks/03_teoria.ipynb` — PCA do zero, scree, imagens PC1–PC3.

**Exercícios**

```bash
cd conteudo/analise-de-imagens/transformacoes/exercicios
python ex03_1.py              # erro de reconstrução vs fórmula (~3.45)
python ex03_2.py              # imprime estimativa de S_N
python ex03_3.py              # grava pc1.png, pc2.png, pc3.png (e GeoTIFF se possível)
```

| Script | Papel |
|--------|--------|
| `ex03_1.py` | Sanidade PCA: erro empírica ↔ autovalores |
| `ex03_2.py` | $\mathbf{S}_N$ por diferenças verticais |
| `ex03_3.py` | Export visual das 3 primeiras PCs → `figuras/` |

**Roteiro sugerido.** Rode o notebook; confira se PC1 carrega estrutura da cena. Rode `ex03_1` com `-r 2` e `-r 5` e veja o erro cair. Rode `ex03_2` e compare a escala de $\mathbf{S}_N$ com $\mathbf{S}$ do Cap. 2. Por fim `ex03_3` e compare com `figuras/pc1.png` etc.

**Ponte auxil:** depois de dominar os `ex03_*`, explore `legado/canty/auxil/scripts/pca.py` e `mnf.py` para o fluxo “de produção” alinhado ao livro.

## 7. Checklist de domínio + dúvidas típicas

**Checklist**

- [ ] Explico redundância espectral com o heatmap do Cap. 2 na cabeça.
- [ ] Recito os 5 passos da PCA e implemento com `eigh` + `argsort`.
- [ ] Interpreto $\lambda_k$ e $\mathbf{w}_k$ e leio um scree.
- [ ] Escrevo a reconstrução truncada e ligo o erro aos autovalores descartados.
- [ ] Contraste PCA vs MNF em duas frases (variância vs SNR / papel de $\mathbf{S}_N$).
- [ ] Sei quando a estimativa de ruído por diferenças espaciais é razoável.
- [ ] Localizo `ex03_1`–`ex03_3`, o notebook e `legado/canty/auxil/scripts/pca.py` / `mnf.py`.

**Dúvidas típicas**

1. *“Quantas PCs usar?”*  
   Scree + inspeção visual + (se houver) erro de reconstrução / desempenho a jusante (classificação). Não existe $r$ universal.

2. *“PCA na covariância ou na correlação?”*  
   Canty/exercícios: covariância após centrar. Se uma banda tiver variância ordens de magnitude maior só por unidade/escala, padronize (equivale a PCA na correlação) e documente.

3. *“Por que minha PC1 veio invertida (clara↔escura)?”*  
   Sinal do autovetor é arbitrário. Multiplique por $-1$ se quiser o contraste visual oposto.

4. *“MNF sempre melhor que PCA?”*  
   Não. Depende da qualidade de $\mathbf{S}_N$. Estimativa ruim de ruído ⇒ MNF pior que PCA.

5. *“O fator $1/2$ em $\mathbf{S}_N$?”*  
   Vem do modelo: diferença de dois ruídos independentes tem variância $2\sigma^2$. Se o sinal não for quase constante entre vizinhos, a estimativa absorve estrutura espacial e “acha” ruído demais.

6. *“Eq. 3.45 exacta no livro?”*  
   Use o PDF para a forma tipográfica final; o `ex03_1.py` operacionaliza a relação erro↔autovalores descartados. Se os dois lados divergirem, o bug está na implementação, não na intuição.
