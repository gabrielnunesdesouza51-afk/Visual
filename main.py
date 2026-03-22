"""
Gerenciador de Receitas - Aplicação Principal
Sistema CLI profissional para gerenciar receitas culinárias
"""
import sys
import os

# Adiciona diretório atual ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from typing import List
from models.receita import Receita
from utils.storage import carregar_receitas, salvar_receitas, proxima_id
from services import receita_service

# ==== OPERAÇÕES DE RECEITA ====

def adicionar_receita(receitas: List[Receita]) -> List[Receita]:
    """Adiciona uma nova receita ao sistema"""
    print("\n" + "="*60)
    print("   ADICIONAR RECEITA")
    print("="*60)
    
    try:
        nome = input("Nome da receita: ").strip()
        if not nome:
            print(" Nome não pode ser vazio!")
            return receitas
        
        categoria = input("Categoria (Doce, Salgado, Bebida, Sobremesa): ").strip()
        if not categoria:
            categoria = "Outro"
        
        print("\nIngredientes (uma por linha, deixe em branco para terminar):")
        ingredientes = []
        while True:
            ing = input("   ").strip()
            if not ing:
                break
            ingredientes.append(ing)
        
        if not ingredientes:
            print(" Receita precisa de pelo menos um ingrediente!")
            return receitas
        
        modo_preparo = input("\nModo de preparo:\n> ").strip()
        if not modo_preparo:
            print(" Modo de preparo não pode ser vazio!")
            return receitas
        
        # Validar porcoes
        while True:
            porcoes_str = input("Número de porções: ").strip()
            porcoes = receita_service.validar_numero(porcoes_str, minimo=1)
            if porcoes is not None:
                break
            print(" Digite um número válido (mínimo 1)!")
        
        # Validar tempo_preparo
        while True:
            tempo_str = input("Tempo de preparo (minutos): ").strip()
            tempo_preparo = receita_service.validar_numero(tempo_str, minimo=0)
            if tempo_preparo is not None:
                break
            print(" Digite um número válido!")
        
        # Criar receita
        nova_receita = Receita(
            id=proxima_id(receitas),
            nome=nome,
            categoria=categoria,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            porcoes=porcoes,
            tempo_preparo=tempo_preparo
        )
        
        receitas.append(nova_receita)
        salvar_receitas(receitas)
        
        print(f"\n Receita '{nome}' adicionada com sucesso!")
        return receitas
        
    except Exception as e:
        print(f"\n Erro ao adicionar receita: {e}")
        return receitas

def listar_receitas(receitas: List[Receita]) -> None:
    """Lista todas as receitas"""
    receita_service.exibir_lista_simples(receitas)

def ver_detalhes_receita(receitas: List[Receita]) -> None:
    """Exibe detalhes completos de uma receita"""
    receita = receita_service.selecionar_receita(receitas, "ver detalhes")
    if not receita:
        return
    
    print("\n" + "="*60)
    print(f"   {receita.nome.upper()}")
    print("="*60)
    print(f"Categoria: {receita.categoria}")
    print(f"Porções: {receita.porcoes}")
    print(f"Tempo de preparo: {receita.tempo_preparo} minutos")
    if receita.avaliacao > 0:
        print(f"Avaliação: {'⭐' * receita.avaliacao}")
    if receita.favorita:
        print(f"Favorita: ❤️")
    
    print(f"\n INGREDIENTES:")
    for i, ing in enumerate(receita.ingredientes, 1):
        print(f"  {i}. {ing}")
    
    print(f"\n MODO DE PREPARO:")
    print(f"  {receita.modo_preparo}")
    
    if receita.calorias > 0:
        calorias_por_porcao = receita.calorias // receita.porcoes
        print(f"\n CALORIAS:")
        print(f"  Total: {receita.calorias} kcal")
        print(f"  Por porção: {calorias_por_porcao} kcal")
    
    print(f"Data: {receita.data}")
    print("="*60)

def buscar_por_ingrediente(receitas: List[Receita]) -> None:
    """Busca receitas que contêm um ingrediente específico"""
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    
    ingrediente = input("\n Digite o ingrediente a buscar: ").strip().lower()
    if not ingrediente:
        return
    
    encontradas = [r for r in receitas if
                  any(ingrediente in ing.lower() for ing in r.ingredientes)]
    
    if encontradas:
        print(f"\n {len(encontradas)} receita(s) encontrada(s):")
        receita_service.exibir_lista_simples(encontradas)
    else:
        print(f"\n Nenhuma receita encontrada com '{ingrediente}'")

def buscar_por_nome(receitas: List[Receita]) -> None:
    """Busca receitas por nome"""
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    
    nome = input("\n Digite o nome da receita: ").strip().lower()
    if not nome:
        return
    
    encontradas = [r for r in receitas if nome in r.nome.lower()]
    
    if encontradas:
        print(f"\n {len(encontradas)} receita(s) encontrada(s):")
        receita_service.exibir_lista_simples(encontradas)
    else:
        print(f"\n Nenhuma receita encontrada com '{nome}'")

def listar_por_categoria(receitas: List[Receita]) -> None:
    """Lista receitas agrupadas por categoria"""
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    
    categorias = {}
    for r in receitas:
        if r.categoria not in categorias:
            categorias[r.categoria] = []
        categorias[r.categoria].append(r)
    
    print(f"\n RECEITAS POR CATEGORIA")
    print("="*60)
    
    for cat in sorted(categorias.keys()):
        print(f"\n{cat.upper()} ({len(categorias[cat])} receita(s))")
        print("-" * 60)
        for r in categorias[cat]:
            estrela = f" {'⭐' * r.avaliacao}" if r.avaliacao > 0 else ""
            print(f"   {r.nome} ({r.tempo_preparo} min){estrela}")

def editar_receita(receitas: List[Receita]) -> List[Receita]:
    """Edita uma receita existente"""
    receita = receita_service.selecionar_receita(receitas, "editar")
    if not receita:
        return receitas
    
    print("\n" + "="*60)
    print(f"    EDITANDO: {receita.nome}")
    print("="*60)
    print("Deixe em branco para manter o valor atual\n")
    
    try:
        novo_nome = input(f"Nome ({receita.nome}): ").strip()
        if novo_nome:
            receita.nome = novo_nome
        
        nova_categoria = input(f"Categoria ({receita.categoria}): ").strip()
        if nova_categoria:
            receita.categoria = nova_categoria
        
        novo_porcoes_str = input(f"Porções ({receita.porcoes}): ").strip()
        if novo_porcoes_str:
            novo_porcoes = receita_service.validar_numero(novo_porcoes_str, minimo=1)
            if novo_porcoes is not None:
                receita.porcoes = novo_porcoes
            else:
                print(" Valor de porções inválido, mantendo anterior!")
        
        novo_tempo_str = input(f"Tempo ({receita.tempo_preparo} min): ").strip()
        if novo_tempo_str:
            novo_tempo = receita_service.validar_numero(novo_tempo_str, minimo=0)
            if novo_tempo is not None:
                receita.tempo_preparo = novo_tempo
            else:
                print(" Valor de tempo inválido, mantendo anterior!")
        
        novo_preparo = input("Novo modo de preparo (deixe em branco para manter): ").strip()
        if novo_preparo:
            receita.modo_preparo = novo_preparo
        
        print("\nNovos ingredientes (deixe em branco para manter) - um por linha:")
        novos_ings = []
        while True:
            ing = input("   ").strip()
            if not ing:
                break
            novos_ings.append(ing)
        
        if novos_ings:
            receita.ingredientes = novos_ings
        
        salvar_receitas(receitas)
        print(f"\n Receita atualizada com sucesso!")
        
    except Exception as e:
        print(f"\n Erro ao editar: {e}")
    
    return receitas

def deletar_receita(receitas: List[Receita]) -> List[Receita]:
    """Deleta uma receita após confirmação"""
    receita = receita_service.selecionar_receita(receitas, "deletar")
    if not receita:
        return receitas
    
    if receita_service.confirmar_acao(f"Deletar '{receita.nome}'? Esta ação não pode ser desfeita"):
        receitas = [r for r in receitas if r.id != receita.id]
        salvar_receitas(receitas)
        print(f" Receita '{receita.nome}' deletada com sucesso!")
    
    return receitas

# ==== ANÁLISE E FERRAMENTAS ====

def avaliar_receita(receitas: List[Receita]) -> List[Receita]:
    """Avalia uma receita com estrelas (1-5)"""
    receita = receita_service.selecionar_receita(receitas, "avaliar")
    if not receita:
        return receitas
    
    while True:
        estrelas_str = input("Avaliação (1-5 estrelas, 0 para remover): ").strip()
        estrelas = receita_service.validar_numero(estrelas_str, minimo=0, maximo=5)
        
        if estrelas is not None:
            receita.avaliacao = estrelas
            salvar_receitas(receitas)
            
            if estrelas > 0:
                print(f"\n Receita avaliada com {estrelas} {'⭐' * estrelas}")
            else:
                print(f"\n Avaliação removida")
            break
        
        print(" Digite um número entre 0 e 5!")
    
    return receitas

def calcular_calorias(receitas: List[Receita]) -> None:
    """Calcula calorias de uma receita"""
    receita = receita_service.selecionar_receita(receitas, "calcular calorias")
    if not receita:
        return
    
    print(f"\n CÁLCULO DE CALORIAS: {receita.nome.upper()}")
    print("="*60)
    
    calorias_total = 0
    
    for ingrediente in receita.ingredientes:
        calorias = receita_service.calcular_calorias_ingrediente(ingrediente)
        calorias_total += calorias
        print(f"   {ingrediente}: ~{calorias} kcal")
    
    receita.calorias = calorias_total
    salvar_receitas(receitas)
    
    calorias_por_porcao = calorias_total // receita.porcoes if receita.porcoes > 0 else 0
    
    print("="*60)
    print(f" Total por porção: ~{calorias_por_porcao} kcal")
    print(f" Total geral: ~{calorias_total} kcal")

def filtrar_por_tempo(receitas: List[Receita]) -> None:
    """Filtra receitas pelo tempo de preparo"""
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    
    while True:
        tempo_str = input("\n Digite o tempo máximo de preparo (minutos): ").strip()
        tempo_max = receita_service.validar_numero(tempo_str, minimo=0)
        
        if tempo_max is not None:
            break
        
        print(" Digite um número válido!")
    
    encontradas = receita_service.filtrar_receitas(receitas, 'tempo', tempo_max)
    
    if encontradas:
        print(f"\n RECEITAS COM ATÉ {tempo_max} MINUTOS:")
        receita_service.exibir_lista_simples(encontradas)
    else:
        print(f"\n Nenhuma receita com até {tempo_max} minutos!")

def gerar_lista_compras(receitas: List[Receita]) -> None:
    """Gera lista agregada de compras"""
    if not receitas:
        print("\n Nenhuma receita registrada!")
        return
    
    receita_service.exibir_lista_simples(receitas)
    
    print("\nDigite os IDs das receitas (separados por vírgula)")
    print("ou deixe em branco para todas:")
    
    entrada = input("> ").strip()
    
    receitas_selecionadas = []
    
    if entrada:
        try:
            ids = [int(x.strip()) for x in entrada.split(',')]
            receitas_selecionadas = [r for r in receitas if r.id in ids]
        except ValueError:
            print(" IDs inválidos!")
            return
    else:
        receitas_selecionadas = receitas
    
    if not receitas_selecionadas:
        print(" Nenhuma receita selecionada!")
        return
    
    ingredientes_agregados = receita_service.gerar_lista_compras_agregada(receitas_selecionadas)
    
    print("\n" + "="*60)
    print(" LISTA DE COMPRAS")
    print("="*60)
    print(f"Receitas: {', '.join([r.nome for r in receitas_selecionadas])}\n")
    
    for i, (ing, qtd) in enumerate(sorted(ingredientes_agregados.items()), 1):
        print(f"   {i}. {qtd}x {ing}")
    
    print("="*60)
    
    salvar_lista = input("\nSalvar em arquivo? (s/n): ").strip().lower()
    if salvar_lista == 's':
        nome_arquivo = f"lista_compras_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write("LISTA DE COMPRAS\n")
                f.write("="*60 + "\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"Receitas: {', '.join([r.nome for r in receitas_selecionadas])}\n\n")
                for i, (ing, qtd) in enumerate(sorted(ingredientes_agregados.items()), 1):
                    f.write(f" {i}. {qtd}x {ing}\n")
            print(f" Lista salva em '{nome_arquivo}'")
        except IOError as e:
            print(f" Erro ao salvar arquivo: {e}")

def top_receitas(receitas: List[Receita]) -> None:
    """Exibe as receitas melhor avaliadas"""
    melhores = receita_service.top_receitas(receitas, quantidade=10)
    
    if not melhores:
        print("\n Nenhuma receita com avaliação!")
        return
    
    print(f"\n TOP RECEITAS (Melhor Avaliadas)")
    print("="*60)
    receita_service.exibir_lista_simples(melhores)

def favoritar_receita(receitas: List[Receita]) -> List[Receita]:
    """Marca/desmarca uma receita como favorita"""
    receita = receita_service.selecionar_receita(receitas, "favoritar")
    if not receita:
        return receitas
    
    receita.favorita = not receita.favorita
    salvar_receitas(receitas)
    
    status = " adicionada" if receita.favorita else "removida"
    print(f" Receita {status} dos favoritos!")
    
    return receitas

def listar_favoritas(receitas: List[Receita]) -> None:
    """Lista apenas receitas favoritas"""
    favoritas = [r for r in receitas if r.favorita]
    
    if not favoritas:
        print("\n Nenhuma receita marcada como favorita!")
        return
    
    print(f"\n  RECEITAS FAVORITAS ({len(favoritas)})")
    print("="*60)
    receita_service.exibir_lista_simples(favoritas)

# ==== MENU PRINCIPAL ====

def exibir_menu() -> None:
    """Exibe o menu principal"""
    print("\n" + "="*60)
    print("   GERENCIADOR DE RECEITAS ")
    print("="*60)
    
    print("\n GERENCIAR RECEITAS")
    print("  1.   Adicionar receita")
    print("  2.   Listar todas as receitas")
    print("  3.   Ver detalhes de receita")
    print("  4.    Editar receita")
    print("  5.    Deletar receita")
    
    print("\n BUSCAR E FILTRAR")
    print("  6.   Buscar por ingrediente")
    print("  7.   Buscar por nome")
    print("  8.   Listar por categoria")
    print("  9.    Filtrar por tempo de preparo")
    
    print("\n ANÁLISE E FERRAMENTAS")
    print("  10.  Avaliar receita")
    print("  11.  Calcular calorias")
    print("  12.  Gerar lista de compras")
    print("  13.  Top receitas")
    print("  14.   Favoritar receita")
    print("  15.   Listar favoritas")
    
    print("\n  0.   Sair")
    print("="*60)

def processar_opcao(opcao: str, receitas: List[Receita]) -> tuple:
    """
    Processa a opção do menu e executa ação correspondente
    
    Returns:
        Tupla (receitas_atualizadas, operacao_valida)
    """
    try:
        if opcao == "1":
            receitas = adicionar_receita(receitas)
        elif opcao == "2":
            listar_receitas(receitas)
        elif opcao == "3":
            ver_detalhes_receita(receitas)
        elif opcao == "4":
            receitas = editar_receita(receitas)
        elif opcao == "5":
            receitas = deletar_receita(receitas)
        elif opcao == "6":
            buscar_por_ingrediente(receitas)
        elif opcao == "7":
            buscar_por_nome(receitas)
        elif opcao == "8":
            listar_por_categoria(receitas)
        elif opcao == "9":
            filtrar_por_tempo(receitas)
        elif opcao == "10":
            receitas = avaliar_receita(receitas)
        elif opcao == "11":
            calcular_calorias(receitas)
        elif opcao == "12":
            gerar_lista_compras(receitas)
        elif opcao == "13":
            top_receitas(receitas)
        elif opcao == "14":
            receitas = favoritar_receita(receitas)
        elif opcao == "15":
            listar_favoritas(receitas)
        elif opcao == "0":
            return receitas, "sair"
        else:
            print("\n Opção inválida! Digite um número de 0 a 15.")
            return receitas, True
        
        return receitas, True
    
    except Exception as e:
        print(f"\n Erro ao processar operação: {e}")
        return receitas, True

def main() -> None:
    """Função principal do aplicativo"""
    print("\n" + "="*30)
    print("Bem-vindo ao Gerenciador de Receitas!")
    print("="*30)
    
    receitas = carregar_receitas()
    
    if receitas:
        print(f"\n {len(receitas)} receita(s) carregada(s) do arquivo!")
    else:
        print("\n Começar adicionando sua primeira receita!")
    
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        receitas, resultado = processar_opcao(opcao, receitas)
        
        if resultado == "sair":
            print("\n Até logo! Bom apetite! ")
            break

if __name__ == "__main__":
    main()
