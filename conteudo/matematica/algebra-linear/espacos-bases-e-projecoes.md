# Espaços, bases e projeções

Em uma imagem multiespectral, cada pixel pode ser visto como um ponto cujas coordenadas são as reflectâncias nas bandas. Bases e projeções dão uma linguagem para separar direções de variação e reduzir a representação. O ganho é computacional e visual; a informação descartada pode, porém, ser importante para distinguir alvos.

## Espaços e coordenadas

Um espaço vetorial é um conjunto em que faz sentido somar elementos e multiplicá-los por escalares, com as regras usuais de soma e distributividade. Aqui usaremos principalmente $\mathbb R^p$, os vetores reais com $p$ coordenadas. Uma combinação linear de vetores $v_1,\ldots,v_k$ tem a forma $a_1v_1+\cdots+a_kv_k$, com coeficientes reais $a_i$. O conjunto de todas essas combinações é o espaço gerado pelos vetores.

Uma base é uma coleção que gera o espaço sem redundância: nenhum vetor da coleção pode ser escrito como combinação dos demais. Em $\mathbb R^2$, os vetores $(1,0)$ e $(0,1)$ formam a base usual. O ponto $x=(3,2)$ tem coordenadas 3 e 2 nessa base. Na base $b_1=(1,1), b_2=(1,-1)$, buscamos $c_1,c_2$ tais que $c_1b_1+c_2b_2=x$. Igualando coordenadas, $c_1+c_2=3$ e $c_1-c_2=2$, logo $c_1=2{,}5$, $c_2=0{,}5$. O ponto não mudou; mudaram as coordenadas usadas para descrevê-lo.

## Ortogonalidade e projeção

O produto interno usual é $u^Tv=\sum_i u_iv_i$. Vetores são ortogonais quando esse produto vale zero. O comprimento é $`\|u\|=\sqrt{u^Tu}`$. Se $u$ é unitário, a projeção ortogonal de $x$ na reta gerada por $u$ é $\hat x=(u^Tx)u$. O resíduo $r=x-\hat x$ é perpendicular a $u$, pois $u^Tr=u^Tx-(u^Tx)u^Tu=0$.

Exemplo. Para resumir um pixel $x=(3,2)$ pela direção diagonal $u=(1,1)/\sqrt2$, temos $u^Tx=5/\sqrt2$. Portanto $\hat x=(5/2,5/2)$, e $r=(1/2,-1/2)$. O produto $u^Tr=0$ confirma a geometria. O erro quadrático descartado é $r^Tr=1/2$. Projetar não significa escolher o pixel mais próximo entre pixels observados: significa encontrar o ponto mais próximo na reta especificada.

Para um subespaço gerado pelas colunas independentes de uma matriz $Q$, a projeção de $x$ é $Q(Q^TQ)^{-1}Q^Tx$. Se as colunas forem ortonormais, $Q^TQ=I$, e a expressão fica $QQ^Tx$. A matriz $P=QQ^T$ satisfaz $P^T=P$ e $P^2=P$: projetar duas vezes dá o mesmo resultado. Se houver colunas dependentes, a inversa não existe; deve-se retirar redundâncias ou usar uma fatoração adequada.

## Posto e dados de imagem

O posto é o número de direções linearmente independentes nas colunas (igual ao das linhas). Se uma matriz de dados tem posto menor que o número de bandas, há relações lineares exatas entre bandas; posto baixo aproximado indica que poucos eixos podem representar boa parte da variação, mas não garante utilidade para toda classificação.

Convenção importante: uma cena com $m$ pixels e $p$ bandas pode ser escrita como $X\in\mathbb R^{m\times p}$, pixels nas linhas e bandas nas colunas. Cada pixel é então uma linha, mas a fórmula de projeção acima usa vetores-coluna. Para um pixel-linha $x$, com componentes principais nas colunas de $V_k$, seus escores são $xV_k$; com dados centrados, use $(x-\mu)V_k$. Não misture essa convenção com $X\in\mathbb R^{p\times m}$, comum em livros que colocam variáveis nas linhas.

### Exercícios

1. Projete $(4,0)$ sobre a direção unitária $(0,1)$.
2. As colunas $(1,0)$ e $(2,0)$ formam base de $\mathbb R^2$?

<details><summary>Respostas comentadas</summary>

1. O produto interno é zero. A projeção é $(0,0)$ e o resíduo é $(4,0)$, perpendicular à direção vertical.
2. Não. A segunda coluna é duas vezes a primeira; não há duas direções independentes nem cobertura do plano. O posto é 1.
</details>

## Para continuar

Pré-requisitos: [vetores e matrizes](vetores-e-matrizes.md) e [produtos e transposta](produtos-e-transposta.md). Próximos passos: [transformações lineares](transformacoes-lineares.md), [autovalores e PCA](autovalores-e-autovetores.md) e [SVD](svd.md). Referência: Jerônimo C. Pellegrini, *Álgebra linear*, versão 130 (2015), seções 1.4–1.5, 2.1–2.4 e capítulo de produtos internos e ortogonalidade. Os exemplos acima são autorais.

[Índice de álgebra linear](README.md)
