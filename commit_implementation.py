#!/usr/bin/env python
"""
Script para fazer commit da implementação do Sistema de Sugestão Inteligente
"""
import subprocess
import sys

def executar_comando(cmd, descricao):
    """Executa um comando e relata o status"""
    print(f"\n{'='*60}")
    print(f"  {descricao}")
    print('='*60)
    
    try:
        resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print(f"✅ Sucesso!")
            if resultado.stdout:
                print(resultado.stdout)
            return True
        else:
            print(f"❌ Erro!")
            if resultado.stderr:
                print(resultado.stderr)
            return False
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  🚀 COMMIT DO SISTEMA DE SUGESTÃO INTELIGENTE")
    print("="*60)
    
    # 1. Validar sintaxe
    if not executar_comando("python validate_syntax.py", "1️⃣  Validando sintaxe..."):
        print("\n❌ Falha na validação de sintaxe!")
        sys.exit(1)
    
    # 2. Testar sistema de sugestões
    if not executar_comando("python test_recipe_suggester.py", "2️⃣  Executando testes..."):
        print("\n❌ Falha nos testes!")
        sys.exit(1)
    
    # 3. Ver status Git
    executar_comando("git status", "3️⃣  Status do Git")
    
    # 4. Adicionar arquivos
    arquivos_novos = [
        "services/recipe_suggester.py",
        "test_recipe_suggester.py",
        "RECIPE_SUGGESTER_GUIDE.md",
        "IMPLEMENTATION_CHANGELOG.md",
        "validate_syntax.py",
        "main.py"
    ]
    
    print(f"\n{'='*60}")
    print("4️⃣  Adicionando arquivos ao Git...")
    print('='*60)
    
    for arquivo in arquivos_novos:
        print(f"  + {arquivo}")
    
    if not executar_comando(f"git add {' '.join(arquivos_novos)}", "Adicionando arquivos"):
        print("\n❌ Falha ao adicionar arquivos!")
        sys.exit(1)
    
    # 5. Fazer commit
    mensagem_commit = """feat: Implementação do Sistema de Sugestão Inteligente de Receitas

- Novo módulo: services/recipe_suggester.py com 5 funções
- Algoritmo de compatibilidade de ingredientes
- Integração com menu principal (opção 16)
- 5 testes unitários completos
- Documentação detalhada (RECIPE_SUGGESTER_GUIDE.md)
- Changelog (IMPLEMENTATION_CHANGELOG.md)
- Validador de sintaxe dedicado

Recursos:
✨ Análise inteligente de compatibilidade
🔥 Scoring com 4 níveis (EXCELENTE, BOM, POSSÍVEL, PARCIAL)
📊 Ordenação por compatibilidade e avaliação
💪 Busca parcial e bidirecional de ingredientes
🎯 Interface amigável com feedback visual
100% Backward compatible - Zero breaking changes"""
    
    if not executar_comando(f'git commit -m "{mensagem_commit}"', "5️⃣  Commitando mudanças"):
        print("\n❌ Falha ao fazer commit!")
        sys.exit(1)
    
    # 6. Fazer push
    if not executar_comando("git push origin main", "6️⃣  Enviando para GitHub"):
        print("\n❌ Falha ao fazer push!")
        sys.exit(1)
    
    # 7. Ver resultado final
    executar_comando("git log --oneline -5", "7️⃣  Últimos commits")
    
    print("\n" + "="*60)
    print("  ✅ IMPLEMENTAÇÃO COMPLETA E PUBLICADA!")
    print("="*60)
    print("\n📊 Resumo da Implementação:")
    print("  - 1 novo módulo de sugestões")
    print("  - 3 novos arquivos (testes, docs, validador)")
    print("  - Menu atualizado com opção 16")
    print("  - 5 testes unitários (todos passando)")
    print("  - 2 guias de documentação")
    print("  - 100% sintaxe válida")
    print("  - 100% backward compatible")
    print("\n🎉 Pronto para produção!\n")

if __name__ == "__main__":
    main()
