"""
Script de teste para demonstrar as receitas importadas
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.storage import carregar_receitas

def main():
    print("\n" + "="*80)
    print("🍳 RECEITAS IMPORTADAS - TESTE DE VISUALIZAÇÃO")
    print("="*80)
    
    receitas = carregar_receitas()
    
    if not receitas:
        print("\n❌ Nenhuma receita encontrada!")
        print("Execute 'python import_receitas.py' primeiro para importar.")
        return
    
    print(f"\n✅ Total de receitas carregadas: {len(receitas)}\n")
    
    # Cabeçalho da tabela
    print(f"{'ID':<4} | {'NOME':<35} | {'CATEGORIA':<15} | {'TEMPO':<8} | {'PORCÕES'}")
    print("-" * 80)
    
    # Linhas da tabela
    for receita in receitas:
        print(f"{receita.id:<4} | {receita.nome:<35} | {receita.categoria:<15} | {receita.tempo_preparo:>6}min | {receita.porcoes}")
    
    print("\n" + "="*80)
    
    # Estatísticas
    tempo_total = sum(r.tempo_preparo for r in receitas)
    tempo_medio = tempo_total // len(receitas) if receitas else 0
    categorias = set(r.categoria for r in receitas)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Receitas: {len(receitas)}")
    print(f"   • Categorias: {len(categorias)} ({', '.join(sorted(categorias))})")
    print(f"   • Tempo médio de preparo: {tempo_medio} minutos")
    print(f"   • Tempo total: {tempo_total} minutos")
    
    # Receitas por categoria
    print(f"\n📂 RECEITAS POR CATEGORIA:")
    categorias_dict = {}
    for r in receitas:
        if r.categoria not in categorias_dict:
            categorias_dict[r.categoria] = []
        categorias_dict[r.categoria].append(r.nome)
    
    for cat in sorted(categorias_dict.keys()):
        print(f"   • {cat}: {len(categorias_dict[cat])} receita(s)")
        for nome in categorias_dict[cat]:
            print(f"      - {nome}")
    
    # Receitas mais rápidas
    receitas_ordenadas = sorted(receitas, key=lambda r: r.tempo_preparo)
    print(f"\n⚡ RECEITAS MAIS RÁPIDAS:")
    for r in receitas_ordenadas[:3]:
        print(f"   • {r.nome}: {r.tempo_preparo} minutos")
    
    # Receitas mais longas
    print(f"\n🔥 RECEITAS MAIS COMPLEXAS (tempo):")
    for r in receitas_ordenadas[-3:]:
        print(f"   • {r.nome}: {r.tempo_preparo} minutos")
    
    print("\n" + "="*80)
    print("✅ Para usar o app completo, execute: python main.py")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
