# Autovalores, autovetores e PCA

Em uma cena com bandas correlacionadas, interessa saber se a variação dos pixels se concentra em poucas direções. Autovalores e autovetores da covariância respondem a essa pergunta: cada autovetor indica uma direção no espaço das bandas; seu autovalor mede a variância nessa direção.

## A equação de autovalor

Para uma matriz quadrada $A$, um vetor não nulo $v$ é autovetor quando $Av=\lambda v$. O número $\lambda$ é o autovalor associado. A transformação pode alongar, encolher ou inverter o sentido nessa reta sem mudar sua direção. Autovetores podem ser multiplicados por qualquer escalar não nulo, então seu comprimento costuma ser normalizado para 1.

Exemplo. Seja

```math
A=\begin{bmatrix}2&1\\1&2\end{bmatrix}.
```

Para $v_1=(1,1)/\sqrt2$, a multiplicação dá $Av_1=(3,3)/\sqrt2=3v_1$, logo $\lambda_1=3$. Para $v_2=(1,-1)/\sqrt2$, temos $Av_2=(1,-1)/\sqrt2=v_2$, logo $\lambda_2=1$. Os vetores são ortogonais. A matriz favorece a direção diagonal: sua escala é três vezes maior que na direção anti-diagonal.

## Covariância e direções principais

Considere $X\in\mathbb R^{m\times p}$, com pixels nas linhas e bandas nas colunas. A média da banda $j$ é $\mu_j$. Forme $X_c=X-\mathbf1\mu^T$, centrando cada coluna. A covariância amostral é $C=X_c^TX_c/(m-1)$, para $m>1$. Ela é simétrica e semidefinida positiva: para qualquer direção unitária $v$, $v^TCv\ge0$, e esse valor é a variância dos escores projetados.

A primeira componente principal maximiza $v^TCv$ sob $v^Tv=1$. As seguintes maximizam a variância sujeitas a serem ortogonais às anteriores. Para covariância, autovetores ortonormais de $C$ dão essas direções, e os autovalores são as variâncias correspondentes. Ordene $\lambda_1\ge\cdots\ge\lambda_p$. A fração da variância total explicada pelos primeiros $k$ eixos é $\sum_{i=1}^k\lambda_i/\sum_{i=1}^p\lambda_i$, se o denominador for positivo.

Exemplo numérico inteiramente resolvido. Suponha que a covariância de duas bandas seja a matriz $A$ do exemplo anterior. As direções unitárias são $v_1=(1,1)/\sqrt2$ e $v_2=(1,-1)/\sqrt2$, com variâncias 3 e 1. A variância total é o traço, 4. Retendo só a primeira componente, explicamos $`3/4=75\%`$ da variância. Para um pixel $x=(4,2)$ cuja média de bandas é $\mu=(3,1)$, o vetor centrado é $(1,1)$. Seu escore na primeira componente é $(1,1)^Tv_1=\sqrt2$, e na segunda é zero. A reconstrução com uma componente é $\mu+\sqrt2v_1=(4,2)$, exata neste pixel. Isso não implica reconstrução exata dos demais.

## Escala importa

PCA centrada subtrai médias, mas preserva unidades e escalas originais. PCA padronizada também divide cada banda pelo desvio-padrão, equivalendo a analisar correlações. Se uma banda tem variância alta por unidade ou faixa dinâmica, ela pode dominar a PCA centrada. Padronizar pode equilibrar bandas, mas também amplificar bandas ruidosas. Escolha conforme a pergunta física e registre o pré-processamento.

O sinal dos autovetores é arbitrário: $v$ e $-v$ representam o mesmo eixo, com escores de sinal oposto. Autovalores repetidos permitem várias bases ortonormais dentro do mesmo subespaço principal. Autovalores pequenos podem refletir ruído, quantização ou relações redundantes, não necessariamente informação dispensável para uma tarefa específica.

### Exercícios

1. Para $C=\operatorname{diag}(9,1)$, qual a fração explicada pela primeira componente?
2. Se multiplicarmos um autovetor por $-1$, muda a variância associada?

<details><summary>Respostas comentadas</summary>

1. A fração é $`9/(9+1)=90\%`$. O total da variância é a soma dos autovalores.
2. Não. A troca de sinal aparece nos escores, mas não na variância nem na reta principal, pois $(-v)^\top C(-v)=v^\top Cv$.
</details>

## Para continuar

Pré-requisitos: [produtos e transposta](produtos-e-transposta.md), [espaços, bases e projeções](espacos-bases-e-projecoes.md). Aplicação computacional: [SVD e PCA](svd.md). Referência: Pellegrini, *Álgebra linear*, versão 130 (2015), capítulo 6, em especial seções 6.1 e 6.5. A relação PCA-covariância é desenvolvida aqui para dados centrados com pixels nas linhas. Exemplos autorais.

[Índice de álgebra linear](README.md)
