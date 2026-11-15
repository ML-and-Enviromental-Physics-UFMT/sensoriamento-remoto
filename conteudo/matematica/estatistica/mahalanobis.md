# Distância de Mahalanobis

Um pixel pode estar longe da média numa banda que varia muito e ainda ser comum. A mesma diferença numa banda quase constante pode ser rara. Mahalanobis compara diferenças levando em conta escalas e associações entre variáveis.

Pré-requisitos: [covariância](covariancia.md) e [sistemas e inversa](../algebra-linear/sistemas-e-inversa.md).

## A definição

Para um vetor de medições $x$, média $\mu$ e covariância definida positiva $\Sigma$,

$$d^2=(x-\mu)^\top\Sigma^{-1}(x-\mu).$$

Essa expressão é a distância ao quadrado. A distância é $d=\sqrt{d^2}$. A covariância deve corresponder à população ou ao modelo com que queremos comparar o pixel.

Se $\Sigma=I$, a fórmula vira distância euclidiana ao quadrado. Se for diagonal, divide o quadrado de cada diferença pela variância da respectiva variável. Quando há covariâncias fora da diagonal, também considera a orientação da nuvem.

## Exemplo resolvido por sistema linear

Considere

```math
\mu=\begin{pmatrix}0\\0\end{pmatrix},\quad
\Sigma=\begin{pmatrix}4&0\\0&1\end{pmatrix},\quad
x=\begin{pmatrix}2\\2\end{pmatrix}.
```

A diferença é $\delta=(2,2)^\top$. Em vez de formar a inversa, resolvemos $\Sigma z=\delta$. Obtemos $z=(0{,}5,2)^\top$. Portanto,

$$d^2=\delta^\top z=2\cdot0{,}5+2\cdot2=5,\qquad d=\sqrt5.$$

A primeira diferença contribui 1 porque corresponde a um desvio-padrão. A segunda contribui 4 porque corresponde a dois desvios-padrão.

```python
import numpy as np
Sigma = np.diag([4., 1.])
delta = np.array([2., 2.])
d2 = delta @ np.linalg.solve(Sigma, delta)
print(d2, np.sqrt(d2))
```

## A orientação também importa

Para

```math
\Sigma=\begin{pmatrix}2&1\\1&2\end{pmatrix},
```

há maior dispersão na direção $(1,1)$ que na direção $(1,-1)$. Os pontos $(1,1)$ e $(1,-1)$ têm a mesma distância euclidiana da média zero. Suas distâncias de Mahalanobis ao quadrado são, respectivamente, $2/3$ e 2. A diferença anti-diagonal é menos compatível com a variação do modelo.

## Distância não é probabilidade de classe

Em uma normal multivariada com média e covariância verdadeiras conhecidas, $d^2$ tem distribuição qui-quadrado com número de graus de liberdade igual à dimensão. Substituir esses parâmetros por estimativas da mesma amostra altera as condições de inferência. Não aplique automaticamente um limiar teórico como se ele garantisse uma taxa de falso alarme real.

Para comparar classes gaussianas, também entram o determinante da covariância e a probabilidade anterior da classe. Escolher apenas a menor distância não equivale em geral à decisão Bayesiana completa.

Se a covariância for singular, a fórmula usual com inversa não se aplica. Reduzir dimensão ou regularizar pode resolver um problema de modelagem específico. Uma pseudoinversa muda o tratamento das direções sem variância; ela não deve ser apresentada como substituição sem consequências.

## Pratique

1. Com $\Sigma=\operatorname{diag}(9,1)$, qual é $d^2$ para $x=(3,0)$ e média zero?
2. No mesmo modelo, qual é $d^2$ para $(0,3)$?
3. É correto chamar $d^2=0{,}8$ de “80% de probabilidade de pertencer à classe”?

<details><summary>Respostas comentadas</summary>

1. $3^2/9=1$, um desvio-padrão no primeiro eixo.
2. $3^2/1=9$, três desvios-padrão no segundo eixo.
3. Não. Uma distância não é uma probabilidade posterior. Para obter probabilidades é preciso especificar e avaliar um modelo.

</details>

Fontes: Canty (2019), capítulo 2 e classificação gaussiana do capítulo 6; [Penn State, STAT 505, distribuição normal multivariada](https://online.stat.psu.edu/stat505/Lesson04). Exemplos autorais. [Determinantes](../algebra-linear/determinantes.md) · [Índice](../README.md).
