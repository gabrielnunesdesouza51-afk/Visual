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
        
        receita = {
            "id": len(receitas) + 1,
            "nome": nome,
            "categoria": categoria,
            "ingredientes": ingredientes,
            "modo_preparo": modo_preparo,
            "porcoes": porcoes,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        receitas.append(receita)
        salvar_receitas(receitas)
        print(f"\n Receita '{nome}' adicionada com sucesso!")
    except ValueError:
        print("\n Erro: Digite valores válidos!")

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
        print("    GERENCIADOR DE RECEITAS ")
        print("="*50)
        print("1.  Adicionar receita")
        print("2.  Listar receitas")
        print("3.  Ver detalhes")
        print("4.  Buscar por ingrediente")
        print("5.  Listar por categoria")
        print("6.   Deletar receita")
        print("7.  Sair")
        print("="*50)
        opcao = input("\nEscolha uma opção (1-7): ")
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
            receitas = deletar_receita(receitas)
        elif opcao == "7":
            print("\n Até logo! Bom apetite! ")
            break
        else:
            print("\n Opção inválida!")

if __name__ == "__main__":
    menu_principal()
