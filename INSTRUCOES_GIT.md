# 📝 Instruções para Fazer Push na Sua Conta

## Opção 1: Criar Novo Repositório (Recomendado)

1. **Criar repositório no GitHub:**
   - Acesse: https://github.com/new
   - Nome: `trabalho-marcio` ou `dijkstra-marica`
   - Descrição: "Algoritmo de Dijkstra com aplicações práticas"
   - Público ou Privado (sua escolha)
   - **NÃO** marque "Add a README file"
   - Clique em "Create repository"

2. **Configurar remote e fazer push:**
```bash
cd "/home/victor/P2 marcio/trabalho-marcio"

# Remover remote antigo
git remote remove origin

# Adicionar seu repositório (substitua macosta123 pelo seu username se diferente)
git remote add origin https://github.com/macosta123/trabalho-marcio.git

# Ou se preferir usar SSH:
# git remote add origin git@github.com:macosta123/trabalho-marcio.git

# Fazer push
git push -u origin master
```

## Opção 2: Fazer Fork do Repositório Original

1. **Fazer fork:**
   - Acesse: https://github.com/PacEvill/trabalho-marcio
   - Clique em "Fork" (canto superior direito)
   - Isso criará uma cópia na sua conta

2. **Configurar remote:**
```bash
cd "/home/victor/P2 marcio/trabalho-marcio"

# Remover remote antigo
git remote remove origin

# Adicionar seu fork
git remote add origin https://github.com/macosta123/trabalho-marcio.git

# Fazer push
git push -u origin master
```

## Autenticação

Se pedir credenciais, você pode usar:

1. **Personal Access Token (Recomendado):**
   - Vá em: https://github.com/settings/tokens
   - "Generate new token" → "Generate new token (classic)"
   - Dê um nome e selecione escopo `repo`
   - Copie o token e use como senha quando pedir

2. **Ou configurar SSH:**
```bash
# Gerar chave SSH (se ainda não tiver)
ssh-keygen -t ed25519 -C "victormacosta11@gmail.com"

# Adicionar ao ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar chave pública
cat ~/.ssh/id_ed25519.pub

# Adicionar em: https://github.com/settings/keys
```

## Verificar Configuração

```bash
# Ver remote configurado
git remote -v

# Ver usuário configurado
git config user.name
git config user.email
```

