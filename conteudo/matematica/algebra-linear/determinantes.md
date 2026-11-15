# Determinantes

Um determinante ajuda a entender se uma transformação preserva dimensões e como ela altera áreas ou volumes. Ele também aparece na densidade gaussiana usada para classificar pixels. Não é uma nota de qualidade da matriz.

Pré-requisitos: [matrizes](vetores-e-matrizes.md) e [sistemas](sistemas-e-inversa.md).

## Uma conta em duas dimensões

Para uma matriz quadrada

```math
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},
```

$$\det A=ad-bc.$$

O valor absoluto é o fator de mudança de área. O sinal informa se a orientação foi preservada ou invertida. Essa interpretação exige que estejamos comparando áreas no mesmo sistema de unidades.

Exemplo. A matriz $A=\operatorname{diag}(2,3)$ multiplica a primeira coordenada por 2 e a segunda por 3. Um quadrado unitário vira um retângulo de área 6, e $\det A=2\cdot3=6$.

Para $B=\operatorname{diag}(-2,3)$, a área também muda por fator 6, mas $\det B=-6$: há uma inversão de orientação. O determinante negativo não significa uma área negativa no terreno.

## O que significa determinante zero

Considere

```math
C=\begin{pmatrix}1&2\\2&4\end{pmatrix}.
```

A segunda coluna é o dobro da primeira. Toda saída está na mesma reta, pois $C(x,y)^\top=(x+2y)(1,2)^\top$.

Seu determinante é $1\cdot4-2\cdot2=0$. A transformação perdeu uma dimensão e não é invertível. Para matrizes quadradas reais, determinante diferente de zero equivale a invertibilidade. No cálculo numérico, porém, decidir singularidade usando apenas um determinante arredondado é frágil.

## Relação com os autovalores

O determinante é o produto dos autovalores, contando multiplicidades. Para uma covariância simétrica semidefinida positiva, os autovalores são não negativos. Se algum é zero, a dispersão ocupa um subespaço e a covariância é singular.

No caso definido positivo, o volume de uma elipse ou elipsoide de covariância, a um nível fixado, é proporcional a $\sqrt{\det\Sigma}$. A raiz importa: o determinante tem escala de produto de variâncias, enquanto os eixos geométricos envolvem desvios-padrão.

## Por que aparece na classificação gaussiana?

Uma densidade gaussiana multivariada tem fator de normalização proporcional a $1/\sqrt{\det\Sigma}$. Mantendo as outras condições, uma distribuição mais espalhada precisa de um pico menor para que sua integral seja 1.

Considere duas classes de média zero, com covariâncias $I$ e $4I$ em duas dimensões. Os determinantes são 1 e 16; as raízes são 1 e 4. No ponto da média, a segunda densidade tem um quarto do pico da primeira. Longe da média, também importa a distância de Mahalanobis; o determinante sozinho não decide a classe.

Na implementação, `np.linalg.slogdet` fornece o sinal e o logaritmo do valor absoluto. Para uma covariância definida positiva, o sinal esperado é positivo. Isso evita alguns problemas de overflow e underflow, mas não corrige uma covariância inválida.

## Pratique

1. Calcule o determinante de

   ```math
   \begin{pmatrix}3&1\\0&2\end{pmatrix}.
   ```
2. A matriz $\operatorname{diag}(10^8,10^{-8})$ tem determinante 1. Isso garante bom condicionamento?
3. Se uma banda é cópia exata de outra, o que pode acontecer com a covariância de duas bandas?

<details><summary>Respostas comentadas</summary>

1. $3\cdot2-1\cdot0=6$. A transformação multiplica áreas por 6.
2. Não. As escalas nas direções são muito diferentes. Seu número de condição na norma 2 é $10^{16}$, embora o determinante seja 1.
3. Há dependência linear, posto menor que 2 e determinante zero. Usar uma inversa usual falha; a solução exige rever variáveis ou modelo, não trocar a definição de determinante.

</details>

Fontes: Pellegrini, *Álgebra linear*, capítulo 5, em especial volume orientado e determinantes; CEDERJ, tópico de determinantes, aula 5 na fonte. A ligação à densidade gaussiana é tratada em Canty (2019), capítulo 2. [Bibliografia](../../../referencias/matematica/README.md) · [Mahalanobis](../estatistica/mahalanobis.md) · [Índice](README.md).
