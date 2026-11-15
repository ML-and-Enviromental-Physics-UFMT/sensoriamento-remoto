# Ponte: treinamento de redes e Caps. 6–7

> Stub. Manual didático completo: [`00_teoria.md`](00_teoria.md).  
> O Apêndice B do Canty cobre o **como treinar** redes (função de custo, gradientes, backprop, variantes). Os Caps. 6–7 cobrem o **papel** das redes na classificação de imagens.

## Ligação prática

| Capítulo | Foco | Onde a rede entra |
|----------|------|-------------------|
| Cap. 6 | Bayes / ML gaussiano | Baseline paramétrico; rede como alternativa sem hipótese gaussiana |
| Cap. 7 | SVM, boosting, redes, avaliação | Treino, arquitetura rasa/MLP, comparação de acurácia/kappa/McNemar |
| Apêndice B | Otimização do treino | Evitar overfit, convergência, regularização |

## No repositório

- Classificadores do livro (incl. redes): `legado/canty/auxil/supervisedclass.py`, `legado/canty/auxil/scripts/classify.py`.
- Neste estudo, Caps. 6–7 usam sklearn (GaussianNB, QDA, RF, SVM) para o fluxo didático; redes profundas ficam como leitura do apêndice + `classify.py -a 3..6`.

Consulte o PDF `Appendix_B_Neural_Network_Training.pdf` e [`00_teoria.md`](00_teoria.md) quando for reproduzir o treino do livro passo a passo.
