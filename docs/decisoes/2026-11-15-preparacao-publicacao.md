# Preparação da cópia pública

Em 15/11/2026, esta pasta foi preparada como uma cópia independente, sem os commits, referências ou objetos do Git anterior. O backup temporário criado durante a limpeza foi apagado a pedido do responsável, que informou manter o repositório antigo salvo. O repositório remoto anterior não foi alterado. Nenhum commit, push ou publicação foi feito nesta etapa.

## Conteúdo retirado

Foram retirados 91 arquivos: o ASTER histórico, 44 imagens e 46 arquivos Python/shell do legado. O material histórico permanece no repositório antigo, conforme informado pelo responsável. As saídas, contagens de execução e anexos dos 13 notebooks foram limpos. As referências a figuras retiradas foram substituídas por avisos, sem inventar novas imagens. O estado local do editor também ficou fora desta cópia.

A [lista dos arquivos retirados](limpeza-publicacao.json) registra também os destinos aposentados do mapa de migração. O mapa principal conserva os destinos que ainda existem. Os relatórios de 14/11 descrevem o estado anterior e não devem ser interpretados como inventário desta cópia.

## Alternativas incluídas

O [raster sintético](../../data/README.md) substitui o ASTER como entrada padrão dos exercícios e notebooks próprios. Os caminhos, imports e rótulos foram atualizados. Três notebooks agora limitam a amostragem ao número de pixels disponíveis. O gerador não lê o ASTER, não possui localização geográfica e usa valores de unidades arbitrárias.

A procedência e as condições de distribuição do ASTER histórico não foram recuperadas. O nome e os metadados insuficientes não permitem identificar o produto. O arquivo deixou de ser uma dependência distribuída; a investigação histórica permanece pendente.

O [guia do Canty](../../legado/canty/README.md) indica a fonte oficial, a licença MIT do autor e um commit de referência para obtenção separada. Os arquivos locais tinham adaptações e não eram todos idênticos ao upstream. A cópia pública não os redistribui nem os substitui silenciosamente. A instalação opcional fica em uma pasta ignorada pelo Git. O exercício de duas datas informa essa exigência antes de importar o pacote externo.

## Verificações

Com Python 3.14.4 e o ambiente virtual já disponível no computador:

- Seis testes passaram: quatro estruturais, auditoria dos arquivos públicos e comparação exata entre o raster incluído e o gerador.
- A conferência matemática passou.
- Os 13 notebooks executaram integralmente com as novas entradas.
- Os 15 scripts selecionados executaram sem erro.
- Não há saídas ou anexos embutidos nos notebooks destinados à publicação.
- A auditoria não encontrou os PDFs, imagens antigas ou fontes do legado entre os arquivos candidatos à publicação.

Notebooks e scripts foram executados em cópias temporárias. Seus resultados não foram promovidos para a cópia pública. A [relação das execuções](2026-11-15-execucoes-publicacao.json) identifica os arquivos verificados.

Para repetir as verificações locais, use o ambiente documentado no projeto e execute na raiz.

```bash
python -m unittest discover -s tests -v
python conteudo/matematica/exercicios/conferir-exemplos.py
python scripts/auditar_publicacao.py
```

## Limites

A instalação limpa com Python 3.11, o legado externo e os exercícios que requerem GDAL ou pontos de controle não foram validados nesta etapa. Execução com números artificiais não valida conclusões ambientais, acurácia de classes reais ou qualidade pedagógica. As figuras didáticas novas e a revisão independente continuam pendentes. A auditoria cobre os arquivos que o Git incluiria, não dados locais ignorados nem revisões futuras.

Ao concluir a preparação local, a branch `main` estava sem commits e sem remoto configurado. O T3 Code pode criar checkpoints internos em `refs/t3/`; eles registram o estado novo da pasta e não constituem histórico herdado do repositório antigo.

A preparação local foi concluída. Criar um remoto, fazer o commit inicial e publicar a cópia são ações separadas.
