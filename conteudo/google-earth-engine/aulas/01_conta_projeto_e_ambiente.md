# Conta, projeto Google Cloud e ambiente Python

Para trabalhar com imagens de satélite no computador local, normalmente você baixa arquivos GeoTIFF de centenas de megabytes antes de calcular um único índice. No Google Earth Engine (GEE), o catálogo de imagens e o processamento ficam nos servidores do Google (Gorelick et al., 2017). Seu código Python monta instruções de processamento, envia essas instruções ao servidor e traz de volta apenas o resumo, o mapa interativo ou o arquivo exportado.

Antes de rodar a primeira linha de código, existe uma etapa administrativa obrigatória: vincular sua conta Google a um projeto do Google Cloud habilitado para o Earth Engine.

## 1. Quando usar o GEE, cotas e limites

O GEE facilita a exploração de séries históricas (Sentinel-2, Landsat, MODIS, Sentinel-1, SRTM, MapBiomas e outros catálogos públicos) sem baixar dezenas de cenas. Ele tem, porém, limites explícitos:

- Exige internet e conta vinculada a um projeto no Google Cloud.
- O acesso gratuito vale para uso não comercial (ensino, pesquisa acadêmica, organizações sem fins lucrativos e projetos pessoais). Uso comercial exige plano pago.
- Desde abril de 2026, projetos não comerciais operam sob cotas mensais de computação em EECU-horas (Earth Engine Compute Units): o nível padrão **Community** oferece 150 EECU-horas por mês; o nível **Contributor** oferece 1.000 EECU-horas por mês (exige conta de faturamento vinculada ao projeto, sem cobrança pelo uso não comercial dentro da cota). Projetos não comerciais passam por reverificação periódica (anual), e criar vários projetos para acumular cotas viola os termos de uso.
- Além da cota mensal, há limites de memória, tempo de requisição interativa e armazenamento de assets.
- O controle sobre detalhes internos de alguns algoritmos é menor do que em código local com NumPy, rasterio e scikit-learn. Por isso, o núcleo local deste repositório continua sendo a base para entender a matemática dos métodos.

## 2. Registrar um projeto no Google Cloud

O Earth Engine exige um identificador de projeto do Google Cloud (`project ID`) na inicialização. Seguir os passos nesta ordem evita a maior parte dos erros:

1. Acesse [https://code.earthengine.google.com/register](https://code.earthengine.google.com/register) logado na sua conta Google.
2. Escolha a opção de uso não comercial, caso esteja estudando ou fazendo pesquisa acadêmica, e selecione o perfil adequado (por exemplo, academia e pesquisa).
3. Crie um novo projeto no Google Cloud ou escolha um projeto existente quando o assistente pedir.
4. Confirme o registro e anote o **ID do projeto** (algo como `ee-seu-usuario` ou `meu-projeto-gee-123456`). O ID nem sempre é igual ao nome de exibição do projeto.
5. Caso o sistema informe que a API não está ativa, abra o console do Google Cloud, selecione o mesmo projeto e ative a **Earth Engine API**.

Não compartilhe credenciais nem chaves privadas em repositórios Git. O fluxo interativo abaixo salva o token fora do projeto, na sua pasta de usuário.

## 3. Instalar o ambiente Python

Da raiz do repositório, crie um ambiente virtual separado para não interferir nas bibliotecas do núcleo local. Recomenda-se Python 3.12 ou superior para usar as versões mais recentes do `geemap` (a partir da versão 0.39, `geemap` exige Python 3.12+; em Python 3.11, o `pip` resolve automaticamente para a série 0.37):

```bash
python3.12 -m venv .venv-gee
source .venv-gee/bin/activate
python -m pip install -r conteudo/google-earth-engine/requirements-gee.txt
```

No Windows, ative com `.venv-gee\Scripts\activate`.

As duas bibliotecas centrais deste percurso são:

- `earthengine-api` (importada como `ee`): biblioteca oficial do Google para montar e enviar comandos ao servidor.
- `geemap` (Wu, 2020): biblioteca construída sobre `ee` e `ipyleaflet` para visualizar camadas em mapas interativos dentro do Jupyter e do Google Colab.

Se optar pelo Google Colab, `earthengine-api` já vem pré-instalado (basta instalar `geemap` com `!pip install -q geemap`), mas será necessário reautenticar a cada nova sessão de runtime.

## 4. Autenticar e inicializar

Na primeira vez em um computador (ou quando o token expirar), execute a autenticação interativa. Para evitar commitar o ID do seu projeto pessoal em notebooks versionados, uma boa prática é defini-lo em uma variável de ambiente (`export GEE_PROJECT_ID="seu-projeto"` no Linux/macOS ou `set GEE_PROJECT_ID=seu-projeto` no Windows) e lê-lo com `os.environ`:

```python
import os
import ee

GEE_PROJECT_ID = os.environ.get("GEE_PROJECT_ID", "SEU_PROJECT_ID_AQUI")

ee.Authenticate()
ee.Initialize(project=GEE_PROJECT_ID)
```

O que acontece em cada etapa:

1. `ee.Authenticate()` abre um link no navegador para você autorizar sua conta Google e gerar o token local (normalmente salvo em `~/.config/earthengine/credentials`). Em execuções seguintes na mesma máquina local, você não precisa repetir essa chamada.
2. `ee.Initialize(project=...)` abre a sessão da API usando o projeto registrado no Google Cloud.

Para testar se a conexão responde, peça ao servidor as bandas do modelo digital de elevação SRTM (USGS/NASA):

```python
dem = ee.Image("USGS/SRTMGL1_003")
print(dem.bandNames().getInfo())
```

Se a saída mostrar `['elevation']`, o ambiente está pronto.

## 5. Erros comuns na primeira configuração

- **`EEException: no project found`**: você chamou `ee.Initialize()` sem passar `project="..."` e não há projeto padrão configurado. Passe o ID explicitamente ou defina um padrão no terminal com `earthengine set_project SEU_PROJECT_ID_AQUI`.
- **`Earth Engine API has not been used in project ...`**: a API ainda não foi habilitada no projeto escolhido no Google Cloud. Ative a Earth Engine API no console e aguarde um ou dois minutos.
- **`Project is not registered`**: o projeto existe no Google Cloud, mas ainda não foi registrado no Earth Engine pelo endereço de registro acima.
- **Erro de permissão IAM (`serviceusage.services.use` / `serviceUsageConsumer`)**: comum em projetos institucionais ou compartilhados. Peça ao administrador do projeto no Google Cloud para atribuir à sua conta o papel `Service Usage Consumer` (`roles/serviceusage.serviceUsageConsumer`) e permissão de uso do Earth Engine.
- **Mapa do `geemap` não aparece no Jupyter**: confira se o kernel selecionado no notebook é o mesmo ambiente `.venv-gee` onde `geemap` foi instalado.

## Tente explicar

1. Por que `ee.Initialize()` precisa do argumento `project`?
2. Qual é a diferença de papel entre `earthengine-api` (`ee`) e `geemap`?
3. Por que o repositório mantém `requirements-gee.txt` separado do ambiente principal?

<details>
<summary>Respostas comentadas</summary>

1. Porque o Earth Engine gerencia permissões, cotas mensais de EECU-horas e registro de uso (não comercial ou comercial) por meio de um projeto no Google Cloud.
2. `ee` é a API oficial que constrói e envia as operações ao servidor do GEE. `geemap` é uma camada complementar voltada a mapas interativos e utilitários no Jupyter.
3. Para que quem estuda o núcleo local de sensoriamento remoto não precise criar conta nem instalar dependências de nuvem para executar os exemplos offline.

</details>

Na próxima etapa, leia [Modelo cliente-servidor e objetos `ee`](02_modelo_cliente_servidor.md) antes de rodar o notebook [Primeiros passos no GEE](../notebooks/01_primeiros_passos_gee.ipynb).

Fontes (consultadas em 25/11/2026): Google, [Earth Engine Python Installation](https://developers.google.com/earth-engine/guides/python_install), [Authentication and Initialization](https://developers.google.com/earth-engine/guides/auth) e [Noncommercial Usage Tiers](https://developers.google.com/earth-engine/guides/noncommercial_tiers); Gorelick et al. (2017); Wu (2020).
