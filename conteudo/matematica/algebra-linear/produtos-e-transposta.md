# Produtos e transposta

Uma média de bandas, uma projeção e uma matriz de covariância usam produtos diferentes. Antes de fazer a conta, confira o tamanho de cada objeto. Isso evita obter uma matriz quando você esperava um número.

Pré-requisito: [vetores e matrizes](vetores-e-matrizes.md).

## Transpor é trocar os índices

Se $A$ tem $m$ linhas e $p$ colunas, sua transposta $A^\top$ tem $p$ linhas e $m$ colunas. O elemento que estava em $(i,j)$ passa para $(j,i)$. Não mudamos o valor, só a posição.

Para

```math
A=\begin{pmatrix}1&2&3\\4&5&6\end{pmatrix},\qquad
A^\top=\begin{pmatrix}1&4\\2&5\\3&6\end{pmatrix}.
```

Transpor duas vezes recupera a matriz original. Para um vetor-coluna, a transposta é uma linha. No NumPy, porém, um array com forma `(p,)` tem só um eixo: `x.T` mantém essa forma. Use `x[:, None]` se precisar de uma coluna explícita.

## Produto interno: um número

Para vetores reais com $p$ componentes,

$$x^\top y=\sum_{j=1}^{p}x_jy_j.$$

O somatório significa multiplicar componentes de mesma posição e somar os resultados. Com $x=(1,2)^\top$ e $y=(3,4)^\top$, temos $x^\top y=1\cdot3+2\cdot4=11$.

A norma euclidiana, ou comprimento, é $`\|x\|=\sqrt{x^\top x}`$. Para $x$, ela vale $\sqrt5$. Se dois vetores não nulos têm produto interno zero, são ortogonais na métrica usual. Escalas e unidades importam: misturar uma variável em metros e outra em graus altera o sentido geométrico dessa conta.

## Produto externo: uma matriz

O produto $xy^\top$ combina cada componente de $x$ com cada componente de $y$:

```math
xy^\top=\begin{pmatrix}3&4\\6&8\end{pmatrix}.
```

Esse objeto tem duas linhas e duas colunas. Quando usamos o mesmo vetor centrado nos dois lados, $xx^\top$ registra produtos entre variáveis. Somar esses produtos é a base da [covariância](../estatistica/covariancia.md).

## Produto de matrizes: linha por coluna

Se $A$ tem forma $m\times p$ e $B$ tem forma $p\times q$, o produto $AB$ tem forma $m\times q$. O elemento $(i,j)$ é o produto interno da linha $i$ de $A$ com a coluna $j$ de $B$.

Exemplo resolvido. Um pixel tem duas bandas, $x=(0{,}2,0{,}6)^\top$. Queremos produzir a diferença e a média dessas bandas:

```math
W=\begin{pmatrix}-1&1\\0{,}5&0{,}5\end{pmatrix},\qquad
Wx=\begin{pmatrix}-0{,}2+0{,}6\\0{,}1+0{,}3\end{pmatrix}
=\begin{pmatrix}0{,}4\\0{,}4\end{pmatrix}.
```

A primeira saída é NIR menos vermelho; a segunda é a média. Para uma tabela $X$ com pixels nas linhas, aplicamos a mesma transformação a todos com $Y=XW^\top$. O transposto aparece porque os pixels agora são linhas.

Em geral, $AB\ne BA$. E `A * B` no NumPy multiplica elemento a elemento, enquanto `A @ B` faz o produto matricial. O produto elemento a elemento de formas diferentes pode usar broadcasting, que precisa ser intencional.

## Pratique

1. Se $X$ tem forma $100\times6$, qual é a forma de $X^\top X$? E de $XX^\top$?
2. Para $x=(2,-1)^\top$, calcule $x^\top x$ e $xx^\top$.
3. Por que uma transformação que recebe seis bandas e gera três saídas tem matriz $3\times6$ para pixels-coluna?

<details><summary>Respostas comentadas</summary>

1. $X^\top X$ tem forma $6\times6$ e combina variáveis; $XX^\top$ tem forma $100\times100$ e combina observações. Nenhum é uma covariância sem os passos de centralização e normalização apropriados.
2. O produto interno é $2^2+(-1)^2=5$. O externo é

   ```math
   \begin{pmatrix}4&-2\\-2&1\end{pmatrix}.
   ```
3. As seis colunas recebem as entradas. Cada uma das três linhas define a combinação que produz uma saída.

</details>

Fonte: Rios, Figueiredo e Cunha, *Álgebra Linear I*, volume 1, tópicos de transposição e multiplicação, identificados como aulas 2–3 na fonte. Os exemplos são autorais. [Bibliografia](../../../referencias/matematica/README.md) · [Índice](README.md).
