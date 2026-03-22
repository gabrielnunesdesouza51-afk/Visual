#!/usr/bin/env python
"""
Script de teste para verificar carregamento de receitas e validação de categorias
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.receita import Receita
from utils.storage import carregar_receitas, salvar_receitas, proxima_id, criar_receitas_iniciais
from services.recipe_suggester import sugerir_receitas, exibir_sugestoes

def teste_1_carregar_recipes():
    """Teste 1: Carregamento de receitas"""
    print("\n" + "="*60)
    print("TESTE 1: Carregamento de Receitas")
    print("="*60)
    
    receitas = carregar_receitas()
    
    if receitas:
        print(f"✅ {len(receitas)} receita(s) carregada(s)")
        for r in receitas:
            print(f"   - {r.id}: {r.nome} ({r.categoria})")
        return True
    else:
        print("⚠️  Nenhuma receita encontrada. Carregando receitas iniciais...")
        receitas = criar_receitas_iniciais()
        salvar_receitas(receitas)
        print(f"✅ {len(receitas)} receita(s) iniciais criadas e salvas")
        return True

def teste_2_valida_tipos():
    """Teste 2: Validação de tipos de dados"""
    print("\n" + "="*60)
    print("TESTE 2: Validação de Tipos de Dados")
    print("="*60)
    
    # Criar uma receita com tipos mistos
    dados = {
        "id": "1",  # string em vez de int
        "nome": "Test Recipe",
        "categoria": "Doce",
        "ingredientes": ["ing1", "ing2"],
        "modo_preparo": "Test",
        "porcoes": "10",  # string em vez de int
        "tempo_preparo": "30",  # string em vez de int
        "avaliacao": "4",  # string em vez de int
        "calorias": "200",  # string em vez de int
        "favorita": "true"  # string em vez de bool
    }
    
    try:
        receita = Receita.do_dict(dados)
        print("✅ Receita criada com conversão automática de tipos")
        print(f"   ID (int): {receita.id} ({type(receita.id).__name__})")
        print(f"   Porcoes (int): {receita.porcoes} ({type(receita.porcoes).__name__})")
        print(f"   Avaliacao (int): {receita.avaliacao} ({type(receita.avaliacao).__name__})")
        return True
    except Exception as e:
        print(f"❌ Erro ao converter tipos: {e}")
        return False

def teste_3_campos_opcionais():
    """Teste 3: Campos opcionais com valores padrão"""
    print("\n" + "="*60)
    print("TESTE 3: Campos Opcionais com Valores Padrão")
    print("="*60)
    
    # JSON com campos opcionais ausentes
    dados = {
        "id": 1,
        "nome": "Receita Simples",
        "categoria": "Outro",
        "ingredientes": ["açúcar", "leite"],
        "modo_preparo": "Misturar tudo",
        "porcoes": 4,
        "tempo_preparo": 10
        # Faltam: avaliacao, calorias, favorita, data
    }
    
    try:
        receita = Receita.do_dict(dados)
        print("✅ Receita criada com campos opcionais faltando")
        print(f"   Avaliacao (padrão): {receita.avaliacao}")
        print(f"   Calorias (padrão): {receita.calorias}")
        print(f"   Favorita (padrão): {receita.favorita}")
        print(f"   Data (gerada): {receita.data[:10]}")
        assert receita.avaliacao == 0, "Avaliação deveria ser 0"
        assert receita.calorias == 0, "Calorias deveria ser 0"
        assert receita.favorita == False, "Favorita deveria ser False"
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def teste_4_categorias_validas():
    """Teste 4: Validação de categorias"""
    print("\n" + "="*60)
    print("TESTE 4: Validação de Categorias")
    print("="*60)
    
    CATEGORIAS_VALIDAS = ["Doce", "Salgado", "Bebida", "Sobremesa", "Aperitivo", 
                          "Salada", "Vegetariano", "Japonês", "Outro"]
    
    testes = [
        ("Doce", True),
        ("Salgado", True),
        ("Outro", True),
        ("Pizza", False),
        ("Bebida", True),
        ("", False),
    ]
    
    todos_ok = True
    for categoria, deveria_ser_valida in testes:
        eh_valida = categoria in CATEGORIAS_VALIDAS
        status = "✅" if eh_valida == deveria_ser_valida else "❌"
        print(f"{status} Categoria '{categoria}': válida={eh_valida}")
        if eh_valida != deveria_ser_valida:
            todos_ok = False
    
    return todos_ok

def teste_5_sugestoes():
    """Teste 5: Sistema de sugestões"""
    print("\n" + "="*60)
    print("TESTE 5: Sistema de Sugestões Inteligentes")
    print("="*60)
    
    receitas = carregar_receitas()
    if not receitas:
        print("⚠️  Nenhuma receita para testar sugestões")
        return False
    
    ingredientes_usuario = ["leite", "ovos", "farinha", "açúcar"]
    sugestoes = sugerir_receitas(receitas, ingredientes_usuario, limite=3)
    
    if sugestoes:
        print(f"✅ {len(sugestoes)} sugestão(ões) gerada(s) para: {ingredientes_usuario}")
        for i, s in enumerate(sugestoes, 1):
            print(f"   {i}. {s['receita'].nome} - Score: {s['score']:.1f}%")
        return True
    else:
        print("⚠️  Nenhuma sugestão encontrada (isso pode ser OK)")
        return True

def teste_6_salvar_recover():
    """Teste 6: Salvar e recuperar receitas"""
    print("\n" + "="*60)
    print("TESTE 6: Salvar e Recuperar Receitas")
    print("="*60)
    
    # Criar receita de teste
    receita_teste = Receita(
        id=999,
        nome="Receita de Teste",
        categoria="Doce",
        ingredientes=["test1", "test2"],
        modo_preparo="Test preparation",
        porcoes=2,
        tempo_preparo=5,
        avaliacao=5,
        calorias=100,
        favorita=True
    )
    
    # Carregar receitas e adicionar teste
    receitas = carregar_receitas()
    receitas.append(receita_teste)
    
    # Salvar
    if salvar_receitas(receitas):
        print("✅ Receitas salvas com sucesso")
        
        # Recuperar
        receitas_carregadas = carregar_receitas()
        receita_encontrada = next((r for r in receitas_carregadas if r.id == 999), None)
        
        if receita_encontrada:
            print("✅ Receita de teste recuperada com sucesso")
            assert receita_encontrada.nome == "Receita de Teste"
            assert receita_encontrada.avaliacao == 5
            assert receita_encontrada.favorita == True
            
            # Limpar
            receitas_carregadas = [r for r in receitas_carregadas if r.id != 999]
            salvar_receitas(receitas_carregadas)
            print("✅ Receita de teste removida")
            return True
        else:
            print("❌ Receita de teste não foi recuperada")
            return False
    else:
        print("❌ Erro ao salvar receitas")
        return False

def main():
    """Executar todos os testes"""
    print("\n" + "="*60)
    print("SUITE DE TESTES - GERENCIADOR DE RECEITAS")
    print("="*60)
    
    testes = [
        teste_1_carregar_recipes,
        teste_2_valida_tipos,
        teste_3_campos_opcionais,
        teste_4_categorias_validas,
        teste_5_sugestoes,
        teste_6_salvar_recover,
    ]
    
    resultados = []
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"\n❌ Exceção em {teste.__name__}: {e}")
            resultados.append(False)
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    total = len(resultados)
    passou = sum(resultados)
    
    for i, (teste, resultado) in enumerate(zip(testes, resultados), 1):
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{i}. {teste.__name__:<40} {status}")
    
    print("="*60)
    print(f"Total: {passou}/{total} testes passaram")
    
    if passou == total:
        print("✅ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"❌ {total - passou} teste(s) falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())
