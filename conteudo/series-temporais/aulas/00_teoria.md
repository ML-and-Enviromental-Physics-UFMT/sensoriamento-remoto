# Cap. 9 — Detecção de mudança

> Referência: Canty, M. J. (2019). *Image Analysis, Classification and Change Detection in Remote Sensing*, Cap. 9.  
> Stub curto: [`deteccao_de_mudanca.md`](deteccao_de_mudanca.md). Álgebra / covariância: [Apêndice A](../../matematica/README.md). Agrupamento/EM: [Cap. 8](../../classificacao/agrupamento/aulas/00_teoria.md).

---

## Antes de chamar a diferença de mudança de cobertura

A repetição das observações permite acompanhar a paisagem, mas cada data também registra uma fase da vegetação e uma condição de aquisição. O ciclo de uma cultura agrícola pode produzir grande variação espectral sem conversão permanente do uso do solo.

Imagine um talhão com NDVI hipotético de `0,20`, depois `0,65` e, após a colheita, `0,25`. Subtrair as duas últimas datas revela uma queda. O nome "desmatamento" não decorre dessa conta. Para sustentar uma interpretação, precisamos saber onde, quando e em que condições os valores foram observados.

Antes de aplicar um método do capítulo, registre a pergunta, a época do ano, a compatibilidade dos produtos e a referência de avaliação. Confira o alinhamento e as máscaras. O exemplo simulado do repositório permite estudar o mecanismo; não estima a capacidade de identificar mudanças reais.

Fonte complementar: Moreira e Rudorff, [Agricultura](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_9.pdf), PDF pp. 5–9; Santos, [Uso escolar](http://www.dsr.inpe.br/DSR/educacao/uso-escolar-sensoriamento-remoto/material-didatico-anos-anteriores/arquivos/capitulo_12.pdf), PDF pp. 8–11. Os valores são inventados. O roteiro [Investigar uma mudança](../../fundamentos/aulas/06_investigar_uma_mudanca.md) desenvolve essa entrada antes da matemática.

## 0. Para quem / objetivos

Este texto é para quem já manipula imagens multiespectrais (Caps. 1–3) e quer **comparar duas datas** (ou simular a comparação) de forma honesta: o que é mudança radiométrica/espectral, o que é artefato de registro, e quais caminhos o Canty e este repositório oferecem — da diferença simples ao MAD/iMAD.

Ao terminar, você deve conseguir:

1. Explicar por que **co-registro** é pré-requisito, não detalhe.
2. Aplicar diferença absoluta + limiar e listar fontes típicas de falso alarme.
3. Descrever a intuição da PCA bitemporal (eixo de “não mudou” vs candidatos a mudança).
4. Situar MAD e iMAD como busca de diferenças canonicamente “interessantes”, com iteração que reforça pixels estáveis.
5. Saber quando rodar `ex09_2.py` (uma imagem, simulação) versus `ex09_1.py` (duas datas reais + `auxil`).
6. Mencionar `legado/canty/auxil/eeMad.py` (Earth Engine) como extensão além do fluxo local.

---

## 1. Pré-requisitos

| Tema | Onde | Uso no Cap. 9 |
|------|------|----------------|
| Arrays / bandas | Cap. 1 | $G_1$, $G_2$ como grades ou vetores |
| Média, covariância, PCA | Caps. 2–3; Apêndice A | PCA bitemporal; MAD via correlação canônica |
| EM / misturas | Cap. 8; `em.py` | `ex09_1` itera PCA + EM no 2º PC |
| Calibração / realce | Cap. 5 (ideia) | Datas comparáveis radiometricamente |

Você **não** precisa derivar toda a teoria de correlação canônica na primeira leitura. Precisa da intuição: procurar direções lineares nas duas imagens cuja **diferença** carregue a estrutura de mudança, não só ruído comum.

---

## 2. Intuição

Duas imagens do mesmo lugar, em datas diferentes, quase nunca são “iguais pixel a pixel” mesmo sem mudança de cobertura. Diferenças de iluminação, atmosfera, umidade do solo, fenologia, calibração do sensor e — sobretudo — **desalinhamento geométrico** geram sinal que *parece* mudança.

A detecção de mudança em SR, no espírito do Cap. 9, é o problema de separar:

- **Mudança de interesse** (desmatamento, urbanização, inundação, conversão de uso…), de
- **Variação espúria** (registro, radiometria, sazonalidade “não desejada”).

O método mais simples — subtrair e limiarizar — já ensina o fluxo e os falsos alarmes. Métodos multivariados (PCA bitemporal, MAD/iMAD) tentam concentrar a mudança em poucos componentes ou em variáveis de diferença com propriedades estatísticas melhores do que a subtração banda a banda.

Metáfora útil: co-registro é alinhar duas folhas transparentes; diferença é olhar o que não coincide; MAD é girar os eixos espectrais das duas folhas até a “não coincidência” ficar o mais estruturada possível; iMAD refaz isso dando mais voz aos pixels que parecem estáveis.

---

## 3. Mapa Canty (Cap. 9)

| Bloco (ideia no livro) | Conteúdo | Neste repo |
|------------------------|----------|------------|
| Pré-processamento geométrico | Co-registro / alinhamento | `registerms.py`, `registersar.py` |
| Diferença / razão / limiar | Mudança univariada | `ex09_2.py` |
| PCA / componentes de mudança | Empilhar datas, projetar | `ex09_1.py` (PCA + EM didático) |
| MAD / iMAD | Diferenças via correlação canônica; iteração | `iMad.py`, `iMad_tf.py`, `iMadmap.py` |
| Mapas / limiares / significância | Pós-processamento do sinal de mudança | `iMadmap.py`; limiar no `ex09_2` |
| Extensão GEE | MAD em Earth Engine | `eeMad.py` (além do exercício local) |

O capítulo dialoga com classificação: às vezes a “mudança” é diferença entre mapas de cobertura (pós-classificação); o foco aqui é **detecção espectral/radiométrica direta** sobre o par bitemporal.

---

## 4. Desenvolvimento guiado

### 4.1 Co-registro: necessidade, não opcional

Comparar a data $t_1$ com $t_2$ só faz sentido se o pixel $(i,j)$ nas duas grades corresponde ao **mesmo** local no terreno (dentro da tolerância do pixel / subpixel desejada).

Se houver deslocamento residual de poucos pixels:

- Bordas de estradas, rios e talhões geram franjas de “mudança”.
- Estatísticas de diferença (média, variância, quantis) ficam contaminadas.
- Métodos multivariados **não** corrigem geometria: eles amplificam o que você lhes der.

Produtos ortorretificados / co-registrados de fábrica reduzem o problema, mas não o eliminam. Cheque visualmente (flicker, composição RGB falsa-cor data1/data2) e, se preciso, use ferramentas do repo:

- `legado/canty/auxil/registerms.py` — registro óptico multiespectral;
- `legado/canty/auxil/registersar.py` — fluxo SAR.

**Regra de ouro.** Antes de discutir MAD, pergunte: *as imagens estão alinhadas?* Se a resposta for “não sei”, pare.

### 4.2 Diferença de imagens

Para uma banda (ou índice) nas datas 1 e 2:

$$
D = |G_2 - G_1|
\quad\text{(ou}\quad
G_2 - G_1
\text{ com sinal, se a direção da mudança importar).}
$$

Um mapa binário típico é

```math
C_{ij} = \mathbf{1}\{D_{ij} \ge \tau\}.
```

O limiar $\tau$ pode ser fixo, um percentil (o `ex09_2` usa o percentil 95 de $D$), ou baseado em modelo de ruído. Simplicidade é virtude didática e armadilha operacional:

**Sensível a:** iluminação, atmosfera, fenologia, calibração, umidade, sombra de nuvem, BRDF.  
**Falso alarme típico:** limiar baixo + variação sazonal → “mudança” em quase toda vegetação.  
**Falso negativo típico:** mudança sutil em banda pouco sensível; limiar alto demais.

**Prática sem segunda data.** `exercicios/ex09_2.py` copia a banda 4 (ou a última), altera um retângulo central (multiplicando por $0{,}55$ e adicionando um pouco de ruído estruturado), calcula $|depois-antes|$, limiariza e grava `before` / `after` / `diff` / `threshold` em `figuras/`. É o caminho que **sempre roda** neste repo com o raster sintético do Cap. 1.

Use o `ex09_2` para aprender o painel visual e o vocabulário (antes, depois, diferença, máscara). Não o confunda com validação científica de mudança real.

### 4.3 PCA em par bitemporal

Ideia: formar, para cada pixel, um vetor que combina informação das duas datas — por exemplo duas bandas homologas $(g^{(1)}, g^{(2)})$, ou o empilhamento de todas as bandas de $t_1$ e $t_2$. Centre os dados e faça PCA (autovetores da covariância; ver Apêndice A).

Intuição frequente (caso bivariado $t_1$ vs $t_2$ na mesma banda):

- A **primeira** componente principal alinha-se à direção de máxima variância conjunta — muitas vezes o eixo ao longo do qual as duas datas **co-variam** (pixels que “acompanham” a correlação temporal).
- Componentes de ordem maior, ou projeções ortogonais a esse eixo, concentram desvios: candidatos a mudança ou a ruído.

O desenho exato (quais bandas empilhar, se usar diferença já no input, etc.) muda a interpretação dos PCs. O ponto didático do Canty e do `ex09_1` é: **mudança pode ser isolada em um subespaço** após uma rotação baseada em covariância.

### 4.4 `ex09_1`: PCA iterada + EM no 2º PC

O `exercicios/ex09_1.py` segue o exercício do livro:

1. Lê duas imagens (GDAL), pega uma banda (até a 4ª), forma a matriz $m\times 2$ com as duas datas centradas.
2. Estima covariância (`auxil.Cpm`), obtém autovalores/autovetores, projeta nos PCs.
3. Usa o **2º PC** para separar candidatos “congelados” (estáveis) vs “não congelados” (possível mudança), com limiar ligado a $\sigma$ do 2º autovalor.
4. Roda **EM** (`em.py`) atualizando responsabilidades, reestima covariância **ponderada** pelos pesos da classe “sem mudança”, e itera algumas vezes.

É um caminho **didático** para a ideia “estime a estrutura do que não mudou e isole o resto” — primo conceitual do iMAD, sem ainda ser o MAD completo.

**Requisitos.** Duas imagens alinhadas + GDAL + `auxil` no `sys.path` (o script já aponta para a raiz do repo e `legado/canty/auxil/scripts`). Sem par bitemporal:

```bash
python conteudo/series-temporais/exercicios/ex09_2.py
```

### 4.5 MAD e iMAD — intuição

**MAD** (*Multivariate Alteration Detection*) procura transformações lineares das duas imagens multivariadas $\mathbf{F}$ e $\mathbf{G}$ tais que as **diferenças** das variáveis canônicas tenham propriedades ótimas (no formalismo: ligadas à correlação canônica). Em português de corredor: em vez de subtrair banda 1 de $t_1$ da banda 1 de $t_2$, o método gira os espaços espectrais das duas datas e produz um conjunto de **imagens diferença** ordenadas do “mais interessante / menos correlacionado temporalmente” ao mais redundante.

Por que isso ajuda:

- Mudança que se manifesta em combinação de bandas aparece concentrada.
- Correlação temporal forte (não mudança) é “absorvida” nas variáveis mais correlacionadas; o que sobra nas diferenças MAD carrega anomalia.

**iMAD** (*iteratively reweighted MAD*) itera o procedimento: pixels que parecem estáveis (pequena mudança nas diferenças MAD, sob um modelo) ganham **mais peso** na reestimação; pixels provavelmente mudados perdem influência. Isso estabiliza a estimativa da transformação diante de uma fração de mudança na cena — eco do que o `ex09_1` faz à mão com EM e pesos.

**No repo.**

- `legado/canty/auxil/scripts/iMad.py` — implementação clássica;
- `legado/canty/auxil/scripts/iMad_tf.py` — variante TensorFlow;
- `legado/canty/auxil/scripts/iMadmap.py` — mapas / pós-processamento associados;
- `legado/canty/auxil/eeMad.py` — MAD no Google Earth Engine (ver seção 5).

Fluxo sugerido de maturidade:

1. `ex09_2` — diferença + limiar (simulado).  
2. Par real co-registrado + diferença / PCA (`ex09_1`).  
3. `iMad.py` / `iMadmap.py` no mesmo par.  
4. Opcional: `eeMad.py` se o laboratório usa GEE.

### 4.6 Falsos alarmes e cuidados de interpretação

Checklist rápido antes de confiar no mapa binário:

| Fonte | Sintoma típico | Mitigação |
|-------|----------------|-----------|
| Desregistro | Franjas em bordas lineares | Co-registro; inspeção visual |
| Nuvem / sombra | Manchas brilhantes/escuras “mudança” | Máscara; datas limpas |
| Fenologia | “Mudança” em toda vegetação | Janelas sazonais comparáveis; índices robustos |
| Calibração | Viés global numa data | TOA/SR consistente; normalização relativa |
| Limiar agressivo | Sal e pimenta | Subir $\tau$; filtrar espacialmente com parcimônia |
| Mudança real pequena | Mapa quase vazio | Revisar banda/índice; método multivariado |

Lembre: ausência de detecção também pode ser erro (falso negativo). Validação com pontos de campo ou interpretação em tela fecha o ciclo — o algoritmo só propõe candidatos.

### 4.7 Fluxo de estudo recomendado

1. Ler seções 2–4.1 (intuição + co-registro).  
2. Rodar `ex09_2.py`, abrir o painel em `figuras/`.
3. Variar mentalmente o percentil do limiar: o que sobra?  
4. Ler a seção MAD/iMAD e abrir os cabeçalhos de `iMad.py`.  
5. Se tiver duas datas: `ex09_1.py t1.tif t2.tif` e comparar com diferença simples.  
6. Anotar três falsos alarmes imagináveis na sua área de estudo.

---

## 5. Além do livro

- **Google Earth Engine — `legado/canty/auxil/eeMad.py`:** leva a lógica MAD para coleções massivas na nuvem. Útil quando o par (ou a série) não cabe no fluxo local GDAL do exercício. Trate como *além do livro / além do `ex09_*`*: mesma família estatística, outra plataforma.
- **Séries temporais densas** (BFAST, LandTrendr, CCDC, etc.): mudança como ruptura em trajetória, não só par $t_1,t_2$.
- **Deep change detection / siamese nets:** aprendem similaridade entre datas; exigem rótulos ou pares bem curados.
- **Pós-classificação:** classifique cada data (Caps. 6–8) e compare mapas — erros de classificação viram “mudança” falsa; combine com métodos espectrais quando possível.
- **SAR:** coerência, razão de intensidades, sequências Wishart (`eeWishart`, scripts SAR) — outro regime de ruído e geometria; o Cap. 9 óptico não se traduz 1:1.

Para a disciplina deste repo, o núcleo avaliável é: co-registro → diferença/`ex09_2` → intuição PCA/EM/`ex09_1` → saber que iMAD e `eeMad` existem.

---

## 6. Prática no repo

| Artefato | Papel |
|----------|--------|
| `exercicios/ex09_2.py` | Simulação com **uma** imagem; sempre executável |
| `exercicios/ex09_1.py` | Exercício do livro; **duas** datas + GDAL + `em` |
| `legado/canty/auxil/scripts/iMad.py`, `iMad_tf.py` | MAD / iMAD |
| `legado/canty/auxil/scripts/iMadmap.py` | Mapas associados |
| `legado/canty/auxil/eeMad.py` | MAD em Earth Engine |
| `legado/canty/auxil/registerms.py`, `registersar.py` | Co-registro |
| `legado/canty/auxil/scripts/em.py` | EM usado no `ex09_1` |
| `figuras/` | PNGs do `ex09_2` |

```bash
# caminho sem segundo arquivo temporal
python conteudo/series-temporais/exercicios/ex09_2.py

# com par bitemporal
python conteudo/series-temporais/exercicios/ex09_1.py caminho/t1.tif caminho/t2.tif
```

---

## 7. Checklist + dúvidas

**Checklist**

- [ ] Explico por que desalinhamento vira falso alarme de mudança.
- [ ] Sei formular $D=|G_2-G_1|$ e o papel do limiar $\tau$.
- [ ] Diferencio o que `ex09_2` ensina (fluxo) do que ele *não* valida (mudança real).
- [ ] Descrevo a intuição da PCA bitemporal e o papel do 2º PC no `ex09_1`.
- [ ] Situo MAD/iMAD em uma frase cada e aponto os scripts `auxil`.
- [ ] Menciono `eeMad.py` como extensão GEE, não como pré-requisito do exercício local.
- [ ] Listo pelo menos três fontes de falso alarme além do registro.

**Dúvidas para levar ao PDF / ao grupo**

1. Na sua área, qual janela fenológica torna $t_1$ e $t_2$ comparáveis?
2. Depois do iMAD, como você limiarizaria as componentes de diferença (quantil, teste qui-quadrado do livro, inspeção)?
3. Se a mudança for <5% da cena, o que acontece com estimativas não ponderadas vs iMAD?
4. Diferença pós-classificação vs MAD: quando cada uma falha?

Com essas respostas esboçadas, o Cap. 9 deixa de ser “subtrair imagens” e passa a ser um protocolo: **alinhar, comparar com método adequado, desconfiar do mapa, validar**.
