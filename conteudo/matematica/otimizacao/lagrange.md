# Multiplicadores de Lagrange

Alguns problemas exigem a melhor solução entre aquelas que obedecem a uma condição. Na PCA, uma direção precisa ter norma fixa: sem isso, aumentar o comprimento do vetor aumentaria artificialmente a variância projetada.

Pré-requisitos: [gradientes](../calculo/derivadas-e-gradientes.md), [produtos](../algebra-linear/produtos-e-transposta.md) e [autovalores](../algebra-linear/autovalores-e-autovetores.md).

## O problema com restrição

Queremos otimizar $f(w)$ sujeito a $g(w)=0$. Para uma restrição diferenciável regular, em um extremo local sob condições usuais, o gradiente de $f$ é paralelo ao da restrição:

$$\nabla f(w)=\lambda\nabla g(w),\qquad g(w)=0.$$

A regularidade da restrição, como $\nabla g\ne0$ no ponto, importa. A Lagrangiana $\mathcal L(w,\lambda)=f(w)-\lambda g(w)$ reúne as condições. Resolver suas derivadas fornece candidatos, não uma classificação automática como máximo ou mínimo.

## Exemplo de duas coordenadas

Vamos maximizar $f(x,y)=x+y$ na circunferência $x^2+y^2=1$. Definimos

$$\mathcal L=x+y-\lambda(x^2+y^2-1).$$

As derivadas em $x$ e $y$ dão $1-2\lambda x=0$ e $1-2\lambda y=0$, portanto $x=y$. A restrição vira $2x^2=1$. Existem dois candidatos, $(1/\sqrt2,1/\sqrt2)$ e $(-1/\sqrt2,-1/\sqrt2)$.

Seus valores de $f$ são $\sqrt2$ e $-\sqrt2$. A circunferência é compacta e $f$ é contínua; os extremos existem. Nesse caso, a comparação entre os candidatos identifica o máximo e o mínimo globais. A existência dessa conclusão não pode ser transferida sem verificar as condições de outro problema.

## A derivação que aparece na PCA

Seja $S$ uma covariância simétrica. Para uma direção-coluna $w$ unitária, a variância projetada é $w^\top Sw$. O problema é

$$\max_w w^\top Sw\quad\text{sujeito a}\quad w^\top w=1.$$

A Lagrangiana é $w^\top Sw-\lambda(w^\top w-1)$. Como $S$ é simétrica, a derivada em $w$ é $2Sw-2\lambda w$. Igualando a zero, obtemos $Sw=\lambda w$: os candidatos são autovetores unitários.

Multiplicar por $w^\top$ mostra que $w^\top Sw=\lambda$. Logo, o maior autovalor fornece a maior variância. Para $S=\operatorname{diag}(4,1)$, os eixos têm variâncias 4 e 1. O eixo $(1,0)^\top$ maximiza o problema. Seu oposto representa a mesma direção.

Sem a restrição, escolher $w=(t,0)^\top$ produziria variância $4t^2$, que cresce sem limite. A restrição evita esse crescimento que não corresponde a uma escolha melhor de direção.

## Onde o método exige cuidado

Várias restrições precisam de vários multiplicadores e condições de regularidade apropriadas. Restrições por desigualdade levam a condições como KKT, com viabilidade e complementaridade adicionais. Uma derivação breve da PCA não cobre toda otimização com restrições.

Também não se deve dizer que “o multiplicador é sempre o preço da restrição” sem definir o problema e as hipóteses de sensibilidade. Aqui ele é, primeiro, o número que faz a condição de estacionariedade valer.

## Pratique

1. Para $S=\operatorname{diag}(9,4)$, qual é a máxima variância projetada com norma 1?
2. Se $S=2I$ em duas dimensões, existe uma única direção que maximiza?
3. Por que encontrar um ponto estacionário da Lagrangiana não basta para qualquer problema?

<details><summary>Respostas comentadas</summary>

1. É 9, obtida nas direções $(1,0)^\top$ e $(-1,0)^\top$.
2. Não. Todo vetor unitário tem $w^\top Sw=2$. O autovalor repetido permite várias bases ótimas.
3. É preciso conferir viabilidade, regularidade, natureza dos candidatos e existência de extremos. Em outros problemas pode haver máximos, mínimos, selas ou candidatos que não resolvem o objetivo desejado.

</details>

Fonte: Canty (2019), ferramentas matemáticas do Apêndice A, seção 1.6 e PCA na seção 3.3. Exemplo da circunferência e contas autorais. [Autovalores](../algebra-linear/autovalores-e-autovetores.md) · [Índice](../README.md).
