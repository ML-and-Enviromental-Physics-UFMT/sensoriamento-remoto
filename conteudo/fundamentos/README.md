# Comece por aqui

Você não precisa conhecer sensoriamento remoto nem álgebra linear para começar esta etapa. O objetivo é entender o que uma imagem mede antes de aplicar um algoritmo. As apostilas do INPE ajudam a construir os fundamentos físicos e geográficos. O livro de Morton Canty (2019) orienta os algoritmos dos capítulos seguintes. As explicações são próprias e podem ser lidas sem abrir os PDFs.

## Primeira sessão

1. Leia [Da paisagem ao número](aulas/01_da_paisagem_ao_numero.md). Não precisa instalar nada.
2. Responda às perguntas antes de abrir as respostas comentadas.
3. Abra [Seu primeiro pixel](notebooks/00_primeiro_pixel.ipynb). Ele usa apenas Python, sem bibliotecas externas, imagens ou conta em serviço remoto.
4. Registre no [diário de aprendizagem](../../docs/modelo-diario.md) o que você conseguiu explicar e onde travou.

Para executar o notebook no computador, instale Jupyter em um ambiente virtual, a partir da raiz do repositório, e selecione esse ambiente como kernel.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install jupyter
python -m jupyter notebook conteudo/fundamentos/notebooks/00_primeiro_pixel.ipynb
```

No Windows, a ativação é `.venv\Scripts\activate`. Se já configurou o ambiente completo descrito no README da raiz, use-o. Ler as células pelo GitHub não executa o código.

## Leituras curtas, uma pergunta por vez

Não precisa ler tudo de uma vez. Reserve uma sessão para cada pergunta e registre uma explicação sua antes de avançar. Os blocos de aprofundamento e respostas ficam recolhidos para não interromper a leitura.

| Ordem | Pergunta | Leitura |
|-------|----------|---------|
| 1 | O que representam os números? | [Da paisagem ao número](aulas/01_da_paisagem_ao_numero.md) e notebook inicial |
| 2 | Por que materiais diferem entre bandas? | [Energia e resposta dos alvos](aulas/02_energia_e_alvos.md) |
| 3 | Como escolher uma observação? | [Satélites, sensores e resoluções](aulas/03_satelites_e_observacao.md) |
| 4 | Como reconhecer a paisagem? | [Interpretar imagens](aulas/04_interpretar_imagens.md) |
| 5 | Como localizar e medir? | [Da imagem ao mapa](aulas/05_da_imagem_ao_mapa.md) |
| 6 | Como investigar sem concluir cedo demais? | [Investigar uma mudança](aulas/06_investigar_uma_mudanca.md) |

O [catálogo do INPE](../../referencias/inpe/README.md) relaciona essas aulas aos links das apostilas na fonte original, com autores e páginas nos textos. Não é necessário ler as 15 apostilas em sequência. As partes históricas de missões e programas não são instruções de instalação ou catálogo atual de dados.

Ainda faltam aulas guiadas de Python com NumPy, matemática básica e leitura de metadados de uma imagem real. A prática inicial usa listas e quatro pixels inventados; não substitui essas aulas. A [trilha de aprendizagem](../../trilha-de-aprendizagem.md) mostra como seguir.

Avance para o [Capítulo 1](aulas/07-imagens-arrays-matrizes.md) quando conseguir explicar por que um pixel tem vários números e por que mudar as cores da tela não calibra a imagem. Se a notação matemática atrapalhar, consulte o [Apêndice A](../matematica/README.md). Não é necessário dominar PCA nesta etapa.
