# Por que cada alvo responde de um jeito?

Na aula anterior, um pixel tinha vermelho 0,10 e NIR 0,50. Por que duas bandas do mesmo lugar podem ter valores tão diferentes? A resposta começa na interação da energia com o material.

Leitura sugerida em dois momentos. Primeiro acompanhe o exemplo da folha. Depois abra o aprofundamento se quiser entender a relação entre comprimento de onda e frequência.

## Uma folha recebe energia

Ao atingir uma folha, parte da energia é refletida, parte é absorvida e parte atravessa o material. Essas proporções dependem do comprimento de onda. Não existe uma única "reflectância da folha" válida para todo o espectro.

No visível, pigmentos absorvem parte da radiação. Em folhas verdes, a absorção costuma ser forte no azul e no vermelho, enquanto uma fração maior do verde pode ser refletida. No infravermelho próximo, o espalhamento na estrutura interna da folha ajuda a explicar uma reflectância maior. Não é a folha emitindo calor nessa banda.

A presença de água também modifica a resposta espectral, com absorções relevantes em regiões do infravermelho. Isso permite estudar propriedades da vegetação, mas uma banda isolada não mede diretamente "saúde da planta".

O satélite raramente observa uma folha isolada. Ele recebe a contribuição de um dossel, o conjunto de copas, folhas, galhos e espaços entre eles. Solo e sombra entram nessa mistura. A disposição das folhas pode alterar o sinal mesmo quando a espécie permanece a mesma.

## Uma conta pequena

Imagine um experimento simplificado. Em uma banda, chegam 100 unidades de energia a uma folha. Ela reflete 20, absorve 50 e transmite 30. A soma fecha em 100. A fração refletida é 20/100, ou 0,20.

Agora imagine outra banda, na qual ela reflete 50, absorve 10 e transmite 40. O material é o mesmo, mas sua resposta depende da banda. É essa diferença que torna útil medir várias faixas do espectro.

Essas contas são inventadas e representam um balanço simplificado. Uma medição direcional por satélite também depende da geometria, da atmosfera e da resposta do instrumento.

## E a água ou o solo?

Água limpa costuma apresentar sinal baixo no NIR. Porém, um corpo d'água pode conter sedimentos e organismos, ter fundo visível ou refletir o Sol em direção ao sensor. Portanto, "água é sempre preta" é uma regra fraca.

A resposta do solo depende de fatores como minerais, matéria orgânica, umidade e textura. Dois solos podem parecer diferentes sem que um seja vegetação. Solo e sombra também podem se misturar com plantas dentro de um pixel.

## A atmosfera participa da medição

Parte da energia é absorvida por gases. Parte é espalhada por moléculas e partículas. Algumas faixas permitem maior passagem de radiação e são chamadas janelas atmosféricas. Isso não significa transparência perfeita.

Uma camada de fumaça pode mudar o sinal recebido sem mudar o solo. Correção atmosférica procura estimar a contribuição da atmosfera, mas não reconstrói automaticamente a superfície escondida por uma nuvem espessa.

<details>
<summary>Aprofundamento opcional: comprimento de onda e frequência</summary>

O comprimento de onda, representado por `λ`, mede a distância entre pontos equivalentes de uma onda. A frequência, `f`, mede quantos ciclos passam por segundo. No vácuo, `c = λ*f`, em que `c` é a velocidade da luz.

Se o comprimento de onda dobra, a frequência cai pela metade. A energia de cada fóton obedece a `E = h*f = h*c/λ`, sendo `h` a constante de Planck. Essa energia por fóton não é a mesma coisa que a energia total de um feixe, que também depende da quantidade de fótons.

Nas unidades usadas nas bandas, 1 µm equivale a 1.000 nm. Assim, 0,65 µm e 650 nm descrevem o mesmo comprimento de onda. Não é necessário memorizar frequências para ler uma imagem multiespectral.

</details>

## Verifique se entendeu

Uma copa ficou mais escura no NIR entre duas imagens. Isso prova que a espécie mudou?

<details>
<summary>Resposta comentada</summary>

Não. Mudanças na estrutura do dossel, sombra, umidade, atmosfera ou geometria podem alterar o sinal. Antes de atribuir uma causa, confira as condições da observação e procure informação independente.

</details>

Fonte de estudo: Elisabete Caria de Moraes, [Fundamentos de sensoriamento remoto](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_1.pdf), PDF pp. 7–18; Flávio Jorge Ponzoni, [Sensoriamento remoto no estudo da vegetação](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_8.pdf), PDF pp. 8–14. Exemplos e contas desta aula são autorais.

[Anterior: da paisagem ao número](01_da_paisagem_ao_numero.md) · [Próxima: escolher a observação](03_satelites_e_observacao.md)
