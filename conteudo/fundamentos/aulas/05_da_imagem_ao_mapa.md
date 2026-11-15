# Da imagem ao mapa

Você reconheceu uma área de vegetação na tela. Agora quer saber onde ela fica e qual é sua extensão. Para responder, precisa relacionar os pixels ao espaço geográfico.

## Linha e coluna não são coordenadas do terreno

Uma posição como linha 10, coluna 20 só faz sentido dentro da matriz. A georreferência relaciona posições dessa grade a coordenadas. O sistema de referência de coordenadas, ou CRS, informa como interpretar essas coordenadas.

Um número como `-56` pode representar uma longitude em graus. Ele não deve ser tratado como distância em metros. Confira o CRS antes de medir comprimentos ou áreas. Métodos de cálculo de área precisam considerar a representação da superfície terrestre e a distorção da projeção.

Ter o mesmo CRS também não garante alinhamento. Duas grades podem ter origens, tamanhos de célula e extensões diferentes. Antes de comparar pixels, confira se eles representam a mesma posição.

## Raster e vetor descrevem o espaço de modos diferentes

Uma imagem é um raster, uma grade de células com valores. Um limite de bairro pode ser representado por um polígono vetorial. Um rio pode aparecer como linha em um mapa e como faixa de vários pixels em uma imagem.

Essas representações não são cópias perfeitas do terreno. A linha simplifica a largura do rio. A grade pode misturar margem e água. Escolha a representação de acordo com a pergunta e a escala.

Um sistema de informações geográficas permite relacionar essas camadas. Por exemplo, pode calcular quanto de uma classe mapeada fica dentro de um bairro. Para isso, as camadas precisam ter referências espaciais compatíveis.

## Uma conta de área, com condições explícitas

Em uma grade plana com células de 20 m por 20 m, cada célula tem área de 400 m². Se uma máscara inclui 25 células inteiras, a área na grade é `25 × 400 = 10.000 m²`, ou 1 hectare.

Isso não significa que existem exatamente 25 células de vegetação pura. A máscara pode errar a classe, as bordas podem atravessar pixels e a projeção pode introduzir distorção. A conta é exata para os números propostos, enquanto a interpretação da área no terreno tem limitações.

## Escala do mapa e resolução da imagem

Em um mapa na escala 1:25.000, 1 cm representa 250 m no terreno. Ampliar o mapa na tela altera sua escala de exibição. Isso não acrescenta medições à imagem original.

Uma barra de escala continua útil quando a figura é redimensionada junto com ela. A escala numérica só permanece correta se o tamanho de reprodução for mantido.

<details>
<summary>Exercício com resposta</summary>

Um trecho mede 4 cm em um mapa impresso na escala 1:25.000. Qual distância ele representa?

`4 × 25.000 = 100.000 cm`, equivalentes a 1.000 m ou 1 km. A conta pressupõe que o mapa está no tamanho correspondente à escala indicada. Medir relevo ou uma trajetória curva exige outros cuidados.

</details>

## O que registrar em uma carta-imagem

Uma imagem usada como documento cartográfico precisa permitir entender lugar, data e representação. Registre a fonte, a data da aquisição, a composição de bandas, a escala e o CRS. Inclua legenda quando houver símbolos ou classes. Explique o processamento que altera a interpretação, como um realce ou uma classificação.

Fontes de estudo: Paulo César Gurgel de Albuquerque, [Ensinando cartografia](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_10.pdf), PDF pp. 6–8; José Carlos Moreira, [Geoprocessamento](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_11.pdf), PDF pp. 5–6; Tania Maria Sausen, [Carta-imagem](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_13.pdf), PDF p. 10. O capítulo de geoprocessamento usa o SPRING como contexto histórico; não é preciso instalá-lo para acompanhar esta aula.

[Anterior: interpretar imagens](04_interpretar_imagens.md) · [Próxima: investigar uma mudança](06_investigar_uma_mudanca.md)
