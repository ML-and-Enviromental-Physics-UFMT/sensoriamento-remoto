# Verificação da reorganização

Verificação local da migração por assuntos em 14/11/2026, com Python 3.14.4 e dependências do `requirements.txt`. O ambiente conda documentado com Python 3.11 não foi executado nesta verificação.

## Resultado

- Quatro testes estruturais passaram: links de leitura, caminhos dos exercícios, localização dos dados e figuras nos notebooks a partir da raiz ou da pasta do notebook, e destinos do mapa de migração.
- Os 12 notebooks executaram integralmente com seus dados de exemplo.
- Os 15 scripts abaixo executaram sem erro.
- Os dados, figuras e PDFs antigos mantiveram seus hashes de conteúdo após a movimentação.
- Os dois livros de matemática passaram por leitura de metadados com `pdfinfo`, e todos os PDFs continuam ignorados pelo Git.

Notebooks e scripts foram executados em cópia temporária da estrutura, para não substituir figuras e saídas já existentes. As saídas dos notebooks versionados não foram atualizadas com essa execução.

## Notebooks executados

- `conteudo/analise-de-imagens/estatistica/notebooks/02_teoria.ipynb`
- `conteudo/analise-de-imagens/filtros/notebooks/04_teoria.ipynb`
- `conteudo/analise-de-imagens/transformacoes/notebooks/03_teoria.ipynb`
- `conteudo/classificacao/agrupamento/notebooks/08_teoria.ipynb`
- `conteudo/classificacao/redes-e-avaliacao/notebooks/07_teoria.ipynb`
- `conteudo/classificacao/supervisionada/notebooks/06_teoria.ipynb`
- `conteudo/fundamentos/notebooks/00_primeiro_pixel.ipynb`
- `conteudo/fundamentos/notebooks/01_pca_propria.ipynb`
- `conteudo/fundamentos/notebooks/01_teoria.ipynb`
- `conteudo/pre-processamento/notebooks/05_teoria.ipynb`
- `conteudo/series-temporais/notebooks/09_teoria.ipynb`
- `projetos/pca-e-agrupamento/notebooks/aplicacao_piloto.ipynb`

## Scripts executados

- `conteudo/analise-de-imagens/estatistica/exercicios/ex02_1.py`
- `conteudo/analise-de-imagens/estatistica/exercicios/ex02_2.py`
- `conteudo/analise-de-imagens/filtros/exercicios/ex04_1.py`
- `conteudo/analise-de-imagens/filtros/exercicios/ex04_2.py`
- `conteudo/analise-de-imagens/transformacoes/exercicios/ex03_1.py`
- `conteudo/analise-de-imagens/transformacoes/exercicios/ex03_2.py`
- `conteudo/analise-de-imagens/transformacoes/exercicios/ex03_3.py`
- `conteudo/classificacao/agrupamento/exercicios/ex08_1.py`
- `conteudo/classificacao/agrupamento/exercicios/ex08_2.py`
- `conteudo/classificacao/redes-e-avaliacao/exercicios/ex07_1.py`
- `conteudo/classificacao/supervisionada/exercicios/ex06_1.py`
- `conteudo/pre-processamento/exercicios/ex05_4.py`
- `conteudo/pre-processamento/exercicios/ex05_viz.py`
- `conteudo/series-temporais/exercicios/ex09_2.py`
- `scripts/generate_outputs.py`

## Limites

Não foram executados `ex01_1.py`, `ex01_2.py`, `ex05_1.py`, `ex05_2.py` e `ex09_1.py`, que exigem GDAL; o último também precisa de duas imagens alinhadas. `ex05_3.py` depende de um arquivo de pontos de controle e não foi executado. O código completo de `legado/canty/` não foi modernizado nem validado.

Esses resultados verificam execução e caminhos na nova estrutura. Não validam classes de cobertura, estimativas de mudança ou qualquer conclusão científica. As áreas com páginas de planejamento continuam a desenvolver.
