# Organização por assuntos

O projeto passa de um caderno organizado pelos capítulos do Canty para percursos por assunto. O objetivo é incorporar várias referências e cobrir progressivamente as especialidades de sensoriamento remoto.

## Decisões

- `conteudo/` reúne os percursos. Matemática tem uma entrada própria, consultável pelas aplicações.
- Estatística, transformações e filtros ficam sob análise de imagens. Classificação mantém blocos supervisionados, redes, avaliação e agrupamento.
- `aulas/`, `notebooks/`, `exercicios/` e `figuras/` nomeiam os tipos de material. Não criamos pastas vazias para conteúdo futuro.
- A distribuição ASTER foi movida sem alteração para `data/exemplos/`. A ligação do antigo Capítulo 2 foi retirada; todos usam a mesma localização.
- O piloto de `mestrado/` virou `projetos/pca-e-agrupamento/`, sem alegação de validação científica ou de dados de dissertação.
- `auxil/` fica em `legado/canty/auxil/`. O nome do pacote foi mantido para preservar seus imports internos.
- `referencias/` reúne fontes e metadados. Todos os PDFs continuam ignorados pelo Git. As cópias antigas foram preservadas em `referencias/local/`; os novos livros estão em `referencias/matematica/`.
- O plano de estudo e o modelo de diário ficam em `docs/`. As pendências correntes ficam em `docs/pendencias.md`.

A [correspondência com Canty](../../referencias/canty.md) orienta quem segue o livro. O [mapa de arquivos](mapa-de-migracao.json) permite localizar materiais da árvore anterior. O plano antigo em `docs/plans/` e a visualização da proposta ficam como histórico, não como instruções de manutenção atuais.

As páginas de LiDAR, hiperespectral, termal, sensores e aplicações são entradas para desenvolvimento. Sua existência não significa que já oferecem um curso completo.

## Matemática por tópicos

Álgebra linear passou a usar páginas temáticas em `conteudo/matematica/algebra-linear/`, sem numeração de aulas. Covariância e Mahalanobis ficam em `estatistica/`; Lagrange fica em `otimizacao/`. O antigo guia reunido em `aulas/00_teoria.md` foi distribuído entre esses tópicos, e os links de consulta foram atualizados.
