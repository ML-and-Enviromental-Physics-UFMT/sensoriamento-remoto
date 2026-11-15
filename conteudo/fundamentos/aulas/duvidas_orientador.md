# Dúvidas para o orientador (Cap. 1)

Perguntas em aberto ao fechar o capítulo 1 do Canty (2019). Cada item tem o contexto e o que preciso decidir.

## 1. SVD fica no cap. 1 ou no apêndice A?

O livro trata a PCA pela autodecomposição da covariância. A SVD aparece de forma mais completa no apêndice A. Coloquei uma subseção curta em `00_teoria.md` (seção 4.9) e a verificação em `notebooks/01_pca_propria.ipynb`.

Pergunta: mantenho a SVD aqui como parte do cap. 1 ou movo para o estudo do apêndice A e deixo só uma referência?

## 2. As figuras Sentinel-1 de Cuiabá bastam como ponte?

Hoje a ligação com dado real é só `figuras/cuiaba_sentinel1_2025_VV.png` e `..._VH.png`. São PNGs de visualização, sem georreferência e sem valores físicos. Não dá para calcular covariância nem PCA sobre eles.

Pergunta: isso basta para o cap. 1 ou devo baixar um recorte pequeno de raster (VV e VH em dB) e rodar a PCA de 2 bandas nele?

## 3. Como ligar este capítulo aos dados do mestrado (WWLLN e ERA5)?

WWLLN são eventos pontuais de raios. ERA5 são campos em grade com várias variáveis por célula. A ideia de "pixel como vetor" serve para ERA5 (cada célula com N variáveis) e para WWLLN depois de agregar em grade (contagem por célula e por período).

Pergunta: faz sentido um exercício pequeno de PCA sobre variáveis ERA5 numa grade regional, ou isso fica para o cap. 2 e 3?

## 4. Versionar uma versão reduzida de `aster_pca.tif`?

O comando do `ex01_2.py` grava `figuras/aster_pca.tif`. Pela regra do repositório esse GeoTIFF não é versionado: o `.gitignore` ignora `conteudo/**/figuras/*.tif` ("PNGs are the versioned artifacts"). O README e a seção 6 de `00_teoria.md` já dizem que ele é gerado localmente.

Pergunta: basta manter assim e versionar só um PNG das componentes, ou vale versionar uma versão reduzida do GeoTIFF (recorte ou reamostrada) como referência?
