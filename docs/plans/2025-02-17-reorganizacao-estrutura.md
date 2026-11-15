# Reorganização do Repositório — Plano de Implementação

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reorganizar o repositório de estudo de sensoriamento remoto para ter estrutura padronizada, clara e navegável em todos os 9 capítulos do livro Canty (4ª ed.).

**Architecture:** Cada `ChapterXX/` torna-se um módulo autossuficiente com `theory/`, `notebooks/`, `exercises/`, `data/` e `outputs/`. Exercícios migram de `auxil/scripts/exercices/` para cada capítulo. Templates padronizados de notebook são criados. Documentação de progresso é centralizada no `README.md` raiz.

**Tech Stack:** Git (renomeações preservando histórico com `git mv`), Python 3.11, Jupyter Notebook (formato `.ipynb` JSON)

---

## Importante antes de começar

- Trabalhar em: `/Users/bruno/Documents/sensoriamento-remoto-python-estudo`
- Usar `git mv` para renomear pastas (preserva histórico)
- Ao final, fazer **um único commit** com tudo
- Verificar `git status` antes do commit para não perder nada

---

### Task 1: Criar pasta `resources/` e mover o PDF do livro

**Files:**
- Criar: `resources/` (nova pasta)
- Mover: `Canty, Morton John - ....pdf` → `resources/`

**Step 1: Criar pasta e mover com git mv**

```bash
cd /Users/bruno/Documents/sensoriamento-remoto-python-estudo
mkdir -p resources
git mv "Canty, Morton John - Image Analysis, Classification and Change Detection in Remote Sensing_ With Algorithms for Python, Fourth Edition-Chapman and Hall_CRC (2019).pdf" "resources/Canty, Morton John - Image Analysis, Classification and Change Detection in Remote Sensing_ With Algorithms for Python, Fourth Edition-Chapman and Hall_CRC (2019).pdf"
```

**Step 2: Verificar**

```bash
ls resources/
git status
```

Esperado: PDF aparece em `resources/`, git mostra `renamed`.

---

### Task 2: Renomear `notes/ → theory/`, `code/ → notebooks/`, `imagens/ → outputs/` em todos os capítulos

**Atenção:** Usar `git mv` para cada renomeação. Fazer capítulo por capítulo.

**Step 1: Capítulo 1**

```bash
cd /Users/bruno/Documents/sensoriamento-remoto-python-estudo
git mv Chapter01/notes Chapter01/theory
git mv Chapter01/code Chapter01/notebooks
git mv Chapter01/imagens Chapter01/outputs
```

**Step 2: Capítulo 2**

```bash
git mv Chapter02/notes Chapter02/theory
git mv Chapter02/code Chapter02/notebooks
# Chapter02 não tem imagens/, então pular outputs
```

**Step 3: Capítulos 3 a 9** (repetir para cada um que tiver as pastas)

```bash
git mv Chapter03/notes Chapter03/theory
git mv Chapter03/code Chapter03/notebooks

git mv Chapter04/notes Chapter04/theory
git mv Chapter04/code Chapter04/notebooks

git mv Chapter05/notes Chapter05/theory
git mv Chapter05/code Chapter05/notebooks

git mv Chapter06/notes Chapter06/theory
git mv Chapter06/code Chapter06/notebooks

git mv Chapter07/notes Chapter07/theory
git mv Chapter07/code Chapter07/notebooks

git mv Chapter08/notes Chapter08/theory
git mv Chapter08/code Chapter08/notebooks

git mv Chapter09/notes Chapter09/theory
git mv Chapter09/code Chapter09/notebooks
```

**Step 4: Criar `outputs/` vazio onde não existia (capítulos 2-9)**

```bash
for i in 02 03 04 05 06 07 08 09; do
  mkdir -p "Chapter${i}/outputs"
  touch "Chapter${i}/outputs/.gitkeep"
done
```

**Step 5: Verificar**

```bash
ls Chapter01/
# Esperado: README.md data/ exercises/ notebooks/ outputs/ theory/ apresentations/
git status | head -40
```

---

### Task 3: Criar pasta `exercises/` em cada capítulo e mover os exercícios

**Step 1: Criar pastas `exercises/` nos capítulos que têm exercícios**

```bash
cd /Users/bruno/Documents/sensoriamento-remoto-python-estudo
mkdir -p Chapter01/exercises
mkdir -p Chapter03/exercises
mkdir -p Chapter05/exercises
mkdir -p Chapter09/exercises
```

**Step 2: Mover exercícios com git mv**

```bash
git mv auxil/scripts/exercices/ex1_1.py Chapter01/exercises/ex01_1.py
git mv auxil/scripts/exercices/ex1_2.py Chapter01/exercises/ex01_2.py
git mv auxil/scripts/exercices/ex3_1.py Chapter03/exercises/ex03_1.py
git mv auxil/scripts/exercices/ex3_2.py Chapter03/exercises/ex03_2.py
git mv auxil/scripts/exercices/ex5_1.py Chapter05/exercises/ex05_1.py
git mv auxil/scripts/exercices/ex5_2.py Chapter05/exercises/ex05_2.py
git mv auxil/scripts/exercices/ex5_3.py Chapter05/exercises/ex05_3.py
git mv auxil/scripts/exercices/ex9_1.py Chapter09/exercises/ex09_1.py
```

**Step 3: Criar `exercises/` com `.gitkeep` nos capítulos sem exercícios ainda**

```bash
for i in 02 04 06 07 08; do
  mkdir -p "Chapter${i}/exercises"
  touch "Chapter${i}/exercises/.gitkeep"
done
```

**Step 4: Verificar**

```bash
ls Chapter01/exercises/
# Esperado: ex01_1.py  ex01_2.py
ls auxil/scripts/exercices/
# Esperado: vazio (ou apenas o diretório)
git status | grep exerc
```

---

### Task 4: Deletar notebooks vazios antigos e arquivos de template incorretos

**Step 1: Remover notebooks vazios (eram placeholders sem conteúdo)**

```bash
cd /Users/bruno/Documents/sensoriamento-remoto-python-estudo
git rm "Chapter01/notebooks/Capítulo_1.ipynb"
git rm Chapter02/notebooks/cap2.ipynb
git rm Chapter03/notebooks/cap3.ipynb
git rm Chapter04/notebooks/cap4.ipynb
git rm Chapter05/notebooks/cap5.ipynb
git rm Chapter06/notebooks/cap6.ipynb
git rm Chapter07/notebooks/cap7.ipynb
git rm Chapter08/notebooks/cap8.ipynb
git rm Chapter09/notebooks/cap9.ipynb
```

**Step 2: Remover arquivos `anotações_chapter_02.md` vazios nos capítulos 4-9**

```bash
git rm Chapter04/theory/anotações_chapter_02.md
git rm Chapter05/theory/anotações_chapter_02.md
git rm Chapter06/theory/anotações_chapter_02.md
git rm Chapter07/theory/anotações_chapter_02.md
git rm Chapter08/theory/anotações_chapter_02.md
git rm Chapter09/theory/anotações_chapter_02.md
```

**Step 3: Remover `anotações_chapter_03.md` vazio no capítulo 3**

```bash
git rm Chapter03/theory/anotações_chapter_03.md
```

**Step 4: Verificar**

```bash
git status | grep deleted
# Espera ver todos os arquivos removidos acima
```

---

### Task 5: Limpar placeholder "blablablablalba" de `section_3.5.md`

**Step 1: Editar o arquivo**

O arquivo está em `Chapter03/theory/section_3.5.md` (após a renomeação da Task 2).

Remover a última linha: `blablablablalba`

Use o Edit tool para remover exatamente:
```
blablablablalba
```

(a linha está no final do arquivo, após o último parágrafo sobre estimação de Σ_N)

**Step 2: Verificar**

```bash
tail -5 Chapter03/theory/section_3.5.md
# Última linha deve ser parágrafo real, não "blablablablalba"
```

---

### Task 6: Criar template de notebook padronizado e aplicar nos 9 capítulos

**Step 1: Definir o conteúdo do template**

O template é um arquivo `.ipynb` (JSON) com células Markdown e código pré-definidas.

Criar `Chapter01/notebooks/01_teoria.ipynb` com este conteúdo:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Capítulo 1 — Fundamentos de Sensoriamento Remoto\n",
    "\n",
    "> 📖 **Referência:** Canty (2019), Capítulo 1\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Intuição\n",
    "\n",
    "*O que este capítulo trata? Qual problema ele resolve? Escreva aqui uma explicação em linguagem simples.*\n",
    "\n",
    "..."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Fundamentos Matemáticos\n",
    "\n",
    "> 📐 **Referência:** Seção X.Y do livro / Apêndice A\n",
    "\n",
    "*Descreva aqui os conceitos matemáticos principais. Use LaTeX para equações.*\n",
    "\n",
    "$$\n",
    "\\text{equação principal}\n",
    "$$"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Implementação\n",
    "\n",
    "*Implemente o algoritmo passo a passo. Explique cada trecho de código.*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Imports\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "# from osgeo import gdal  # descomente se precisar de GDAL"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Visualizações\n",
    "\n",
    "*Gere aqui os gráficos e imagens. Salve em `outputs/` com `plt.savefig('outputs/nome.png')`.*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Exemplo: plt.savefig('outputs/figura_cap01.png', dpi=150, bbox_inches='tight')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Usando scripts do `auxil/`\n",
    "\n",
    "*Liste aqui quais scripts do `auxil/` são usados neste capítulo e como chamá-los.*\n",
    "\n",
    "```python\n",
    "# Exemplo:\n",
    "# %run ../../auxil/scripts/pca.py -p [1,2,3] data/imagem.tif\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Exercícios\n",
    "\n",
    "*Enunciados dos exercícios do capítulo. As soluções ficam em `exercises/`.*\n",
    "\n",
    "**Exercício 1.1:** ..."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

**Step 2: Criar notebook para cada capítulo restante**

Copiar o template acima adaptando o número e título do capítulo. Criar:
- `Chapter02/notebooks/02_teoria.ipynb` (título: "Variáveis Aleatórias e Estatística")
- `Chapter03/notebooks/03_teoria.ipynb` (título: "Transformações Espectrais — MNF")
- `Chapter04/notebooks/04_teoria.ipynb` (título: "Capítulo 4")
- `Chapter05/notebooks/05_teoria.ipynb` (título: "Capítulo 5")
- `Chapter06/notebooks/06_teoria.ipynb` (título: "Capítulo 6")
- `Chapter07/notebooks/07_teoria.ipynb` (título: "Capítulo 7")
- `Chapter08/notebooks/08_teoria.ipynb` (título: "Capítulo 8")
- `Chapter09/notebooks/09_teoria.ipynb` (título: "Capítulo 9")

**Step 3: Verificar**

```bash
ls Chapter01/notebooks/
ls Chapter09/notebooks/
# Esperado: 01_teoria.ipynb (e similar para os outros)
```

---

### Task 7: Criar `ChapterXX/README.md` para cada capítulo

**Step 1: Criar README para capítulo 1**

Arquivo: `Chapter01/README.md`

```markdown
# Capítulo 1 — Fundamentos de Sensoriamento Remoto

**Status:** 🟡 Em andamento

## Tópicos Abordados

- Sensores passivos e ativos
- Radar de Abertura Sintética (SAR)
- Polarização e frequências de radar
- Fundamentos de matrizes de covariância
- Extremos de funções em imagens

> 📖 Seções do livro: 1.1 – 1.X

## Conteúdo

| Tipo | Arquivo | Descrição |
|------|---------|-----------|
| Notebook | `notebooks/01_teoria.ipynb` | Implementações e exemplos do capítulo |
| Teoria | `theory/SAR.md` | Fundamentos de SAR |
| Teoria | `theory/anotações_chapter_01.md` | Resumo geral do capítulo |
| Teoria | `theory/matrices.md` | Matrizes de covariância |
| Teoria | `theory/minima and maxima.md` | Extremos em imagens |
| Exercícios | `exercises/ex01_1.py` | Exercício 1.1 — leitura de imagem com GDAL |
| Exercícios | `exercises/ex01_2.py` | Exercício 1.2 |

## Scripts do `auxil/` utilizados

*(a preencher conforme o estudo avança)*

## Pré-requisitos

Nenhum — este é o capítulo introdutório.
```

**Step 2: Criar README para capítulo 2**

Arquivo: `Chapter02/README.md`

```markdown
# Capítulo 2 — Variáveis Aleatórias e Estatística

**Status:** 🟡 Em andamento

## Tópicos Abordados

- Pixels como variáveis aleatórias
- Números Digitais (DN)
- Matriz de Covariância
- Análise de Componentes Principais (PCA)
- Autovalores e autovetores

> 📖 Seções do livro: 2.1 – 2.X

## Conteúdo

| Tipo | Arquivo | Descrição |
|------|---------|-----------|
| Notebook | `notebooks/02_teoria.ipynb` | Implementações e exemplos do capítulo |
| Teoria | `theory/random variables.md` | Variáveis aleatórias, PCA, covariância |

## Scripts do `auxil/` utilizados

- `auxil/scripts/pca.py` — Análise de Componentes Principais

## Pré-requisitos

- Capítulo 1
```

**Step 3: Criar README para capítulo 3**

Arquivo: `Chapter03/README.md`

```markdown
# Capítulo 3 — Transformações Espectrais

**Status:** 🟡 Em andamento

## Tópicos Abordados

- Minimum Noise Fraction (MNF)
- Estimação de matrizes de covariância de ruído
- Autocorrelação espacial para isolamento de ruído
- Diferença entre PCA e MNF

> 📖 Seções do livro: 3.1 – 3.5

## Conteúdo

| Tipo | Arquivo | Descrição |
|------|---------|-----------|
| Notebook | `notebooks/03_teoria.ipynb` | Implementações e exemplos do capítulo |
| Teoria | `theory/section_3.5.md` | MNF — visão geral e estimação de covariância |
| Exercícios | `exercises/ex03_1.py` | Exercício 3.1 |
| Exercícios | `exercises/ex03_2.py` | Exercício 3.2 |

## Scripts do `auxil/` utilizados

- `auxil/scripts/mnf.py` — Minimum Noise Fraction
- `auxil/scripts/pca.py` — PCA (para comparação)

## Pré-requisitos

- Capítulo 2 (PCA e covariância)
```

**Step 4: Criar READMEs para capítulos 4-9 (template mínimo)**

Para os capítulos ainda não estudados, usar um template mínimo:

```markdown
# Capítulo X — [Título a definir]

**Status:** ⬜ Não iniciado

## Tópicos Abordados

*(a preencher conforme o estudo avança)*

> 📖 Seções do livro: X.1 – X.X

## Conteúdo

| Tipo | Arquivo | Descrição |
|------|---------|-----------|
| Notebook | `notebooks/0X_teoria.ipynb` | Template — a preencher |

## Scripts do `auxil/` utilizados

*(a definir)*

## Pré-requisitos

- Capítulo X-1
```

Criar para: `Chapter04/README.md`, `Chapter05/README.md`, `Chapter06/README.md`, `Chapter07/README.md`, `Chapter08/README.md`, `Chapter09/README.md`

Para o `Chapter05/README.md`, adicionar os exercícios já existentes:
```markdown
| Exercícios | `exercises/ex05_1.py` | Exercício 5.1 — detecção de cantos/arestas |
| Exercícios | `exercises/ex05_2.py` | Exercício 5.2 |
| Exercícios | `exercises/ex05_3.py` | Exercício 5.3 |
```

Para o `Chapter09/README.md`:
```markdown
| Exercícios | `exercises/ex09_1.py` | Exercício 9.1 |
```

**Step 5: Verificar**

```bash
ls Chapter*/README.md
# Esperado: 9 arquivos README.md
```

---

### Task 8: Criar `auxil/README.md` com tabela de scripts × capítulos

**Files:**
- Criar: `auxil/README.md`

**Step 1: Criar o arquivo**

```markdown
# auxil/ — Biblioteca de Scripts e Módulos

Esta pasta contém os módulos Python e scripts de linha de comando do Apêndice C do livro Canty (2019).

## Módulos importáveis (`auxil/*.py`)

| Módulo | Descrição | Usado em |
|--------|-----------|----------|
| `auxil1.py` | Funções auxiliares (regressão ortogonal, tabelas de cores) | Vários |
| `supervisedclass.py` | Classificação supervisionada (MaxLike, SVM, RF, Neural Net, DNN) | Cap 7 |
| `readshp.py` | Leitura de shapefiles | Cap 7 |
| `eeMad.py` | Detecção de mudanças via Google Earth Engine | Cap 8 |
| `eeWishart.py` | Classificação Wishart via GEE | Cap 8 |
| `registerms.py` | Registro de imagens multiespectrais | Cap 3 |
| `registersar.py` | Registro de imagens SAR | Cap 1 |
| `congrid.py` | Interpolação de grade (congruência) | Vários |
| `eeSar_seq.py` | Sequência temporal SAR via GEE | Cap 8 |
| `lookup.py` | Tabelas de busca | Vários |

## Scripts de linha de comando (`auxil/scripts/*.py`)

### Análise e Transformação Espectral

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `pca.py` | Análise de Componentes Principais | Cap 2, 3 | `python pca.py [-p bandas] [-n] imagem.tif` |
| `kpca.py` | Kernel PCA | Cap 3 | `python kpca.py imagem.tif` |
| `mnf.py` | Minimum Noise Fraction | Cap 3 | `python mnf.py [-p bandas] imagem.tif` |
| `hcl.py` | Transformação HCL | Cap 3 | `python hcl.py imagem.tif` |
| `atwt.py` | Transformação wavelet adaptativa | Cap 3 | `python atwt.py imagem.tif` |
| `dwt.py` | Discrete Wavelet Transform | Cap 3 | `python dwt.py imagem.tif` |

### Classificação

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `classify.py` | Classificação supervisionada (7 algoritmos) | Cap 7 | `python classify.py -a 1 imagem.tif` |
| `adaboost.py` | AdaBoost ensemble | Cap 7 | `python adaboost.py imagem.tif` |

### Clustering

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `kmeans.py` | K-means clustering | Cap 6 | `python kmeans.py -k 5 imagem.tif` |
| `kkmeans.py` | Kernel K-means | Cap 6 | `python kkmeans.py imagem.tif` |
| `som.py` | Self-Organizing Maps | Cap 6 | `python som.py imagem.tif` |
| `meanshift.py` | Mean Shift | Cap 6 | `python meanshift.py imagem.tif` |
| `em.py` | Expectation Maximization | Cap 6 | `python em.py imagem.tif` |

### Detecção de Mudanças

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `iMad.py` | Iterated MAD (detecção de mudanças) | Cap 8 | `python iMad.py -i 30 img1.tif img2.tif` |
| `iMad_tf.py` | iMAD versão TensorFlow | Cap 8 | `python iMad_tf.py img1.tif img2.tif` |
| `iMadmap.py` | Mapeamento de resultados iMAD | Cap 8 | `python iMadmap.py imad_result.tif` |

### Detecção de Anomalias

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `rx.py` | RX detector de anomalias | Cap 5 | `python rx.py imagem.tif` |
| `krx.py` | Kernel RX | Cap 5 | `python krx.py imagem.tif` |

### Processamento SAR

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `sar_seqQ.py` | SAR sequencial com teste Q | Cap 8 | `python sar_seqQ.py` |
| `c_corr.py` | C-correction para SAR | Cap 1 | `python c_corr.py imagem.tif` |

### Filtros

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `mmse_filter.py` | Filtro MMSE | Cap 5 | `python mmse_filter.py imagem.tif` |
| `gamma_filter.py` | Gamma filter (despeckling SAR) | Cap 5 | `python gamma_filter.py imagem.tif` |

### Calibração e Estatística

| Script | Descrição | Capítulo(s) | Uso básico |
|--------|-----------|-------------|-----------|
| `radcal.py` | Calibração radiométrica | Cap 2 | `python radcal.py imagem.tif` |
| `mcnemar.py` | Teste estatístico de McNemar | Cap 7 | `python mcnemar.py` |
| `crossvalidate.py` | Cross-validation | Cap 7 | `python crossvalidate.py` |
| `scatterplot.py` | Gráfico de dispersão espectral | Vários | `python scatterplot.py imagem.tif` |

> **Nota:** Os capítulos indicados são estimativas baseadas nos algoritmos. Serão atualizados conforme o estudo avançar.
```

**Step 2: Verificar**

```bash
cat auxil/README.md | head -10
```

---

### Task 9: Atualizar `README.md` raiz com tabela de progresso

**Files:**
- Modificar: `README.md`

**Step 1: Adicionar seção de progresso após os Objetivos (antes de "Estrutura do Repositório")**

Inserir logo após a seção `## 💡 Filosofia de Estudo` e antes de `## 📦 Estrutura do Repositório`:

```markdown
## 📊 Progresso dos Capítulos

| Cap | Tópico Principal | Status | Theory | Notebooks | Exercises |
|-----|-----------------|--------|--------|-----------|-----------|
| 1 | Fundamentos, Sensores, SAR | 🟡 Em andamento | ✅ | ⬜ | ✅ |
| 2 | Variáveis Aleatórias, PCA | 🟡 Em andamento | ✅ | ⬜ | ⬜ |
| 3 | Transformações Espectrais, MNF | 🟡 Em andamento | ✅ | ⬜ | ✅ |
| 4 | *(a definir)* | ⬜ Não iniciado | ⬜ | ⬜ | ⬜ |
| 5 | *(a definir)* | ⬜ Não iniciado | ⬜ | ⬜ | ✅ |
| 6 | *(a definir)* | ⬜ Não iniciado | ⬜ | ⬜ | ⬜ |
| 7 | *(a definir)* | ⬜ Não iniciado | ⬜ | ⬜ | ⬜ |
| 8 | *(a definir)* | ⬜ Não iniciado | ⬜ | ⬜ | ⬜ |
| 9 | *(a definir)* | ⬜ Não iniciado | ⬜ | ⬜ | ✅ |

> **Legenda:** ✅ Completo · 🟡 Em andamento · ⬜ Não iniciado
```

**Step 2: Atualizar a seção `## 📦 Estrutura do Repositório`** para refletir os novos nomes:

Substituir referências a `notes/`, `code/`, `imagens/` pelos novos nomes `theory/`, `notebooks/`, `outputs/`.

Texto atualizado da seção:

```markdown
## 📦 Estrutura do Repositório

```
sensoriamento-remoto-python-estudo/
├── ChapterXX/                  # Um por capítulo (Chapter01 a Chapter09)
│   ├── README.md               # Status, tópicos, scripts usados, pré-requisitos
│   ├── theory/                 # Anotações teóricas em Markdown (com LaTeX)
│   ├── notebooks/              # Jupyter Notebooks com implementações
│   ├── exercises/              # Scripts de resolução dos exercícios do livro
│   ├── data/                   # Dados e imagens de entrada
│   └── outputs/                # Visualizações e resultados gerados
├── auxil/
│   ├── README.md               # Tabela de scripts × capítulos
│   ├── *.py                    # Módulos importáveis (Apêndice C)
│   └── scripts/
│       └── *.py                # Scripts de linha de comando (Apêndice C.4)
├── resources/
│   └── *.pdf                   # Livro e materiais de referência
├── docs/
│   └── plans/                  # Planos de implementação
├── README.md
├── CLAUDE.md
└── guia-github-iniciantes.md
```

---

### Task 10: Atualizar `CLAUDE.md` para refletir nova estrutura

**Files:**
- Modificar: `CLAUDE.md`

**Step 1: Atualizar a seção `## Estrutura do Repositório`**

Substituir a estrutura antiga pela nova:

```markdown
## Estrutura do Repositório

```
.
├── ChapterXX/
│   ├── README.md        # Status, tópicos, scripts usados, pré-requisitos
│   ├── theory/          # Anotações teóricas em Markdown (antigo notes/)
│   ├── notebooks/       # Jupyter Notebooks com exemplos (antigo code/)
│   ├── exercises/       # Scripts de exercícios (vindos de auxil/scripts/exercices/)
│   ├── data/            # Imagens e dados de entrada
│   └── outputs/         # Visualizações geradas (antigo imagens/)
├── auxil/
│   ├── README.md        # Tabela de scripts × capítulos
│   ├── *.py             # Módulos auxiliares reutilizáveis
│   └── scripts/
│       └── *.py         # Scripts de algoritmos (pca, classify, iMad, etc.)
├── resources/           # Livro PDF e materiais de referência
├── docs/
│   └── plans/           # Planos de implementação
├── README.md
└── guia-github-iniciantes.md
```

**Step 2: Verificar**

Confirmar que as mudanças estão salvas.

---

### Task 11: Commit final com todas as mudanças

**Step 1: Verificar status geral**

```bash
cd /Users/bruno/Documents/sensoriamento-remoto-python-estudo
git status
```

Conferir se todas as mudanças esperadas estão presentes e nenhum arquivo foi perdido acidentalmente.

**Step 2: Adicionar novos arquivos não rastreados**

```bash
git add Chapter01/exercises/
git add Chapter02/exercises/
git add Chapter03/exercises/
git add Chapter04/exercises/
git add Chapter05/exercises/
git add Chapter06/exercises/
git add Chapter07/exercises/
git add Chapter08/exercises/
git add Chapter09/exercises/
git add Chapter01/README.md Chapter02/README.md Chapter03/README.md
git add Chapter04/README.md Chapter05/README.md Chapter06/README.md
git add Chapter07/README.md Chapter08/README.md Chapter09/README.md
git add Chapter01/notebooks/ Chapter02/notebooks/ Chapter03/notebooks/
git add Chapter04/notebooks/ Chapter05/notebooks/ Chapter06/notebooks/
git add Chapter07/notebooks/ Chapter08/notebooks/ Chapter09/notebooks/
git add Chapter02/outputs/ Chapter03/outputs/ Chapter04/outputs/
git add Chapter05/outputs/ Chapter06/outputs/ Chapter07/outputs/
git add Chapter08/outputs/ Chapter09/outputs/
git add auxil/README.md
git add resources/
git add docs/
```

**Step 3: Criar o commit**

```bash
git commit -m "$(cat <<'EOF'
reorganiza estrutura do repositório para padronizar capítulos

- Renomeia notes/ → theory/, code/ → notebooks/, imagens/ → outputs/
- Distribui exercícios de auxil/scripts/exercices/ para cada ChapterXX/exercises/
- Cria README.md por capítulo com status e tabela de conteúdo
- Cria template padronizado de notebook (XX_teoria.ipynb) para os 9 capítulos
- Cria auxil/README.md com tabela de scripts × capítulos
- Move PDF do livro para resources/
- Remove notebooks vazios (placeholders) e arquivos de template incorretos
- Limpa placeholder "blablablablalba" do section_3.5.md
- Atualiza README.md raiz com tabela de progresso por capítulo
- Atualiza CLAUDE.md com nova estrutura

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**Step 4: Verificar commit**

```bash
git log --oneline -3
git show --stat HEAD
```

---

## Verificação Final (Checklist)

Após o commit, confirmar:

- [ ] `ls Chapter01/` mostra: `README.md  data/  exercises/  notebooks/  outputs/  theory/  apresentations/`
- [ ] `ls Chapter09/` mostra: `README.md  data/  exercises/  notebooks/  outputs/  theory/`
- [ ] `ls auxil/scripts/exercices/` está vazio
- [ ] `ls resources/` contém o PDF do livro
- [ ] `ls Chapter01/notebooks/` contém `01_teoria.ipynb`
- [ ] Nenhum arquivo `cap2.ipynb`, `Capítulo_1.ipynb` existe
- [ ] `Chapter03/theory/section_3.5.md` não contém "blablablablalba"
- [ ] `auxil/README.md` existe e tem tabela de scripts
- [ ] `README.md` raiz tem seção `📊 Progresso dos Capítulos`
- [ ] `CLAUDE.md` reflete nova estrutura de pastas
- [ ] `git log --oneline -1` mostra o commit de reorganização
