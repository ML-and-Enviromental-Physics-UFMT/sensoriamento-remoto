# Como contribuir

Escolha o módulo pelo assunto. Use o README do módulo para indicar a ordem de leitura, os pré-requisitos e o estado do material.

Escreva aulas curtas em português. Explique os símbolos e resolva um exemplo pequeno antes de usar uma imagem real. Exercícios devem ter objetivo e resultado interpretável. Identifique simulações e preserve as incertezas.

Registre fontes por autoria, título, versão e link original em `referencias/`. As aulas apontam as seções usadas. PDFs públicos ou privados ficam só no computador e são ignorados pelo Git.

Dados compartilhados ficam em `data/`, com origem e condições de uso. Utilitários próprios ficam em `study_utils/`. O software do livro é obtido separadamente, conforme `legado/canty/README.md`, e permanece em `referencias/local/`, ignorado pelo Git. Não acrescente dados externos ou código de terceiros sem registrar a fonte e as condições de distribuição.

Antes de propor uma mudança, confira os links, execute as práticas afetadas e registre os limites da verificação. Da raiz, as verificações estruturais são executadas com:

```bash
python -m unittest discover -s tests
```

A existência de uma aula ou a execução de um notebook não demonstra validação científica do método.

Ao contribuir, você concorda em publicar seu texto sob CC BY 4.0 e seu código sob a licença MIT, as mesmas do repositório, descritas no [README](README.md#licença).

Antes de publicar, remova saídas e anexos dos notebooks e execute `python scripts/auditar_publicacao.py`. A auditoria desta cópia aceita somente o raster sintético como binário. Novas figuras próprias precisam de revisão de procedência e atualização explícita dessa regra.
