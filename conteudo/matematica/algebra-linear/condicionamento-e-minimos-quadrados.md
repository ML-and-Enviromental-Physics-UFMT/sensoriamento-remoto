# Condicionamento e mínimos quadrados

Um modelo pode ter mais observações que parâmetros e ainda assim ser difícil de ajustar. Duas perguntas diferentes ajudam: quanto o modelo consegue explicar e quão sensível é o ajuste a pequenas mudanças nas entradas?

Pré-requisitos: [sistemas](sistemas-e-inversa.md), [produtos](produtos-e-transposta.md) e [projeções](espacos-bases-e-projecoes.md).

## Ajustar sem exigir igualdade exata

Para $A\in\mathbb R^{m\times p}$, observações $b\in\mathbb R^m$ e parâmetros $\beta\in\mathbb R^p$, mínimos quadrados procura

```math
\min_\beta\|A\beta-b\|_2^2.
```

O resíduo $b-A\beta$ guarda as diferenças não explicadas. No sensoriamento remoto, esse modelo pode representar uma regressão entre medições ou um ajuste geométrico. O significado dos parâmetros depende do modelo escolhido.

Exemplo resolvido. Queremos ajustar $y=a+bt$ aos pares $(0,1)$, $(1,2)$ e $(2,2)$:

```math
A=\begin{pmatrix}1&0\\1&1\\1&2\end{pmatrix},\qquad b=\begin{pmatrix}1\\2\\2\end{pmatrix}.
```

As equações normais são $A^\top A\beta=A^\top b$. Aqui,

```math
\begin{pmatrix}3&3\\3&5\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix}
=\begin{pmatrix}5\\6\end{pmatrix}.
```

Subtraindo as equações, $2b=1$, então $b=1/2$ e $a=7/6$. As previsões são $(7/6,10/6,13/6)$; os resíduos, $(-1/6,2/6,-1/6)$. A soma dos quadrados é $1/6$.

No ótimo, $A^\top(b-A\beta)=0$: o resíduo é ortogonal ao espaço das colunas de $A$. Isso conecta o ajuste à projeção. A solução é única se as colunas de $A$ forem independentes.

## Como calcular no computador

```python
import numpy as np
A = np.array([[1., 0.], [1., 1.], [1., 2.]])
y = np.array([1., 2., 2.])
beta, residuos, posto, valores_singulares = np.linalg.lstsq(A, y, rcond=None)
print(beta)                       # aproximadamente [1.16666667, 0.5]
print(np.sum((y - A @ beta)**2))  # aproximadamente 1/6
```

As equações normais explicam o problema, mas formá-las explicitamente pode piorar a precisão: para posto completo, o número de condição de $A^\top A$ na norma 2 é o quadrado do de $A$. Fatorações como QR e SVD evitam esse agravamento. `lstsq` também informa posto e valores singulares para investigar redundância.

## Sensibilidade não é erro de ajuste

Para uma matriz invertível, o número de condição na norma 2 é $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$. Um valor grande indica que certas perturbações pequenas podem produzir mudanças grandes na solução. Ele não diz que qualquer perturbação terá o pior efeito possível.

Por exemplo, $A=\operatorname{diag}(1,0{,}001)$ tem condição 1.000. Mudar o segundo componente de $b$ em 0,001 muda o segundo componente da solução em 1. O resíduo da solução exata ainda pode ser zero. Sensibilidade e resíduo medem coisas distintas.

Padronizar pode melhorar diferenças de escala, mas não remove dependência exata entre bandas. Regularização também muda o problema: reduz sensibilidade ao custo de introduzir uma preferência sobre os parâmetros.

## Pratique

1. Ajuste uma constante aos valores 1, 2 e 3. Qual constante minimiza a soma dos erros quadráticos?
2. Por que incluir duas colunas idênticas não permite determinar separadamente seus dois coeficientes?
3. Um ajuste com resíduo zero prova que ele generaliza para outra imagem?

<details><summary>Respostas comentadas</summary>

1. A média, 2. A soma de quadrados é $(1-2)^2+(2-2)^2+(3-2)^2=2$.
2. Só a soma dos coeficientes é identificável: acrescentar um valor a um coeficiente e subtraí-lo do outro mantém as previsões.
3. Não. Pode haver sobreajuste, poucos dados ou diferenças de aquisição. Avaliar generalização exige dados independentes e um desenho de validação adequado.

</details>

Fontes: Pellegrini, tópicos de projeção e mínimos quadrados; [notas de SVD da University of Illinois](https://cs357.cs.illinois.edu/textbook/notes/svd.html), seções de aproximação e condicionamento. Exemplos autorais. [SVD](svd.md) · [Índice](README.md).
