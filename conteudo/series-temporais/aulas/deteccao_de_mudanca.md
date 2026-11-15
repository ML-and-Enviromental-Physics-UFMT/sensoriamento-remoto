# Detecção de Mudança

> Stub. Teoria didática completa: [`00_teoria.md`](00_teoria.md).  
> Referência: Canty (2019), Cap. 9.

## Premissa crítica: co-registro

Comparar duas datas só faz sentido se os pixels correspondem ao **mesmo** local. Erro de registro vira “mudança” falsa nas bordas. Em produtos já ortorretificados o problema diminui, mas ainda vale checar deslocamento residual (`legado/canty/auxil/registerms.py`, `legado/canty/auxil/registersar.py`).

## Diferença de imagens

Para uma banda (ou índice) $G_1$, $G_2$:

$$
D = |G_2 - G_1|.
$$

Limiar em $D$ produz mapa binário de mudança. Simples, sensível a iluminação, fenologia e calibração radiométrica. O exercício `ex09_2.py` simula mudança em **uma** imagem (altera uma região) para praticar o fluxo sem segunda data real.

## PCA bitemporal

Empilha (ou forma pares) as bandas das duas datas, centra e faz PCA. Mudança forte tende a aparecer em componentes de menor variância ou em eixos específicos — depende do desenho. Intuição: direção de máxima correlação = “não mudou”; desvios ortogonais = candidatos a mudança.

## MAD / iMAD

**MAD** (*Multivariate Alteration Detection*) procura transformações lineares das duas imagens cuja diferença tenha variância máxima sob correlação canônica — diferenças “mais interessantes” que a simples subtração banda a banda.

**iMAD** itera o MAD reponderando pixels (pixels estáveis ganham peso) para estabilizar a estimativa. Referências no repositório:

- `legado/canty/auxil/scripts/iMad.py`, `legado/canty/auxil/scripts/iMad_tf.py`
- `legado/canty/auxil/scripts/iMadmap.py`
- `legado/canty/auxil/eeMad.py` (Earth Engine)

O `ex09_1.py` (do livro) ilustra PCA iterada com EM sobre o 2º PC — caminho didático para a ideia de separar “mudou / não mudou”. Requer duas imagens e o módulo `auxil`.

## Fluxo prático sugerido

1. Garantir co-registro e calibração comparável.
2. Começar com diferença absoluta + limiar (`ex09_2.py`).
3. Evoluir para MAD/iMAD quando houver par multiespectral bem alinhado.
