# 🚀 Guia Rápido - Automação de Commit e Push

## ⚡ Forma Mais Rápida (3 segundos)

```powershell
# Abra o terminal integrado do VS Code (Ctrl + `)
.\commit.ps1
```

**Pronto!** Seu código será commitado e enviado ao GitHub automaticamente.

---

## 📋 3 Maneiras de Usar

### Opção 1️⃣: PowerShell (Recomendado para Windows)
```powershell
# Mensagem padrão
.\commit.ps1

# Com mensagem personalizada
.\commit.ps1 -Mensagem "Meu commit super importante"

# Em outro branch
.\commit.ps1 -Branch "develop"
```

### Opção 2️⃣: Python (Multiplataforma)
```bash
# Mensagem padrão
python auto_commit.py

# Com mensagem personalizada
python auto_commit.py -m "Meu commit"

# Em outro branch
python auto_commit.py -b develop
```

### Opção 3️⃣: Batch (CMD clássico do Windows)
```cmd
REM Duplo clique em commit.bat OU
commit.bat "Sua mensagem aqui"
```

---

## 🎯 Uso em Sessão Típica

1. **Trabalhe no seu código**
   ```
   Edite arquivos, teste, etc...
   ```

2. **Ao finalizar, execute no terminal:**
   ```powershell
   .\commit.ps1 -Mensagem "Feature x implementada"
   ```

3. **Pronto!** ✅ Seu código está no GitHub

---

## ⚙️ Configuração Inicial (Uma Única Vez)

### Se é seu primeiro uso:

```powershell
# 1. Configure seu nome e email no Git
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@github.com"

# 2. Verifique se tudo está certo
git config --global --list

# 3. Pronto! Agora use normalmente
.\commit.ps1
```

---

## 📚 Exemplos Reais

### ✅ Commit após adicionar feature
```powershell
.\commit.ps1 -Mensagem "feat: Adicionado busca por ingrediente"
```

### ✅ Commit após corrigir bug
```powershell
.\commit.ps1 -Mensagem "fix: Corrigido cálculo de calorias"
```

### ✅ Commit com documentação
```powershell
.\commit.ps1 -Mensagem "docs: Atualizado README com exemplos"
```

### ✅ Hotfix urgente
```powershell
.\commit.ps1 -Mensagem "hotfix: Erro crítico em produção" -Branch "main"
```

---

## 🔍 O que Acontece Automaticamente?

O script executa estas etapas na ordem:

```
1. ✅ Verifica se Git está instalado
2. ✅ Inicializa repositório (se necessário)
3. ✅ Mostra arquivos pendentes
4. ✅ Adiciona todos os arquivos (git add -A)
5. ✅ Faz commit com sua mensagem
6. ✅ Faz push para o branch
7. ✅ Mostra status final e últimos commits
```

---

## 💡 Dicas Profissionais

### 1. Crear um Alias Permanente
```powershell
# Adicione isso ao seu perfil PowerShell:
Set-Alias -Name c -Value {.\commit.ps1} -Scope Global

# Depois use:
c "Sua mensagem"
```

### 2. Atalho no VS Code
**View → Command Palette → `>Tasks: Open User Tasks`**

Cole isto:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Git Commit & Push",
      "type": "shell",
      "command": "powershell",
      "args": ["-Command", ".\\commit.ps1"],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

Depois pressione `Ctrl + Shift + B` para executar!

### 3. Integração com Git Hooks (Avançado)
```bash
# Crie arquivo: .git/hooks/post-commit
# e coloque comando para executar seu script
```

---

## 🐛 Problemas Comuns

### ❌ "Permission denied" / "Arquivo bloqueado"
```powershell
# Solução:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ "Git not found"
```bash
# Git não está instalado
# Baixe em: https://git-scm.com/download/win
```

### ❌ "Authentication failed"
```bash
# Configure credenciais:
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@github.com"

# Ou use SSH key (recomendado)
```

### ❌ "fatal: destination path"
```bash
# Repositório remoto não configurado:
git remote add origin https://github.com/seu_usuario/seu_repo.git
```

---

## 📞 Suporte Técnico

### Verificar Configuração Atual
```bash
git config --global --list
git remote -v
```

### Ver Status do Repositório
```bash
git status
git log --oneline -10
```

### Desfazer Último Commit (se necessário)
```bash
git reset --soft HEAD~1
```

---

## 🎓 Próximos Passos

1. ✅ Use `.\commit.ps1` em seu workflow diário
2. ✅ Configure um alias para `c` ou `cpush`
3. ✅ Integre com GitHub Actions para CI/CD
4. ✅ Explore mais opções em [README_AUTOMACAO.md](README_AUTOMACAO.md)

---

## 📝 Chavetas Rápidas

| Comando | Descrição |
|---------|-----------|
| `.\commit.ps1` | Commit com mensagem padrão |
| `.\commit.ps1 -M "msg"` | Commit com mensagem personalizada |
| `git status` | Ver status |
| `git log --oneline -5` | Ver últimos 5 commits |
| `git diff` | Ver mudanças |

---

**Que fácil é agora! 🎉** Seu workflow ficou 10x mais rápido!

Para mais detalhes, veja [README_AUTOMACAO.md](README_AUTOMACAO.md)
