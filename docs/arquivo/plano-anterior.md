# Planejamento anterior

Registro histórico preservado na reorganização. As marcações não representam uma nova validação do material.


Os registros abaixo foram preservados. Marcações históricas não foram revalidadas nesta reorganização e não indicam progresso pessoal de quem estuda.

### A fazer, planejamento de 6 meses

Estado em 2026-07-29: conteúdo base dos Caps. 1–9 + infra implementados; próximo ciclo = aprofundar com dados reais do mestrado e revisitar auxil.

Este arquivo deve conter apenas tarefas ainda pendentes. Historico de execucao deve ficar em notas de sessao ou nos `README.md` dos capitulos; decisoes mais estaveis devem ir para `docs/`.

Horizonte deste plano: `2026-06-18` a `2026-12-31`.

## Prioridade 1 - Definir linha de base e recuperar capitulos iniciais

Objetivo: deixar os Capitulos 1, 2 e 3 em um estado consistente antes de avancar para os blocos mais densos do livro.

Janela sugerida: `2026-06-18` a `2026-07-14`.

- [x] Revisar o `README.md` de cada capitulo ja iniciado e marcar o status real: leitura, teoria, notebook, exercicios, outputs e aplicacao a dado real.
- [x] Consolidar o Capitulo 1 como modelo de organizacao para os demais capitulos.
- [x] Mover ou integrar a nota solta `notes_Chapter 01 - Images, Arrays, and Matrices.md` ao material do Capitulo 1, se ela ainda for util.
- [x] Completar as lacunas principais de `aulas/` nos Capitulos 1, 2 e 3.
- [x] Rodar os notebooks dos Capitulos 1, 2 e 3 e registrar quais celulas ainda precisam de ajuste.
- [x] Resolver ou revisar os exercicios ja existentes nos Capitulos 1 e 3.
- [x] Gerar ao menos um output reproduzivel por capitulo inicial quando fizer sentido.
- [x] Atualizar os `README.md` dos Capitulos 1, 2 e 3 com o que ficou concluido e o que permanece pendente.
- [ ] Gerar/regerar outputs dos Caps. 2–3 se ainda faltarem (`PYTHONPATH=. python Chapter_02_.../ex02_*.py` e equivalentes do Cap. 3).
- [ ] Aprofundar trechos de teoria ainda finos nos Caps. 1–3 apos releitura com dado real.

## Prioridade 2 - Fechar o bloco de fundamentos visuais e pre-processamento

Objetivo: estudar os Capitulos 4 e 5 com foco em filtros, kernels, campos, realce e correcao de imagens.

Janela sugerida: `2026-07-15` a `2026-08-12`.

- [x] Ler o Capitulo 4 e registrar em `aulas/` quais problemas filtros e kernels resolvem no sensoriamento remoto.
- [x] Rodar o notebook `conteudo/analise-de-imagens/filtros/notebooks/04_teoria.ipynb`.
- [x] Criar exercicios praticos para o Capitulo 4 usando dados simples do repositorio.
- [x] Gerar outputs visuais do Capitulo 4 em `figuras/`, priorizando comparacoes antes/depois.
- [x] Ler o Capitulo 5 e separar o que e enhancement, correcao radiometrica e correcao geometrica.
- [x] Rodar o notebook `conteudo/pre-processamento/notebooks/05_teoria.ipynb`.
- [x] Revisar os scripts `ex05_1.py`, `ex05_2.py` e `ex05_3.py`, documentando entrada, saida e objetivo.
- [x] Atualizar os `README.md` dos Capitulos 4 e 5 com exemplos concretos do que foi reproduzido.
- [ ] Aprofundar teoria de correcao radiometrica/geometrica com dados reais do mestrado, se aplicavel.

## Prioridade 3 - Preparar a base matematica e computacional para classificacao

Objetivo: reduzir gargalos antes dos capitulos de classificacao supervisionada, que sao centrais e mais densos.

Janela sugerida: `2026-08-13` a `2026-09-02`.

- [x] Revisar o `conteudo/matematica/` e listar quais topicos matematicos serao consultados durante classificacao.
- [x] Criar notas curtas para os conceitos matematicos que aparecerem repetidamente: matrizes de covariancia, autovalores, distancia estatistica e probabilidade.
- [x] Revisar o `conteudo/classificacao/treinamento-de-redes/` antes de entrar nos Capitulos 6 e 7.
- [x] Conferir quais scripts de `legado/canty/auxil/` sao usados nos capitulos de classificacao.
- [x] Criar um checklist de ambiente Python minimo para rodar notebooks e scripts sem depender de tentativa e erro (`environment.yml` / `requirements.txt` + Setup no README).
- [ ] Documentar no `legado/canty/auxil/README.md` os scripts efetivamente usados e limpar bits legados de Python 2.
- [ ] (Opcional) Empacotar ambiente em Docker alem de conda/`requirements.txt`.
## Prioridade 4 - Estudar classificacao supervisionada parte 1

Objetivo: transformar o Capitulo 6 em um bloco utilizavel para entender classificacao supervisionada em imagens de sensoriamento remoto.

Janela sugerida: `2026-09-03` a `2026-10-30`.

- [x] Ler o Capitulo 6 com foco nos classificadores principais e nas hipoteses de cada metodo.
- [x] Rodar o notebook `conteudo/classificacao/supervisionada/notebooks/06_teoria.ipynb`.
- [x] Criar notas em `aulas/` explicando os classificadores do capitulo em linguagem propria.
- [x] Reproduzir pelo menos um exemplo de classificacao do livro usando os scripts de apoio.
- [x] Implementar uma versao simples de um classificador central em notebook proprio, sem copiar diretamente o codigo do livro.
- [x] Gerar matriz de confusao, acuracia e uma saida visual classificada quando houver dado adequado.
- [x] Registrar duvidas tecnicas para discutir depois, separando problema matematico de problema de implementacao.
- [x] Atualizar o `README.md` do Capitulo 6 com status, comandos usados e resultados gerados.
- [ ] Reexecutar/validar o Cap. 6 com amostras e rasters reais do mestrado.

## Prioridade 5 - Estudar classificacao supervisionada parte 2 e consolidar avaliacao

Objetivo: completar o bloco supervisionado e sair dele com criterios de avaliacao claros.

Janela sugerida: `2026-10-31` a `2026-11-27`.

- [x] Ler o Capitulo 7 conectando cada metodo ao que foi estudado no Capitulo 6.
- [x] Rodar o notebook `conteudo/classificacao/redes-e-avaliacao/notebooks/07_teoria.ipynb`.
- [x] Criar notas em `aulas/` com comparacao direta entre os metodos dos Capitulos 6 e 7.
- [x] Reproduzir ao menos um fluxo completo de treino, predicao e avaliacao.
- [x] Consolidar metricas de avaliacao em um notebook ou nota reutilizavel.
- [x] Testar um exemplo piloto relacionado ao mestrado (pasta `projetos/pca-e-agrupamento/`, ainda com ASTER placeholder).
- [x] Comparar o resultado supervisionado com uma classificacao mais simples, para entender ganho real.
- [x] Atualizar o `README.md` do Capitulo 7 e registrar o que ficou pronto para uso futuro.
- [ ] Trocar o placeholder ASTER por dados reais do mestrado no fluxo supervisionado (Caps. 6–7 / `projetos/pca-e-agrupamento/`).
## Prioridade 6 - Estudar classificacao nao supervisionada e deteccao de mudanca

Objetivo: fechar os Capitulos 8 e 9, conectando agrupamento, segmentacao e mudanca temporal com aplicacoes reais.

Janela sugerida: `2026-10-28` a `2026-11-25`.

- [x] Ler o Capitulo 8 e separar os metodos nao supervisionados por objetivo: agrupamento, reducao de dimensionalidade ou segmentacao.
- [x] Rodar o notebook `conteudo/classificacao/agrupamento/notebooks/08_teoria.ipynb`.
- [x] Gerar ao menos uma classificacao nao supervisionada com output visual.
- [x] Comparar qualitativamente classificacao supervisionada e nao supervisionada em um mesmo dado, se possivel.
- [x] Ler o Capitulo 9 com foco em deteccao de mudanca e interpretacao temporal.
- [x] Rodar o notebook `conteudo/series-temporais/notebooks/09_teoria.ipynb`.
- [x] Revisar e executar `conteudo/series-temporais/exercicios/ex09_1.py`.
- [x] Gerar um exemplo de deteccao de mudanca e registrar limitacoes do resultado.
- [x] Atualizar os `README.md` dos Capitulos 8 e 9 com exemplos, outputs e pendencias.
- [ ] Rodar `ex09_1` com duas imagens co-registradas reais (hoje depende de GDAL/`auxil`; `ex09_2` cobre o cenario simulado).
- [ ] Aplicar agrupamento/mudanca a series temporais do mestrado.

## Prioridade 7 - Consolidar portfolio tecnico e conexao com o mestrado

Objetivo: transformar o estudo em material reutilizavel, com evidencias claras do que foi aprendido e do que pode ser aplicado na pesquisa.

Janela sugerida: `2026-12-1` a `2026-12-31`.

- [x] Revisar todos os capitulos e marcar no `README.md` da raiz o status final de cada um.
- [x] Criar uma tabela de progresso por capitulo com: teoria, notebook, exercicios, outputs, aplicacao real e pendencias.
- [x] Separar os outputs mais representativos em uma lista curta de evidencias tecnicas.
- [x] Conferir se arquivos temporarios, caches e artefatos locais ficaram fora do plano de versionamento.
- [x] Definir o proximo ciclo de estudo: aprofundar classificacao, aplicar a dados do mestrado ou preparar material didatico.
- [ ] Aplicar dados reais do mestrado em `projetos/pca-e-agrupamento/` (substituir placeholder ASTER no piloto PCA+k-means).
- [ ] Escrever sintese em `docs/` e identificar tecnicas reaproveitaveis na pesquisa (apos dados reais).
- [ ] Revisar a organizacao de `legado/canty/auxil/` depois do uso real dos scripts (limpeza legado Py2).
- [ ] Aprofundar teoria onde ainda estiver fina, apos uso com dado da tese.
- [ ] Gerar/regerar outputs Caps. 2–3 se ainda faltarem no working tree.
- [ ] (Opcional) Docker para reproducao do ambiente alem de conda/`requirements.txt`.
- [ ] Atualizar `docs/como-estudar.md` com o que foi aprendido neste ciclo.