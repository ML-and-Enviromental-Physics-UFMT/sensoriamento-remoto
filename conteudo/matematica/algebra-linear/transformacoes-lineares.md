# Transformações lineares

Uma transformação linear descreve uma regra que combina medidas sem distorcer somas e escalas. Em sensoriamento remoto, uma transformação pode misturar bandas, projetar pixels em componentes principais ou converter coordenadas. A matriz é uma representação da regra, não a própria ideia.

## Definição e matriz

Uma função $T: \mathbb R^n\to\mathbb R^m$ é linear quando $T(x+y)=T(x)+T(y)$ e $T(ax)=aT(x)$. Equivalentemente, $T(ax+by)=aT(x)+bT(y)$. Toda transformação linear entre espaços coordenados pode ser representada por uma matriz $A\in\mathbb R^{m\times n}$, com $T(x)=Ax$. As colunas de $A$ são as imagens dos vetores da base usual: $Ae_j$ é a coluna $j$.

Exemplo. Para

```math
A=\begin{bmatrix}1&1\\0&1\end{bmatrix},
```

temos $T(x_1,x_2)=(x_1+x_2,x_2)$. A base $e_1=(1,0)$ vai a $(1,0)$, e $e_2=(0,1)$ vai a $(1,1)$; por isso essas imagens formam as colunas da matriz. No pixel espectral $x=(0{,}2,0{,}5)$, a saída é $(0{,}7,0{,}5)$. É uma mistura matemática de bandas, não uma reflectância automaticamente física: a primeira saída soma as duas entradas.

## Núcleo, imagem e posto

O núcleo $`\ker(T)=\{x:Ax=0\}`$ contém entradas apagadas pela transformação. A imagem $`\operatorname{im}(T)=\{Ax:x\in\mathbb R^n\}`$ contém todas as saídas possíveis. O posto é a dimensão da imagem. No exemplo, $\det(A)=1$, então o posto é 2, o núcleo contém apenas o vetor zero e toda saída do plano é possível. Se

```math
A=\begin{bmatrix}1&1\\2&2\end{bmatrix},
```

as colunas são dependentes, o posto é 1 e $(1,-1)$ pertence ao núcleo; essa diferença entre bandas é removida.

Para uma imagem com pixels nas linhas, aplicar a transformação de bandas $A\in\mathbb R^{q\times p}$ a cada pixel-linha é escrever $Y=XA^T$, onde $X\in\mathbb R^{m\times p}$ e $Y\in\mathbb R^{m\times q}$. O transposto aparece porque a fórmula de vetor-coluna é $y=Ax$. Dimensões ajudam a evitar uma transposição errada.

## Projeção como transformação

Se $u$ é unitário, projetar em sua reta corresponde à matriz $P=uu^T$. Para $u=(1,1)/\sqrt2$, temos

```math
P=\frac12\begin{bmatrix}1&1\\1&1\end{bmatrix}.
```

Aplicando a $x=(2,0)$, sai $Px=(1,1)$, e o resíduo $(1,-1)$ é perpendicular a $u$. A projeção reduz duas coordenadas a uma direção. Como $P^2=P$, uma segunda aplicação não muda a saída. Em PCA com $V_k$ contendo $k$ direções ortonormais, as coordenadas reduzidas são $V_k^Tx_c$; a reconstrução projetada é $V_kV_k^Tx_c$.

Transformações lineares fixam a origem: $T(0)=0$. Uma translação, como somar a média para voltar da representação centrada, não é linear. Em PCA, subtrair a média antes da transformação é um passo afim separado. Também não confunda posto da matriz com quantidade de colunas: só colunas independentes contam como direções de saída distintas.

### Exercícios

1. A regra $T(x)=Ax+b$, com $b\ne0$, é linear?
2. Para pixels em linhas, quantas colunas tem $Y=XA^T$ se há 5 bandas de entrada e 3 saídas?

<details><summary>Respostas comentadas</summary>

1. Não. Uma transformação linear precisa levar zero a zero, enquanto $Ax+b$ leva zero a $b\ne0$.
2. São três colunas de saída. Na multiplicação de matrizes, as 5 colunas de $X$ devem casar com as 5 linhas de $A^	op$, deixando 3 colunas de saída.
</details>

## Para continuar

Pré-requisitos: [vetores e matrizes](vetores-e-matrizes.md), [sistemas e inversa](sistemas-e-inversa.md) e [espaços, bases e projeções](espacos-bases-e-projecoes.md). Aplicações: [autovalores](autovalores-e-autovetores.md) e [SVD](svd.md). Referência: Pellegrini, *Álgebra linear*, versão 130 (2015), capítulo 3, seções 3.1–3.3 e capítulo 4. Exemplos autorais.

[Índice de álgebra linear](README.md)
