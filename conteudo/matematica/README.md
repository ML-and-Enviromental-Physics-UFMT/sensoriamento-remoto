# Matemática para sensoriamento remoto

Os tópicos podem ser consultados separadamente ou estudados pelas dependências sugeridas. Cada texto apresenta o conceito, calcula um exemplo pequeno e oferece exercícios com respostas comentadas. As contas usam números inventados e não dependem de abrir um livro ou baixar uma imagem.

Se os símbolos ainda forem uma barreira, comece por [notação e funções](notacao-e-funcoes.md). Depois, use os blocos abaixo. Não é preciso ler tudo em uma sessão.

## Álgebra linear

O [índice de álgebra linear](algebra-linear/README.md) explicita os pré-requisitos e as aplicações.

- [Vetores e matrizes](algebra-linear/vetores-e-matrizes.md): representar pixels e bandas.
- [Produtos e transposta](algebra-linear/produtos-e-transposta.md): combinar medições e conferir dimensões.
- [Sistemas e inversa](algebra-linear/sistemas-e-inversa.md): resolver incógnitas e reconhecer sistemas sem solução única.
- [Determinantes](algebra-linear/determinantes.md): área, volume e singularidade.
- [Espaços, bases e projeções](algebra-linear/espacos-bases-e-projecoes.md): descrever coordenadas e informação descartada.
- [Transformações lineares](algebra-linear/transformacoes-lineares.md): núcleo, imagem, posto e mistura de bandas.
- [Autovalores e autovetores](algebra-linear/autovalores-e-autovetores.md): direções de variância e PCA.
- [SVD](algebra-linear/svd.md): fatoração, reconstrução e ligação com PCA.
- [Condicionamento e mínimos quadrados](algebra-linear/condicionamento-e-minimos-quadrados.md): sensibilidade e ajuste com resíduos.

## Probabilidade e estatística

- [Probabilidade e informação condicional](estatistica/probabilidade.md): eventos, Bayes e efeito da prevalência.
- [Distribuições e estimação](estatistica/distribuicoes-e-estimacao.md): densidade, média, variância e incerteza da estimativa.
- [Covariância e correlação](estatistica/covariancia.md): variação conjunta e singularidade.
- [Mahalanobis](estatistica/mahalanobis.md): distância considerando escala e orientação.

## Cálculo e otimização

- [Derivadas, gradientes e cadeia](calculo/derivadas-e-gradientes.md): como o erro muda com os parâmetros.
- [Gradiente descendente](otimizacao/gradiente-descendente.md): passo, estabilidade e parada.
- [Lagrange](otimizacao/lagrange.md): otimização com restrição e derivação da direção principal.

Esses textos desenvolvem a base de cálculo e otimização exigida pelos exemplos atuais. Integração, cálculo vetorial, inferência estatística aprofundada e métodos avançados de otimização continuam como expansão do percurso. Isso não altera a ambição de cobertura ampla do projeto.

## Prática e consulta

O [notebook de experimentos](notebooks/explorar-conceitos.ipynb) permite alterar matrizes, direções, prevalência e passo de otimização, com figuras de projeção e convergência. Precisa de NumPy e Matplotlib, disponíveis no ambiente do repositório.

O [script de conferência](exercicios/conferir-exemplos.py) recalcula os exemplos principais. Execute da raiz:

```bash
python conteudo/matematica/exercicios/conferir-exemplos.py
```

A [consulta rápida](consulta-rapida.md) reúne fórmulas. A [bibliografia](../../referencias/matematica/README.md) registra os livros e as fontes complementares. Cada tópico aponta a referência usada; a incorporação integral de todos os livros não está concluída. PDFs locais ficam fora do Git.

Para aplicar PCA, retome projeções, autovalores, SVD e covariância. Para classificação gaussiana, retome probabilidade, determinantes e Mahalanobis. Para redes, retome a cadeia e a otimização e avance para [treinamento de redes](../classificacao/treinamento-de-redes/README.md).
