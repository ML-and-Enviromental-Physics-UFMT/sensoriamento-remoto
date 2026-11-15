# Probabilidade e informação condicional

Um classificador pode indicar que um pixel é compatível com água. Para entender essa afirmação, precisamos distinguir a frequência de água na área da chance de observar determinado sinal quando há água. Inverter essas duas probabilidades é um erro comum.

## Experimentos, eventos e condições

Uma probabilidade está ligada a um modelo ou mecanismo de amostragem. Se sorteamos uniformemente um pixel entre 100 pixels válidos de uma área e 20 deles têm classe de referência água, a probabilidade de selecionar água nesse conjunto é $20/100=0{,}20$.

Um evento é um conjunto de resultados, como selecionar água. Uma variável aleatória atribui um valor a cada resultado. Pode ser discreta, como uma classe, ou contínua no modelo, como reflectância antes da quantização digital.

Para eventos $A$ e $B$ com $P(B)>0$,

$$P(A\mid B)=\frac{P(A\cap B)}{P(B)}.$$

O símbolo $\mid$ significa “sabendo que”. Condicionar muda o conjunto de referência. $P(A\mid B)$ não é, em geral, igual a $P(B\mid A)$. Independência significaria $P(A\cap B)=P(A)P(B)$; não é algo a presumir só porque os dados estão em linhas diferentes de uma tabela.

## Exemplo de Bayes resolvido

Considere 1.000 pixels hipotéticos. A referência indica 200 de água e 800 de não água. Uma regra chama 180 pixels de água corretamente, mas também chama 80 pixels de não água de água.

| Referência | Regra positiva | Regra negativa | Total |
|------------|----------------|----------------|-------|
| Água | 180 | 20 | 200 |
| Não água | 80 | 720 | 800 |

A regra é positiva em $180+80=260$ pixels. Assim, entre os positivos, a proporção de água é $180/260\approx0{,}6923$. Ela é diferente da sensibilidade $180/200=0{,}90$.

A mesma conta pode ser escrita por Bayes. Defina $W$ como água e $+$ como regra positiva. Temos $P(W)=0{,}20$, $P(+\mid W)=0{,}90$ e $P(+\mid\neg W)=0{,}10$. Então

$$P(W\mid+)=\frac{0{,}90\cdot0{,}20}{0{,}90\cdot0{,}20+0{,}10\cdot0{,}80}
=\frac{0{,}18}{0{,}26}\approx0{,}6923.$$

O denominador soma as duas maneiras de produzir um positivo. Não é uma constante escolhida para favorecer a hipótese.

## O contexto altera a interpretação

Se a prevalência de água cair para 1%, mantendo as duas taxas condicionais do exemplo, o valor passa a $`0{,}009/(0{,}009+0{,}099)\approx8{,}33\%`$. O resultado depende do contexto. Isso não prova que as taxas condicionais realmente permaneceriam iguais ao transferir uma regra para outra região.

Para uma medida contínua $x$, o classificador gaussiano usa densidades condicionais $p(x\mid W)$, não probabilidades de observar exatamente aquele número. A verossimilhança considera o sinal observado como fixo e compara parâmetros ou hipóteses. A probabilidade posterior também precisa das probabilidades anteriores e do modelo adotado.

Uma saída numérica de um classificador não é automaticamente uma probabilidade calibrada. Calibração deve ser avaliada com dados de referência adequados e separados do ajuste.

## Pratique

1. No conjunto da tabela, qual é $P(W\cap+)$?
2. Qual é $P(W\mid-)$?
3. Se dois pixels são vizinhos, a classe de um pode informar sobre a do outro? Isso é compatível com independência?

<details><summary>Respostas comentadas</summary>

1. $180/1000=0{,}18$, pois sorteamos no conjunto completo.
2. Há 20 pixels de água entre $20+720=740$ negativos. Portanto, $`20/740\approx2{,}70\%`$.
3. Pode informar, por exemplo em um lago ou talhão. Nessa situação, não devemos tratar independência entre pixels como fato. A hipótese precisa ser examinada no desenho amostral e na avaliação.

</details>

Fonte: Canty (2019), seções 2.1 e 2.4, sobre variáveis aleatórias, Bayes, verossimilhança e classificação. Números e tabela autorais. [Distribuições e estimação](distribuicoes-e-estimacao.md) · [Índice de matemática](../README.md).
