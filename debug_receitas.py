#!/usr/bin/env python
"""Script para validar o carregamento de receitas com debug detalhado"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_json():
    """Valida JSON diretamente"""
    print("\n" + "="*60)
    print("DEBUG 1: Verificando arquivo JSON")
    print("="*60)
    
    arquivo = "receitas.json"
    
    # 1. Verificar existência
    if os.path.exists(arquivo):
        print(f"✅ Arquivo encontrado: {arquivo}")
        print(f"   Tamanho: {os.path.getsize(arquivo)} bytes")
    else:
        print(f"❌ Arquivo NÃO encontrado: {arquivo}")
        return False
    
    # 2. Validar JSON
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        print(f"✅ JSON válido")
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}")
        return False
    
    # 3. Verificar tipo
    if isinstance(dados, list):
        print(f"✅ Tipo correto: list")
    else:
        print(f"❌ Tipo incorreto: {type(dados).__name__}")
        return False
    
    # 4. Contar receitas
    print(f"✅ Total de registros: {len(dados)}")
    
    if dados:
        print(f"\n📝 Estrutura da primeira receita:")
        primeiro = dados[0]
        for chave in primeiro.keys():
            valor = primeiro[chave]
            if isinstance(valor, list):
                print(f"   {chave}: list ({len(valor)} itens)")
            else:
                print(f"   {chave}: {type(valor).__name__} = {str(valor)[:50]}")
    
    return True

def debug_carregar():
    """Valida função carregar_receitas()"""
    print("\n" + "="*60)
    print("DEBUG 2: Testando carregar_receitas()")
    print("="*60)
    
    from utils.storage import carregar_receitas
    from models.receita import Receita
    
    receitas = carregar_receitas()
    
    print(f"✅ Função executada sem erro")
    print(f"✅ Tipo retornado: {type(receitas).__name__}")
    print(f"✅ Total de receitas: {len(receitas)}")
    
    if receitas:
        print(f"\n📝 Validando primeira receita:")
        r = receitas[0]
        
        # Verificar tipo
        if isinstance(r, Receita):
            print(f"   ✅ É objeto Receita (não JSON cru)")
            print(f"   ID: {r.id} (type: {type(r.id).__name__})")
            print(f"   Nome: {r.nome}")
            print(f"   Categoria: {r.categoria}")
            print(f"   Ingredientes: {len(r.ingredientes)} itens")
            print(f"   Tempo: {r.tempo_preparo} min")
            print(f"   Avaliação: {r.avaliacao}")
        else:
            print(f"   ❌ NÃO é Receita, é {type(r).__name__}")
            return False
    
    return len(receitas) > 0

def debug_exibir():
    """Valida função exibir_lista_simples()"""
    print("\n" + "="*60)
    print("DEBUG 3: Testando exibir_lista_simples()")
    print("="*60)
    
    from utils.storage import carregar_receitas
    from services.receita_service import exibir_lista_simples
    
    receitas = carregar_receitas()
    
    if not receitas:
        print("⚠️  Nenhuma receita para exibir")
        return False
    
    print(f"📋 Exibindo {len(receitas)} receita(s):\n")
    
    try:
        exibir_lista_simples(receitas)
        print("\n✅ Função funcionou sem erro")
        return True
    except Exception as e:
        print(f"❌ Erro ao exibir: {e}")
        return False

def debug_listar():
    """Debug adicional - listar todas as receitas"""
    print("\n" + "="*60)
    print("DEBUG 4: Detalhes de Todas as Receitas")
    print("="*60)
    
    from utils.storage import carregar_receitas
    
    receitas = carregar_receitas()
    
    if not receitas:
        print("⚠️  Nenhuma receita")
        return False
    
    for i, r in enumerate(receitas, 1):
        print(f"\n{i}. {r.nome}")
        print(f"   ID: {r.id}")
        print(f"   Categoria: {r.categoria}")
        print(f"   Tempo: {r.tempo_preparo} min")
        print(f"   Porções: {r.porcoes}")
        print(f"   Ingredientes: {', '.join(r.ingredientes[:3])}{'...' if len(r.ingredientes) > 3 else ''}")

def main():
    print("\n" + "="*60)
    print("VALIDAÇÃO COMPLETA - CARREGAMENTO DE RECEITAS")
    print("="*60)
    
    testes = [
        ("Validar JSON", debug_json),
        ("Carregar Receitas", debug_carregar),
        ("Exibir Lista", debug_exibir),
        ("Listar Detalhes", debug_listar),
    ]
    
    resultados = []
    for nome, funcao in testes:
        try:
            resultado = funcao()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"\n❌ ERRO em {nome}: {e}")
            import traceback
            traceback.print_exc()
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} | {nome}")

if __name__ == "__main__":
    main()
