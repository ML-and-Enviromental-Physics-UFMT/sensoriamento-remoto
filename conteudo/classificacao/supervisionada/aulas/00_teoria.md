# Capítulo 6 — Classificação supervisionada (Parte 1)

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../../data/README.md).

> Referência: Canty, M. J. (2019). *Image Analysis, Classification and Change Detection in Remote Sensing*, Cap. 6.  
> Apoio matemático: [Apêndice A](../../../matematica/consulta-rapida.md).
> Treino de redes (contexto futuro): [Apêndice B](../../treinamento-de-redes/aulas/treino_redes.md).

## Antes do classificador: de onde vêm as classes?

Uma classe de referência começa com uma interpretação. Ao rotular uma região como vegetação, registre se a decisão veio de campo, de uma imagem de referência datada ou de outra fonte. Cor, forma e contexto ajudam, mas não eliminam a incerteza.

Considere uma área agrícola que parece vegetada durante o crescimento e apresenta solo exposto após a colheita. Rotulá-la como "agricultura" descreve seu uso; rotulá-la como "vegetação" descreve uma cobertura observada em certa data. As duas decisões podem ser coerentes, mas respondem a perguntas diferentes. Defina a legenda antes de selecionar amostras.

O classificador aprende a relação entre seus dados e os rótulos fornecidos. Se rótulos errados ou ambíguos entram no treino, um mapa visualmente convincente pode repetir esses problemas. Para avaliar o mapa, use referências adequadas à data e mantenha a avaliação separada do ajuste do modelo, considerando também a dependência espacial.

Fonte complementar: Ponzoni, [Vegetação](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_8.pdf), seção 3; Moreira e Rudorff, [Agricultura](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_9.pdf), PDF pp. 5–9; Santos, [Uso escolar](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_12.pdf), PDF pp. 9–11. O exemplo de legenda e os cuidados de avaliação são aplicações didáticas desses temas ao capítulo. Comece por [Interpretar imagens](../../../fundamentos/aulas/04_interpretar_imagens.md) se reconhecer os alvos ainda for uma dificuldade.

## 0. Para quem é este guia / o que você vai saber ao final

Este guia é para quem já consegue abrir um raster multiespectral (ex.: raster sintético em `data/exemplos/exemplo_sintetico.tif`), calcular um índice simples e quer dar o passo seguinte: **rotular a imagem em classes de cobertura** com exemplos conhecidos.

Você não precisa ter lido o PDF do Cap. 6 antes. O texto começa no zero pedagógico (espaço de atributos, amostras) e sobe até o classificador de máxima verossimilhança gaussiano do livro, com a ponte para o que o `sklearn` chama de QDA e Naive Bayes.

Ao final, você deve ser capaz de:

1. Explicar o que é classificação **supervisionada** e por que ela depende de amostras de treino.
2. Desenhar mentalmente nuvens de pixels no espaço de bandas e dizer o que acontece quando as nuvens se sobrepõem.
3. Aplicar o teorema de Bayes em linguagem de “prior × verossimilhança → posterior”.
4. Relacionar distância de Mahalanobis, covariância por classe e o discriminante do ML gaussiano.
5. Distinguir priors, GaussianNB (covariância diagonal) e QDA (covariância cheia).
6. Ler uma matriz de confusão sem se iludir com acurácia alta em rótulos sintéticos.
7. Saber onde está a implementação “de livro” (`legado/canty/auxil/supervisedclass.py`, `legado/canty/auxil/scripts/classify.py`) e onde está o exercício didático (`exercicios/ex06_1.py`).

## 1. Pré-requisitos (o que o livro assume e quase não explica)

O Canty assume fluência em ideias dos Caps. 1–2 (e um pouco do Apêndice A). Em português curto:

| Ideia | Por que importa aqui |
|-------|----------------------|
| Pixel como vetor $\mathbf{x}\in\mathbb{R}^N$ | Cada pixel é um ponto no espaço de $N$ bandas (atributos). |
| Média e covariância amostrais | O ML gaussiano estima $\boldsymbol{\mu}_k$ e $\boldsymbol{\Sigma}_k$ por classe. |
| Matriz invertível / determinante | Entram na distância de Mahalanobis e no termo $\log\det\boldsymbol{\Sigma}_k$. |
| Histograma / densidade | A “nuvem” de uma classe é modelada por uma densidade $p(\mathbf{x}\mid k)$. |
| Autocorrelação espacial (Cap. 2) | Pixels vizinhos não são independentes; isso enviesa métricas se você ignora. |

Pré-requisitos de Python neste repositório: NumPy (arrays 2D de amostras × bandas), noção de `train_test_split`, e disposição para olhar saídas PNG em `figuras/`. Rasterio ajuda se o raster sintético estiver presente; senão o exercício cai em gaussianas 2D sintéticas.

Se “covariância” ainda for abstrato, releia a consulta rápida do Apêndice A (Mahalanobis e $\mathbf{S}$) antes da seção 4 deste guia.

## 2. Intuição do problema (sem equação)

Imagine a cena raster sintético sobre uma paisagem com água, solo exposto e vegetação. Cada pixel tem um conjunto de valores nas bandas VNIR (e eventualmente SWIR). Se você plotasse só duas bandas — digamos vermelho × NIR — veria três manchas de pontos: água mais escura em ambas, vegetação alta em NIR e baixa no vermelho, solo em outro canto.

Classificar supervisionadamente é: **você mostra ao algoritmo alguns pontos de cada mancha com o rótulo correto**; o algoritmo aprende uma regra (“se o pixel cair nesta região do espaço, chame de vegetação”) e aplica essa regra a todos os demais pixels.

Três intuções que evitam frustração:

1. **A regra vive no espaço de atributos, não no mapa.** O mapa colorido é só a projeção espacial da decisão tomada banda a banda (ou atributo a atributo).
2. **Amostras ruins geram mapa bonito e mentiroso.** Se você só amostrar o “centro” de uma floresta homogênea, o classificador não aprende bordas, sombras nem misturas. Se amostrar pixels vizinhos demais, o teste “parece” ótimo porque treino e teste compartilham a mesma vizinhança.
3. **Sobreposição é erro estrutural.** Se duas classes ocupam a mesma região espectral, nenhum Bayes milagroso separa 100%. A saída honesta é probabilidade / incerteza, não só um rótulo duro.

Diferença em relação a “machine learning genérico”: em sensoriamento remoto o atributo típico é o vetor espectral (às vezes + índices, textura, DEM); as classes são coberturas ou usos; e a avaliação precisa lidar com espacialidade, mistura de pixel e desenho amostral.

## 3. O que o Canty ensina neste capítulo (mapa das seções + ideias-chave)

O Cap. 6 do livro organiza a classificação supervisionada “clássica” em torno de Bayes e do modelo gaussiano. Em mapa mental (nomes de seção variam ligeiramente entre edições; o fio é este):

| Bloco | Ideia-chave | O que guardar |
|-------|-------------|----------------|
| Espaço de atributos / features | Pixels como vetores; classes como nuvens | Dimensão = nº de bandas (ou atributos derivados) |
| Amostras de treino | Estimar parâmetros da densidade por classe | Viés, representatividade, autocorrelação |
| Teorema de Bayes | Posterior $\propto$ verossimilhança × prior | Decisão = $\arg\max_k P(k\mid\mathbf{x})$ |
| ML gaussiano | $p(\mathbf{x}\mid k)=\mathcal{N}(\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)$ | Distância de Mahalanobis + $\log\det$ + prior |
| Discriminantes | Linear (LDA, $\boldsymbol{\Sigma}$ comum) vs quadrático (QDA, $\boldsymbol{\Sigma}_k$) | Livro enfatiza o caso geral (por classe) |
| Avaliação introdutória | Matriz de confusão, taxas de erro | Cap. 7 aprofunda kappa, McNemar, CV |
| Implementação | Código / scripts do ecossistema do livro | Aqui: `Maxlike` em `supervisedclass.py` |

Ideias-chave que o livro martela e que este guia repete:

- Estimar bem $\boldsymbol{\mu}_k$ e $\boldsymbol{\Sigma}_k$ exige **amostras suficientes** por classe — especialmente se $N$ (bandas) for grande: a covariância tem $N(N+1)/2$ parâmetros livres.
- O prior $P(k)$ desloca a fronteira a favor de classes mais frequentes (ou mais importantes, se você definir prior por custo/utilidade).
- Redes neurais e SVM **não** são o centro do Cap. 6; aparecem com força no Cap. 7 e no Apêndice B. Aqui o baseline paramétrico é o ML gaussiano.

## 4. Desenvolvimento guiado (conceitos do livro, com derivação/explicação acessível)

### 4.1 Espaço de atributos

Seja uma imagem com $N$ bandas. O pixel na linha $i$, coluna $j$ vira

$$
\mathbf{x}_{ij} = \bigl(x_{ij}^{(1)},\ldots,x_{ij}^{(N)}\bigr)^\top \in \mathbb{R}^N.
$$

Na prática empilhamos pixels em uma matriz de desenho $\mathbf{X}\in\mathbb{R}^{m\times N}$ ($m$ amostras). Classes $k=1,\ldots,K$ são rótulos inteiros. Visualmente: cada classe é uma nuvem; o classificador particiona $\mathbb{R}^N$ em regiões $R_1,\ldots,R_K$.

Atributos podem ser só DN/reflectância, ou incluir NDVI, PC1–PC3 (Cap. 3), textura (Cap. 4), etc. Mais atributos ≠ automaticamente melhor: covariâncias ficam mais difíceis de estimar e aparece a maldição da dimensionalidade.

### 4.2 Amostras de treino: viés e autocorrelação espacial

O conjunto de treino $`\mathcal{T}=\{(\mathbf{x}_s,y_s)\}_{s=1}^{n}`$ deve representar a **variabilidade** de cada classe na cena (e, idealmente, nas condições em que você vai aplicar o modelo).

Armadilhas típicas em SR:

1. **Viés de conveniência.** Só amostrar beira de estrada acessível → classes “floresta” e “pasto” sem o interior real.
2. **Rótulo errado.** Um pixel de sombra rotulado como água puxa $\boldsymbol{\mu}_{\text{água}}$ e infla $\boldsymbol{\Sigma}$.
3. **Autocorrelação espacial.** Pixels adjacentes são parecidos. Se você sorteia 70% treino / 30% teste **ao acaso no mesmo polígono**, o teste não é independente: a acurácia sobe artificialmente.
4. **Desbalanceamento.** 90% da cena é vegetação; se o prior empírico refletir isso sem cuidado, classes raras somem do mapa.

Regra prática: descreva sempre **como** as amostras foram obtidas (campo, fotointerpretação, produto de referência) junto com qualquer número de acurácia.

### 4.3 Teorema de Bayes, com calma

Queremos a classe mais provável dado o pixel:

```math
\hat{k}(\mathbf{x}) = \arg\max_{k}\, P(k\mid\mathbf{x}).
```

Bayes diz

```math
P(k\mid\mathbf{x}) = \frac{p(\mathbf{x}\mid k)\,P(k)}{p(\mathbf{x})},
```

onde $p(\mathbf{x})=\sum_{\ell} p(\mathbf{x}\mid\ell)P(\ell)$ não depende de $k$ na comparação. Logo

```math
\hat{k}(\mathbf{x}) = \arg\max_{k}\, p(\mathbf{x}\mid k)\,P(k).
```

Leitura em português:

- $p(\mathbf{x}\mid k)$ — “quão típico é este espectro se a verdade for a classe $k$?” (verossimilhança)
- $P(k)$ — “quão comum / esperada é a classe $k$ a priori?” (prior)
- $P(k\mid\mathbf{x})$ — “depois de ver o pixel, qual a probabilidade da classe $k$?” (posterior)

Se os priors forem iguais, sobra só maximizar a verossimilhança (daí o nome *maximum likelihood* no jargão de SR, mesmo quando o prior entra no discriminante completo).

### 4.4 Modelo gaussiano e distância de Mahalanobis

Assuma

```math
p(\mathbf{x}\mid k) = (2\pi)^{-N/2}\,|\boldsymbol{\Sigma}_k|^{-1/2}\,
\exp\Bigl(-\tfrac12 (\mathbf{x}-\boldsymbol{\mu}_k)^\top\boldsymbol{\Sigma}_k^{-1}(\mathbf{x}-\boldsymbol{\mu}_k)\Bigr).
```

O expoente contém a **distância de Mahalanobis** ao quadrado:

$$
d_k^2(\mathbf{x}) = (\mathbf{x}-\boldsymbol{\mu}_k)^\top\boldsymbol{\Sigma}_k^{-1}(\mathbf{x}-\boldsymbol{\mu}_k).
$$

Diferente da distância euclidiana, ela alonga/encolhe e rotaciona o espaço conforme a elipse da classe: desviar na direção de alta variância “custa menos” do que desviar na direção estreita.

Tomando $\log$ de $p(\mathbf{x}\mid k)P(k)$ e descartando constantes comuns a todas as classes, maximizar o posterior equivale a maximizar o discriminante

$$
\delta_k(\mathbf{x}) = -\tfrac12 d_k^2(\mathbf{x}) - \tfrac12\log|\boldsymbol{\Sigma}_k| + \log P(k)
$$

(ou formas equivalentes com sinal trocado: minimizar $d_k^2 + \log|\boldsymbol{\Sigma}_k| - 2\log P(k)$).

Estimativas a partir do treino da classe $k$ (com $n_k$ amostras):

$$
\hat{\boldsymbol{\mu}}_k = \frac{1}{n_k}\sum_{s:y_s=k}\mathbf{x}_s,\qquad
\hat{\boldsymbol{\Sigma}}_k = \frac{1}{n_k-1}\sum_{s:y_s=k}(\mathbf{x}_s-\hat{\boldsymbol{\mu}}_k)(\mathbf{x}_s-\hat{\boldsymbol{\mu}}_k)^\top.
$$

O prior pode ser uniforme, empírico $n_k/n$, ou definido por conhecimento de área.

**Conexão com o código do livro.** Em `legado/canty/auxil/supervisedclass.py`, a classe `Maxlike` estima $\boldsymbol{\mu}_k$ e $\boldsymbol{\Sigma}_k$, inverte a covariância e, na classificação, usa um escore proporcional a $-d_k^2 - \log\det\boldsymbol{\Sigma}_k$ (priors iguais no trecho típico). O script `legado/canty/auxil/scripts/classify.py` com `-a 1` dispara esse algoritmo (`MaxLike`).

### 4.5 Priors: quando mexer e quando não

- Prior uniforme: fronteira só pela forma das densidades.
- Prior empírico: classes abundantes “ganham território” no mapa — útil se a cena for realmente dominada por elas; perigoso se o treino não refletir a cena.
- Prior por custo: raramente explícito no exercício didático, mas em aplicação (ex.: detectar uma classe rara de interesse) você pode inflar $P(k)$ ou trabalhar com limiar na posterior.

### 4.6 QDA versus Naive Bayes (e o que o sklearn faz)

| Modelo | Hipótese sobre $\boldsymbol{\Sigma}$ | Fronteira | No ecossistema deste repo |
|--------|--------------------------------------|-----------|---------------------------|
| **QDA** (quadratic discriminant analysis) | $\boldsymbol{\Sigma}_k$ cheia, por classe | Quadrática | Próximo do ML gaussiano do Canty; `QuadraticDiscriminantAnalysis` |
| **LDA** | $\boldsymbol{\Sigma}$ comum a todas | Linear | Caso particular; menos parâmetros |
| **GaussianNB** | Diagonal (bandas independentes dada a classe) | “Ingênua” | `GaussianNB`; subestima correlação espectral |

Bandas de satélite **são** correlacionadas (Cap. 2–3). Por isso Naive Bayes espectral é um baseline rápido, não o modelo físico preferido. Ainda assim é excelente didaticamente: treina com pouco dado e falha de forma interpretável.

O exercício `ex06_1.py` tenta QDA primeiro e, se a estimativa falhar (poucas amostras / covariância singular), cai para `GaussianNB`.

### 4.7 Matriz de confusão (básico)

Seja $C$ a matriz $K\times K$ em que $C_{ij}$ conta pixels com verdade $i$ preditos como $j$ (convenção comum; confirme sempre linhas×colunas na sua biblioteca).

- Diagonal $C_{ii}$: acertos da classe $i$.
- Fora da diagonal: confusões (ex.: vegetação → solo).
- Acurácia global: $\sum_i C_{ii}/N_{\text{teste}}$.

No Cap. 6 basta saber **ler** a matriz e desconfiar de acurácia alta quando os rótulos de “verdade” foram fabricados a partir do próprio espectro (próxima subseção). Kappa, McNemar e validação cruzada ficam para o Cap. 7.

### 4.8 Caveat dos rótulos sintéticos em `ex06_1`

O exercício cria três classes por limiar em um NDVI-like (bandas raster sintético ≈ vermelho e NIR):

- NDVI baixo → classe 0  
- intermediário → classe 1  
- alto → classe 2  

Isso **não** é verdade de campo. É um gerador de rótulos para praticar o *pipeline*: montar $\mathbf{X}$, separar treino/teste, ajustar QDA/NB, imprimir confusão, gravar mapa.

Consequência: o classificador, em parte, **reaprende o limiar** que você usou para rotular, agora no espaço de todas as bandas. Acurácia alta é esperada e **não** prova que o método mapearia bem coberturas reais. Em tese de mestrado ou mapa operacional, substitua por amostras independentes (GPS, interpretação em alta resolução, produto de referência externo).

Se o GeoTIFF raster sintético não existir, o script gera três gaussianas 2D — aí a hipótese do modelo coincide com o processo gerador, e o exercício vira laboratório limpo de Bayes gaussiano.

## 5. Além do livro (prática moderna, armadilhas, ligação com sklearn/GEE/SAR/mestrado)

**sklearn.** Para o Cap. 6, o núcleo é `GaussianNB` e `QuadraticDiscriminantAnalysis`, com `StandardScaler` (QDA/NB sensíveis à escala se misturar atributos de unidades diferentes), `confusion_matrix` e `ConfusionMatrixDisplay`. O livro fala em ML; o sklearn fala em QDA — é a mesma família.

**Google Earth Engine.** Classificadores supervisionados (smileRandomForest, smileCart, etc.) dominam tutoriais GEE; o análogo bayesiano gaussiano é menos comum na UI, mas a lógica de amostras (`SampleRegions`), split espacial e matriz de confusão é a mesma discussão deste capítulo.

**SAR.** Intensidade/speckle viola a hipótese gaussiana em DN linear de forma brutal; frequentemente trabalha-se em log, com atributos polarimétricos, ou com modelos não gaussianos. Não force ML gaussiano “ótico” em SAR sem revisar a distribuição.

**Mestrado / publicação.** Exija: (i) desenho amostral documentado; (ii) separação espacial treino/teste; (iii) métricas por classe, não só overall; (iv) mapa de incerteza se possível; (v) comparação com um baseline simples (NB/QDA) antes de redes.

**Armadilhas modernas que o livro já antecipa em espírito:**

- Treinar em uma cena e aplicar em outra data sem checar deslocamento espectral (atmosfera, fenologia).
- Usar todas as bandas hiperespectrais com poucas dezenas de amostras por classe → $\boldsymbol{\Sigma}_k$ instável (regularize, reduza dimensão com PCA/MNF, ou mude de modelo).
- Reportar acurácia de validação aleatória por pixel como se fosse acurácia de mapa.

## 6. Como praticar neste repositório (notebook + exercícios + outputs)

Ordem sugerida:

1. Ler este `00_teoria.md` até a seção 4.
2. Abrir `notebooks/06_teoria.ipynb` e acompanhar a narrativa ML vs SR + código.
3. Rodar a partir da raiz do repo ou do capítulo:

```bash
python conteudo/classificacao/supervisionada/exercicios/ex06_1.py
```

4. Inspecionar:

- `figuras/ex06_1_classification_map.png` — NDVI-like, rótulos sintéticos, mapa classificado
- `figuras/ex06_1_confusion_matrix.png` — confusão no hold-out

5. (Opcional, fluxo “livro completo”.) Estudar `legado/canty/auxil/supervisedclass.py` (`Maxlike`) e `legado/canty/auxil/scripts/classify.py` (`-a 1` = MaxLike). Os exercícios deste capítulo preferem sklearn de propósito: menos dependências pesadas, foco no raciocínio.

Raster de referência: `data/exemplos/exemplo_sintetico.tif`.

Ponte para o Cap. 7: mesmos rótulos sintéticos, mas comparando NB × Random Forest (e SVM quando couber), com kappa e McNemar.

## 7. Checklist de domínio + dúvidas típicas

**Checklist — só avance ao Cap. 7 se conseguir marcar com honestidade:**

- [ ] Sei explicar supervisão vs não supervisão (Cap. 8) em uma frase.
- [ ] Consigo escrever Bayes: posterior $\propto$ verossimilhança × prior.
- [ ] Sei o que Mahalanobis “corrige” em relação à distância euclidiana.
- [ ] Distingo QDA (covariância cheia) de GaussianNB (diagonal).
- [ ] Sei por que autocorrelação espacial infla acurácia em split aleatório.
- [ ] Olhando `ex06_1`, sei dizer por que rótulo via NDVI não é verdade de campo.
- [ ] Sei apontar `Maxlike` / `classify.py -a 1` como implementação Canty e `ex06_1.py` como laboratório didático.

**Dúvidas típicas**

1. *“Acurácia 0,95 no ex06_1 — meu classificador é ótimo?”*  
   Não necessariamente. Os rótulos vêm do próprio NDVI; você está quase medindo quão bem o espectro reconstrói um limiar que você inventou.

2. *“Por que QDA falhou e caiu no NB?”*  
   Covariância singular ou instável: poucas amostras por classe em dimensão $N$, ou colinearidade entre bandas. NB não estima correlações e “passa”.

3. *“Preciso do prior?”*  
   Com classes equilibradas no treino e na cena, prior uniforme costuma bastar. Se uma classe rara importa, prior ou limiar na posterior importa mais que trocar de kernel.

4. *“LDA ou QDA?”*  
   LDA assume a mesma forma elíptica (só deslocada) para todas as classes — menos parâmetros, mais estável. QDA é o default conceitual do ML por classe no livro. Com pouco dado, LDA (ou NB) pode generalizar melhor.

5. *“Onde entram as redes?”*  
   Conceito e avaliação: Cap. 7. Como treinar (backprop, regularização): Apêndice B. Neste capítulo o baseline é gaussiano.

6. *“Posso usar só PC1–PC3 em vez das bandas?”*  
   Sim, e muitas vezes ajuda a estabilizar $\boldsymbol{\Sigma}_k$. Lembre que PCA não usa os rótulos (é não supervisionada); a discriminação ainda fica a cargo do classificador.

---

*Próximo passo natural:* Cap. 7 — por que sair do ML gaussiano, SVM/ensembles/redes em alto nível, e como comparar classificadores com kappa, McNemar e validação que respeite o espaço.
