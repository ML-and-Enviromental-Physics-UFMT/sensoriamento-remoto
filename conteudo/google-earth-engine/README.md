# Google Earth Engine com Python

Este percurso ensina, passo a passo, como usar o Google Earth Engine (GEE) com Python (`earthengine-api` e `geemap`) para buscar imagens de satélite na nuvem, aplicar fatores de escala e máscaras de nuvens, calcular índices, extrair séries temporais, exportar resultados e treinar classificadores supervisionados.

Ele funciona como uma linha prática paralela à trilha principal do repositório. O núcleo de [fundamentos](../fundamentos/README.md), [análise de imagens](../analise-de-imagens/README.md) e [classificação](../classificacao/README.md) continua independente e executável sem conta em plataforma externa. Este percurso corresponde a uma entrega parcial ligada à frente de nuvem e processamento escalável (issue #17) no [plano de desenvolvimento](../../docs/planejamento/desenvolvimento.md).

## Estado do material e limites de verificação

- Escopo inicial: somente API Python (`earthengine-api` e `geemap`). O Code Editor em JavaScript não faz parte desta etapa.
- Conteúdo disponível: seis aulas graduais em `aulas/` e três notebooks práticos em `notebooks/`.
- Verificação realizada em 25/11/2026: todos os três notebooks executaram ponta a ponta contra o servidor do Google Earth Engine em Python 3.11.18 (`earthengine-api` 1.7.53, `geemap` 0.37.2), mantendo os arquivos do repositório sem saídas embutidas; links internos, 6/6 testes estruturais/publicação e auditoria de publicação conferidos; coordenadas dos polígonos dos notebooks 2 e 3 conferidas sobre cenas públicas Sentinel-2 L2A de 2024.
- Limites explícitos: executar os notebooks exige conexão com a internet, conta Google pessoal e projeto registrado no Google Cloud; as chamadas `.start()` de exportação para o Google Drive permanecem comentadas nos exemplos; os polígonos usados no notebook 3 são didáticos e não substituem amostragem probabilística ou validação de campo.

## Pré-requisitos

- Conceitos básicos de banda, pixel, reflectância e exibição em [Fundamentos](../fundamentos/README.md).
- Noções básicas de Python (variáveis, funções, listas e dicionários).
- Uma conta Google com projeto registrado no Earth Engine (veja a Aula 1).

## Ambiente opcional

As bibliotecas do GEE ficam separadas em [requirements-gee.txt](requirements-gee.txt) para não alterar o ambiente base do repositório. Recomenda-se Python 3.12 ou superior para instalar as versões mais recentes do `geemap` (a partir do `geemap` 0.39, o pacote exige Python 3.12+; em Python 3.11, o `pip` instala automaticamente a série 0.37).

A partir da raiz do projeto:

```bash
python3.12 -m venv .venv-gee
source .venv-gee/bin/activate
python -m pip install -r conteudo/google-earth-engine/requirements-gee.txt
jupyter notebook
```

No Windows, ative o ambiente com `.venv-gee\Scripts\activate`. O padrão `.venv*/` está no `.gitignore`, então `.venv-gee/` não entra no controle de versão. Se preferir, você também pode abrir os notebooks no Google Colab (onde `earthengine-api` já vem instalado e basta instalar `geemap`, lembrando de reautenticar a cada sessão).

## Sequência de estudo

Leia cada aula antes de abrir o notebook correspondente. Em todas as etapas, responda às perguntas de verificação antes de abrir as respostas comentadas e anote dúvidas no [diário de aprendizagem](../../docs/modelo-diario.md).

| Ordem | Tema | Aula | Prática |
|-------|------|------|---------|
| 1 | Conta, projeto Google Cloud e autenticação em Python | [01_conta_projeto_e_ambiente.md](aulas/01_conta_projeto_e_ambiente.md) | [01_primeiros_passos_gee.ipynb](notebooks/01_primeiros_passos_gee.ipynb) |
| 2 | Modelo cliente-servidor e tipos de objetos `ee` | [02_modelo_cliente_servidor.md](aulas/02_modelo_cliente_servidor.md) | [01_primeiros_passos_gee.ipynb](notebooks/01_primeiros_passos_gee.ipynb) |
| 3 | Catálogo, filtros, fatores de escala e máscaras de nuvens | [03_catalogo_filtros_e_nuvens.md](aulas/03_catalogo_filtros_e_nuvens.md) | [01_primeiros_passos_gee.ipynb](notebooks/01_primeiros_passos_gee.ipynb) |
| 4 | Composições temporais, índices espectrais e visualização | [04_composicoes_indices_e_visualizacao.md](aulas/04_composicoes_indices_e_visualizacao.md) | [01_primeiros_passos_gee.ipynb](notebooks/01_primeiros_passos_gee.ipynb) |
| 5 | Redutores espaciais, séries temporais e exportação | [05_redutores_series_e_exportacao.md](aulas/05_redutores_series_e_exportacao.md) | [02_series_temporais_e_exportacao.ipynb](notebooks/02_series_temporais_e_exportacao.ipynb) |
| 6 | Classificação supervisionada e avaliação no GEE | [06_classificacao_e_validacao_no_gee.md](aulas/06_classificacao_e_validacao_no_gee.md) | [03_classificacao_supervisionada_gee.ipynb](notebooks/03_classificacao_supervisionada_gee.ipynb) |

## Crédito dos dados referenciados

Nenhum dado de satélite externo é redistribuído neste repositório. Os exemplos e conferências de coordenadas referenciam dados públicos de terceiros:

- Sentinel-2 L2A: Contains modified Copernicus Sentinel data 2024 (ESA / Copernicus).
- Landsat Collection 2 Level-2 e SRTM: USGS / NASA (domínio público).

## Pontes com o restante do repositório

- Realce versus medição física: [Pré-processamento](../pre-processamento/README.md).
- Estatística espacial, matrizes de confusão e validação: [Classificação](../classificacao/README.md).
- Comparação multitemporal e detecção de mudanças: [Séries temporais](../series-temporais/README.md).
- Navegação geral: [Trilha de aprendizagem](../../trilha-de-aprendizagem.md) e [Referências](../../referencias/README.md).
