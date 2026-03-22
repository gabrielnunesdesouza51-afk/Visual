#!/usr/bin/env python
"""
Script de Automação para Commit e Push no GitHub
Automatiza o processo de adicionar, fazer commit e push do projeto
"""
import os
import subprocess
import sys
from datetime import datetime

class AutoCommitGit:
    """Classe para automatizar commit e push no Git"""
    
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.commit_message_default = "Atualização de receitas"
        
    def executar_comando(self, comando, mostrar_erro=True):
        """
        Executa um comando no terminal
        
        Args:
            comando: Comando a executar
            mostrar_erro: Se deve mostrar erros
            
        Returns:
            tuple: (sucesso, output)
        """
        try:
            resultado = subprocess.run(
                comando,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                shell=True
            )
            
            if resultado.returncode != 0 and mostrar_erro:
                print(f"⚠️  Erro ao executar: {comando}")
                print(f"   {resultado.stderr}")
                return False, resultado.stderr
            
            return True, resultado.stdout.strip()
        except Exception as e:
            if mostrar_erro:
                print(f"❌ Exceção: {e}")
            return False, str(e)
    
    def verificar_git_inicializado(self):
        """Verifica se o repositório Git está inicializado"""
        sucesso, _ = self.executar_comando("git status", mostrar_erro=False)
        return sucesso
    
    def inicializar_git(self):
        """Inicializa um novo repositório Git se necessário"""
        if not self.verificar_git_inicializado():
            print("📁 Inicializando repositório Git...")
            sucesso, _ = self.executar_comando("git init")
            if sucesso:
                print("✅ Repositório inicializado")
                return True
            else:
                print("❌ Falha ao inicializar repositório")
                return False
        else:
            print("✅ Repositório Git já inicializado")
            return True
    
    def verificar_arquivos_pendentes(self):
        """Verifica se há arquivos não rastreados ou modificados"""
        sucesso, output = self.executar_comando("git status --porcelain", mostrar_erro=False)
        
        if sucesso and output:
            print(f"\n📝 Arquivos pendentes:")
            for linha in output.split('\n'):
                if linha.strip():
                    print(f"   {linha}")
            return True
        return False
    
    def adicionar_arquivos(self):
        """Adiciona todos os arquivos ao staging area"""
        print("\n📦 Adicionando arquivos ao Git...")
        sucesso, output = self.executar_comando("git add -A")
        
        if sucesso:
            print("✅ Arquivos adicionados com sucesso")
            return True
        else:
            print("❌ Falha ao adicionar arquivos")
            return False
    
    def fazer_commit(self, mensagem=None):
        """
        Faz commit dos arquivos
        
        Args:
            mensagem: Mensagem do commit (usa padrão se não fornecer)
        """
        if not mensagem:
            mensagem = self.commit_message_default
        
        print(f"\n💾 Fazendo commit com mensagem: '{mensagem}'")
        
        comando_commit = f'git commit -m "{mensagem}"'
        sucesso, output = self.executar_comando(comando_commit)
        
        if sucesso:
            print("✅ Commit realizado com sucesso")
            if output:
                print(f"   {output}")
            return True
        else:
            # Pode falhar se não há mudanças
            if "nothing to commit" in output or "nothing added to commit" in output:
                print("ℹ️  Nenhuma mudança para fazer commit")
                return True
            print("❌ Falha ao fazer commit")
            return False
    
    def fazer_push(self, branch="main"):
        """
        Faz push para o repositório remoto
        
        Args:
            branch: Branch para fazer push (padrão: main)
        """
        print(f"\n🚀 Fazendo push para o branch '{branch}'...")
        
        comando_push = f"git push origin {branch}"
        sucesso, output = self.executar_comando(comando_push)
        
        if sucesso:
            print(f"✅ Push realizado com sucesso")
            if output:
                print(f"   {output}")
            return True
        else:
            # Tenta detectar o erro
            if "no changes added to commit" in output:
                print("ℹ️  Nenhuma mudança para fazer push")
                return True
            elif "fatal: destination path" in output or "Connection refused" in output:
                print("⚠️  Não foi possível conectar ao repositório remoto")
                print("   Verifique a conexão de internet ou configuração do Git")
                return False
            else:
                print(f"❌ Falha ao fazer push: {output}")
                return False
    
    def exibir_status_final(self):
        """Exibe o status final do repositório"""
        print("\n" + "="*60)
        print("📊 STATUS FINAL DO REPOSITÓRIO")
        print("="*60)
        
        sucesso, output = self.executar_comando("git status", mostrar_erro=False)
        if sucesso:
            print(output)
        
        print("\n📜 ÚLTIMOS COMMITS:")
        sucesso, output = self.executar_comando("git log --oneline -5", mostrar_erro=False)
        if sucesso:
            print(output)
    
    def processar_completo(self, mensagem_commit=None):
        """
        Executa o processo completo de commit e push
        
        Args:
            mensagem_commit: Mensagem personalizada para o commit
        """
        print("\n" + "="*60)
        print("🔄 AUTOMATIZAÇÃO DE COMMIT E PUSH")
        print("="*60)
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
        # Etapa 1: Inicializar Git se necessário
        if not self.inicializar_git():
            print("❌ Não foi possível inicializar o repositório")
            return False
        
        # Etapa 2: Verificar arquivos pendentes
        if not self.verificar_arquivos_pendentes():
            print("ℹ️  Nenhum arquivo pendente para commit")
            self.exibir_status_final()
            return True
        
        # Etapa 3: Adicionar arquivos
        if not self.adicionar_arquivos():
            print("❌ Não foi possível adicionar arquivos")
            return False
        
        # Etapa 4: Fazer commit
        if not self.fazer_commit(mensagem_commit):
            print("❌ Não foi possível fazer commit")
            return False
        
        # Etapa 5: Fazer push
        if not self.fazer_push():
            print("⚠️  Não foi possível fazer push, mas commit foi realizado localmente")
        
        # Exibir status final
        self.exibir_status_final()
        
        print("\n" + "="*60)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("="*60 + "\n")
        
        return True


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automatiza commit e push no GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python auto_commit.py                           # Usa mensagem padrão
  python auto_commit.py -m "Nova feature"         # Mensagem personalizada
  python auto_commit.py -b develop                # Push em branch diferente
  python auto_commit.py -m "Fix bug" -b develop   # Ambas as opções
        """
    )
    
    parser.add_argument(
        "-m", "--mensagem",
        type=str,
        help="Mensagem personalizada do commit",
        default=None
    )
    
    parser.add_argument(
        "-b", "--branch",
        type=str,
        help="Branch para fazer push (padrão: main)",
        default="main"
    )
    
    parser.add_argument(
        "-p", "--path",
        type=str,
        help="Caminho do repositório (padrão: diretório atual)",
        default="."
    )
    
    args = parser.parse_args()
    
    # Criar instância e executar
    auto_commit = AutoCommitGit(repo_path=args.path)
    sucesso = auto_commit.processar_completo(mensagem_commit=args.mensagem)
    
    # Retornar código de saída apropriado
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
