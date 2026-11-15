# Gradiente descendente e escolha do passo

O gradiente informa uma direção local. Um algoritmo ainda precisa decidir quanto andar, quando parar e como conferir o resultado. Um passo mal escolhido pode aumentar o erro, mesmo seguindo o negativo do gradiente.

Pré-requisito: [derivadas e gradientes](../calculo/derivadas-e-gradientes.md).

## A atualização

Para parâmetros $\theta$, função objetivo diferenciável $L$ e passo $\eta>0$,

$$\theta_{t+1}=\theta_t-\eta\nabla L(\theta_t).$$

O índice $t$ identifica a iteração. O passo também é chamado taxa de aprendizagem. Em um problema geral, um valor fixo não garante descida em todo ponto. Podemos precisar de busca de passo, reescala ou outro algoritmo.

## Exemplo resolvido

Minimizamos $L(w)=(2w-3)^2$, cuja derivada é $4(2w-3)$. Começamos com $w_0=0$ e escolhemos $\eta=0{,}1$.

| Iteração | $w$ | Derivada | $L(w)$ |
|----------|-----|----------|--------|
| 0 | 0 | −12 | 9 |
| 1 | 1,2 | −2,4 | 0,36 |
| 2 | 1,44 | −0,48 | 0,0144 |
| 3 | 1,488 | −0,096 | 0,000576 |

A primeira atualização é $0-0{,}1(-12)=1{,}2$. A segunda é $1{,}2-0{,}1(-2{,}4)=1{,}44$. O mínimo analítico é $w=1{,}5$, portanto conseguimos comparar aproximação e solução conhecida.

Definindo o erro de parâmetro $e_t=w_t-1{,}5$, obtemos $e_{t+1}=(1-8\eta)e_t$. Para que ele diminua em módulo com passo constante, precisamos de $|1-8\eta|<1$, isto é, $0<\eta<0{,}25$. Essa faixa vale para esta função, não para qualquer modelo.

Com $\eta=0{,}3$, o fator é −1,4. O parâmetro oscila e se afasta do mínimo. O sinal negativo indica alternância; o módulo maior que 1 indica crescimento do erro.

## Escala, custo e generalização

Em várias dimensões, curvaturas muito diferentes por direção podem tornar um passo seguro em um eixo ruim para outro. Padronizar entradas pode ajudar a geometria do ajuste, mas muda o pré-processamento e precisa ser registrado e ajustado apenas com os dados de treinamento.

O gradiente de toda a amostra pode ser caro. Métodos estocásticos usam observações ou minibatches e produzem atualizações ruidosas. Um erro que oscila de uma iteração para outra não tem, sozinho, a mesma interpretação da divergência determinística demonstrada acima.

Não confunda erro de treinamento com erro de avaliação. Parada antecipada usa uma partição de validação e não deve consultar repetidamente o conjunto reservado para a avaliação final.

## Experimento

```python
w = 0.0
passo = 0.1
for t in range(4):
    perda = (2*w - 3)**2
    print(t, w, perda)
    w -= passo * 4*(2*w - 3)
```

Compare a saída com a tabela. Depois altere `passo` para 0,3 e explique o padrão antes de executar mais iterações. Não é preciso baixar imagens para estudar o mecanismo.

## Pratique

1. Qual é o fator de redução do erro para $\eta=0{,}1$ no exemplo?
2. O que ocorre com $\eta=0{,}25$ se o parâmetro inicial não for o mínimo?
3. Qual informação adicional você buscaria antes de concluir que uma perda pequena indica um modelo útil?

<details><summary>Respostas comentadas</summary>

1. $1-8\cdot0{,}1=0{,}2$: o erro de parâmetro é multiplicado por 0,2 a cada passo. A perda quadrática é multiplicada por 0,04.
2. O fator é −1. O erro alterna de sinal, mas mantém o módulo; a sequência não converge ao mínimo.
3. Desempenho em referência independente, representatividade, métricas por classe e espacialização dos erros, além da compatibilidade com a pergunta. A perda de treino não responde sozinha a isso.

</details>

Fonte de ligação às aplicações: Canty (2019), seção 1.6, capítulo 6 e Apêndice B. O exemplo quadrático e sua faixa de convergência foram derivados aqui. [Lagrange](lagrange.md) · [Índice](../README.md).
