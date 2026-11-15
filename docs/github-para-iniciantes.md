# Guia Prático: GitHub, Pull Requests e Colaboração

## Introdução
Este guia foi criado a partir de uma conversa sobre como usar o GitHub para colaboração em projetos. É ideal para iniciantes que querem entender os conceitos básicos de fork, branch, commit e pull request.

## 1. Conceitos Fundamentais

### O que é um Fork?
Um fork é uma cópia completa de um repositório que você cria na sua própria conta do GitHub. É usado quando:
- Você não tem permissão direta de escrita no projeto original
- Quer testar alterações sem impactar o repositório original
- Deseja propor melhorias para projetos de terceiros

**Vantagens do fork:**
- Protege o repositório original de modificações não autorizadas
- Facilita testes e experimentos
- Permite escalar a colaboração com controle

### O que é uma Branch?
Uma branch é como uma "ramificação" do código principal onde você pode trabalhar isoladamente. É recomendado criar uma nova branch para cada alteração ou feature.

**Por que usar branches?**
- Evita conflitos na branch principal ("main" ou "master")
- Mantém o histórico organizado
- Facilita a revisão de código
- É uma boa prática em projetos colaborativos

## 2. Fluxo Básico de Trabalho

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### Passo 2: Crie uma Nova Branch
```bash
git checkout -b nome-da-sua-branch
```
*Exemplo: `git checkout -b ajuste-readme`*

### Passo 3: Faça as Alterações
- Edite os arquivos necessários no VSCode ou editor de sua preferência
- Salve as mudanças

### Passo 4: Adicione e Faça Commit das Alterações
```bash
git add .
git commit -m "Descrição clara do que foi alterado"
```

### Passo 5: Envie a Branch para o GitHub
```bash
git push origin nome-da-sua-branch
```

### Passo 6: Crie um Pull Request
1. Acesse seu repositório no GitHub
2. Clique em "Pull requests"
3. Clique em "New pull request"
4. Selecione sua branch em "compare" e a branch principal em "base"
5. Adicione título e descrição
6. Clique em "Create pull request"

## 3. Editando Arquivos Diretamente no GitHub

### Método Simples (pelo navegador)
1. Acesse o arquivo no seu repositório
2. Clique no ícone de lápis ("Edit this file")
3. Faça a edição desejada
4. Role até o final da página
5. Escreva uma mensagem de commit
6. Marque "Create a new branch for this commit and start a pull request"
7. Clique em "Propose changes"

## 4. Verificando e Gerenciando Branches

### Ver todas as branches locais
```bash
git branch
```
*A branch atual aparece com asterisco (*)*

### Ver branches remotas
```bash
git branch -r
```

### No VSCode
- Use a aba de controle de código-fonte (ícone de ramo/branch)
- Clique no nome da branch atual para ver todas as disponíveis
- Use o terminal integrado (Ctrl + `) para comandos git

## 5. Após o Merge do Pull Request

### O que acontece?
- Suas alterações são incorporadas à branch principal
- A branch continua existindo até ser excluída manualmente
- No GitHub, aparece a opção "Delete branch" após o merge

### Limpeza de Branches

#### Excluir pelo GitHub
- Clique em "Delete branch" na página do PR após o merge
- Ou vá em "Branches" no repositório e delete manualmente

#### Excluir localmente (VSCode/terminal)
```bash
# Se a branch foi mesclada
git branch -d nome-da-branch

# Para forçar a exclusão (se não foi mesclada)
git branch -D nome-da-branch

# Excluir branch remota
git push origin --delete nome-da-branch
```

### Quando o git informa que o branch não está totalmente mesclado
- Pode acontecer se o merge foi feito no repositório remoto (GitHub), mas seu repositório local não está atualizado
- Atualize a branch principal local e remota:
  ```bash
  git checkout main
  git pull origin main
  ```
- Se ainda assim quiser excluir mesmo com aviso de merge incompleto, use o comando de força:
  ```bash
  git branch -D nome-da-branch
  ```

## 6. Boas Práticas

### Nomes de Branch
- Use nomes descritivos: `feature-login`, `fix-bug-header`, `ajuste-readme`
- Evite espaços e caracteres especiais
- Use hífens para separar palavras

### Mensagens de Commit
- Seja claro e específico sobre o que foi alterado
- Use verbos no imperativo: "Adiciona", "Corrige", "Remove"
- Exemplo: "Adiciona validação de email no formulário de login"

### Organização
- Crie uma branch para cada alteração ou feature
- Delete branches antigas após o merge
- Mantenha a branch principal sempre limpa e funcional

## 7. Comandos de Referência Rápida

```bash
# Clonar repositório
git clone [url-do-repo]

# Criar e trocar para nova branch
git checkout -b nome-da-branch

# Ver status das alterações
git status

# Adicionar arquivos para commit
git add .

# Fazer commit
git commit -m "Mensagem do commit"

# Enviar para GitHub
git push origin nome-da-branch

# Ver branches locais
git branch

# Deletar branch local
git branch -d nome-da-branch

# Trocar de branch
git checkout nome-da-branch
```

## 8. Troubleshooting Comum

### Branch ainda aparece no VSCode após merge
- É normal! O branch continua localmente até ser excluído manualmente
- Use `git branch -d nome-da-branch` para remover

### Não consigo fazer push
- Verifique se fez commit das alterações: `git status`
- Certifique-se de estar na branch correta: `git branch`

### Esqueci em qual branch estou
- Use `git branch` - a atual aparece com asterisco (*)

### Erro ao tentar deletar branch: "used by worktree"
- Esse erro ocorre se você estiver tentando deletar o branch que está ativo no momento
- Troque para outro branch, como "main":
  ```bash
  git checkout main
  ```
- Depois tente deletar o branch novamente

### Erro ao deletar branch não totalmente mesclado
- O git pode avisar que o branch não está totalmente mesclado, mesmo depois do merge no remoto
- Atualize sua branch principal localmente
- Use `git branch -D nome-da-branch` para forçar a exclusão se tiver certeza de que suas alterações foram mescladas

## 9. Fluxo para Testar Colaboração

### Para testar se colaboradores conseguem contribuir:
1. Crie uma segunda conta no GitHub
2. Faça fork do seu repositório com a segunda conta
3. Clone o fork e faça alterações
4. Crie um PR da segunda conta para a primeira
5. Teste se tudo funciona corretamente

Este método ajuda a identificar problemas de permissão ou arquivos que podem estar causando dificuldades para colaboradores.

---

## Conclusão
Este guia cobre o fluxo básico de trabalho com GitHub, desde conceitos fundamentais até práticas avançadas. Lembre-se: a prática leva à perfeição. Comece com projetos pequenos e vá evoluindo gradualmente para workflows mais complexos.

**Dica final:** Sempre teste suas alterações localmente antes de fazer push, e mantenha seus commits organizados e descritivos para facilitar a colaboração com outros desenvolvedores.
