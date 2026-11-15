# Capítulo 7 — Classificação supervisionada (Parte 2)

> Os exemplos desta página usam dados sintéticos gerados pelo projeto. Não são observações ASTER nem permitem interpretar valores como reflectância, temperatura ou classes reais. Veja [os dados de exemplo](../../../../data/README.md).

> Referência: Canty, M. J. (2019). *Image Analysis, Classification and Change Detection in Remote Sensing*, Cap. 7.  
> Treino de redes: [Apêndice B](../../treinamento-de-redes/aulas/treino_redes.md).
> Baseline gaussiano (Parte 1): [Cap. 6 — 00_teoria.md](../../supervisionada/aulas/00_teoria.md).

## 0. Para quem é este guia / o que você vai saber ao final

Este guia continua o Cap. 6. Você já viu Bayes, ML gaussiano, Mahalanobis, QDA vs Naive Bayes e a matriz de confusão básica. Agora a pergunta muda de *“como classificar sob hipótese gaussiana?”* para *“e se a hipótese falhar — e como comparar modelos com rigor?”*

Público: quem rodou (ou pelo menos leu) `ex06_1.py` e quer entender SVM, redes, boosting/ensembles e o pacote de avaliação do livro (acurácia, kappa, McNemar, validação cruzada), sem precisar abrir o PDF primeiro.

Ao final, você deve ser capaz de:

1. Listar motivos concretos para ir além do ML gaussiano.
2. Explicar SVM como maximização de margem (e o papel do kernel em uma frase).
3. Situar redes neurais no fluxo de classificação de imagem e apontar o Apêndice B para o *como treinar*.
4. Descrever bagging/boosting e por que florestas aleatórias dominam muita prática atual em SR tabular.
5. Calcular e interpretar acurácia, kappa e o espírito do teste de McNemar.
6. Desenhar um protocolo de validação que não ignore autocorrelação espacial.
7. Ler o resultado de `ex07_1.py` (NB vs Random Forest) sem confundir “ganhou no hold-out sintético” com “melhor mapa operacional”.
8. Citar, no nível de mestrado, RF, XGBoost e U-Net como além-do-livro, com o cuidado de amostragem e desbalanceamento.

## 1. Pré-requisitos (o que o livro assume e quase não explica)

| Pré-requisito | Onde revisitar |
|---------------|----------------|
| Espaço de atributos, treino rotulado, Bayes/ML gaussiano | Cap. 6 deste repo |
| Matriz de confusão (linhas/colunas, diagonal) | Cap. 6 §4.7 |
| Covariância, inversão, dimensionalidade | Apêndice A |
| Ideia de otimização / gradiente (para redes) | Apêndice B (pode ler em paralelo) |
| Split treino/teste e estratificação | Cap. 6 + `sklearn.model_selection` |

O Canty também assume que você aceita comparar classificadores na **mesma** amostra de teste: sem isso, McNemar e “A vs B” não fazem sentido. Em Python, ajuda saber o que é um estimador `fit`/`predict` e o que significa `random_state` para reprodutibilidade.

## 2. Intuição do problema (sem equação)

No Cap. 6 as classes eram elipses no espaço de bandas. Na vida real, a nuvem de “área urbana” pode ter forma de banana, multimodal (telhado claro + asfalto + sombra), e a fronteira com “solo exposto” pode ser irregular. Um modelo que só desenha elipses erra de forma sistemática.

Além disso, dois mapas podem ter a **mesma** acurácia global e errar em lugares diferentes: um confunde rio com sombra; outro confunde pasto seco com solo. Decidir qual classificador “é melhor” exige mais do que um único percentual.

Três metáforas úteis:

1. **SVM** — em vez de modelar o miolo de cada classe, concentra-se na **cerca** entre elas e escolhe a cerca com maior margem de segurança.
2. **Rede neural** — empilha transformações não lineares até que, num espaço interno, as classes fiquem mais fáceis de separar; o preço é precisar de mais dados e de disciplina de treino (Apêndice B).
3. **Ensemble (floresta / boosting)** — vários classificadores fracos votam ou se corrigem; o erro individual se dilui se os membros erram de formas diferentes.

A avaliação deixa de ser “acertei quantos?” e passa a incluir: acertei **quais** classes, o acordo além do acaso (kappa), a diferença entre dois modelos é ruído ou sinal (McNemar), e meu protocolo de teste é honesto no espaço.

## 3. O que o Canty ensina neste capítulo (mapa das seções + ideias-chave)

Mapa mental do Cap. 7 (agrupando o fio do livro):

| Bloco | Ideia-chave | No repositório |
|-------|-------------|----------------|
| Limitações do ML gaussiano | Forma de classe, dimensionalidade, robustez | Motivação de `ex07_1` |
| SVM | Margem, vetores de suporte, kernels | `supervisedclass.py` / `classify.py -a 7` (SVM); sklearn `SVC` |
| Redes (FFNN / variantes de treino) | Backprop, gradiente conjugado, Kalman; DNN | `classify.py -a 3..6`; Apêndice B |
| Boosting / ensembles | Combinar hipóteses fracas | `legado/canty/auxil/scripts/adaboost.py`; RF no classify |
| Métricas | Overall accuracy, kappa | `ex07_1`, `classification_report` |
| Comparação de dois classificadores | McNemar em pares acerto/erro | `legado/canty/auxil/scripts/mcnemar.py`; trecho em `ex07_1` |
| Validação cruzada | Estabilidade da estimativa de erro | `legado/canty/auxil/scripts/crossvalidate.py` |

Ideias-chave:

- Trocar de algoritmo **sem** melhorar amostras e protocolo de validação raramente salva um mapa.
- Kappa corrige acordo esperado pelo acaso, mas não substitui olhar erros por classe nem o padrão espacial do erro.
- McNemar responde: “na *mesma* amostra, A e B diferem de forma significativa nos erros?”, não “qual tem maior acurácia no absoluto”.

## 4. Desenvolvimento guiado (conceitos do livro, com derivação/explicação acessível)

### 4.1 Por que ir além do ML gaussiano?

Motivos frequentes em imagens:

1. **Densidades não gaussianas / multimodais.** Uma classe “agricultura” mistura estágios fenológicos.
2. **Muitas bandas, poucas amostras.** Estimar $\boldsymbol{\Sigma}_k$ cheia fica instável (já visto no Cap. 6).
3. **Atributos heterogêneos.** Juntar bandas, índices, DEM, textura: hipóteses de normalidade conjunta enfraquecem.
4. **Fronteiras complexas.** Interação não linear entre atributos.
5. **Outliers e mistura.** Um único pixel misturado puxa média e covariância.

Isso não invalida o ML gaussiano: ele continua sendo o **baseline interpretável**. O Cap. 7 acrescenta ferramentas quando o baseline saturua.

### 4.2 SVM — intuição e o mínimo de formalismo

Considere duas classes linearmente separáveis. Há infinitos hiperplanos que separam os pontos de treino. A SVM de margem máxima escolhe o hiperplano que maximiza a distância até os pontos mais próximos (os **vetores de suporte**).

Para o caso soft-margin (dados não perfeitamente separáveis), admite-se uma folga e se penaliza violações com um parâmetro $C$: $C$ grande → menos tolerância a erro de treino (risco de overfit); $C$ pequeno → margem mais “folgada”.

Quando a separação linear no espaço original falha, um **kernel** $K(\mathbf{x},\mathbf{x}')$ implementa um produto interno num espaço de maior dimensão sem calcular o mapa explicitamente. O kernel RBF

```math
K(\mathbf{x},\mathbf{x}') = \exp\bigl(-\gamma\|\mathbf{x}-\mathbf{x}'\|^2\bigr)
```

é o default prático em muitos tutoriais. Intuição: “pontos próximos no espaço de atributos influenciam a decisão localmente”.

Em SR: SVM brilha com **poucas amostras bem escolhidas** e fronteiras não lineares; pode ficar lento e sensível a escala (normalize!) com dezenas de milhares de pixels de treino. No `ex07_1.py`, o `SVC(kernel="rbf")` só entra se a dimensão/amostra for modesta — de propósito.

### 4.3 Redes neurais em alto nível + ponte ao Apêndice B

Uma rede feed-forward rasas/MLP compõe

$$
\mathbf{x} \mapsto \mathbf{h}^{(1)} = f(\mathbf{W}^{(1)}\mathbf{x}+\mathbf{b}^{(1)}) \mapsto \cdots \mapsto \text{saídas (scores / softmax)}.
$$

Cada camada introduz não linearidade ($f$ = ReLU, tanh, etc.). Diferente do ML gaussiano, **não** se assume forma elíptica das classes: a fronteira é aprendida pelos pesos.

O Cap. 7 do Canty discute arquiteturas e variantes de treinamento usadas no ecossistema do livro (back-propagation, scaled conjugate gradient, filtro de Kalman estendido; depois DNN via TensorFlow). O **como** minimizar a função de custo, regularizar e evitar overfit está concentrado no **Apêndice B**.

Leitura operacional neste repo:

- Entender o *papel* da rede: Cap. 7 (este texto) + `classify.py` algoritmos 3–6.
- Entender o *treino*: `Appendix_B_.../aulas/` e o PDF do apêndice.
- Para o exercício didático do capítulo, preferimos RF/NB/SVM em sklearn — redes profundas ficam como leitura e experimento opcional.

### 4.4 Boosting e ensembles

**Bagging (ex.: Random Forest):** treina várias árvores em bootstrap das amostras (e, no RF, subconjuntos aleatórios de atributos em cada divisão). A predição final é voto majoritário (classificação). Reduz variância; tolera outliers melhor que uma única árvore profunda.

**Boosting (ex.: AdaBoost, depois gradient boosting):** treina hipóteses em sequência, aumentando o peso dos exemplos que a hipótese anterior errou. O livro aponta AdaBoost; o script `legado/canty/auxil/scripts/adaboost.py` ilustra o fluxo. Na prática moderna de dados tabulares, XGBoost/LightGBM/CatBoost são os herdeiros mais usados — ver seção 5.

Intuição única: ensembles funcionam quando os membros são **razoavelmente bons e diversificados**. Cem cópias do mesmo erro não ajudam.

### 4.5 Acurácia, kappa e leitura por classe

Com matriz de confusão $C$ ($C_{ij}$ = verdade $i$, predito $j$) e $N=\sum_{ij} C_{ij}$:

**Acurácia global (overall accuracy)**

$$
p_o = \frac{1}{N}\sum_{i} C_{ii}.
$$

**Acurácia do produtor (recall da classe $i$)** — “dos que são realmente $i$, quantos acertei?”

$$
\frac{C_{ii}}{\sum_j C_{ij}}.
$$

**Acurácia do usuário (precision da classe $i$)** — “dos que chamei de $i$, quantos eram $i$?”

$$
\frac{C_{ii}}{\sum_j C_{ji}}.
$$

(Confirme a orientação da sua matriz; a intuição precision/recall é o que importa.)

**Kappa de Cohen**

$$
\kappa = \frac{p_o - p_e}{1 - p_e},
$$

onde $p_e$ é o acordo esperado se as previsões fossem independentes das verdades, tipicamente

$$
p_e = \sum_i \Bigl(\frac{\sum_j C_{ij}}{N}\Bigr)\Bigl(\frac{\sum_j C_{ji}}{N}\Bigr).
$$

$\kappa\approx 0$ ≈ acordo de acaso; $\kappa\to 1$ acordo alto além do acaso. Limitações: kappa é discutido na literatura (depende da prevalência das classes); use-o **junto** com métricas por classe e com o mapa de erros, nunca sozinho como selo de qualidade.

No `ex07_1.py`: `accuracy_score`, `cohen_kappa_score`, `classification_report`.

### 4.6 McNemar: comparar dois classificadores na mesma amostra

Sejam A e B dois classificadores avaliados nos **mesmos** pixels de teste. Monte a tabela 2×2 de acertos/erros:

|  | B acerta | B erra |
|--|----------|--------|
| **A acerta** | $n_{11}$ | $n_{10}$ |
| **A erra** | $n_{01}$ | $n_{00}$ |

O teste de McNemar foca em $n_{01}$ e $n_{10}$ (discordâncias). Uma estatística comum com correção de continuidade é

$$
\chi^2 = \frac{\bigl(|n_{01}-n_{10}|-1\bigr)^2}{n_{01}+n_{10}},
$$

comparada a uma $\chi^2_1$. Ideia: se A e B fossem equivalentes em taxa de erro, esperamos $n_{01}\approx n_{10}$.

Útil quando as acurácias globais são parecidas (“0,872 vs 0,875”) e você quer saber se a diferença é flutuação. Implementação de referência do livro: `legado/canty/auxil/scripts/mcnemar.py`. O `ex07_1.py` imprime um McNemar simplificado entre o primeiro e o segundo modelo da lista (NB vs RF).

Cuidado: pixels de teste espacialmente correlacionados **também** afetam a independência das observações do teste — McNemar herda o protocolo de amostragem.

### 4.7 Validação cruzada

Em $k$-fold, parte-se os dados em $k$ blocos; treina em $k-1$, testa em 1, rota e média o erro. Reduz a dependência de um único split.

Em sensoriamento remoto o aviso do Cap. 6 volta com força:

1. Fold **aleatório por pixel** ignora autocorrelação → métricas otimistas.
2. Prefira folds por **blocos espaciais**, polígonos, tiles ou datas.
3. Se só houver pontos de campo, use CV estratificada e reporte o desenho amostral.
4. Nested CV entra quando há hiperparâmetros ( $C$, $\gamma$, profundidade de árvore) a tunar sem vazar informação para o teste.

Script de referência: `legado/canty/auxil/scripts/crossvalidate.py`. O exercício `ex07_1` usa um único hold-out estratificado de propósito didático — consciente de que, com rótulos sintéticos densos, o número ainda é otimista.

### 4.8 O exercício `ex07_1`: NB vs Random Forest

Fluxo:

1. Mesma lógica de rótulos do Cap. 6 (raster sintético + limiar NDVI-like, ou gaussianas 2D).
2. Subamostra de pixels → `train_test_split` estratificado.
3. `StandardScaler` no treino; aplica no teste.
4. Treina `GaussianNB` e `RandomForestClassifier` (e SVM RBF se a carga for leve).
5. Imprime acurácia, kappa, confusão, `classification_report`.
6. McNemar simplificado NB vs RF.
7. Mapa do melhor modelo em `figuras/ex07_1_comparison_map.png`.

Interpretação honesta: RF quase sempre “ganha” em atributos correlacionados com um limiar NDVI porque árvores recortam o espaço com partições flexíveis. Isso demonstra o *pipeline de comparação*, não coroa RF como verdade absoluta para coberturas reais.

## 5. Além do livro (prática moderna, armadilhas, ligação com sklearn/GEE/SAR/mestrado)

**Random Forest** tornou-se o cavalo de batalha em classificação pixel-a-pixel com atributos tabulares (bandas + índices + DEM). No GEE, `smileRandomForest` é o exemplo padrão dos codelabs. Hiperparâmetros que mais importam na prática: número de árvores, profundidade máxima, e o desenho amostral — mais do que micro-otimizar `max_features`.

**XGBoost / LightGBM:** boosting de gradiente em árvores; frequentemente lideram benchmarks tabulares. Exigem mais cuidado com overfit e com vazamento espacial na validação. Não estão no núcleo do Canty 2019, mas são o “além” natural do capítulo de ensembles.

**U-Net e segmentação semântica:** em vez de classificar cada pixel de forma i.i.d., redes convolucionais usam contexto espacial (vizinhança) e geram mapas densos. É o salto típico de projetos/pca-e-agrupamento/doutorado em deep learning para SR — **além do livro**, mas alinhado à crítica do Cap. 7: o modelo certo depende da estrutura do dado. Treino exige mais dados rotulados, GPU e disciplina de generalização espacial (tiles de teste em outra região/data).

**sklearn.** Além de NB/RF/SVM: `GradientBoostingClassifier`, `HistGradientBoostingClassifier`, métricas em `sklearn.metrics`, CV em `model_selection`. Para McNemar formal, `statsmodels` ou a fórmula do livro/`mcnemar.py`.

**SAR / polarimetria.** Ensembles e redes com atributos polarimétricos ou CNN em patches costumam superar gaussiano óptico “cego”. Speckle e distribuição não gaussiana reforçam a mensagem deste capítulo.

**Desbalanceamento e desenho amostral**

- Classes raras (desmatamento, lamaçal, telhado específico): acurácia global mente; use recall/precision da classe rara, F1, ou médias macro.
- Strategies: oversample da classe rara no treino, undersample da dominante, *class_weight*, ou amostragem estratificada por área.
- Nunca avalie só nos pixels fáceis do interior de polígonos grandes; inclua bordas e confusões esperadas.
- Separe treino/teste no **espaço** (e, em séries, no **tempo**).

**Armadilha de mestrado:** publicar “RF 94%” com validação aleatória na mesma cena e rótulos correlacionados ao NDVI. O comitê vai perguntar pelo protocolo — tenha a resposta pronta (este guia §4.7 e Cap. 6 §4.2).

## 6. Como praticar neste repositório (notebook + exercícios + outputs)

Ordem sugerida:

1. Revisar Cap. 6 (`00_teoria.md` + saída de `ex06_1`) se Bayes/QDA ainda estiver fresco demais ou frio demais.
2. Ler este guia até §4.8.
3. Abrir `notebooks/07_teoria.ipynb`.
4. Rodar:

```bash
python conteudo/classificacao/redes-e-avaliacao/exercicios/ex07_1.py
```

5. Conferir o PNG `figuras/ex07_1_comparison_map.png` e a tabela McNemar no terminal.
6. (Opcional.) Explorar referências do livro:

| Artefato | Papel |
|----------|--------|
| `legado/canty/auxil/scripts/classify.py` | Menu de algoritmos (MaxLike, kernels, redes, SVM, RF) |
| `legado/canty/auxil/supervisedclass.py` | Classes `Maxlike`, SVM, redes, etc. |
| `legado/canty/auxil/scripts/crossvalidate.py` | CV no espírito do livro |
| `legado/canty/auxil/scripts/mcnemar.py` | Comparação formal A vs B |
| `legado/canty/auxil/scripts/adaboost.py` | Boosting |
| Apêndice B | Treino / regularização de redes |

Raster: `data/exemplos/exemplo_sintetico.tif` (mesmo do Cap. 6).

## 7. Checklist de domínio + dúvidas típicas

**Checklist**

- [ ] Sei dizer pelo menos três motivos para sair do ML gaussiano.
- [ ] Explico SVM como margem + (opcionalmente) kernel, sem misturar com “é uma rede”.
- [ ] Sei onde estudar o treino de redes (Apêndice B) vs o papel delas (este capítulo).
- [ ] Distingo bagging (RF) de boosting (AdaBoost / XGBoost).
- [ ] Interpreto $p_o$, precision/recall por classe e $\kappa$.
- [ ] Sei montar $n_{01}$, $n_{10}$ e o que McNemar testa.
- [ ] Consigo criticar um paper que só reporta overall accuracy com split aleatório.
- [ ] Olhando `ex07_1`, não confundo vitória do RF em rótulo sintético com validação de mapa real.
- [ ] Tenho consciência de desbalanceamento e de RF/XGBoost/U-Net como horizonte além do Canty.

**Dúvidas típicas**

1. *“RF ganhou do NB no ex07_1 — posso largar Bayes?”*  
   Não. NB/QDA continuam baselines rápidos e interpretáveis. Em dados verdadeiramente gaussianos e poucos parâmetros, o modelo paramétrico pode ser melhor e mais estável.

2. *“Kappa 0,8 é ‘muito bom’?”*  
   Depende do número e da prevalência das classes e do protocolo. Prefira mostrar a matriz e as métricas por classe; use faixas de kappa só como linguagem informal.

3. *“McNemar deu não significativo, mas a acurácia de B é maior.”*  
   Com a amostra de teste que você tem, a diferença de erros discordantes não se distingue de flutuação. Aumente teste independente ou aceite empate prático.

4. *“Quando usar SVM em vez de RF?”*  
   Poucas amostras, problema mais binário ou com margem clara após boa normalização; ou quando quiser kernel explícito. Para atributos tabulares mistos e treino médio/grande, RF (ou boosting) costuma ser mais simples de calibrar.

5. *“Preciso de U-Net para o exercício do livro?”*  
   Não. U-Net é horizonte moderno (seção 5). O capítulo se completa com sklearn + scripts `auxil` + Apêndice B.

6. *“Minha classe rara some no mapa.”*  
   Olhe recall dessa classe, pesos de classe, amostragem dirigida e se o prior/limiar está enterrando a classe. Acurácia global pode subir enquanto a classe de interesse desaparece.

7. *“Validação cruzada no GEE/sklearn já resolve autocorrelação?”*  
   Só se os folds forem espacialmente sensatos. CV aleatória por pixel não “resolve” — muitas vezes piora a autoilusão.

---

*Fechamento do arco supervisionado (Caps. 6–7):* do Bayes gaussiano ao cardápio de modelos e à disciplina de avaliação. O Cap. 8 parte para o caso **sem** rótulos de treino (agrupamento); o Cap. 9, para mudança no tempo.
