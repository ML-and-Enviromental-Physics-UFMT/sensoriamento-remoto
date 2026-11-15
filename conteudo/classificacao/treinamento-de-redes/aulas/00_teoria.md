# Apêndice B — Treinamento de redes neurais (manual de serviço)

> Referência: Canty, M. J. (2019), Appendix B — Neural Network Training.  
> Stub curto: [`treino_redes.md`](treino_redes.md).  
> Ponte direta: [Cap. 6](../../supervisionada/aulas/00_teoria.md) (papel do classificador) e [Cap. 7](../../redes-e-avaliacao/aulas/00_teoria.md) (redes, SVM, avaliação).

---

## 0. Para quem / objetivos

Para quem chegou aos Caps. 6–7 e precisa entender **como** uma rede aprende pesos a partir de amostras rotuladas — função de custo, backpropagation, overfitting e freios (regularização, early stopping) — sem transformar este apêndice num curso completo de deep learning.

Ao terminar, você deve conseguir:

1. Descrever perceptron / MLP como composição de combinações lineares + não linearidades.
2. Relacionar *loss* ao erro de classificação / ajuste nos rótulos.
3. Explicar backprop como “regra da cadeia organizada” para obter gradientes.
4. Diagnosticar overfitting e citar regularização e early stopping como remédios clássicos do livro.
5. Situar o Apêndice B como **oficina de treino**; Caps. 6–7 como **papel na classificação de imagem**.
6. Separar o que é Canty (2019) do que é nota moderna (Adam, dropout) na seção 5.

---

## 1. Pré-requisitos

| Tema | Onde | Por quê |
|------|------|---------|
| Classificação supervisionada | Cap. 6 | Redes também mapeiam $\mathbf{x}\mapsto\hat{y}$, sem hipótese gaussiana |
| Amostras de treino / teste, kappa | Cap. 7 | Avaliar rede como qualquer classificador |
| Vetores, produtos $\mathbf{W}\mathbf{x}$ | Apêndice A | Camadas são matrizes |
| Gradiente (ideia) | Cálculo básico | Passo de descida |

Não é necessário dominar TensorFlow/PyTorch na primeira passagem. O livro e `legado/canty/auxil/supervisedclass.py` / `classify.py` trazem o fluxo histórico; este texto fixa a intuição.

---

## 2. Intuição

Uma rede neural rasa (MLP) é uma máquina de **fronteiras flexíveis** no espaço espectral. O Cap. 6 parte de elipses gaussianas; a rede parte de hiperplanos empilhados com funções de ativação (sigmoide, tanh, ReLU…) e, com profundidade/largura suficientes, aproxima fronteiras bem mais tortuosas.

Treinar é ajustar pesos $\boldsymbol{\theta}$ para que, nas amostras $(\mathbf{x}_i,y_i)$, a saída $f(\mathbf{x}_i;\boldsymbol{\theta})$ fique perto de $y_i$ segundo uma **loss** $L$. O algoritmo de aprendizado (gradiente, gradiente conjugado, etc., no espírito do Canty) **desce** $L$ no espaço de pesos.

Dois extremos a evitar:

- **Subajuste:** rede demais linear / treino curto → parece um classificador fraco.
- **Sobreajuste:** memoriza ruído e pixels de treino → ótimo no treino, frágil no mapa e no teste.

O Apêndice B é o manual da oficina: como girar os parafusos do treino. Os Caps. 6–7 decidem *quando* vale a pena usar a rede no lugar do ML gaussiano, da SVM ou do boosting.

---

## 3. Mapa do que o apêndice cobre

| Bloco no espírito do Apêndice B | Conteúdo | Ligação no repo |
|----------------------------------|----------|-----------------|
| Perceptron / MLP | Arquitetura, forward pass | `supervisedclass.py`, `classify.py` |
| Função de custo (loss) | Erro a minimizar | Mesmos scripts; Cap. 7 métricas *depois* do treino |
| Backpropagation | Gradientes camada a camada | Intuição aqui; detalhe no PDF |
| Algoritmos de treino | GD, variantes do livro (conjugado, Kalman…) | PDF + `classify.py -a …` |
| Generalização | Overfitting, regularização, early stopping | Caps. 6–7 (split treino/teste) |
| Notas modernas | Adam, dropout | Seção 5 (*além do Canty*) |

O PDF `Appendix_B_Neural_Network_Training.pdf` permanece a referência de derivações e dos métodos específicos adotados no texto.

---

## 4. Desenvolvimento guiado

### 4.1 Perceptron e MLP

**Perceptron (visão didática).** Uma unidade calcula $z=\mathbf{w}^\top\mathbf{x}+b$ e aplica ativação $\sigma(z)$ (historicamente degrau ou sigmoide). Em classificação binária, o sinal de $z$ (ou limiar em $\sigma$) define o lado do hiperplano.

**MLP (multilayer perceptron).** Empilha camadas:

```math
\mathbf{h}^{(1)} = \sigma\!\left(\mathbf{W}^{(1)}\mathbf{x}+\mathbf{b}^{(1)}\right),
\quad
\mathbf{h}^{(2)} = \sigma\!\left(\mathbf{W}^{(2)}\mathbf{h}^{(1)}+\mathbf{b}^{(2)}\right),
\quad \ldots
```

até uma saída (logits / probabilides por classe). Cada $\mathbf{W}^{(\ell)}$ é uma matriz de pesos — daí o Apêndice A.

Em SR, $\mathbf{x}$ é tipicamente o vetor espectral (e eventualmente atributos derivados). A rede **não** assume $\mathcal{N}(\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)$; ela aprende a forma da fronteira se houver dados e regularização suficientes.

### 4.2 Loss (função de custo)

A loss $L(\boldsymbol{\theta})$ agrega o desajuste entre previsão e rótulo. Exemplos de família (nomes modernos para ancorar a intuição):

- Erro quadrático (mais clássico em regressão / alguns treinos antigos);
- Entropia cruzada / log-loss em classificação probabilística.

O ponto do apêndice: **treinar = otimizar $L$** em $\boldsymbol{\theta}$. Acurácia, kappa e McNemar (Cap. 7) avaliam o produto **depois**; não substituem a loss no laço de treino, embora monitorem o mesmo fenômeno (acerto/erro).

### 4.3 Backpropagation — intuição

O forward pass calcula saídas camada a camada. Para atualizar pesos, precisamos $\partial L/\partial W_{ij}^{(\ell)}$. A **backpropagation** aplica a regra da cadeia de trás para frente: o erro na saída propaga-se às camadas ocultas, reutilizando cálculos intermediários.

Metáfora: cada camada pergunta “quanto eu contribuí para o erro final?” e recebe um sinal local. Com esses gradientes, um passo do tipo

```math
\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \eta\,\nabla_{\boldsymbol{\theta}} L
```

(ou uma variante mais sofisticada do livro) move os pesos na direção que reduz $L$ localmente. $\eta$ é a taxa de aprendizado: grande demais oscila; pequena demais demora ou fica presa.

Você **não** precisa expandir todas as derivadas na primeira leitura. Precisa saber: sem gradientes eficientes, MLP com milhares de pesos seria impraticável; backprop é essa eficiência.

### 4.4 Overfitting

Sintoma clássico:

- Loss / acurácia no **treino** excelentes;
- No **teste** (ou no mapa visual fora das amostras) desempenho cai;
- Fronteiras absurdamente irregulares no espaço espectral.

Em SR o risco é agudo: amostras espacialmente correlacionadas fazem o “teste aleatório” parecer fácil (Cap. 7 já alerta). Uma rede com capacidade alta memoriza IDs de pixel disfarçados de espectro.

### 4.5 Regularização e early stopping

**Regularização.** Penalizar pesos grandes (ex.: termo $`\lambda\|\boldsymbol{\theta}\|^2`$ na loss) ou restringir arquitetura (poucas unidades ocultas). Intuição: preferir funções mais suaves, alinhadas à ideia de margem / simplicidade.

**Early stopping.** Monitorar erro num conjunto de validação durante o treino; parar quando o erro de validação sobe de forma sustentada, mesmo que o erro de treino ainda caia. É um freio barato e muito usado — espírito plenamente compatível com o Apêndice B / prática do livro.

Outros freios no mesmo espírito: mais dados / melhor amostragem; redução de atributos (PCA); ensembles (Cap. 7) em vez de uma rede enorme.

### 4.6 Ponte explícita Caps. 6–7 ↔ Apêndice B

| Pergunta | Cap. 6–7 | Apêndice B |
|----------|----------|------------|
| Que modelo usar? | ML gaussiano, SVM, RF, rede… | — |
| Como a rede atualiza pesos? | Menção / uso via `classify` | Loss, backprop, otimizadores |
| A rede generalizou? | Kappa, matriz de confusão, McNemar, CV | Overfit, regularização, early stopping |
| Hipótese gaussiana? | Cap. 6 assume; rede não | Rede como alternativa flexível |

Neste estudo, os exercícios dos Caps. 6–7 privilegiam sklearn (GaussianNB, QDA, RF, SVM) para o fluxo didático. Redes do ecossistema Canty entram via:

- `legado/canty/auxil/supervisedclass.py`
- `legado/canty/auxil/scripts/classify.py` (algoritmos `-a` na faixa de redes, conforme README/ajuda do script)

O Apêndice B explica o *porquê* de você não “só apertar classify” sem olhar curva de treino/validação.

### 4.7 Mini-roteiro de estudo

1. Releia Cap. 6: o que a gaussiana *não* cobre.  
2. Leia esta seção 4 até early stopping.  
3. No Cap. 7, compare métricas entre um modelo linear/raso e um mais flexível.  
4. Abra o PDF do Apêndice B nas seções de backprop / algoritmos do autor.  
5. Só então experimente `classify.py` com rede, com split honesto de treino/validação/teste.

---

## 5. Além do livro (notas modernas)

Canty (2019) fixa o núcleo clássico de treino. Práticas que você encontrará fora do texto — **úteis, mas marcadas como além**:

- **Adam / RMSProp / momentum:** adaptam passo por parâmetro; hoje default em deep learning. O livro discute outras estratégias de otimização; a intuição “descer $\nabla L$ com cuidado” permanece.
- **Dropout:** desliga unidades aleatoriamente no treino — regularização por ruído; comum em redes profundas, menos central no MLP raso espectral do livro.
- **ReLU, batch norm, redes profundas / CNNs:** operam em patch ou em imagem; mudam o atributo de “vetor de bandas” para “contexto espacial”. Fora do escopo mínimo do Apêndice B, mas são a continuação natural se você seguir para deep learning em SR.
- **Frameworks:** PyTorch/TensorFlow vs implementações `auxil` — mesma geometria de treino, outra engenharia.

Use essas notas para ler papers atuais sem achar que o Canty “está errado”: o apêndice ensina o mecanismo; a indústria mudou os defaults.

---

## 6. Como os outros capítulos usam este apêndice

| Capítulo / artefato | Uso |
|---------------------|-----|
| Cap. 6 | Rede como alternativa ao ML gaussiano; baseline paramétrico primeiro |
| Cap. 7 | Incluir redes na comparação; avaliação (kappa, McNemar) *após* treino cuidadoso |
| `legado/canty/auxil/scripts/classify.py` | Entrada prática aos classificadores do livro (incl. redes) |
| `legado/canty/auxil/supervisedclass.py` | Implementações |
| `legado/canty/auxil/scripts/adaboost.py` | Ensemble (vizinho do Cap. 7; não é backprop, mas mesmo espírito de “além do ML”) |
| Stub [`treino_redes.md`](treino_redes.md) | Ponte curta Cap. 6–7 ↔ apêndice |

Não há `exB_*` dedicado neste repo: a prática é (1) dominar avaliação no Cap. 7 com sklearn e (2) só então reproduzir treino de rede via `classify.py` / PDF, olhando overfitting de frente.

---

## 7. Checklist + dúvidas

**Checklist**

- [ ] Descrevo forward pass de um MLP em uma frase.
- [ ] Sei que treinar = minimizar loss em $\boldsymbol{\theta}$, e que kappa vem depois.
- [ ] Explico backprop como regra da cadeia para gradientes (sem exigir todas as derivadas).
- [ ] Reconheço overfitting e cito regularização + early stopping.
- [ ] Distingo o papel do Apêndice B (oficina) do papel dos Caps. 6–7 (classificação / avaliação).
- [ ] Sei onde ficam `supervisedclass.py` e `classify.py`.
- [ ] Marco Adam/dropout como *além do Canty*, não como conteúdo central do PDF de 2019.

**Dúvidas**

1. Com o tamanho da sua amostra de treino espectral, quantas unidades ocultas ainda são razoáveis antes do overfit?
2. Seu protocolo de split é por pixel aleatório ou por bloco espacial? (A rede sente a diferença.)
3. Se a loss de treino cai e a de validação sobe, você para (early stopping) ou regulariza mais — ou as duas?
4. Em que cenário você **não** trocaria QDA/SVM por MLP neste dataset?

Quando essas perguntas tiverem resposta operacional, o Apêndice B cumpriu o ofício: tornar o treino de redes um processo **controlado**, plugado aos Caps. 6–7, em vez de uma caixa-preta que só vomita mapa colorido.
