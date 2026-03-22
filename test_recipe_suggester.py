"""
Testes para o sistema de sugestão inteligente de receitas
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.receita import Receita
from services.recipe_suggester import (
    calcular_score_compatibilidade,
    sugerir_receitas,
    listar_ingredientes_que_faltam,
    calcular_melhor_receita
)


def criar_receitas_teste():
    """Cria receitas de teste"""
    receitas = [
        Receita(
            id=1,
            nome="Brigadeiro",
            categoria="Sobremesa",
            ingredientes=["leite condensado", "chocolate em pó", "manteiga", "chocolate granulado"],
            modo_preparo="Misture e cozinhe",
            porcoes=20,
            tempo_preparo=20,
            avaliacao=5,
            calorias=150
        ),
        Receita(
            id=2,
            nome="Bolo de Chocolate",
            categoria="Doce",
            ingredientes=["farinha de trigo", "açúcar", "ovos", "chocolate em pó", "leite", "óleo", "fermento"],
            modo_preparo="Misture tudo e asse",
            porcoes=12,
            tempo_preparo=60,
            avaliacao=4,
            calorias=250
        ),
        Receita(
            id=3,
            nome="Macarrão à Carbonara",
            categoria="Salgado",
            ingredientes=["macarrão", "ovos", "bacon", "queijo pecorino", "sal", "pimenta preta"],
            modo_preparo="Cozinhe e misture",
            porcoes=4,
            tempo_preparo=30,
            avaliacao=4,
            calorias=400
        )
    ]
    return receitas


def testar_compatibilidade():
    """Testa cálculo de compatibilidade"""
    print("\n" + "="*60)
    print("TESTE 1: Cálculo de Compatibilidade")
    print("="*60)
    
    receitas = criar_receitas_teste()
    ingredientes_usuario = ["leite condensado", "chocolate em pó", "manteiga"]
    
    score, encontrados, faltantes = calcular_score_compatibilidade(
        ingredientes_usuario,
        receitas[0].ingredientes
    )
    
    print(f"\nRece receita: {receitas[0].nome}")
    print(f"Seus ingredientes: {ingredientes_usuario}")
    print(f"Score: {score:.1f}%")
    print(f"Encontrados: {encontrados}/{receitas[0].ingredientes}")
    print(f"Faltantes: {faltantes}")
    
    assert score == 75.0, f"Score esperado 75.0, obteve {score}"
    assert encontrados == 3, f"Esperado 3 ingredientes encontrados, obteve {encontrados}"
    assert faltantes == 1, f"Esperado 1 faltante, obteve {faltantes}"
    
    print("\n✅ Teste de compatibilidade passou!")


def testar_sugestoes():
    """Testa geração de sugestões"""
    print("\n" + "="*60)
    print("TESTE 2: Geração de Sugestões")
    print("="*60)
    
    receitas = criar_receitas_teste()
    ingredientes_usuario = ["chocolate em pó", "leite", "óleo", "fermento"]
    
    sugestoes = sugerir_receitas(receitas, ingredientes_usuario, limite=3)
    
    print(f"\nSeus ingredientes: {ingredientes_usuario}")
    print(f"Receitas sugeridas encontradas: {len(sugestoes)}")
    
    for sugestao in sugestoes:
        print(f"\n  - {sugestao['receita'].nome}")
        print(f"    Score: {sugestao['score']:.1f}%")
        print(f"    Ingredientes encontrados: {sugestao['encontrados']}/{sugestao['total_ingredientes']}")
    
    assert len(sugestoes) > 0, "Deveria ter encontrado pelo menos uma sugestão"
    assert sugestoes[0]['score'] >= 50, "Score deveria ser >= 50"
    
    print("\n✅ Teste de sugestões passou!")


def testar_ingredientes_faltantes():
    """Testa lista de ingredientes faltantes"""
    print("\n" + "="*60)
    print("TESTE 3: Ingredientes Faltantes")
    print("="*60)
    
    receitas = criar_receitas_teste()
    ingredientes_usuario = ["leite condensado", "chocolate em pó"]
    
    receita = receitas[0]
    faltam = listar_ingredientes_que_faltam(receita, ingredientes_usuario)
    
    print(f"\nRece receita: {receita.nome}")
    print(f"Seus ingredientes: {ingredientes_usuario}")
    print(f"Ingredientes que faltam: {faltam}")
    
    assert len(faltam) == 2, f"Esperado 2 faltantes, obteve {len(faltam)}"
    assert "manteiga" in faltam, "Manteiga deveria estar na lista de faltantes"
    
    print("\n✅ Teste de ingredientes faltantes passou!")


def testar_melhor_receita():
    """Testa cálculo da melhor receita"""
    print("\n" + "="*60)
    print("TESTE 4: Melhor Receita")
    print("="*60)
    
    receitas = criar_receitas_teste()
    ingredientes_usuario = ["chocolate em pó", "leite", "óleo", "açúcar", "farinha de trigo", "fermento"]
    
    melhor = calcular_melhor_receita(receitas, ingredientes_usuario)
    
    if melhor:
        print(f"\nMelhor receita com seus ingredientes: {melhor['receita'].nome}")
        print(f"Score: {melhor['score']:.1f}%")
        print(f"Avaliação: {'⭐' * melhor['receita'].avaliacao}")
    else:
        print("Nenhuma receita correspondente encontrada")
    
    assert melhor is not None, "Deveria ter encontrado uma receita"
    
    print("\n✅ Teste da melhor receita passou!")


def testar_sem_ingredientes():
    """Testa com lista vazia de ingredientes"""
    print("\n" + "="*60)
    print("TESTE 5: Lista Vazia de Ingredientes")
    print("="*60)
    
    receitas = criar_receitas_teste()
    ingredientes_usuario = []
    
    sugestoes = sugerir_receitas(receitas, ingredientes_usuario)
    
    print(f"\nSeus ingredientes: {ingredientes_usuario}")
    print(f"Sugestões: {len(sugestoes)}")
    
    assert len(sugestoes) == 0, "Não deveria ter sugestões com ingredientes vazios"
    
    print("\n✅ Teste de lista vazia passou!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTES DO SISTEMA DE SUGESTÃO DE RECEITAS")
    print("="*60)
    
    try:
        testar_compatibilidade()
        testar_sugestoes()
        testar_ingredientes_faltantes()
        testar_melhor_receita()
        testar_sem_ingredientes()
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ Teste falhou: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante testes: {e}")
        exit(1)
