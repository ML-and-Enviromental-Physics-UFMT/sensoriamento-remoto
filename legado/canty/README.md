# Código de referência do Canty

A cópia pública não redistribui os arquivos Python e shell do antigo `auxil/`. O material histórico permanece no repositório antigo. O backup temporário da limpeza foi apagado a pedido do responsável. As menções a `legado/canty/auxil/*.py` nas aulas indicam caminhos históricos de consulta, não arquivos incluídos nesta versão.

A fonte oficial para a quarta edição é [mortcanty/CRC4Docker](https://github.com/mortcanty/CRC4Docker). A [licença MIT do autor](https://github.com/mortcanty/CRC4Docker/blob/e52a6e88d4469284a071c0b96d009f6684dbb2ea/LICENSE.txt) declara copyright de Mort Canty, 2018. Essa licença do software não é uma autorização de redistribuição do livro ou de imagens utilizadas nos exemplos. Componentes incorporados podem ter avisos adicionais, que devem ser preservados.

## Obtenção opcional

Para consultar a fonte oficial, execute na raiz.

```bash
git clone https://github.com/mortcanty/CRC4Docker.git referencias/local/CRC4Docker
git -C referencias/local/CRC4Docker checkout --detach e52a6e88d4469284a071c0b96d009f6684dbb2ea
```

`referencias/local/` fica fora do versionamento. O commit fixa a fonte consultada em 15/11/2026; não garante compatibilidade com o ambiente deste projeto. Os arquivos locais retirados tinham adaptações e não eram todos idênticos a essa versão. Não os substituímos automaticamente pelo upstream.

O exercício opcional de duas datas usa `referencias/local/CRC4Docker/src` por padrão. Para outra instalação, defina `CANTY_SRC` com o caminho da pasta `src`, que contém `auxil/` e `scripts/`.

```bash
PYTHONPATH=. python conteudo/series-temporais/exercicios/ex09_1.py imagem_t1.tif imagem_t2.tif
```

Esse fluxo requer duas imagens compatíveis, GDAL e as dependências do software externo, incluindo a biblioteca nativa usada por `auxil1.py`. O upstream contém rotinas antigas. A obtenção está documentada, mas a execução do legado completo não foi validada. Os exemplos próprios de PCA e agrupamento não exigem esse pacote.
