import json
import os
from datetime import datetime

# Arquivo para salvar as receitas
ARQUIVO_RECEITAS = "receitas.json"

def carregar_receitas():
    if os.path.exists(ARQUIVO_RECEITAS):
        with open(ARQUIVO_RECEITAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_receitas(receitas):
    with open(ARQUIVO_RECEITAS, 'w', encoding='utf-8') as f:
        json.dump(receitas, f, indent=2, ensure_ascii=False)

def adicionar_receita(receitas):
    print("\n=== ADICIONAR RECEITA ===")
    try:
        nome = input("Nome da receita: ")
        categoria = input("Categoria (Doce, Salgado, Bebida, Sobremesa, Outro): ")
        ingredientes_str = input("Ingredientes (separados por vírgula): ")
        ingredientes = [i.strip() for i in ingredientes_str.split(',')]
        modo_preparo = input("Modo de preparo: ")
        porcoes = input("Número de porções: ")
        tempo_preparo = input("Tempo de preparo (em minutos): ")
        
        receita = {
            "id": len(receitas) + 1,
            "nome": nome,
            "categoria": categoria,
            "ingredientes": ingredientes,
            "modo_preparo": modo_preparo,
            "porcoes": porcoes,
            "tempo_preparo": int(tempo_preparo) if tempo_preparo.isdigit() else 0,
            "avaliacao": 0,
            "calorias": 0,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        receitas.append(receita)
        salvar_receitas(receitas)
        print(f"\n✓ Receita '{nome}' adicionada com sucesso!")
    except ValueError:
        print("\n✗ Erro: Digite valores válidos!")

def listar_receitas(receitas):
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    print("\n=== LISTA DE RECEITAS ===")
    print(f"{'ID':<4} {'Nome':<25} {'Categoria':<15} {'Porções':<10}")
    print("-" * 60)
    for r in receitas:
        nome_trunc = r['nome'][:24] if len(r['nome']) > 24 else r['nome']
        print(f"{r['id']:<4} {nome_trunc:<25} {r['categoria']:<15} {r['porcoes']:<10}")

def ver_detalhes(receitas):
    listar_receitas(receitas)
    if not receitas:
        return
    try:
        id_receita = int(input("\nDigite o ID para ver detalhes: "))
        for r in receitas:
            if r['id'] == id_receita:
                print("\n" + "="*50)
                print(f" {r['nome']}")
                print("="*50)
                print(f"Categoria: {r['categoria']}")
                print(f"Porções: {r['porcoes']}")
                print(f"\nIngredientes:")
                for i, ing in enumerate(r['ingredientes'], 1):
                    print(f"  {i}. {ing}")
                print(f"\nModo de Preparo:\n{r['modo_preparo']}")
                print("="*50)
                return
        print("\n Receita não encontrada!")
    except ValueError:
        print(" ID inválido!")

def buscar_ingrediente(receitas):
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    ingrediente = input("\nDigite o ingrediente a buscar: ").lower()
    encontradas = [r for r in receitas if any(ingrediente in ing.lower() for ing in r['ingredientes'])]
    if not encontradas:
        print(f"\n Nenhuma receita com '{ingrediente}'")
        return
    print(f"\n {len(encontradas)} receita(s) encontrada(s):")
    print(f"{'ID':<4} {'Nome':<25} {'Categoria':<15}")
    print("-" * 50)
    for r in encontradas:
        nome_trunc = r['nome'][:24] if len(r['nome']) > 24 else r['nome']
        print(f"{r['id']:<4} {nome_trunc:<25} {r['categoria']:<15}")

def listar_por_categoria(receitas):
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    categorias = {}
    for r in receitas:
        cat = r['categoria']
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(r)
    print("\n=== RECEITAS POR CATEGORIA ===")
    for cat in sorted(categorias.keys()):
        print(f"\n {cat} ({len(categorias[cat])} receita(s))")
        for r in categorias[cat]:
            print(f"   {r['nome']}")

def avaliar_receita(receitas):
    """Permite o usuário avaliar uma receita com estrelas (1-5)"""
    listar_receitas(receitas)
    if not receitas:
        return receitas
    try:
        id_receita = int(input("\nDigite o ID da receita a avaliar: "))
        for r in receitas:
            if r['id'] == id_receita:
                while True:
                    try:
                        estrelas = int(input("Avaliação (1-5 estrelas): "))
                        if 1 <= estrelas <= 5:
                            r['avaliacao'] = estrelas
                            salvar_receitas(receitas)
                            estrela_visual = "⭐" * estrelas
                            print(f"\n✓ Receita avaliada com {estrelas} estrelas! {estrela_visual}")
                            return receitas
                        else:
                            print("✗ Digite um valor entre 1 e 5!")
                    except ValueError:
                        print("✗ Digite um número válido!")
        print("\n✗ Receita não encontrada!")
    except ValueError:
        print("✗ ID inválido!")
    return receitas

def calcular_calorias(receitas):
    """Calcula e exibe as calorias de uma receita"""
    tabela_calorias = {
        "ovo": 70, "ovos": 70, "leite": 60, "açúcar": 400, "farinha": 360,
        "manteiga": 717, "óleo": 884, "sal": 0, "pão": 250, "presunto": 145,
        "queijo": 400, "tomate": 18, "alface": 15, "cebola": 40, "alho": 149,
        "frango": 165, "carne": 250, "peixe": 100, "arroz": 130, "feijão": 76,
        "batata": 77, "cenoura": 41, "maçã": 52, "banana": 89, "chocolate": 535,
        "café": 0, "chá": 0, "agua": 0, "sal": 0, "pimenta": 251
    }
    
    listar_receitas(receitas)
    if not receitas:
        return
    try:
        id_receita = int(input("\nDigite o ID da receita: "))
        for r in receitas:
            if r['id'] == id_receita:
                calorias_total = 0
                print(f"\n=== CALORIAS DE '{r['nome'].upper()}' ===")
                
                for ingrediente in r['ingredientes']:
                    ing_lower = ingrediente.lower()
                    calorias = 0
                    for chave, valor in tabela_calorias.items():
                        if chave in ing_lower:
                            calorias = valor
                            break
                    calorias_total += calorias
                    print(f"  • {ingrediente}: ~{calorias} kcal")
                
                r['calorias'] = calorias_total
                salvar_receitas(receitas)
                print(f"\n📊 Total por porção: ~{calorias_total // int(r['porcoes']) if r['porcoes'].isdigit() else calorias_total} kcal")
                print(f"📊 Total geral: ~{calorias_total} kcal")
                return
        print("\n✗ Receita não encontrada!")
    except ValueError:
        print("✗ ID inválido!")

def filtrar_por_tempo(receitas):
    """Filtra receitas pelo tempo de preparo"""
    if not receitas:
        print("\n⚠️ Nenhuma receita registrada!")
        return
    
    try:
        tempo_max = int(input("\nDigite o tempo máximo de preparo (em minutos): "))
        encontradas = [r for r in receitas if r.get('tempo_preparo', 0) <= tempo_max]
        
        if not encontradas:
            print(f"\n⚠️ Nenhuma receita com até {tempo_max} minutos de preparo")
            return
        
        print(f"\n⏱️ RECEITAS COM ATÉ {tempo_max} MINUTOS:")
        print(f"{'ID':<4} {'Nome':<25} {'Tempo':<15} {'Categoria':<15}")
        print("-" * 65)
        
        for r in encontradas:
            tempo_str = f"{r.get('tempo_preparo', 0)} min"
            nome_trunc = r['nome'][:24] if len(r['nome']) > 24 else r['nome']
            print(f"{r['id']:<4} {nome_trunc:<25} {tempo_str:<15} {r['categoria']:<15}")
            
    except ValueError:
        print("✗ Digite um número válido!")

def gerar_lista_compras(receitas):
    """Gera uma lista de compras a partir dos ingredientes das receitas"""
    if not receitas:
        print("\n⚠️ Nenhuma receita registrada!")
        return
    
    listar_receitas(receitas)
    print("\nDigite os IDs das receitas para gerar lista (separados por vírgula)")
    print("ou deixe em branco para usar todas:")
    
    entrada = input("IDs das receitas: ").strip()
    
    receitas_selecionadas = []
    if entrada:
        try:
            ids = [int(x.strip()) for x in entrada.split(',')]
            receitas_selecionadas = [r for r in receitas if r['id'] in ids]
        except ValueError:
            print("✗ IDs inválidos!")
            return
    else:
        receitas_selecionadas = receitas
    
    if not receitas_selecionadas:
        print("\n✗ Nenhuma receita encontrada!")
        return
    
    ingredientes_unicos = set()
    for r in receitas_selecionadas:
        for ing in r['ingredientes']:
            ingredientes_unicos.add(ing.strip())
    
    print("\n" + "="*50)
    print("🛒 LISTA DE COMPRAS")
    print("="*50)
    print(f"Receitas selecionadas: {', '.join([r['nome'] for r in receitas_selecionadas])}\n")
    
    for i, ing in enumerate(sorted(ingredientes_unicos), 1):
        print(f"  ☐ {i}. {ing}")
    
    print("\n" + "="*50)
    salvar_lista = input("\nDeseja salvar a lista em arquivo? (s/n): ")
    if salvar_lista.lower() == 's':
        nome_arquivo = f"lista_compras_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("LISTA DE COMPRAS\n")
            f.write("="*50 + "\n")
            f.write(f"Receitas: {', '.join([r['nome'] for r in receitas_selecionadas])}\n\n")
            for i, ing in enumerate(sorted(ingredientes_unicos), 1):
                f.write(f"☐ {i}. {ing}\n")
        print(f"✓ Lista salva em '{nome_arquivo}'")

def editar_receita(receitas):
    """Edita uma receita existente"""
    listar_receitas(receitas)
    if not receitas:
        return receitas
    try:
        id_receita = int(input("\nDigite o ID da receita a editar: "))
        for r in receitas:
            if r['id'] == id_receita:
                print(f"\n=== EDITANDO: {r['nome']} ===")
                print("Deixe em branco para manter o valor atual\n")
                
                novo_nome = input(f"Nome ({r['nome']}): ").strip()
                if novo_nome:
                    r['nome'] = novo_nome
                
                nova_categoria = input(f"Categoria ({r['categoria']}): ").strip()
                if nova_categoria:
                    r['categoria'] = nova_categoria
                
                novo_porcoes = input(f"Porções ({r['porcoes']}): ").strip()
                if novo_porcoes:
                    r['porcoes'] = novo_porcoes
                
                novos_ingredientes = input("Ingredientes novos (separados por vírgula) ou deixe em branco: ").strip()
                if novos_ingredientes:
                    r['ingredientes'] = [i.strip() for i in novos_ingredientes.split(',')]
                
                novo_preparo = input("Novo modo de preparo ou deixe em branco: ").strip()
                if novo_preparo:
                    r['modo_preparo'] = novo_preparo
                
                salvar_receitas(receitas)
                print(f"\n✓ Receita atualizada com sucesso!")
                return receitas
        print("\n✗ Receita não encontrada!")
    except ValueError:
        print("✗ ID inválido!")
    return receitas

def deletar_receita(receitas):
    listar_receitas(receitas)
    if not receitas:
        return receitas
    try:
        id_receita = int(input("\nDigite o ID para deletar: "))
        for r in receitas:
            if r['id'] == id_receita:
                nome = r['nome']
                receitas = [x for x in receitas if x['id'] != id_receita]
                salvar_receitas(receitas)
                print(f" '{nome}' deletada!")
                return receitas
        print(" Receita não encontrada!")
    except ValueError:
        print(" ID inválido!")
    return receitas

def menu_principal():
    receitas = carregar_receitas()
    while True:
        print("\n" + "="*50)
        print("   📚 GERENCIADOR DE RECEITAS 👨‍🍳")
        print("="*50)
        print("GERENCIAR RECEITAS")
        print("  1.  ➕ Adicionar receita")
        print("  2.  📋 Listar receitas")
        print("  3.  👀 Ver detalhes")
        print("  4.  🔍 Buscar por ingrediente")
        print("  5.  📂 Listar por categoria")
        print("  6.  ✏️  Editar receita")
        print("  7.  🗑️  Deletar receita")
        print("\nANÁLISE E FERRAMENTAS")
        print("  8.  ⭐ Avaliar receita")
        print("  9.  📊 Calcular calorias")
        print("  10. ⏱️  Filtrar por tempo")
        print("  11. 🛒 Gerar lista de compras")
        print("\n  0.  🚪 Sair")
        print("="*50)
        opcao = input("\nEscolha uma opção: ")
        if opcao == "1":
            adicionar_receita(receitas)
        elif opcao == "2":
            listar_receitas(receitas)
        elif opcao == "3":
            ver_detalhes(receitas)
        elif opcao == "4":
            buscar_ingrediente(receitas)
        elif opcao == "5":
            listar_por_categoria(receitas)
        elif opcao == "6":
            receitas = editar_receita(receitas)
        elif opcao == "7":
            receitas = deletar_receita(receitas)
        elif opcao == "8":
            receitas = avaliar_receita(receitas)
        elif opcao == "9":
            calcular_calorias(receitas)
        elif opcao == "10":
            filtrar_por_tempo(receitas)
        elif opcao == "11":
            gerar_lista_compras(receitas)
        elif opcao == "0":
            print("\n👋 Até logo! Bom apetite! 🍽️")
            break
        else:
            print("\n✗ Opção inválida!")

if __name__ == "__main__":
    menu_principal()
