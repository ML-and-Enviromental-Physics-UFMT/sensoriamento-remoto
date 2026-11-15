# Derivadas, gradientes e regra da cadeia

Treinar um modelo exige saber como o erro muda quando alteramos um parâmetro. Uma derivada mede essa variação local. Um gradiente reúne as derivadas em relação a vários parâmetros.

Pré-requisitos: operações com funções, [vetores](../algebra-linear/vetores-e-matrizes.md) e [produtos](../algebra-linear/produtos-e-transposta.md).

## Da variação média à derivada

Para uma função escalar $f$, a taxa média entre $x$ e $x+h$ é $[f(x+h)-f(x)]/h$. A derivada é o limite dessa taxa quando $h$ tende a zero, quando o limite existe:

$$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}h.$$

Se $f(x)=x^2$, expandir $(x+h)^2$ dá $[2xh+h^2]/h=2x+h$. No limite, $f'(x)=2x$. Em $x=3$, a inclinação é 6: uma pequena mudança $h$ altera $f$ em aproximadamente $6h$. Para $h=0{,}01$, a diferença exata é 0,0601, próxima da aproximação 0,06.

A derivada tem unidades de saída por unidade de entrada. Não é automaticamente um efeito causal observado: ela descreve a função ou modelo que você especificou.

## Um erro de previsão com um parâmetro

Suponha uma previsão $\hat y=wx$ e erro $L(w)=(wx-y)^2$. Com entrada $x=2$ e alvo $y=3$, temos $L(w)=(2w-3)^2$.

A função externa eleva ao quadrado e a interna é $2w-3$. A regra da cadeia multiplica as duas variações:

$$L'(w)=2(2w-3)\cdot2=4(2w-3).$$

Em $w=1$, o erro é 1 e a derivada é −4. Uma pequena mudança positiva em $w$ tende a reduzir o erro. O mínimo ocorre em $w=1{,}5$, com erro zero neste único par. Isso não demonstra desempenho para novos dados.

## Mais parâmetros: derivadas parciais

Para $f(a,b)=(a-1)^2+2(b+1)^2$, a derivada parcial em $a$ trata $b$ como constante: $\partial f/\partial a=2(a-1)$. A parcial em $b$ é $\partial f/\partial b=4(b+1)$.

O gradiente é o vetor-coluna

```math
\nabla f=\begin{pmatrix}2(a-1)\\4(b+1)\end{pmatrix}.
```

Em $(a,b)=(0,0)$, ele vale $(-2,4)^\top$. Para uma pequena perturbação $\delta$, a aproximação de primeira ordem é $f(\theta+\delta)\approx f(\theta)+\nabla f(\theta)^\top\delta$. Na métrica euclidiana, o gradiente aponta a direção de maior crescimento local; seu negativo é uma direção de descida se o gradiente não for zero e o passo for suficientemente pequeno.

## Ponto estacionário não é sempre mínimo

Ter derivada ou gradiente zero fornece uma condição de estacionariedade para um ótimo interior diferenciável. Para $f(x)=x^2$, zero é mínimo. Para $f(x)=-x^2$, zero é máximo. Para $f(x)=x^3$, zero é um ponto estacionário sem máximo nem mínimo local.

Em várias dimensões, a Hessiana reúne derivadas de segunda ordem e ajuda a examinar a curvatura. Ela não é necessária para toda execução de gradiente descendente, mas mostra por que parar só porque o gradiente ficou pequeno exige cautela.

Uma diferença finita pode conferir um cálculo, por exemplo $[f(x+h)-f(x-h)]/(2h)$. Um passo excessivamente pequeno sofre cancelamento numérico; um grande aproxima mal a variação local. Essa checagem numérica não substitui a derivação.

## Pratique

1. Derive $(3w-1)^2$ e avalie em $w=0$.
2. Calcule o gradiente de $a^2+3b^2$ em $(1,-1)$.
3. Gradiente zero em um ponto prova que o treinamento encontrou o melhor modelo possível?

<details><summary>Respostas comentadas</summary>

1. Pela cadeia, $2(3w-1)\cdot3=6(3w-1)$; em zero, −6.
2. As parciais são $2a$ e $6b$, portanto o gradiente é $(2,-6)^\top$.
3. Não. Pode haver máximo, sela, ótimo local ou problema numérico. Mesmo um mínimo global do erro de treino não garante generalização.

</details>

Fontes: [OpenStax, definição da derivada](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative) e [regra da cadeia](https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule); [MIT OpenCourseWare, gradiente e derivadas direcionais](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/part-b-chain-rule-gradient-and-directional-derivatives/). Exemplos autorais. [Gradiente descendente](../otimizacao/gradiente-descendente.md) · [Índice](../README.md).
