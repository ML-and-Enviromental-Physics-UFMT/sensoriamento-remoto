# Vetores e matrizes

Uma imagem multibanda mede várias coisas no mesmo lugar. No pixel de uma imagem Sentinel-2, por exemplo, podemos guardar reflectâncias de bandas diferentes. Vetores organizam essas medidas; matrizes organizam muitos pixels ou descrevem transformações entre medidas.

## Um pixel como vetor

Considere um pixel com reflectâncias 0,12 na banda vermelha e 0,30 no infravermelho próximo. Vamos representá-lo por

```math
\mathbf{x}=\begin{pmatrix}0{,}12\\0{,}30\end{pmatrix}\in\mathbb{R}^2.
```

O símbolo $\mathbb{R}^2$ diz que há dois números reais ordenados. A ordem importa: a primeira coordenada é a banda vermelha, a segunda é o infravermelho próximo. Trocar a ordem sem trocar a interpretação muda o dado.

Em geral, um pixel com $p$ bandas é um vetor $\mathbf{x}=(x_1,\ldots,x_p)^\top$. Cada $x_j$ é a medida da banda $j$, já convertida para a unidade escolhida, como reflectância ou temperatura. O sobrescrito $\top$ indica transposição e transforma a lista horizontal em coluna.

## Muitos pixels como matriz

Para registrar $n$ pixels e $p$ bandas, colocamos um pixel por linha:

```math
X=\begin{pmatrix}x_{11}&\cdots&x_{1p}\\\vdots&\ddots&\vdots\\x_{n1}&\cdots&x_{np}\end{pmatrix}\in\mathbb{R}^{n\times p}.
```

O elemento $x_{ij}$ é a medida do pixel $i$ na banda $j$. Assim, a matriz tem $n$ linhas e $p$ colunas. Em Python, essa é a convenção usual para uma tabela de amostras: `X.shape == (n_pixels, n_bandas)`. Um cubo de imagem costuma ter eixos linha, coluna e banda; ao selecionar e empilhar pixels, precisamos explicitar como os eixos viram linhas e colunas.

### Exemplo resolvido

Três pixels foram medidos em duas bandas. Seus vetores são $\mathbf{x}_1=(0{,}12,0{,}30)^\top$, $\mathbf{x}_2=(0{,}20,0{,}25)^\top$ e $\mathbf{x}_3=(0{,}05,0{,}10)^\top$. A tabela de amostras fica

```math
X=\begin{pmatrix}0{,}12&0{,}30\\0{,}20&0{,}25\\0{,}05&0{,}10\end{pmatrix}.
```

Logo $X$ tem forma $3\times2$. A coluna 2 é $(0{,}30,0{,}25,0{,}10)^\top$, isto é, os valores da segunda banda nos três pixels. A linha 2 é $(0{,}20,0{,}25)$, o espectro do segundo pixel. A média da primeira banda é $(0{,}12+0{,}20+0{,}05)/3=0{,}1233$ aproximadamente.

## Matriz como transformação

Uma matriz $A\in\mathbb{R}^{q\times p}$ transforma um vetor $\mathbf{x}\in\mathbb{R}^p$ em $\mathbf{y}=A\mathbf{x}\in\mathbb{R}^q$. Cada linha de $A$ combina as entradas de $\mathbf{x}$ para formar uma saída. Isso modela, por exemplo, um índice espectral ou uma mudança de coordenadas. As dimensões são uma checagem prática: o número de colunas de $A$ precisa coincidir com o número de componentes de $\mathbf{x}$.

Se

```math
A=\begin{pmatrix}-1&1\end{pmatrix}
```

e $\mathbf{x}=(0{,}12,0{,}30)^\top$, então $A\mathbf{x}=-0{,}12+0{,}30=0{,}18$. A saída é uma coordenada: diferença entre infravermelho próximo e vermelho. O NDVI usa outra combinação, com divisão pela soma; não é uma transformação linear porque há uma razão dependente do próprio pixel.

## Erros e limites

Uma matriz não sabe que seus números são bandas, metros ou graus. A interpretação vem da ordem e das unidades documentadas. Não misture escalas digitais e reflectâncias sem conversão. Também não confunda linhas e colunas: com amostras nas linhas, algumas fórmulas de livros escritas para amostras em colunas exigem transposição. Valores ausentes, pixels mascarados e pixels fora de registro não se resolvem com álgebra; precisam de tratamento antes da análise.

## Pratique

1. Uma amostra contém azul, verde, vermelho e NIR. Quantos componentes tem seu vetor?
2. Uma matriz de 500 pixels e 6 bandas tem qual forma?

<details><summary>Respostas comentadas</summary>

Na primeira questão, o vetor está em $\mathbb{R}^4$. A escolha de ordem não é universal, mas deve ser consistente. Na segunda, as 500 observações são linhas e as seis variáveis são colunas; transpor produz $6\times500$ e altera a convenção, não os dados subjacentes.
</details>

## Fontes e continuidade

Rios, Figueiredo e Cunha, *Álgebra Linear I*, CEDERJ, 3ª ed., §1, Aula 1, “Matrizes”, pp. 9–17 do material impresso: notação, dimensões e operações matriciais. Pellegrini, *Álgebra linear*, versão 130 (2015), capítulos 1 e 4, sobre espaços vetoriais e matrizes. Exemplos de sensoriamento remoto e contas acima são autorais. [Produtos e transposta](produtos-e-transposta.md) usa esta notação; [índice de matemática](../README.md) organiza os demais tópicos.
