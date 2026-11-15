# Pendências de desenvolvimento

O acompanhamento operacional está no [projeto do Linear](https://linear.app/brunommv/project/sensoriamento-remoto-com-python-desenvolvimento-da-referencia-aberta-3e1e8c2dc45d), com 29 entregas e seis marcos. As issues medem produção e revisão de material. Não acompanham leitura nem domínio pessoal de Bruno.

O [plano local](planejamento/desenvolvimento.md) registra esforço, dependências, critérios de pronto e hipóteses do calendário. O [arquivo estruturado](planejamento/desenvolvimento.json) espelha a versão inicial do planejamento. Mudanças operacionais precisam ser reconciliadas com essa cópia.

## Próximas entregas

- [BRU-198, ambiente e integração contínua](https://linear.app/brunommv/issue/BRU-198): conferir instalação limpa no ambiente suportado e automatizar verificações.
- [BRU-199, dados](https://linear.app/brunommv/issue/BRU-199): recuperar procedência e condições de uso do recorte ASTER.
- [BRU-200, Python/NumPy](https://linear.app/brunommv/issue/BRU-200): completar a entrada de programação.
- [BRU-201, matemática](https://linear.app/brunommv/issue/BRU-201): revisar independentemente e consolidar os tópicos já escritos, exemplos e referências.
- [BRU-147, fundamentos](https://linear.app/brunommv/issue/BRU-147): integrar essas bases ao percurso de entrada.

A matemática desta sessão já foi escrita e suas contas principais foram conferidas. A revisão independente e a aplicação com referências científicas são etapas distintas, ainda pendentes. A execução de 12 notebooks e 15 scripts na reorganização permanece registrada no relatório, sem equivaler a teste de todo o ambiente legado.

## Histórico

O [planejamento anterior](arquivo/plano-anterior.md) foi preservado como registro. Seus checklists pessoais não são mais o modelo de gestão do projeto.

## Preparação da cópia pública em 15/11/2026

O ASTER histórico e o código legado foram retirados desta cópia, com alternativas documentadas em [dados](../data/README.md) e [legado](../legado/canty/README.md). Os exemplos próprios usam um raster sintético. A origem do recorte antigo continua sem confirmação; esta limpeza não encerra automaticamente a BRU-199. Veja o [relatório de preparação](decisoes/2026-11-15-preparacao-publicacao.md).
