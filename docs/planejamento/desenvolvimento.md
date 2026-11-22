# Plano de desenvolvimento do repositório

Este plano acompanha a produção do recurso educacional. O estudo individual de quem contribui fica fora das issues. A [estimativa de estudo](estimativa-de-estudo.md) trata do esforço de um leitor e não consome automaticamente a capacidade registrada aqui.

Base de planejamento em 14/11/2026. As 29 entregas estão nas [issues do repositório](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues), distribuídas em seis [marcos](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/milestones), com dependências registradas em cada issue. O quadro do projeto da organização acompanha status, prioridade e horas estimadas.

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

O plano considera uma capacidade de **5 horas por semana para desenvolvimento**, separadas do estudo. O calendário assume 46 semanas produtivas por ano, isto é, 230 horas anuais de produção/revisão. Essa margem de calendário cobre semanas sem trabalho; a reserva de esforço abaixo cobre incerteza das tarefas. São fatores distintos.

A estimativa foi feita por pacote de entrega: pesquisa dirigida para produzir o material, redação, exercícios, execução, revisão e documentação. Os intervalos são julgamento inicial, não tempos medidos nem intervalos estatísticos de confiança. Apoio de IA pode acelerar a redação, mas não dispensa revisão de contas, fontes, dados e interpretação.

O total-base é **900–1.476 horas humanas**. Uma reserva global de 25% leva a **1.125–1.845 horas**. A reserva é aplicada uma vez. As descrições das issues mantêm apenas o esforço-base; no quadro do projeto, os campos de horas mínimas e máximas registram essa mesma faixa.

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

As datas dos marcos representam o trimestre do cenário central. As janelas acima usam os limites inferior e superior acumulados. Não são períodos para trabalhar simultaneamente em tudo, nem prazos de estudo. A capacidade total de 5 horas é compartilhada entre as frentes.

O primeiro marco entrega uma entrada estável e uma base matemática/programacional. O segundo fecha um núcleo de análise de imagens utilizável. Não é preciso esperar a versão abrangente para esses percursos serem úteis; eventual publicação continua dependendo de decisão própria.

## Pacotes e dependências

| Issue | Entrega | Esforço-base | Depende de |
|-------|---------|--------------|------------|
| [#1](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/1) | Estabilizar ambiente, caminhos e integração contínua | 16–24 h | Sem pré-requisito |
| [#2](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/2) | Documentar procedência, acesso e qualidade dos dados de exemplo | 20–32 h | Sem pré-requisito |
| [#3](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/3) | Produzir percurso de Python e NumPy para iniciantes | 24–40 h | #1 |
| [#4](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/4) | Revisar e consolidar o percurso de matemática por tópicos | 20–36 h | #1 |
| [#5](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/5) | Consolidar fundamentos e representação de imagens para iniciantes | 16–28 h | #3, #4 |
| [#6](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/6) | Fechar estatística aplicada de imagens | 16–28 h | #4, #2 |
| [#7](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/7) | Fechar transformações, PCA, MNF, Fourier e wavelets | 20–32 h | #6 |
| [#8](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/8) | Fechar filtros, kernels e vizinhança | 16–28 h | #6 |
| [#9](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/9) | Fechar realce, calibração, correções e registro | 24–40 h | #2, #5 |
| [#10](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/10) | Fechar classificação supervisionada com amostras reais | 24–40 h | #9, #6 |
| [#11](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/11) | Fechar redes, treinamento e avaliação de modelos | 24–40 h | #10 |
| [#12](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/12) | Fechar agrupamento e interpretação dos grupos | 16–28 h | #7 |
| [#13](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/13) | Fechar comparação bitemporal e detecção de mudança | 24–40 h | #9, #7 |
| [#14](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/14) | Desenvolver sensores, órbitas, produtos e cartografia prática | 32–48 h | #5, #2 |
| [#15](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/15) | Desenvolver transferência radiativa e fundamentos físicos avançados | 48–80 h | #4, #14 |
| [#16](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/16) | Desenvolver amostragem, validação e propagação de incerteza | 32–48 h | #6, #10 |
| [#17](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/17) | Desenvolver SIG, catálogos, nuvem e processamento escalável | 24–40 h | #14, #1 |
| [#18](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/18) | Desenvolver percurso completo de radar e SAR | 64–112 h | #15, #8, #16 |
| [#19](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/19) | Desenvolver percurso de LiDAR e nuvens de pontos | 48–80 h | #14, #4, #16 |
| [#20](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/20) | Desenvolver percurso hiperespectral | 48–80 h | #15, #7, #16 |
| [#21](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/21) | Desenvolver percurso termal e recuperação de temperatura | 48–80 h | #15, #16 |
| [#22](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/22) | Ampliar séries temporais densas e detecção de rupturas | 40–64 h | #13, #16 |
| [#23](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/23) | Desenvolver segmentação, aprendizado profundo e fusão | 40–64 h | #11, #16 |
| [#24](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/24) | Produzir aplicações de vegetação, agricultura e cidades | 40–64 h | #10, #22, #21 |
| [#25](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/25) | Produzir aplicações de águas continentais, zonas costeiras e oceanos | 40–64 h | #15, #20, #16 |
| [#26](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/26) | Produzir aplicações de atmosfera e clima | 40–64 h | #15, #22, #16 |
| [#27](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/27) | Produzir aplicações de geologia, relevo e desastres | 40–64 h | #18, #19, #20 |
| [#28](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/28) | Revisar acessibilidade, navegação e material com leitores | 32–48 h | #24, #25, #26, #27, #23, #17 |
| [#29](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/29) | Preparar versão de cobertura ampla e manutenção | 24–40 h | #28 |

As dependências indicam material necessário à aceitação da entrega. Rascunhos podem ser escritos antes de todas elas terminarem, mas não devem ser declarados concluídos sem a integração. Não há dependências cíclicas no plano.

## Critério comum de pronto

Uma entrega precisa de explicação própria e fontes verificáveis, símbolos e unidades definidos, exemplo resolvido, exercícios com respostas comentadas, pré-requisitos e limites explícitos. Práticas devem executar no ambiente documentado; links, figuras e leitura matemática precisam ser acessíveis.

Inferências com dados reais precisam de referência de avaliação adequada. Dados sintéticos e rótulos produzidos pelo mesmo índice usado no treinamento não demonstram acurácia real. PDFs continuam fora do Git. Dados e código de terceiros exigem condições de uso documentadas.

A evidência do trabalho pode ser um relatório de execução e revisão, um diff revisado ou outra verificação apropriada. Não marcar Done apenas porque a IA escreveu o texto ou o notebook executou.

## Controle da incerteza

Reestimar depois dos dois primeiros pacotes e ao fechar cada marco. Registrar horas reais de produção e revisão, falhas e retrabalho; comparar com os intervalos. Não converter o desempenho inicial em velocidade garantida para uma especialidade ainda não conhecida.

Os maiores riscos são aprofundamento do escopo, obtenção/licença de dados, cobertura de referências, validação independente, disponibilidade de revisão técnica e compatibilidade do legado. Se uma frente atrasar, atualizar dependências e projeções; preservar o escopo visível, em vez de esconder a lacuna.

O arquivo [desenvolvimento.json](desenvolvimento.json) registra pacotes, horas, dependências e links usados nesta versão do plano. As issues são o acompanhamento operacional; atualizar a cópia local quando o plano mudar.


## Confirmação do horizonte

O horizonte de tempo foi aceito e o planejamento foi mantido como está. A possibilidade de terminar antes não altera as estimativas-base, a reserva, a capacidade de 5 h/semana nem as datas de referência. Reestimar com evidência de esforço real após as primeiras entregas.
