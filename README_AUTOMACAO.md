# 🤖 Automação de Commit e Push

Este diretório contém scripts para automatizar o processo de commit e push do seu projeto Python no GitHub.

## 📋 Arquivos de Automação

### 1. **auto_commit.py** (Python)
Script baseado em Python que automatiza o processo completo.

#### Uso:
```bash
# Com mensagem padrão ("Atualização de receitas")
python auto_commit.py

# Com mensagem personalizada
python auto_commit.py -m "Nova feature de busca"

# Em branch diferente
python auto_commit.py -b develop

# Combinando opções
python auto_commit.py -m "Fix bug" -b develop

# Em repositório diferente
python auto_commit.py -p "C:\outro\caminho"
```

#### Ajuda:
```bash
python auto_commit.py --help
```

### 2. **commit.ps1** (PowerShell)
Script para PowerShell com interface colorida e amigável.

#### Uso:
```powershell
# Com mensagem padrão
.\commit.ps1

# Com mensagem personalizada
.\commit.ps1 -Mensagem "Atualização de features"

# Em branch diferente
.\commit.ps1 -Branch "develop"

# Combinando opções
.\commit.ps1 -Mensagem "Fix crítico" -Branch "hotfix"
```

#### Execução Rápida (VS Code):
1. Abra o terminal integrado (Ctrl + `)
2. Digite: `.\commit.ps1`
3. Ou personalize:
   ```powershell
   .\commit.ps1 -Mensagem "Descrição do commit"
   ```

### 3. **setup_aliases.ps1** (PowerShell Aliases)
Cria atalhos para execução rápida.

#### Instalação:
```powershell
# Executar uma vez para configurar
.\setup_aliases.ps1
```

#### Usando os Aliases:
```powershell
# Commit automático com mensagem padrão
c

# Commit com mensagem personalizada
c "Descrição do commit"

# Push rápido
cpush "Descrição"

# Status do git
gs

# Log do git
gl

# Log com 20 últimos commits
gl -Linhas 20
```

---

## 🚀 Fluxo de Trabalho Recomendado

### Opção 1: Usando Python (Multiplataforma)
```bash
# Ao final da sessão
python auto_commit.py -m "Features implementadas"
```

### Opção 2: Usando PowerShell (Windows)
```powershell
# Ao final da sessão
.\commit.ps1 -Mensagem "Features implementadas"
```

### Opção 3: Usando Aliases (Mais Rápido)
```powershell
# Uma única letra!
cpush "Features implementadas"
```

---

## 📝 Etapas Automatizadas

Ambos os scripts executam automaticamente:

1. ✅ **Inicializar Git** (se necessário)
   - Verifica se o repositório está inicializado
   - Inicializa automaticamente se não estiver

2. ✅ **Detectar Alterações**
   - Lista arquivos modificados/novos
   - Mostra o status antes do commit

3. ✅ **Adicionar Arquivos**
   - Executa `git add -A`
   - Prepara todos os arquivos para commit

4. ✅ **Fazer Commit**
   - Commit com mensagem clara
   - Mostra resultado

5. ✅ **Fazer Push**
   - Envia ao branch remoto
   - Trata erros de conexão

6. ✅ **Exibir Status Final**
   - Status do repositório
   - Últimos 5 commits

---

## 🔧 Personalizações

### Alterar Mensagem Padrão

**Python (auto_commit.py):**
```python
# Linha ~15
self.commit_message_default = "Sua mensagem padrão"
```

**PowerShell (commit.ps1):**
```powershell
# Linha 6
$Mensagem = "Sua mensagem padrão"
```

### Alterar Branch Padrão

**Python:**
```python
# Na função fazer_push()
def fazer_push(self, branch="seu_branch"):
```

**PowerShell:**
```powershell
# Linha 7
$Branch = "seu_branch"
```

---

## 🎯 Exemplos Práticos

### Exemplo 1: Commit com Timestamp
```bash
python auto_commit.py -m "Atualização $(Get-Date -Format 'dd/MM HH:mm')"
```

### Exemplo 2: Commit em Blog de Produção
```powershell
.\commit.ps1 -Mensagem "Deploy production" -Branch "main"
```

### Exemplo 3: Commit de Hotfix
```powershell
cpush "Hotfix: Corrigido erro crítico"
```

---

## ⚠️ Requisitos

- **Git** instalado e configurado
- **Credenciais Git** configuradas (token, SSH key, ou credenciais globais)
- **Acesso ao repositório remoto**

### Verificar Configuração:
```bash
git config --global user.name
git config --global user.email
git remote -v
```

### Configurar Git (se necessário):
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
git remote add origin https://github.com/seu_usuario/seu_repo.git
```

---

## 🐛 Troubleshooting

### Erro: "fatal: destination path"
- Verifique configuração do repositório remoto
- Execute: `git remote -v`

### Erro: "Authentication failed"
- Atualize credenciais do Git
- Use SSH key ou token de acesso pessoal
- Verifique permissões no repositório

### Script não executa
```powershell
# PowerShell: erro de execução
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Nenhuma mudança para commit
- Normal! Significa que não há arquivos novos/modificados
- Use `git status` para verificar

---

## 📊 Comparação dos Scripts

| Feature | Python | PowerShell |
|---------|--------|-----------|
| Multiplataforma | ✅ | Windows |
| Cores/Ícones | ✅ | ✅✅ |
| Sem dependências | ✅ | ✅ |
| Argumentos | ✅ | ✅ |
| Válido em VS Code | ✅ | ✅ |

---

## 🎓 Integração com VS Code

### Adicionar Tarefa ao tasks.json
```json
{
  "label": "Git: Commit e Push",
  "type": "shell",
  "command": "${workspaceFolder}/commit.ps1",
  "group": {
    "kind": "build",
    "isDefault": false
  },
  "presentation": {
    "reveal": "always",
    "panel": "new"
  }
}
```

Depois, execute com `Ctrl+Shift+B` → Selecionar tarefa

---

## 💡 Dicas

1. **Atalho Rápido**: Use `cpush` para commit + push em uma linha
2. **Automação**: Agende com Windows Task Scheduler
3. **CI/CD**: Integre com GitHub Actions
4. **Aliases**: Configure aliases no seu PowerShell profile
5. **Log**: Revise histórico com `gl` antes de push

---

## 📚 Recursos Adicionais

- [Documentação Git](https://git-scm.com/doc)
- [GitHub Help](https://docs.github.com)
- [PowerShell Scripting](https://learn.microsoft.com/en-us/powershell/)

---

**Desenvolvido para automatizar seu workflow! 🚀**
