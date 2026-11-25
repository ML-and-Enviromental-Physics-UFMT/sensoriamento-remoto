# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- Percurso passo a passo de Google Earth Engine em Python (`conteudo/google-earth-engine/`), com seis aulas, três notebooks práticos e dependências opcionais isoladas (entrega parcial relacionada à issue #17).
- Entrada em português para iniciantes, com seis leituras de fundamentos, prática de pixels simulados e diário de aprendizagem.
- Matemática por tópicos: 17 explicações com exemplos resolvidos, exercícios comentados, notebook de experimentos e script de conferência.
- Catálogos de referências do INPE e de álgebra linear com links de origem e metadados, sem distribuir os PDFs.
- Planejamento de desenvolvimento com entregas, dependências e capacidade de 5 h/semana, separado da estimativa de estudo do leitor.
- Verificações estruturais e documentação de contribuição, migração e limites de validação.

### Changed
- Conteúdo organizado por assunto em `conteudo/`, com matemática independente dos livros de referência.
- ASTER compartilhado centralizado em `data/exemplos/` e caminhos de scripts/notebooks atualizados.
- Piloto de mestrado transferido para `projetos/pca-e-agrupamento/` e código de referência isolado em `legado/canty/`.
- PDFs retirados do versionamento e ignorados em qualquer pasta; cópias locais preservadas.

## [0.2.0] - 2026-07-29

### Added
- Conteúdo-base dos Capítulos 1–9: notas em `theory/`, notebooks preenchidos, exercícios e PNGs em `outputs/` onde aplicável.
- Teoria consolidada do Cap. 1 em `theory/notas_consolidadas.md`; stubs de consulta nos Apêndices A e B.
- Exercícios novos: `ex02_1`–`ex02_2`, `ex03_3`, `ex04_1`–`ex04_2`, `ex05_4`/`ex05_viz`, `ex06_1`, `ex07_1`, `ex08_1`–`ex08_2`, `ex09_2`.
- Pasta `mestrado/` com README, notebook piloto (`aplicacao_piloto.ipynb`) e output de PCA + k-means (ASTER como placeholder).
- Infra de reprodução: `.gitignore`, `environment.yml`, `requirements.txt`, `study_utils/`, `scripts/generate_outputs.py`, `data/README.md`.
- Outputs gerados para Caps. 1–9 e piloto do mestrado (histogramas, PCs, filtros, realce, classificação, mudança simulada).

### Changed
- `README.md` com setup (conda/pip), tabela de status e organização alinhada ao conteúdo preenchido.
- `tasks/todo.md` atualizado: prioridades 1–7 refletindo o que foi concluído e o que resta (dados reais do mestrado, `auxil` legado).
- ASTER do Cap. 2 passou a symlink da cópia canônica em Cap. 1 (remove duplicata de ~34 MB).
- Nota solta na raiz do Cap. 1 agora aponta para `theory/notas_consolidadas.md`.

### Fixed
- `ex03_1.py`: path do ASTER via argparse/default; substituição de `np.mat` por arrays NumPy.
- `ex03_2.py`: path padrão coerente com o ASTER do Cap. 1.
- `ex09_1.py`: import de `em` via `auxil.scripts` e `PYTHONPATH` da raiz do repositório.

## [0.1.0] - 2026-03-24

### Added
- Estrutura principal do repositório para estudo prático do livro *Image Analysis, Classification and Change Detection in Remote Sensing: With Algorithms for Python*.
- Organização do material por capítulos, cobrindo do Capítulo 1 ao Capítulo 9, além dos apêndices matemático e de treinamento de redes neurais.
- Diretórios padronizados para cada capítulo, incluindo `notebooks/`, `theory/`, `exercises/`, `outputs/` e materiais de apoio.
- Capítulo 1 como capítulo mais desenvolvido, contendo anotações teóricas, scripts de exercício, apresentações, dados ASTER, figuras geradas e imagens Sentinel-1 para Cuiabá.
- Material inicial para os Capítulos 2 e 3, incluindo notebooks, notas teóricas e scripts de exercício.
- Estrutura inicial para os Capítulos 4 a 9, com notebooks base, scripts pontuais e pastas preparadas para evolução.
- Pasta `auxil/` com código auxiliar derivado do apêndice de software do livro.
- Pasta `resources/` para o PDF completo do livro-base.
- Pasta `docs/` para documentação interna sobre organização do repositório.
- Pasta `tasks/` e `planejamento_de_estudos.md` com cronograma e backlog de seis meses.

### Changed
- Reorganização da estrutura do repositório para padronizar os capítulos.
- Renomeação de `notes/` para `theory/`, `code/` para `notebooks/` e `imagens/` para `outputs/`.
- Distribuição dos exercícios de `auxil/scripts/exercices/` para as pastas `exercises/` de cada capítulo.
- Criação de READMEs por capítulo e templates de notebooks `XX_teoria.ipynb`.
- Atualização dos READMEs da raiz, `auxil/` e `resources/`.

### Fixed
- Remoção de notebooks vazios e arquivos de template incorretos.
- Limpeza de placeholder textual em `section_3.5.md`.
- Correção parcial da organização anterior dos arquivos.

### Removed
- Estrutura anterior menos padronizada (`notes/`, `code/`, `imagens/`).
- Placeholders e arquivos vazios sem conteúdo real.

[Unreleased]: https://github.com/brunomartinsmv/sensoriamento-remoto-python-estudo/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/brunomartinsmv/sensoriamento-remoto-python-estudo/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/brunomartinsmv/sensoriamento-remoto-python-estudo/releases/tag/v0.1.0
