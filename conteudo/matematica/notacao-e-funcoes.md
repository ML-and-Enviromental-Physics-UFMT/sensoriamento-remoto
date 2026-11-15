# Como ler a notação e as funções

Uma fórmula comprime uma sequência de operações. Para começar, vale traduzir cada símbolo para uma instrução, em vez de tentar memorizar o desenho inteiro.

## Valores, variáveis e índices

Um escalar é um número. Uma variável representa um valor que pode mudar. Em `y = 2*x + 1`, a função recebe `x`, multiplica por 2, soma 1 e devolve `y`. Para `x = 3`, a saída é 7.

Uma função não precisa representar uma relação causal. Pode ser apenas uma regra de processamento. Uma conversão de código digital para grandeza física, por exemplo, precisa ser definida pela documentação do produto, não inventada a partir da aparência dos valores.

O subscrito identifica uma posição ou categoria. Se os valores são $x_1=2$, $x_2=4$ e $x_3=6$, a expressão $x_i$ significa o valor da posição $i$. Em uma matriz, $x_{ij}$ indica linha $i$ e coluna $j$. Python costuma contar posições a partir de zero; as fórmulas deste percurso normalmente começam em 1.

## O somatório

O símbolo $\sum$ instrui a somar uma sequência. A expressão

$$\sum_{i=1}^{3}x_i=x_1+x_2+x_3=2+4+6=12.$$

A média escreve a soma dividida pela quantidade de valores:

$$\bar x=\frac1n\sum_{i=1}^{n}x_i.$$

Com $n=3$, a média é $12/3=4$. A barra sobre $x$ identifica a média, não uma nova medição.

## Parênteses e quadrados fazem diferença

Compare a média dos quadrados, $(2^2+4^2+6^2)/3=56/3$, com o quadrado da média, $4^2=16$. Eles não são a mesma operação.

Para os desvios em relação à média, temos $(-2,0,2)$. A soma dos desvios é zero. Por isso usamos quadrados para medir dispersão: $(-2)^2+0^2+2^2=8$. Somar desvios com sinal não descreve seu tamanho total.

## Compor funções

Se $g(x)=2x+1$ e $f(z)=z^2$, então $f(g(x))=(2x+1)^2$. Para $x=3$, primeiro calculamos $g(3)=7$ e depois $f(7)=49$. Trocar a ordem dá $g(f(3))=g(9)=19$.

A composição aparece quando uma entrada passa por várias etapas de um modelo. A [regra da cadeia](calculo/derivadas-e-gradientes.md) descreve como uma mudança se propaga por essas etapas.

## Símbolos que reaparecem

| Notação | Leitura neste percurso |
|---------|------------------------|
| $\mathbb R$ | Conjunto dos números reais |
| $\mathbb R^p$ | Vetores reais com $p$ coordenadas |
| $A^\top$ | Transposta da matriz |
| $A^{-1}$ | Inversa, quando existe; não é dividir 1 por cada elemento |
| $\Vert x\Vert$ | Norma, uma medida de tamanho especificada no contexto |
| $\mu$, $\Sigma$ | Frequentemente média e covariância populacionais |
| $\lambda$ | Autovalor ou multiplicador, conforme a definição local |
| $\approx$ | Aproximação, em vez de igualdade exata |

O símbolo não tem significado fixo fora do contexto. Cada tópico deve dizer o que está usando. A letra $p$ pode representar número de bandas em uma página e uma probabilidade em outra expressão explicitamente definida.

## Pratique

1. Para valores 1, 3 e 8, calcule a soma e a média.
2. Se $g(x)=x-2$ e $f(z)=3z$, quanto vale $f(g(5))$?
3. A expressão $A^{-1}$ pode ser calculada para qualquer matriz?

<details><summary>Respostas comentadas</summary>

1. A soma é 12 e a média é 4.
2. Primeiro $g(5)=3$ e depois $f(3)=9$.
3. Não. A inversa usual exige uma matriz quadrada invertível. A operação também é diferente de tomar o inverso de cada número isoladamente.

</details>

Esta página é uma preparação autoral para a notação usada por Canty (2019), seções 1.3 e 2.1, e pelos [livros de álgebra linear](../../referencias/matematica/README.md). [Vetores e matrizes](algebra-linear/vetores-e-matrizes.md) · [Índice de matemática](README.md).
