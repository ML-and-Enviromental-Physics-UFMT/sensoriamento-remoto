# Decomposição em valores singulares

Uma imagem multibanda pode ter milhões de pixels e poucas bandas. A decomposição em valores singulares (SVD) separa uma matriz em padrões ortogonais e seus pesos. Isso permite reconstruir uma aproximação compacta e, quando os dados são centrados, conecta-se diretamente à PCA.

## A fatoração

Para qualquer matriz real $X\in\mathbb R^{m\times p}$, existe uma SVD $X=U\Sigma V^T$. Na forma reduzida, $r=\min(m,p)$, $U$ tem tamanho $m\times r$, $V$ tem tamanho $p\times r$, e suas colunas são ortonormais. Na forma reduzida, $\Sigma$ é quadrada de ordem $r$ e diagonal, com valores singulares $\sigma_1\ge\cdots\ge\sigma_r\ge0$. Assim, $X=\sum_i\sigma_i u_iv_i^T$. Cada termo é um padrão de posto um.

Exemplo resolvido. Considere

```math
X=\begin{bmatrix}3&0\\0&1\end{bmatrix}.
```

Uma SVD é $U=I$, $V=I$, $\Sigma=\operatorname{diag}(3,1)$, pois o produto retorna $X$. Mantendo só o primeiro termo,

```math
X_1=3(1,0)^T(1,0)=\begin{bmatrix}3&0\\0&0\end{bmatrix}.
```

O erro é $X-X_1=\operatorname{diag}(0,1)$, cuja norma de Frobenius é 1. A norma de Frobenius, raiz da soma dos quadrados dos elementos, do original vale $\sqrt{10}$. Portanto a energia quadrática retida é $`9/10=90\%`$. O erro relativo em norma é $1/\sqrt{10}$, cerca de 31,6%.

Entre todas as matrizes de posto no máximo $k$, truncar a SVD nos primeiros $k$ termos minimiza o erro quadrático de Frobenius. Isso torna a compressão ótima para esse critério, não necessariamente para preservar classes ou detalhes de interesse. Um alvo raro pode ocupar pouca energia e ainda ser cientificamente importante.

## Da SVD à PCA

Assuma pixels nas linhas: $X\in\mathbb R^{m\times p}$, com observações nas linhas e bandas nas colunas. Centre as colunas para obter $X_c$, e calcule $X_c=U\Sigma V^T$. Então

$$C=\frac{X_c^TX_c}{m-1}=V\frac{\Sigma^T\Sigma}{m-1}V^T.$$

Logo as colunas de $V$ são direções principais e os autovalores amostrais da covariância são $\lambda_i=\sigma_i^2/(m-1)$. Os escores PCA são $X_cV=U\Sigma$. Para um pixel-linha novo $x$, use $(x-\mu)V_k$. Se a matriz for definida com bandas nas linhas, as fórmulas transpostas mudam; declare a orientação antes de interpretar vetores.

No exemplo, interprete as linhas de

```math
X=\begin{bmatrix}2&0\\-2&0\end{bmatrix}
```

como dois pixels e duas bandas. As colunas já estão centradas. Uma SVD usa

```math
U=\frac1{\sqrt2}\begin{pmatrix}1&1\\-1&1\end{pmatrix},
```

$\Sigma=\operatorname{diag}(2\sqrt2,0)$ e $V=I$. Multiplicar essas matrizes devolve exatamente $X$. Para duas observações, a covariância é $X^TX/(2-1)=\operatorname{diag}(8,0)$. O primeiro eixo explica toda a variância; a segunda banda não varia nesta amostra. Note que a direção PCA está no espaço das bandas, isto é, nas colunas de $V$, enquanto $U$ descreve padrões entre pixels.

## Limites práticos

SVD não exige calcular $X^TX$, operação que pode piorar condicionamento numérico. Bibliotecas oferecem algoritmos completos ou aproximados; em imagens grandes, aproximações economizam memória e tempo. Valores singulares iguais permitem não unicidade dos vetores dentro do subespaço correspondente, e os sinais de pares $(u_i,v_i)$ podem ser invertidos juntos. PCA centrada não equivale à PCA após padronização: esta divide bandas pelo desvio-padrão e muda a métrica, podendo dar peso excessivo a ruído.

### Exercícios

1. Para valores singulares 5 e 2, qual a fração de energia retida ao manter o primeiro?
2. Em dados com pixels nas linhas, em que espaço vivem as direções principais?

<details><summary>Respostas comentadas</summary>

1. A fração é $25/(25+4)=25/29$, aproximadamente 86,2%. A energia quadrática é a soma dos quadrados dos valores singulares.
2. As direções principais estão no espaço das bandas, nas colunas de $V$. As linhas de $U$ representam coordenadas associadas às observações; os vetores de $V$ combinam as variáveis/bandas.
</details>

## Para continuar

Pré-requisitos: [espaços, bases e projeções](espacos-bases-e-projecoes.md) e [autovalores e autovetores](autovalores-e-autovetores.md). Fonte local: Canty (2019), *Image Analysis, Classification and Change Detection in Remote Sensing*, seção 1.5, referência já indicada na bibliografia do projeto; a derivação acima é própria. Para teoremas de bases e fatorações, Pellegrini, *Álgebra linear*, versão 130 (2015), capítulos 2 e 6; a SVD não é atribuída a esse livro sem conferência de seção específica.

[Índice de álgebra linear](README.md)
