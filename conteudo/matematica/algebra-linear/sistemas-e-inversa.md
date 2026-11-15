# Sistemas lineares e inversa

Uma transformação geométrica ou um ajuste de modelo costuma levar à pergunta: quais valores desconhecidos explicam estas observações? Um sistema linear organiza as equações que essas incógnitas precisam satisfazer.

Pré-requisito: [produtos e transposta](produtos-e-transposta.md).

## Do conjunto de equações à matriz

No sistema

$$2x+y=5,\qquad x-y=1,$$

$x$ e $y$ são as incógnitas. Podemos escrever

```math
Az=b,\qquad
A=\begin{pmatrix}2&1\\1&-1\end{pmatrix},\quad
z=\begin{pmatrix}x\\y\end{pmatrix},\quad
b=\begin{pmatrix}5\\1\end{pmatrix}.
```

Cada linha representa uma equação. As colunas guardam os coeficientes de uma mesma incógnita.

Somando as equações, $3x=6$, então $x=2$. Substituindo na segunda, $y=1$. A conferência é direta: $A(2,1)^\top=(5,1)^\top$. Resolver não é suficiente; substituir a solução ajuda a detectar erros de sinal e de ordem.

## Pode haver uma, nenhuma ou muitas soluções

Se a segunda equação fosse $4x+2y=10$, seria apenas o dobro da primeira. Ela não acrescentaria uma restrição independente. Haveria infinitos pares na reta $2x+y=5$.

Se fosse $4x+2y=11$, as duas exigências seriam incompatíveis e não haveria solução exata. Não é um defeito do algoritmo: os dados do sistema entram em conflito.

Para uma matriz quadrada de ordem $p$, uma solução única para todo $b$ exige posto $p$, isto é, $p$ colunas independentes. Matrizes retangulares também podem ter solução única para certos problemas, mas não têm inversa quadrada usual.

## A inversa desfaz uma transformação

Quando uma matriz quadrada é invertível, existe $A^{-1}$ tal que $A^{-1}A=AA^{-1}=I$. A identidade $I$ mantém o vetor inalterado. No exemplo,

```math
A^{-1}=\begin{pmatrix}1/3&1/3\\1/3&-2/3\end{pmatrix}.
```

Multiplicar por $b$ recupera $z=(2,1)^\top$. A fórmula ajuda a interpretar a transformação, mas no computador não precisamos formar a inversa explicitamente para resolver $Az=b$:

```python
import numpy as np
A = np.array([[2., 1.], [1., -1.]])
b = np.array([5., 1.])
z = np.linalg.solve(A, b)
print(z)                 # [2. 1.]
print(A @ z - b)         # resíduo próximo de zero
```

## Resíduo pequeno não garante solução precisa

O resíduo é $r=b-Az$. Em ponto flutuante, ele pode ser pequeno mesmo quando um sistema mal condicionado torna a solução sensível a pequenas perturbações dos dados. Bandas quase redundantes podem criar esse tipo de dificuldade em matrizes derivadas de imagens.

Se há mais equações que incógnitas e elas não fecham exatamente, podemos procurar o menor resíduo quadrático. Esse é o problema de [mínimos quadrados](condicionamento-e-minimos-quadrados.md), não uma autorização para chamar toda aproximação de solução exata.

## Pratique

1. Resolva $x+y=4$ e $x-y=2$.
2. As equações $x+2y=3$ e $2x+4y=6$ determinam um par único?
3. Por que trocar o segundo lado direito da questão 2 por 7 muda a situação?

<details><summary>Respostas comentadas</summary>

1. Somando, $2x=6$, então $x=3$ e $y=1$. Substituir confirma ambas as equações.
2. Não. A segunda é redundante; há infinitas soluções, como $(3,0)$ e $(1,1)$.
3. O lado esquerdo continua sendo o dobro do primeiro. Ele deveria valer 6, mas passou a exigir 7. Nenhum par atende às duas equações.

</details>

Fonte: Rios, Figueiredo e Cunha, *Álgebra Linear I*, tópicos de inversão e sistemas, aulas 4, 6 e 7 da fonte. Exemplos e código autorais. [Bibliografia](../../../referencias/matematica/README.md) · [Índice](README.md).
