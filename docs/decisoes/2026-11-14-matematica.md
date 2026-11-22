# Desenvolvimento da base matemática e planejamento

Foram desenvolvidos 17 tópicos: notação, nove de álgebra linear, quatro de probabilidade/estatística, um de cálculo e dois de otimização. Os índices e a consulta rápida não entram nessa contagem. Cada tópico tem exemplos e exercícios com respostas recolhidas. As fontes apontam livros locais e materiais universitários ou editoriais primários; os PDFs permanecem ignorados pelo Git.

## Verificação

- O script `conteudo/matematica/exercicios/conferir-exemplos.py` recalculou produtos, solução de sistemas, determinantes, mínimos quadrados, projeção, autovalores, SVD, Bayes, covariâncias, Mahalanobis, diferenças finitas, trajetória de descida e condições de Lagrange.
- Foi corrigida uma SVD explícita cujo fator U inicialmente não reconstruía a matriz. A versão corrigida reconstrói o exemplo no script de conferência.
- O notebook `conteudo/matematica/notebooks/explorar-conceitos.ipynb` executou integralmente. Suas saídas didáticas e duas figuras foram salvas no próprio notebook.
- As quatro verificações estruturais passaram. Links de Markdown/notebooks/planejamento, blocos de fórmulas e seções de respostas foram conferidos.
- Os 29 pacotes do plano foram relidos, incluindo títulos, horas, marco e dependências; as relações corresponderam ao plano e não apresentaram ciclos. Nenhuma issue foi marcada Done nesta operação.

A execução ocorreu no ambiente local da verificação anterior, Python 3.14.4. Não demonstra instalação limpa em Python 3.11, validação científica de métodos nem revisão independente por especialista.

## Gestão e estudo

O [plano de desenvolvimento](../planejamento/desenvolvimento.md) usa a capacidade informada de 5 h/semana para produzir e revisar o repositório. A [estimativa de estudo](../planejamento/estimativa-de-estudo.md) foi escrita separadamente. As antigas issues de estudo foram reformuladas como entregas de material didático.

A escrita inicial e a conferência numérica desta sessão não encerram a revisão independente ou os testes com leitores. Essas etapas permanecem visíveis no planejamento. Não houve commit, push ou publicação das mudanças locais.
