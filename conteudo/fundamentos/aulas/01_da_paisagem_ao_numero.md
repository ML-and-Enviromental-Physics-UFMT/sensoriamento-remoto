# Da paisagem ao número

Uma pergunta possível em Cuiabá é se a vegetação de uma área diminuiu entre duas datas. Antes de escolher um algoritmo, precisamos saber o que o satélite observa e o que pode mudar na imagem sem que as plantas tenham sido removidas.

Nesta primeira leitura, fique com uma ideia. Uma imagem de satélite reúne medições, e cada medição precisa de contexto para virar informação sobre o terreno.

## O que chega ao sensor

Sensoriamento remoto permite investigar um alvo sem tocá-lo diretamente, por meio da energia detectada por um sensor. O satélite transporta o sensor; o sensor faz a medição.

Em uma imagem de luz solar refletida, a energia atravessa a atmosfera, interage com a superfície e percorre a atmosfera novamente até o instrumento. O sinal recebido depende do alvo e desse caminho.

Sensores passivos medem energia disponível, como luz solar refletida ou emissão térmica. O imageamento solar depende de iluminação; o termal pode observar à noite. Um radar é ativo, emite micro-ondas e mede o retorno. Seu brilho depende de propriedades como umidade, rugosidade e geometria. Não se interpreta radar como reflectância óptica.

## Por que um pixel tem várias medições

Uma banda mede uma faixa de comprimentos de onda. Vermelho e infravermelho próximo, ou NIR, são duas dessas faixas. O olho humano não vê NIR, mas um sensor pode medi-lo.

Considere reflectâncias hipotéticas, sem unidade.

| Pixel | Vermelho | NIR |
|-------|----------|-----|
| A | 0,10 | 0,50 |
| B | 0,20 | 0,25 |

O A apresenta maior contraste entre NIR e vermelho. Esse padrão pode ser compatível com vegetação verde. Ele não identifica sozinho uma espécie nem demonstra a quantidade de carbono armazenada.

A imagem organiza as medições em linhas e colunas. Cada célula é um pixel. Uma banda forma uma matriz; várias bandas formam uma pilha de matrizes. Assim, o pixel A contém um vetor de dois valores, `[0,10; 0,50]`, na ordem vermelho e NIR.

## O pixel pode misturar alvos

Uma célula de 10 m por 10 m tem área nominal de 100 m². Nela podem caber copa, solo e parte de um telhado. A resposta espacial do instrumento também pode envolver a vizinhança.

Por isso, não trate um pixel como uma árvore. E não espere recuperar uma árvore isolada só por reamostrar uma imagem de 30 m para uma grade de 10 m. A nova grade tem mais células, mas o sensor não fez novas medições.

## A tela não mostra uma grandeza automaticamente

Uma composição escolhe bandas para os canais vermelho, verde e azul da tela. Se colocarmos NIR no canal vermelho, a vegetação pode aparecer vermelha. Mudou a exibição, não a superfície.

Um número digital, ou DN, é um código armazenado. A documentação do produto informa se ele representa radiância, reflectância ou outra grandeza e quais conversões são necessárias. Esticar os valores para deixar a figura mais legível não aplica essa conversão e não remove a atmosfera.

## Experimente uma conta

O NDVI combina NIR e vermelho.

```text
NDVI = (NIR - vermelho) / (NIR + vermelho)
```

No A, a conta é `(0,50 - 0,10) / (0,50 + 0,10)`, aproximadamente 0,67. No B, é aproximadamente 0,11. A diferença resume o contraste entre essas bandas, mas não fornece um limiar universal para classificar floresta.

A conta pressupõe entradas adequadas. Em dados reais, confira escala, deslocamento e máscaras do produto. Denominador zero não gera um índice válido. NoData indica ausência de dado válido e não deve entrar automaticamente como zero.

## Tente explicar

1. Vegetação vermelha na tela significa que ela mudou de cor no terreno?
2. Um DN igual a 2500 já informa a reflectância?
3. Um pixel com NDVI maior prova maior área de floresta?

<details>
<summary>Respostas comentadas</summary>

1. Não. A cor depende das bandas atribuídas aos canais e do realce escolhido.
2. Não. Faltam a grandeza armazenada e as regras de conversão e validade do produto.
3. Não. O índice depende da resposta espectral, da mistura de alvos e das condições da observação. Uma classe de cobertura exige mais evidências.

</details>

Agora abra [Seu primeiro pixel](../notebooks/00_primeiro_pixel.ipynb). Os números são inventados, sem dados externos. Depois continue em [Energia e resposta dos alvos](02_energia_e_alvos.md), para entender por que as bandas diferem.

Fonte de estudo: Elisabete Caria de Moraes, [Fundamentos de sensoriamento remoto](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_1.pdf), PDF pp. 7–21. A representação por matrizes prepara as seções 1.1 e 1.3 de Canty (2019). Texto, perguntas e números desta aula são autorais.
