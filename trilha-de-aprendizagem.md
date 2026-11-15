# Trilha de aprendizagem

O objetivo é cobrir o sensoriamento remoto de forma ampla, com entradas acessíveis e aprofundamento progressivo. O núcleo atual permite começar pela interpretação física e chegar a análise de imagens, classificação e comparação entre datas. As outras frentes serão integradas conforme suas aulas forem desenvolvidas.

## Sequência inicial

| Etapa | Pergunta | Material |
|-------|----------|----------|
| Primeiro contato | O que o sensor mede? | [Fundamentos](conteudo/fundamentos/README.md) |
| Matemática de apoio | Como representar e transformar as medições? | [Matemática](conteudo/matematica/README.md), em paralelo às aplicações |
| Preparação | Posso comparar estes pixels? | [Pré-processamento](conteudo/pre-processamento/README.md) |
| Descrição | Como resumir a variação das bandas? | [Estatística](conteudo/analise-de-imagens/estatistica/README.md) |
| Transformação | O que uma combinação de bandas revela ou perde? | [Transformações](conteudo/analise-de-imagens/transformacoes/README.md) |
| Vizinhança | Como os pixels próximos entram na análise? | [Filtros](conteudo/analise-de-imagens/filtros/README.md) |
| Classes | Como aprender com exemplos e avaliar erros? | [Classificação](conteudo/classificacao/README.md) |
| Mudança | O que mudou no terreno e o que mudou na aquisição? | [Séries temporais](conteudo/series-temporais/README.md) |
| Integração | Consigo explicar um fluxo completo? | [Projetos](projetos/README.md) |

Os métodos podem exigir retornos à matemática. Não é necessário terminar todos os livros antes de começar os exemplos. A sequência de Python/NumPy de entrada e a inspeção guiada de metadados ainda precisam de aulas próprias.

## Matemática com várias referências

O percurso reúne álgebra linear, probabilidade, estatística e, progressivamente, cálculo e otimização. O [guia atual](conteudo/matematica/README.md) indica o que já existe e os tópicos disponíveis e os aprofundamentos pendentes.

A [bibliografia de matemática](referencias/matematica/README.md) inclui *Álgebra linear*, de Jerônimo C. Pellegrini, e *Álgebra Linear I*, volume 1, do CEDERJ, hospedado na UFJF. Outros livros poderão complementar cada assunto. Cada tópico deve apontar as fontes e as seções usadas, sem ficar presa à organização de uma obra.

## Especialidades e aplicações

| Frente | Entrada atual e expansão prevista |
|--------|----------------------------------|
| [Sensores](conteudo/sensores/README.md) | Ampliar órbitas, plataformas, resposta dos instrumentos, aquisição e produtos |
| [Radar e SAR](conteudo/radar-sar/README.md) | Partir da nota existente e construir processamento, polarimetria e interferometria |
| [LiDAR](conteudo/lidar/README.md) | Desenvolver nuvens de pontos e modelos de superfície, terreno e vegetação |
| [Hiperespectral](conteudo/hiperespectral/README.md) | Desenvolver espectroscopia, mistura e identificação de materiais |
| [Termal](conteudo/termal/README.md) | Desenvolver emissão, emissividade, atmosfera e recuperação de temperatura |
| [Aplicações](conteudo/aplicacoes/README.md) | Organizar vegetação, agricultura, cidades, água, oceanos, atmosfera, clima, geologia e desastres |

Essas entradas são um mapa de desenvolvimento, não uma declaração de conteúdo concluído. Novos temas podem ser incorporados sem criar uma nova coleção de pastas por livro.

## Como avançar sem tornar a leitura pesada

Leia uma seção curta, faça uma previsão e execute um exemplo pequeno. Depois altere uma condição e explique o efeito. Use o [diário](docs/modelo-diario.md) para registrar sua explicação e localizar a dúvida. O [guia de estudo](docs/como-estudar.md) detalha esse ciclo.

Uma aula deve apresentar a pergunta, o fenômeno, a representação e a prática. Equações precisam de símbolos definidos e de um exemplo numérico. Detalhes que interrompem a primeira leitura podem ficar em aprofundamentos opcionais.

Dados simulados devem ser identificados. Dados reais precisam de procedência, unidade, escala, validade e condições de acesso. Executar sem erro não demonstra que o resultado foi interpretado corretamente.

## Referências e desenvolvimento

As [apostilas do INPE](referencias/inpe/README.md) sustentam as aulas introdutórias. O [mapa do Canty](referencias/canty.md) mostra onde cada capítulo foi incorporado. Os catálogos contêm links para as fontes; PDFs ficam apenas no computador, ignorados pelo Git.

Consulte as [pendências](docs/pendencias.md) para o trabalho a desenvolver. A validação dos métodos com dados reais permanece distinta das demonstrações didáticas.

O esforço estimado do leitor está na [estimativa de estudo](docs/planejamento/estimativa-de-estudo.md). As entregas para ampliar o repositório ficam no [plano de desenvolvimento](docs/planejamento/desenvolvimento.md) e no Linear, sem registrar estudo pessoal.
