# Sensoriamento remoto com Python

Material em desenvolvimento, ainda sem revisão técnica independente completa. Uma fonte gratuita de estudo em português, do básico ao avançado, com a ambição de cobrir as diferentes especialidades e aplicações do sensoriamento remoto. O conteúdo cresce conforme é estudado, experimentado e revisado. As lacunas ficam explícitas.

O livro de Canty e as apostilas do INPE formam o núcleo inicial. Novos livros entram como referências por assunto, inclusive no percurso de matemática. A organização das aulas não depende da sequência de um único livro.

## Comece aqui

1. Leia [Fundamentos](conteudo/fundamentos/README.md), mesmo se ainda não souber programar.
2. Execute [Seu primeiro pixel](conteudo/fundamentos/notebooks/00_primeiro_pixel.ipynb), que usa somente Python e números inventados.
3. Siga a [trilha de aprendizagem](trilha-de-aprendizagem.md). Consulte [Matemática](conteudo/matematica/README.md) quando uma conta ou notação exigir revisão.

O [guia de estudo](docs/como-estudar.md) sugere sessões curtas. O [modelo de diário](docs/modelo-diario.md) ajuda a registrar suas explicações e dúvidas. Arquivo preenchido não significa aprendizado nem validação científica.

## Percursos por assunto

| Percurso | Estado do material |
|----------|--------------------|
| [Fundamentos](conteudo/fundamentos/README.md) | Seis leituras iniciais, imagens e matrizes, notebooks e exercícios |
| [Matemática](conteudo/matematica/README.md) | 17 tópicos com exemplos resolvidos, exercícios e prática de álgebra, estatística, cálculo e otimização |
| [Sensores e aquisição](conteudo/sensores/README.md) | Frente a desenvolver; introdução disponível em fundamentos |
| [Pré-processamento](conteudo/pre-processamento/README.md) | Realce, correções e registro; práticas reais a aprofundar |
| [Análise de imagens](conteudo/analise-de-imagens/README.md) | Estatística, transformações e filtros |
| [Classificação](conteudo/classificacao/README.md) | Métodos supervisionados, redes, agrupamento e avaliação |
| [Séries temporais e mudança](conteudo/series-temporais/README.md) | Núcleo bitemporal disponível; séries densas a desenvolver |
| [Radar e SAR](conteudo/radar-sar/README.md) | Nota introdutória; percurso completo a desenvolver |
| [LiDAR](conteudo/lidar/README.md) | Frente a desenvolver |
| [Hiperespectral](conteudo/hiperespectral/README.md) | Frente a desenvolver |
| [Termal](conteudo/termal/README.md) | Frente a desenvolver |
| [Aplicações](conteudo/aplicacoes/README.md) | Frente a desenvolver por área de uso |

As especialidades previstas fazem parte do escopo. A tabela distingue essa ambição do que já pode ser estudado hoje.

## Estrutura

```text
conteudo/       Aulas, notebooks, exercícios e figuras por assunto
projetos/       Aplicações que integram métodos e dados
referencias/    Bibliografia e links das fontes
data/          Dados compartilhados e documentação de origem
study_utils/   Utilitários próprios usados pelos exemplos
scripts/       Comandos de apoio
legado/canty/  Fonte, licença e obtenção opcional do software do livro
docs/          Como estudar, decisões e pendências de manutenção
tests/         Verificações da estrutura e dos caminhos
```

Em cada módulo, o README indica por onde começar. `aulas/` contém a explicação; `notebooks/` permite experimentar; `exercicios/` reúne scripts; `figuras/` guarda resultados selecionados. Pastas só são criadas quando têm material.

O [projeto de PCA e agrupamento](projetos/pca-e-agrupamento/README.md) usa o raster sintético compartilhado. Ele veio do piloto antes chamado `mestrado/` e continua como demonstração técnica, sem validação de classes de cobertura.

## Ambiente

A prática inicial precisa apenas de Python e Jupyter. Para os demais exemplos, o ambiente conda inclui GDAL e as bibliotecas geoespaciais.

```bash
conda env create -f environment.yml
conda activate sensoriamento-remoto
jupyter notebook
```

Alternativa com pip, em Linux ou macOS, a partir da raiz.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook
```

No Windows, ative com `.venv\Scripts\activate`. O `requirements.txt` não instala `osgeo.gdal`; scripts que exigem essa biblioteca precisam do ambiente conda ou de uma instalação compatível separada.

Para executar scripts próprios, use a raiz do repositório.

```bash
PYTHONPATH=. python conteudo/analise-de-imagens/transformacoes/exercicios/ex03_1.py
```

O [guia do legado](legado/canty/README.md) documenta a fonte oficial, a licença e a obtenção opcional das rotinas do livro. Esse código não acompanha a cópia pública.

## Referências e contribuição

O [catálogo](referencias/README.md) reúne Canty, INPE e os livros de matemática. PDFs públicos ou privados são apenas de consulta local e ficam fora do Git. Se uma fonte estiver indisponível, entre em contato com Bruno pelo [GitHub do projeto](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues) para solicitar o material.

Para ampliar uma aula, veja [como contribuir](CONTRIBUTING.md). As [pendências](docs/pendencias.md) acompanham o desenvolvimento do material. A [decisão de organização](docs/decisoes/2026-11-14-organizacao.md) registra a migração e a correspondência com a estrutura anterior.

O [plano de desenvolvimento](docs/planejamento/desenvolvimento.md) organiza a cobertura ampla em entregas e marcos acompanhados nas [issues](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues). A [estimativa de estudo](docs/planejamento/estimativa-de-estudo.md) trata do esforço de quem usa o material e fica separada desse plano.

## Licença

Os textos, as figuras e os notebooks próprios deste repositório estão sob [CC BY 4.0](LICENSE): você pode copiar, adaptar e redistribuir, desde que dê o crédito a Bruno Martins e indique as alterações. O código próprio, em `study_utils/`, `scripts/`, `tests/` e nos exercícios, está sob a [licença MIT](LICENSE-CODE).

O raster de exemplo é sintético, autoral e distribuído sob CC BY 4.0, como registra o [guia dos dados](data/README.md). As licenças próprias não cobrem os livros, as apostilas ou o software de terceiros indicado nas referências. O ASTER histórico, o código legado e as figuras antigas não acompanham esta cópia pública.
