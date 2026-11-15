# Covariância e correlação

Duas bandas podem subir e descer juntas porque respondem a características comuns da cena. A covariância descreve essa variação conjunta e fornece a geometria usada pela PCA e por classificadores gaussianos.

Pré-requisitos: [médias e variâncias](distribuicoes-e-estimacao.md) e [produtos matriciais](../algebra-linear/produtos-e-transposta.md).

## Centralizar antes de comparar

Seja $X\in\mathbb R^{n\times p}$ uma matriz com pixels nas linhas e bandas nas colunas. A média da coluna $j$ é $\bar x_j$. A matriz centrada $X_c$ resulta de subtrair a média de cada coluna, sem dividir pelo desvio-padrão.

Para duas bandas, a covariância amostral é

$$s_{12}=\frac{1}{n-1}\sum_{i=1}^n(x_{i1}-\bar x_1)(x_{i2}-\bar x_2).$$

Quando os desvios costumam ter o mesmo sinal, seus produtos são positivos. Quando uma banda costuma subir enquanto a outra desce, os produtos tendem a ser negativos. Produtos de sinais distintos podem se compensar; covariância zero não prova independência.

## Exemplo resolvido

Considere três pixels e duas bandas hipotéticas, com valores 1, 2 e 3 na primeira e 2, 4 e 6 na segunda. As médias são 2 e 4. Temos

```math
X_c=\begin{pmatrix}-1&-2\\0&0\\1&2\end{pmatrix},\qquad
X_c^\top X_c=\begin{pmatrix}2&4\\4&8\end{pmatrix}.
```

Dividindo por $n-1=2$,

```math
S=\frac{X_c^\top X_c}{n-1}=\begin{pmatrix}1&2\\2&4\end{pmatrix}.
```

A diagonal contém as variâncias 1 e 4. Os elementos fora da diagonal são ambos 2, pois a covariância é simétrica. A segunda banda é exatamente o dobro da primeira; o determinante é zero. A covariância existe, mas não tem inversa usual.

## A matriz tem uma geometria

Para qualquer vetor $a$, $`a^\top Sa=\|X_ca\|^2/(n-1)\ge0`$. Isso mostra que uma covariância calculada desse modo é semidefinida positiva. Na direção $a$, esse valor é a variância dos escores projetados.

O posto de $S$ é no máximo $\min(p,n-1)$. Se há menos observações independentes que o necessário para representar as bandas, ou se elas têm relações exatas, a covariância pode ser singular. Valores numéricos minúsculos negativos em autovalores podem vir de arredondamento; valores negativos relevantes exigem investigar o cálculo ou o estimador.

## Correlação tira a escala, não o problema físico

Se os desvios-padrão são positivos, a correlação é $r_{12}=s_{12}/(s_1s_2)$. No exemplo, $r=2/(1\cdot2)=1$. Multiplicar a segunda banda por 10 multiplica sua covariância com a primeira por 10, mas mantém essa correlação.

Covariância preserva as unidades. Correlação é adimensional e varia entre −1 e 1. Se uma banda é constante, seu desvio-padrão é zero e a correlação usual com ela é indefinida. Não atribua zero automaticamente.

## Fazer a mesma conta no NumPy

```python
import numpy as np
X = np.array([[1., 2.], [2., 4.], [3., 6.]])
Xc = X - X.mean(axis=0)
S = Xc.T @ Xc / (len(X) - 1)
print(S)
print(np.cov(X, rowvar=False, ddof=1))
```

As duas expressões devem coincidir. `rowvar=False` informa que variáveis estão nas colunas. Mudar a orientação sem mudar a opção calcula outro objeto.

## Pratique

1. Se a segunda banda assumir 3, 2 e 1, mantendo a primeira como 1, 2 e 3, qual será a covariância?
2. Em uma matriz com 5 pixels e 10 bandas, qual é o posto máximo da covariância amostral centrada?
3. Uma correlação alta prova que uma banda causa a resposta da outra?

<details><summary>Respostas comentadas</summary>

1. As médias são ambas 2. Os produtos dos desvios são −1, 0 e −1, então a covariância é −1 e a correlação é −1.
2. No máximo 4. A centralização impõe uma dependência entre as linhas, e $n-1=4$. Portanto, uma matriz de covariância $10\times10$ desse conjunto não será invertível no sentido usual.
3. Não. As bandas podem compartilhar iluminação, cobertura ou outros fatores. A medida descreve associação linear.

</details>

Fonte: Canty (2019), seções 2.1.3 e 2.3.1. [Autovalores e PCA](../algebra-linear/autovalores-e-autovetores.md) · [Mahalanobis](mahalanobis.md) · [Índice](../README.md).
