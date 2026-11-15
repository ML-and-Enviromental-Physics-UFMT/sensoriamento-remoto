# Plano de desenvolvimento do repositório

Este plano acompanha a produção do recurso educacional. O estudo pessoal de Bruno fica fora das issues. A [estimativa de estudo](estimativa-de-estudo.md) trata do esforço de um leitor e não consome automaticamente a capacidade registrada aqui.

Base de planejamento em 14/11/2026. O projeto existente no Linear foi atualizado em [P-BRU-14](https://linear.app/brunommv/project/sensoriamento-remoto-com-python-desenvolvimento-da-referencia-aberta-3e1e8c2dc45d). As nove issues BRU-147 a BRU-155 foram convertidas de checklists pessoais por capítulo em entregas de material didático. Foram criadas outras 20 issues, com seis marcos e dependências.

O [documento operacional no Linear](https://linear.app/brunommv/document/plano-de-desenvolvimento-cobertura-ampla-capacidade-e-criterios-de-01e1d03b3c22) contém o mesmo plano, com os links das entregas.

## O que significa concluir uma versão de cobertura ampla

A ambição é cobrir as especialidades do sensoriamento remoto. Para tornar a conclusão verificável, a primeira versão abrangente precisa atender à matriz abaixo. Cada frente deve oferecer entrada para iniciantes, aprofundamento e prática, com avaliação e limites de interpretação.

- Matemática, programação e fundamentos físicos e cartográficos.
- Aquisição, sensores, produtos, metadados, processamento e infraestrutura local/nuvem.
- Análise de imagens, classificação, segmentação, aprendizado profundo e séries temporais.
- Radar/SAR, polarimetria e interferometria; LiDAR; hiperespectral; termal.
- Vegetação, agricultura, cidades, águas continentais, oceanos/costas, atmosfera/clima, geologia, relevo e desastres.
- Dados, incerteza, validação, acessibilidade, referências, direitos de uso e manutenção.

Esse fechamento não esgota o conhecimento da área. Novos métodos e referências continuam a entrar depois. Se a matriz ganhar uma frente ou nível de profundidade adicional, é preciso estimar e incorporar o trabalho, não absorvê-lo silenciosamente no prazo.

## Base observada

O checkout já tem organização por assuntos, textos do núcleo Canty/INPE, exemplos em Python e um piloto PCA/k-means. Na migração, 12 notebooks e 15 scripts executaram. Essa evidência não equivale a validação científica, revisão por outro autor, instalação limpa em todas as plataformas ou publicação das mudanças.

A matemática foi ampliada nesta sessão. A issue de matemática cobre revisão independente, integração e lacunas, sem cobrar de novo a redação já produzida. Há páginas de planejamento em sensores, LiDAR, hiperespectral, termal e aplicações; uma página de entrada não representa uma especialidade concluída.

Na elaboração inicial deste plano, as mudanças estavam locais, sem commit/push. A proposta será submetida por PR autorizado separadamente; isso não declara merge nem publicação de uma versão concluída.

## Capacidade e método da estimativa

Bruno informou **5 horas por semana para desenvolvimento**, separadas do estudo. O calendário assume 46 semanas produtivas por ano, isto é, 230 horas anuais de produção/revisão. Essa margem de calendário cobre semanas sem trabalho; a reserva de esforço abaixo cobre incerteza das tarefas. São fatores distintos.

A estimativa foi feita por pacote de entrega: pesquisa dirigida para produzir o material, redação, exercícios, execução, revisão e documentação. Os intervalos são julgamento inicial, não tempos medidos nem intervalos estatísticos de confiança. Apoio de IA pode acelerar a redação, mas não dispensa revisão de contas, fontes, dados e interpretação.

O total-base é **900–1.476 horas humanas**. Uma reserva global de 25% leva a **1.125–1.845 horas**. A reserva é aplicada uma vez. As descrições das issues mantêm apenas o esforço-base; o campo de pontos do Linear não foi preenchido com horas.

A 5 h/semana, são 225–369 semanas de trabalho. Com 46 semanas produtivas por ano, isso corresponde a aproximadamente **4,9–8,0 anos**. Mantidas as hipóteses e o início em novembro de 2026, a janela é aproximadamente o segundo semestre de 2031 ao fim de 2034. O cenário central cai em 2033. Não é um compromisso de data.

## Fases e entregas intermediárias

| Marco | Entrega | Esforço-base da fase | Janela acumulada condicional |
|-------|---------|---------------------|------------------------------|
| M0 | Base editorial, computacional e matemática | 96–160 h | 2027-05 a 2027-09 |
| M1 | Núcleo de análise de imagens revisado | 164–276 h | 2028-04 a 2029-03 |
| M2 | Física, sensores e avaliação | 136–216 h | 2029-01 a 2030-05 |
| M3 | Especialidades e métodos avançados | 288–480 h | 2030-07 a 2032-12 |
| M4 | Aplicações integradas por área | 160–256 h | 2031-06 a 2034-05 |
| M5 | Revisão pública e versão abrangente | 56–88 h | 2031-09 a 2034-11 |

As datas-alvo no Linear representam o trimestre do cenário central. As janelas acima usam os limites inferior e superior acumulados. Não são períodos para trabalhar simultaneamente em tudo, nem prazos de estudo. A capacidade total de 5 horas é compartilhada entre as frentes.

O primeiro marco entrega uma entrada estável e uma base matemática/programacional. O segundo fecha um núcleo de análise de imagens utilizável. Não é preciso esperar a versão abrangente para esses percursos serem úteis; eventual publicação continua dependendo de decisão própria.

## Pacotes e dependências no Linear

| Issue | Entrega | Esforço-base | Depende de |
|-------|---------|--------------|------------|
| [BRU-198](https://linear.app/brunommv/issue/BRU-198/estabilizar-ambiente-caminhos-e-integracao-continua) | Estabilizar ambiente, caminhos e integração contínua | 16–24 h | Sem pré-requisito de issue |
| [BRU-199](https://linear.app/brunommv/issue/BRU-199/documentar-procedencia-acesso-e-qualidade-dos-dados-de-exemplo) | Documentar procedência, acesso e qualidade dos dados de exemplo | 20–32 h | Sem pré-requisito de issue |
| [BRU-200](https://linear.app/brunommv/issue/BRU-200/produzir-percurso-de-python-e-numpy-para-iniciantes) | Produzir percurso de Python e NumPy para iniciantes | 24–40 h | BRU-198 |
| [BRU-201](https://linear.app/brunommv/issue/BRU-201/revisar-e-consolidar-o-percurso-de-matematica-por-topicos) | Revisar e consolidar o percurso de matemática por tópicos | 20–36 h | BRU-198 |
| [BRU-147](https://linear.app/brunommv/issue/BRU-147/consolidar-fundamentos-e-representacao-de-imagens-para-iniciantes) | Consolidar fundamentos e representação de imagens para iniciantes | 16–28 h | BRU-200, BRU-201 |
| [BRU-148](https://linear.app/brunommv/issue/BRU-148/fechar-estatistica-aplicada-de-imagens) | Fechar estatística aplicada de imagens | 16–28 h | BRU-201, BRU-199 |
| [BRU-149](https://linear.app/brunommv/issue/BRU-149/fechar-transformacoes-pca-mnf-fourier-e-wavelets) | Fechar transformações, PCA, MNF, Fourier e wavelets | 20–32 h | BRU-148 |
| [BRU-150](https://linear.app/brunommv/issue/BRU-150/fechar-filtros-kernels-e-vizinhanca) | Fechar filtros, kernels e vizinhança | 16–28 h | BRU-148 |
| [BRU-151](https://linear.app/brunommv/issue/BRU-151/fechar-realce-calibracao-correcoes-e-registro) | Fechar realce, calibração, correções e registro | 24–40 h | BRU-199, BRU-147 |
| [BRU-152](https://linear.app/brunommv/issue/BRU-152/fechar-classificacao-supervisionada-com-amostras-reais) | Fechar classificação supervisionada com amostras reais | 24–40 h | BRU-151, BRU-148 |
| [BRU-153](https://linear.app/brunommv/issue/BRU-153/fechar-redes-treinamento-e-avaliacao-de-modelos) | Fechar redes, treinamento e avaliação de modelos | 24–40 h | BRU-152 |
| [BRU-154](https://linear.app/brunommv/issue/BRU-154/fechar-agrupamento-e-interpretacao-dos-grupos) | Fechar agrupamento e interpretação dos grupos | 16–28 h | BRU-149 |
| [BRU-155](https://linear.app/brunommv/issue/BRU-155/fechar-comparacao-bitemporal-e-deteccao-de-mudanca) | Fechar comparação bitemporal e detecção de mudança | 24–40 h | BRU-151, BRU-149 |
| [BRU-202](https://linear.app/brunommv/issue/BRU-202/desenvolver-sensores-orbitas-produtos-e-cartografia-pratica) | Desenvolver sensores, órbitas, produtos e cartografia prática | 32–48 h | BRU-147, BRU-199 |
| [BRU-203](https://linear.app/brunommv/issue/BRU-203/desenvolver-transferencia-radiativa-e-fundamentos-fisicos-avancados) | Desenvolver transferência radiativa e fundamentos físicos avançados | 48–80 h | BRU-201, BRU-202 |
| [BRU-204](https://linear.app/brunommv/issue/BRU-204/desenvolver-amostragem-validacao-e-propagacao-de-incerteza) | Desenvolver amostragem, validação e propagação de incerteza | 32–48 h | BRU-148, BRU-152 |
| [BRU-205](https://linear.app/brunommv/issue/BRU-205/desenvolver-sig-catalogos-nuvem-e-processamento-escalavel) | Desenvolver SIG, catálogos, nuvem e processamento escalável | 24–40 h | BRU-202, BRU-198 |
| [BRU-206](https://linear.app/brunommv/issue/BRU-206/desenvolver-percurso-completo-de-radar-e-sar) | Desenvolver percurso completo de radar e SAR | 64–112 h | BRU-203, BRU-150, BRU-204 |
| [BRU-207](https://linear.app/brunommv/issue/BRU-207/desenvolver-percurso-de-lidar-e-nuvens-de-pontos) | Desenvolver percurso de LiDAR e nuvens de pontos | 48–80 h | BRU-202, BRU-201, BRU-204 |
| [BRU-208](https://linear.app/brunommv/issue/BRU-208/desenvolver-percurso-hiperespectral) | Desenvolver percurso hiperespectral | 48–80 h | BRU-203, BRU-149, BRU-204 |
| [BRU-209](https://linear.app/brunommv/issue/BRU-209/desenvolver-percurso-termal-e-recuperacao-de-temperatura) | Desenvolver percurso termal e recuperação de temperatura | 48–80 h | BRU-203, BRU-204 |
| [BRU-210](https://linear.app/brunommv/issue/BRU-210/ampliar-series-temporais-densas-e-deteccao-de-rupturas) | Ampliar séries temporais densas e detecção de rupturas | 40–64 h | BRU-155, BRU-204 |
| [BRU-211](https://linear.app/brunommv/issue/BRU-211/desenvolver-segmentacao-aprendizado-profundo-e-fusao) | Desenvolver segmentação, aprendizado profundo e fusão | 40–64 h | BRU-153, BRU-204 |
| [BRU-212](https://linear.app/brunommv/issue/BRU-212/produzir-aplicacoes-de-vegetacao-agricultura-e-cidades) | Produzir aplicações de vegetação, agricultura e cidades | 40–64 h | BRU-152, BRU-210, BRU-209 |
| [BRU-213](https://linear.app/brunommv/issue/BRU-213/produzir-aplicacoes-de-aguas-continentais-zonas-costeiras-e-oceanos) | Produzir aplicações de águas continentais, zonas costeiras e oceanos | 40–64 h | BRU-203, BRU-208, BRU-204 |
| [BRU-214](https://linear.app/brunommv/issue/BRU-214/produzir-aplicacoes-de-atmosfera-e-clima) | Produzir aplicações de atmosfera e clima | 40–64 h | BRU-203, BRU-210, BRU-204 |
| [BRU-215](https://linear.app/brunommv/issue/BRU-215/produzir-aplicacoes-de-geologia-relevo-e-desastres) | Produzir aplicações de geologia, relevo e desastres | 40–64 h | BRU-206, BRU-207, BRU-208 |
| [BRU-216](https://linear.app/brunommv/issue/BRU-216/revisar-acessibilidade-navegacao-e-material-com-leitores) | Revisar acessibilidade, navegação e material com leitores | 32–48 h | BRU-212, BRU-213, BRU-214, BRU-215, BRU-211, BRU-205 |
| [BRU-217](https://linear.app/brunommv/issue/BRU-217/preparar-versao-de-cobertura-ampla-e-manutencao) | Preparar versão de cobertura ampla e manutenção | 24–40 h | BRU-216 |

As dependências indicam material necessário à aceitação da entrega. Rascunhos podem ser escritos antes de todas elas terminarem, mas não devem ser declarados concluídos sem a integração. Não há dependências cíclicas no plano.

## Critério comum de pronto

Uma entrega precisa de explicação própria e fontes verificáveis, símbolos e unidades definidos, exemplo resolvido, exercícios com respostas comentadas, pré-requisitos e limites explícitos. Práticas devem executar no ambiente documentado; links, figuras e leitura matemática precisam ser acessíveis.

Inferências com dados reais precisam de referência de avaliação adequada. Dados sintéticos e rótulos produzidos pelo mesmo índice usado no treinamento não demonstram acurácia real. PDFs continuam fora do Git. Dados e código de terceiros exigem condições de uso documentadas.

A evidência do trabalho pode ser um relatório de execução e revisão, um diff revisado ou outra verificação apropriada. Não marcar Done apenas porque a IA escreveu o texto ou o notebook executou.

## Controle da incerteza

Reestimar depois dos dois primeiros pacotes e ao fechar cada marco. Registrar horas reais de produção e revisão, falhas e retrabalho; comparar com os intervalos. Não converter o desempenho inicial em velocidade garantida para uma especialidade ainda não conhecida.

Os maiores riscos são aprofundamento do escopo, obtenção/licença de dados, cobertura de referências, validação independente, disponibilidade de revisão técnica e compatibilidade do legado. Se uma frente atrasar, atualizar dependências e projeções; preservar o escopo visível, em vez de esconder a lacuna.

O arquivo [desenvolvimento.json](desenvolvimento.json) registra pacotes, horas, dependências e links usados nesta versão do plano. O Linear é o acompanhamento operacional; atualizar a cópia local quando o plano mudar.


## Confirmação do horizonte

Bruno confirmou que não há problema com o horizonte de tempo e pediu para manter o planejamento como está. A possibilidade de terminar antes não altera as estimativas-base, a reserva, a capacidade de 5 h/semana nem as datas de referência. Reestimar com evidência de esforço real após as primeiras entregas.
