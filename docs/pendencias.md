# Pendências de desenvolvimento

O acompanhamento operacional está nas [issues do repositório](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues), com 29 entregas e seis [marcos](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/milestones). As issues medem produção e revisão de material. Não acompanham leitura nem domínio pessoal de Bruno.

O [plano local](planejamento/desenvolvimento.md) registra esforço, dependências, critérios de pronto e hipóteses do calendário. O [arquivo estruturado](planejamento/desenvolvimento.json) espelha a versão inicial do planejamento. Mudanças operacionais precisam ser reconciliadas com essa cópia.

## Próximas entregas

- [#1, ambiente e integração contínua](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/1): conferir instalação limpa no ambiente suportado e automatizar verificações.
- [#2, dados](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/2): recuperar procedência e condições de uso do recorte ASTER.
- [#3, Python/NumPy](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/3): completar a entrada de programação.
- [#4, matemática](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/4): revisar independentemente e consolidar os tópicos já escritos, exemplos e referências.
- [#5, fundamentos](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/5): integrar essas bases ao percurso de entrada.

A matemática desta sessão já foi escrita e suas contas principais foram conferidas. A revisão independente e a aplicação com referências científicas são etapas distintas, ainda pendentes. A execução de 12 notebooks e 15 scripts na reorganização permanece registrada no relatório, sem equivaler a teste de todo o ambiente legado.

## Histórico

O [planejamento anterior](arquivo/plano-anterior.md) foi preservado como registro. Seus checklists pessoais não são mais o modelo de gestão do projeto.

## Preparação da cópia pública em 15/11/2026

O ASTER histórico e o código legado foram retirados desta cópia, com alternativas documentadas em [dados](../data/README.md) e [legado](../legado/canty/README.md). Os exemplos próprios usam um raster sintético. A origem do recorte antigo continua sem confirmação; esta limpeza não encerra automaticamente a [issue de dados](https://github.com/ML-and-Enviromental-Physics-UFMT/sensoriamento-remoto/issues/2). Veja o [relatório de preparação](decisoes/2026-11-15-preparacao-publicacao.md).
