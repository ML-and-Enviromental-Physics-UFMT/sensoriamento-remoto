# Cap. 8 — Classificação não supervisionada (agrupamento)

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../../data/README.md).

> Referência: Canty, M. J. (2019). *Image Analysis, Classification and Change Detection in Remote Sensing*, Cap. 8.  
> Stub curto: [`agrupamento.md`](agrupamento.md). Matemática de apoio: [Apêndice A](../../../matematica/README.md).

---

## Antes de nomear os grupos

Um algoritmo de agrupamento reúne pixels conforme as variáveis e a medida de semelhança escolhidas. Ele não sabe que você quer mapear floresta, agricultura ou cidade. Os nomes das coberturas exigem uma interpretação posterior.

Uma floresta pode aparecer em dois grupos porque partes estão iluminadas e outras sombreadas. Um único grupo também pode reunir alvos distintos com respostas semelhantes nas bandas usadas. A composição das copas e a mistura com solo ajudam a explicar por que o número de grupos não precisa coincidir com o número de classes desejadas.

Depois de executar o algoritmo, procure exemplos de cada grupo em locais conhecidos, compare outras bandas e confronte uma referência datada. Se não puder atribuir uma cobertura com segurança, mantenha a identificação numérica e registre a dúvida. Não transforme um nome conveniente em evidência de acerto.

Fonte complementar: Ponzoni, [Vegetação](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_8.pdf), PDF pp. 12–14, para estrutura do dossel; Santos, [Uso escolar](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_12.pdf), PDF pp. 9–11, para integração de evidências. A relação com agrupamento é uma explicação autoral para este capítulo. A [aula de interpretação](../../../fundamentos/aulas/04_interpretar_imagens.md) prepara essa etapa.

## 0. Para quem / objetivos

Este texto é para quem já leu (ou está lendo em paralelo) os Caps. 1–3 e 6 do Canty e quer entender **agrupamento espectral** sem rótulos de campo: o que o algoritmo devolve, o que isso *não* é, e como o repositório materializa k-means, EM/GMM e SOM.

Ao terminar, você deve conseguir:

1. Distinguir **cluster espectral** de **classe de cobertura** (legenda).
2. Explicar, sem fórmula na mão, o ciclo do k-means e por que escala das bandas importa.
3. Relacionar EM a uma mistura de gaussianas (GMM) e contrastar *hard* vs *soft* assignment.
4. Situar SOM como mapa topológico 2D, não como substituto automático de k-means.
5. Escolher $K$ com critério e ceticismo (inércia, BIC, interpretação espacial).
6. Rodar `ex08_1.py` / `ex08_2.py` e apontar os scripts `auxil` correspondentes.

---

## 1. Pré-requisitos

| Tema | Onde no livro / repo | Por que precisa |
|------|----------------------|-----------------|
| Pixel = vetor $\mathbf{x}\in\mathbb{R}^N$ | Cap. 1 | Agrupamos no espaço espectral |
| Média, covariância, PCA | Caps. 2–3; Apêndice A | Pré-processamento e GMM |
| Distância euclidiana vs Mahalanobis | Cap. 6; Apêndice A | k-means usa a primeira; GMM “encorpora” a segunda |
| Classificação supervisionada | Caps. 6–7 | Contraste: aqui **não** há $y$ de treino |

Não é obrigatório dominar EM em toda a generalidade estatística. Basta a intuição: estimar parâmetros de uma mistura quando os rótulos latentes são desconhecidos.

---

## 2. Intuição

Imagine a nuvem de pixels de uma cena raster sintético no espaço de $N$ bandas. Sem amostras de campo, você **não** sabe quais pontos são “água” ou “floresta”. Ainda assim, a nuvem costuma ter **aglomerados**: regiões densas separadas por vazios relativos.

A classificação não supervisionada responde: *“quantas bolhas densas consigo descrever, e a qual bolha cada pixel pertence?”* O mapa de cores que sai do algoritmo é um mapa de **índices de cluster** $1,\ldots,K$. A legenda (“água”, “urbano”…) é trabalho **posterior**: fotointerpretação, pontos de campo, ou cruzamento com outro produto.

Três armadilhas comuns:

- **Cluster ≠ cobertura.** Dois tipos de solo espectralmente parecidos podem cair no mesmo cluster; uma mesma cobertura com sombra e sol pleno pode rachar em dois.
- **$K$ é escolha, não descoberta mágica.** Métodos ajudam a *sugerir* $K$; a cena e o objetivo fecham a decisão.
- **Escala das bandas.** Se uma banda varia de 0–10000 e outra de 0–1, a distância euclidiana é dominada pela primeira. Padronizar (`StandardScaler`) ou trabalhar em PCs equaliza o jogo — o `ex08_1` faz isso.

Pense no Cap. 6 (ML gaussiano) ao contrário: lá você estima $\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k$ **com** rótulos; aqui os rótulos são latentes e o algoritmo os inventa juntos com os parâmetros (EM) ou só com centróides (k-means).

---

## 3. Mapa Canty (Cap. 8)

No Canty (2019), o Cap. 8 organiza o não supervisionado em torno de agrupamento no espaço de atributos e de algoritmos clássicos em sensoriamento remoto:

| Bloco do livro (ideia) | Conteúdo | Neste repo |
|------------------------|----------|------------|
| Motivação / exploração | Clusters como estrutura espectral sem legenda | Esta seção 2 |
| k-means (e variantes) | Partição por centróides; critério de soma de quadrados | `kmeans.py`, `ekmeans.py`, `ex08_1.py` |
| EM / misturas | Soft membership + gaussianas | `em.py`, `ex08_2.py` (sklearn GMM) |
| SOM | Mapa auto-organizável, topologia | `som.py` (leitura / experimento) |
| Escolha de $K$ / interpretação | Critérios e leitura do mapa | Seções 4.4–4.5 abaixo |

O livro também discute o papel do agrupamento como **pré-etapa** (reduzir complexidade, gerar candidatos a classes) antes ou ao lado da classificação supervisionada dos Caps. 6–7. Spectral clustering no sentido de “cortar o grafo de similaridade” não é o foco didático central do capítulo — mas a confusão de nomes com “cluster espectral = agrupamento nas bandas” merece o aviso da seção 4.5.

---

## 4. Desenvolvimento guiado

### 4.1 k-means

**Objetivo.** Particionar $`\{\mathbf{x}_i\}_{i=1}^m`$ em $K$ conjuntos $C_1,\ldots,C_K$ minimizando (aproximadamente) a inércia

```math
J = \sum_{k=1}^{K}\sum_{\mathbf{x}_i\in C_k}\|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2,
```

onde $\boldsymbol{\mu}_k$ é a média (centróide) dos pontos em $C_k$.

**Algoritmo (Lloyd):**

1. Escolha $K$ centróides iniciais (aleatório, k-means++, ou seeds fixas para reprodutibilidade).
2. **Atribuição:** cada pixel vai para o centróide mais próximo (norma euclidiana).
3. **Atualização:** $\boldsymbol{\mu}_k \leftarrow$ média dos pixels atribuídos a $k$.
4. Repita 2–3 até estabilizar rótulos / $J$, ou atingir um máximo de iterações.

**O que assume.** Clusters aproximadamente esféricos (em distância euclidiana), de tamanho comparável. Elipses alongadas, densidades muito diferentes ou “faixas” espectrais quebram o modelo — daí o interesse em GMM.

**No repo.**

- `legado/canty/auxil/scripts/kmeans.py` — fluxo alinhado ao livro.
- `legado/canty/auxil/scripts/ekmeans.py` — variante estendida (veja o script e o PDF do capítulo para detalhes de inicialização / critério).
- `exercicios/ex08_1.py` — versão didática com sklearn: lê raster sintético, padroniza bandas, ajusta k-means numa **subamostra** (`MAX_FIT`) e prediz o mapa completo; salva PNG em `figuras/`.

Leia o `ex08_1` como protocolo de escala: em cenas grandes, ajustar em todos os pixels é caro e desnecessário se a amostra for representativa; a predição (`predict`) cobre a grade inteira.

### 4.2 EM e mistura de gaussianas (GMM)

Modele a densidade marginal dos pixels como mistura:

```math
p(\mathbf{x}) = \sum_{k=1}^{K} \pi_k\,\mathcal{N}(\mathbf{x};\,\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k),
\quad
\pi_k\ge 0,\quad \sum_k\pi_k=1.
```

Os $\pi_k$ são pesos (priors da mistura). Cada componente é uma elipse gaussiana no espaço espectral — a mesma família do ML do Cap. 6, só que agora a classe é **latente**.

**Expectation–Maximization** alterna:

- **E-step.** Responsabilidades (soft assignment)

```math
\gamma_{ik} = \frac{\pi_k\,\mathcal{N}(\mathbf{x}_i;\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_{j=1}^{K}\pi_j\,\mathcal{N}(\mathbf{x}_i;\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}.
```

$\gamma_{ik}$ é a probabilidade posterior de o pixel $i$ pertencer ao componente $k$ dados os parâmetros atuais.

- **M-step.** Atualize $\pi_k$, $\boldsymbol{\mu}_k$, $\boldsymbol{\Sigma}_k$ como médias ponderadas por $\gamma_{ik}$ (máxima verossimilhança ponderada).

Repita até a verossimilhança estabilizar. O mapa “duro” usual é $\hat{k}_i=\arg\max_k\gamma_{ik}$; o mapa de $\gamma_{ik}$ (ou entropia das responsabilidades) revela misturas e bordas incerteza — útil em SR, onde pixels misturados são a regra, não a exceção.

**k-means vs GMM (resumo tutor):**

| | k-means | GMM + EM |
|--|---------|----------|
| Atribuição | Hard | Soft ($\gamma$) |
| Forma do cluster | Esfera (euclidiana) | Elipse ($\boldsymbol{\Sigma}_k$) |
| Custo | Baixo | Maior (inversas / dets) |
| Ligação Cap. 6 | Centróides | Mesma família gaussiana |

**No repo.** `legado/canty/auxil/scripts/em.py` implementa o EM do livro (também reutilizado no Cap. 9). `ex08_2.py` usa `sklearn.mixture.GaussianMixture` com `covariance_type="full"`, tipicamente nas primeiras 4 bandas e subamostra, e imprime BIC da amostra de ajuste — gancho para a seção seguinte.

### 4.3 SOM (Self-Organizing Map), em breve

Uma SOM é uma grade 2D de neurônios, cada um com um vetor-peso no espaço espectral. No treino, cada pixel “ativa” o neurônio vencedor (mais próximo) e atualiza também os **vizinhos** na grade. Resultado: pixels espectralmente próximos tendem a neurônios topologicamente próximos.

**Para quê em SR.** Visualização exploratória, compressão de variedade espectral, agrupamento suave. **Não** substitui automaticamente k-means/GMM quando o produto desejado é um mapa de $K$ rótulos com interpretação clara — a SOM devolve uma organização 2D que ainda precisa de corte / rotulagem.

**No repo.** `legado/canty/auxil/scripts/som.py`. Não há exercício dedicado neste capítulo: trate como leitura + experimento opcional depois de dominar `ex08_1`/`ex08_2`.

### 4.4 Escolhendo $K$

Não existe $K$ “certo” universal. Ferramentas úteis:

1. **Cotovelo da inércia $J(K)$** (k-means): plote $J$ vs $K$ e procure o joelho — depois do qual o ganho diminui. Subjetivo, mas barato.
2. **BIC / AIC** (GMM): `GaussianMixture` no sklearn expõe `bic`/`aic`; o `ex08_2` já imprime BIC na subamostra. Menor BIC favorece compromisso ajuste × complexidade. Cuidado: amostra espacialmente correlacionada ≠ i.i.d.; use o número como **guia**, não como sentença.
3. **Estabilidade.** Rode várias seeds; clusters que mudam de forma drástica são suspeitos.
4. **Mapa espacial.** Clusters que viram “sal e pimenta” puro ou que fundem coberturas óbvias pedem outro $K$ ou outro pré-processamento (PCA, máscara de nuvem, etc.).
5. **Objetivo da aplicação.** Inventário grosseiro de 4–6 coberturas ≠ segmentação fina de 20 espectros.

Uma prática saudável: fixar um $K$ candidato, interpretar centróides/médias espectrais (assinaturas), **depois** nomear classes — nunca o contrário.

### 4.5 “Spectral clustering” vs significado de cobertura

Duas leituras do adjetivo *spectral* se misturam na literatura e na conversa de laboratório:

- **Agrupamento no espaço espectral (bandas):** o que este capítulo faz. Distâncias e densidades vivem em $\mathbb{R}^N$ das reflectâncias/Radares.
- **Spectral clustering (ML):** algoritmo que corta o grafo de similaridade via autovetores do Laplaciano. É outro método; o Canty não o coloca como eixo principal do Cap. 8.

Mesmo no primeiro sentido, **cluster espectral ≠ classe de cobertura do solo**. Cobertura é categoria semântica (uso/ocupação). Cluster é partição estatística. A ponte entre os dois é interpretação humana + validação. Sem isso, um mapa colorido de k-means é só uma compressão visual da variedade espectral.

### 4.6 Fluxo recomendado de estudo

1. Reler a intuição (seção 2) e o contraste com Cap. 6.
2. Rodar `ex08_1.py`, olhar `figuras/ex08_1_kmeans_map.png`, variar $K$ mentalmente (ou no código).
3. Rodar `ex08_2.py`, comparar o mapa GMM com o k-means; anotar BIC.
4. Abrir `legado/canty/auxil/scripts/kmeans.py` / `em.py` / `som.py` só para mapear API do livro — não precisa reimplementar tudo.
5. Escrever, em uma página, a legenda tentativa dos seus $K$ clusters (mesmo que provisória).

---

## 5. Além do livro

Canty (2019) fixa o núcleo clássico. Fora do texto, mas útil no mesmo problema:

- **k-means++ / mini-batch** — inicialização e escala para big data (já refletidos em parte no sklearn).
- **HDBSCAN / DBSCAN** — densidade sem $K$ fixo; sensíveis a escala e a SR com misturas.
- **Deep clustering / autoencoders** — representação aprendida antes de agrupar; exige cuidado com interpretação espectral.
- **Segmentação objeto (GEOBIA)** — agrupa espacialmente antes ou junto do espectral; muda a unidade de análise do pixel para o objeto.
- **Validação com referência externa** — quando houver mapa de cobertura confiável, use-o para *avaliar* clusters (pureza, NMI), não para treinar (senão vira supervisionado disfarçado).

Para este curso, o “além” serve para contextualizar leituras; a prática obrigatória continua k-means + GMM no raster sintético do repo.

---

## 6. Prática no repo

| Artefato | Papel |
|----------|--------|
| `exercicios/ex08_1.py` | k-means + `StandardScaler` + subamostra; mapa PNG |
| `exercicios/ex08_2.py` | GMM (`GaussianMixture`); BIC; mapa PNG |
| `legado/canty/auxil/scripts/kmeans.py` | Referência Canty k-means |
| `legado/canty/auxil/scripts/ekmeans.py` | Variante estendida |
| `legado/canty/auxil/scripts/em.py` | EM do livro (também Cap. 9) |
| `legado/canty/auxil/scripts/som.py` | SOM |
| `legado/canty/auxil/scripts/kkmeans.py` | Variante kernel (exploração avançada) |
| `notebooks/08_teoria.ipynb` | Narrativa interativa (se presente) |
| `figuras/` | PNGs gerados pelos exercícios |

Comandos típicos (a partir da raiz do repo):

```bash
python conteudo/classificacao/agrupamento/exercicios/ex08_1.py
python conteudo/classificacao/agrupamento/exercicios/ex08_2.py
```

Dados: `data/exemplos/exemplo_sintetico.tif` (caminho já resolvido pelos scripts).

---

## 7. Checklist + dúvidas

**Checklist**

- [ ] Sei explicar por que o mapa de clusters ainda não é um mapa de cobertura.
- [ ] Descrevo os passos do k-means e o papel do `StandardScaler` no `ex08_1`.
- [ ] Contrastei hard assignment (k-means) com responsabilidades $\gamma_{ik}$ (EM/GMM).
- [ ] Sei onde olhar BIC / inércia e por que não absolutizo o número.
- [ ] Localizo `kmeans.py`, `ekmeans.py`, `em.py`, `som.py` no `auxil`.
- [ ] Rodei `ex08_1` e `ex08_2` e abri os PNGs em `figuras/`.
- [ ] Diferencio “agrupamento espectral” de “spectral clustering” (grafo).

**Dúvidas para levar ao PDF / ao grupo**

1. No seu $K$, quais centróides/médias têm assinatura interpretável e quais parecem “lixo” (nuvem, sombra, mistura)?
2. Se você mascarar água a priori e reagrupar o resto, o mapa melhora? (Experimento mental ou prático.)
3. O EM do `auxil` e o `GaussianMixture` do sklearn batem qualitativamente na mesma cena? Onde divergem?
4. SOM: o que a topologia 2D revela que um mapa de $K$ rótulos esconde?

Quando essas perguntas tiverem resposta tentativas (mesmo incompletas), o Cap. 8 cumpriu o papel: transformar pixels sem rótulo em **hipóteses espectrais** honestas, prontas para validação ou para alimentar o Cap. 6 com candidatos a classes.
