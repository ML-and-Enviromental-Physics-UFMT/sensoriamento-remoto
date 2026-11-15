# Distribuições, médias e estimação

Um histograma resume os valores observados numa imagem. Ele não é a distribuição verdadeira de todos os pixels possíveis nem elimina a necessidade de definir a população que queremos descrever.

Pré-requisito: [probabilidade](probabilidade.md).

## Probabilidade discreta e densidade

Numa variável discreta, como a classe de cobertura, podemos atribuir probabilidade a cada valor. As probabilidades somam 1. Em um modelo contínuo, usamos uma densidade $f(x)$ e obtemos probabilidades integrando intervalos:

```math
P(a\le X\le b)=\int_a^b f(x)\,dx.
```

A integral representa a área acumulada sob a curva. O valor de $f(x)$ é uma altura, não a probabilidade do valor exato. Para uma distribuição contínua, $P(X=x)=0$, embora intervalos tenham probabilidade positiva. Uma densidade pode ser maior que 1 se sua concentração ocorrer em um intervalo estreito.

Por exemplo, uma variável uniforme entre 0 e 0,2 tem densidade 5 nesse intervalo. A probabilidade de cair entre 0 e 0,1 é $5\cdot0{,}1=0{,}5$, não 5. Arquivos digitais quantizam medições; o modelo contínuo é uma aproximação que deve ser escolhida conscientemente.

## Média e dispersão

A esperança $\mu=E[X]$ é a média da distribuição. A variância $\sigma^2=E[(X-\mu)^2]$ mede dispersão ao redor dela. O desvio-padrão é $\sigma$, na mesma unidade de $X$; a variância tem unidade ao quadrado.

Para $n$ observações, estimamos a média por $\bar x=\sum_i x_i/n$. Sob amostragem independente da mesma distribuição com variância finita, a variância amostral não viesada é

$$s^2=\frac{1}{n-1}\sum_{i=1}^n(x_i-\bar x)^2,\qquad n>1.$$

O divisor $n-1$ decorre de estimar a média com os mesmos dados. Ele não corrige dependência espacial, seleção enviesada ou valores inválidos.

## Exemplo resolvido

Três reflectâncias hipotéticas são 0,1, 0,2 e 0,3. A média é $(0{,}1+0{,}2+0{,}3)/3=0{,}2$. Os desvios são $-0{,}1$, 0 e 0,1; seus quadrados somam 0,02. A variância amostral é $0{,}02/2=0{,}01$ e o desvio-padrão é 0,1.

Se estivermos descrevendo apenas esse conjunto finito inteiro, a média dos quadrados dos desvios usa divisor 3 e vale aproximadamente 0,00667. A fórmula depende da pergunta: descrição do conjunto ou estimação de uma variância populacional sob hipóteses.

Uma distribuição normal de média $\mu$ e variância $\sigma^2>0$ tem densidade

$$f(x)=\frac{1}{\sqrt{2\pi}\sigma}\exp\left[-\frac{(x-\mu)^2}{2\sigma^2}\right].$$

Seu formato pode ser útil como modelo de medições ou de classes. Porém, uma cena que mistura água, solo, vegetação e sombra não precisa ter distribuição normal. Um histograma parecido com um sino também não prova normalidade.

## Incerteza da estimativa e desenho amostral

O erro-padrão da média, sob independência e condições usuais, é estimado por $s/\sqrt n$. No exemplo, seria aproximadamente 0,0577. Isso não é o desvio-padrão dos pixels: resume a incerteza da média sob o modelo de amostragem.

Milhares de pixels vizinhos não equivalem necessariamente a milhares de observações independentes. Para intervalos e validação, considere blocos, unidades amostrais e representatividade. Não há um intervalo de confiança universal que se torne correto apenas aumentando o número de pixels.

Estimar a média ou ajustar um modelo usa dados para aprender parâmetros. Avaliar o modelo pergunta como ele funciona em observações separadas. Usar os mesmos dados nas duas tarefas pode produzir uma avaliação otimista.

## Pratique

1. A média dos valores 1, 2 e 3 é 2. Qual é a variância amostral e qual é a variância descritiva do conjunto?
2. A densidade uniforme em um intervalo de largura 0,5 pode ter altura 2?
3. O divisor $n-1$ corrige uma amostra formada só por pixels de uma única área fácil de classificar?

<details><summary>Respostas comentadas</summary>

1. Os quadrados dos desvios somam 2. Com divisor 2, a amostral é 1; com divisor 3, a descritiva é $2/3$.
2. Sim. Altura 2 vezes largura 0,5 dá área total 1. A altura não é uma probabilidade pontual.
3. Não. Esse divisor não resolve seleção nem falta de representatividade. É preciso rever como os dados foram amostrados.

</details>

Fonte: Canty (2019), seções 2.1–2.2. Exemplos autorais. [Covariância](covariancia.md) · [Índice](../README.md).
