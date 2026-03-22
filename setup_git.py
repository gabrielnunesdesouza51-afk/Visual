#!/usr/bin/env python
"""
Script de Configuração Inicial do Git
Configura automaticamente o Git e os scripts de automação
"""
import os
import subprocess
import sys
from pathlib import Path

class SetupGit:
    """Classe para configurar Git automaticamente"""
    
    def __init__(self):
        self.nome_usuario = None
        self.email_usuario = None
        
    def executar_comando(self, comando):
        """Executa comando no terminal"""
        try:
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                shell=True
            )
            return resultado.returncode == 0, resultado.stdout.strip()
        except Exception as e:
            return False, str(e)
    
    def obter_input_usuario(self, pergunta, default=""):
        """Obtém input do usuário com valor padrão"""
        if default:
            prompt = f"{pergunta} [{default}]: "
        else:
            prompt = f"{pergunta}: "
        
        resposta = input(prompt).strip()
        return resposta if resposta else default
    
    def verificar_git_instalado(self):
        """Verifica se Git está instalado"""
        sucesso, _ = self.executar_comando("git --version")
        return sucesso
    
    def obter_config_git(self):
        """Obtém configuração atual do Git"""
        _, nome = self.executar_comando("git config --global user.name")
        _, email = self.executar_comando("git config --global user.email")
        return nome, email
    
    def configurar_usuario_git(self):
        """Configura nome e email do Git"""
        nome_atual, email_atual = self.obter_config_git()
        
        print("\n" + "="*60)
        print("⚙️  CONFIGURAÇÃO DO GIT")
        print("="*60)
        
        if nome_atual:
            print(f"\n✅ Nome atual: {nome_atual}")
            mudar = input("Deseja alterar? (s/n): ").lower()
            if mudar != 's':
                self.nome_usuario = nome_atual
            else:
                self.nome_usuario = self.obter_input_usuario("Nome do usuário")
        else:
            self.nome_usuario = self.obter_input_usuario("Nome do usuário")
        
        if email_atual:
            print(f"✅ Email atual: {email_atual}")
            mudar = input("Deseja alterar? (s/n): ").lower()
            if mudar != 's':
                self.email_usuario = email_atual
            else:
                self.email_usuario = self.obter_input_usuario("Email do GitHub")
        else:
            self.email_usuario = self.obter_input_usuario("Email do GitHub")
        
        # Configurar
        print("\n📝 Configurando Git...")
        self.executar_comando(f'git config --global user.name "{self.nome_usuario}"')
        self.executar_comando(f'git config --global user.email "{self.email_usuario}"')
        
        print(f"✅ Git configurado com sucesso!")
    
    def verificar_repositorio_remoto(self):
        """Verifica se repositório remoto está configurado"""
        _, saida = self.executar_comando("git remote -v")
        return "origin" in saida if saida else False
    
    def configurar_repositorio_remoto(self):
        """Configura repositório remoto"""
        print("\n" + "="*60)
        print("🔗 REPOSITÓRIO REMOTO")
        print("="*60)
        
        if self.verificar_repositorio_remoto():
            print("\n✅ Repositório remoto já configurado")
            _, saida = self.executar_comando("git remote -v")
            print(saida)
            return
        
        print("\n⚠️  Repositório remoto não configurado")
        
        url_repo = self.obter_input_usuario(
            "URL do repositório remoto (ex: https://github.com/usuario/repo.git)"
        )
        
        if url_repo:
            print("\n📝 Configurando repositório remoto...")
            sucesso, _ = self.executar_comando(f"git remote add origin {url_repo}")
            
            if sucesso:
                print("✅ Repositório remoto configurado!")
            else:
                print("⚠️  Não foi possível configurar repositório remoto")
    
    def configurar_powershell(self):
        """Configura aliases no PowerShell"""
        print("\n" + "="*60)
        print("🔧 CONFIGURAÇÃO DO POWERSHELL")
        print("="*60)
        
        resposta = input("\nDeseja configurar atalhos no PowerShell? (s/n): ").lower()
        if resposta != 's':
            return
        
        # Criar alias global
        print("\n📝 Configurando PowerShell...")
        
        # Adicionar ao profile
        profile_path = Path(os.path.expandvars(r"%USERPROFILE%\Documents\PowerShell\profile.ps1"))
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Verificar se já existe
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                conteudo = f.read()
            
            if 'Set-Alias -Name c' in conteudo or 'Set-Alias -Name cpush' in conteudo:
                print("✅ Aliases já configurados no PowerShell")
                return
        
        # Adicionar aliases
        aliases_code = '''
# Aliases para automação Git
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Alias -Name c -Value {& "$scriptPath\\commit.ps1"} -Scope Global -Force
Set-Alias -Name cpush -Value {& "$scriptPath\\commit.ps1" -Mensagem "Atualização automática"} -Scope Global -Force
Set-Alias -Name gs -Value {git status} -Scope Global -Force
Set-Alias -Name gl -Value {git log --oneline -10} -Scope Global -Force
'''
        
        try:
            with open(profile_path, 'a') as f:
                f.write(aliases_code)
            print(f"✅ Aliases configurados em: {profile_path}")
            print("   Feche e reabra o PowerShell para usar os aliases")
        except Exception as e:
            print(f"⚠️  Erro ao configurar aliases: {e}")
    
    def criar_arquivo_gitignore(self):
        """Cria arquivo .gitignore se não existir"""
        gitignore_path = Path(".gitignore")
        
        if gitignore_path.exists():
            print("\n✅ .gitignore já existe")
            return
        
        gitignore_content = """# Arquivos Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Dados locais
receitas.json
*.db
*.sqlite

# Logs
*.log
logs/

# Testes
.pytest_cache/
.coverage
htmlcov/

# Temporários
temp/
tmp/
lista_compras_*.txt
"""
        
        try:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print("\n✅ Arquivo .gitignore criado")
        except Exception as e:
            print(f"\n⚠️  Erro ao criar .gitignore: {e}")
    
    def executar_setup_completo(self):
        """Executa setup completo"""
        print("\n" + "="*60)
        print("🚀 SETUP INICIAL - AUTOMAÇÃO GIT")
        print("="*60)
        print("\nEste script irá configurar seu ambiente Git\n")
        
        # Verificar Git
        print("📦 Verificando Git...")
        if not self.verificar_git_instalado():
            print("❌ Git não está instalado!")
            print("   Baixe em: https://git-scm.com/download/win")
            return False
        print("✅ Git instalado e disponível")
        
        # Configurar usuário
        self.configurar_usuario_git()
        
        # Configurar remoto
        self.configurar_repositorio_remoto()
        
        # Criar .gitignore
        self.criar_arquivo_gitignore()
        
        # Configurar PowerShell
        self.configurar_powershell()
        
        # Status final
        print("\n" + "="*60)
        print("✅ CONFIGURAÇÃO INICIAL CONCLUÍDA!")
        print("="*60)
        print("\n📚 Próximos passos:")
        print("   1. Use: .\\commit.ps1 para fazer commit automático")
        print("   2. Ou use alias 'c' se configurou PowerShell")
        print("   3. Veja: QUICK_START.md para mais informações")
        print("   4. Veja: README_AUTOMACAO.md para documentação completa")
        print("\n")
        
        return True


def main():
    """Função principal"""
    setup = SetupGit()
    sucesso = setup.executar_setup_completo()
    
    if not sucesso:
        sys.exit(1)


if __name__ == "__main__":
    main()
