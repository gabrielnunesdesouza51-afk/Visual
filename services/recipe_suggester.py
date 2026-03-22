"""
Serviço de sugestão inteligente de receitas baseado em ingredientes
Recomenda as melhores receitas baseado nos ingredientes que o usuário possui
"""
from typing import List, Tuple, Dict, Optional
from models.receita import Receita


def calcular_score_compatibilidade(ingredientes_usuario: List[str], 
                                   ingredientes_receita: List[str]) -> Tuple[float, int, int]:
    """
    Calcula um score de compatibilidade entre ingredientes do usuário e receita
    
    Args:
        ingredientes_usuario: Lista de ingredientes que o usuário tem
        ingredientes_receita: Lista de ingredientes da receita
        
    Returns:
        Tupla com (score_percentual, ingredientes_encontrados, faltantes)
    """
    if not ingredientes_receita:
        return 0.0, 0, 0
    
    ingredientes_usuario_lower = [ing.lower().strip() for ing in ingredientes_usuario]
    
    encontrados = 0
    faltantes = 0
    
    for ing_receita in ingredientes_receita:
        ing_receita_lower = ing_receita.lower().strip()
        
        # Busca o ingrediente ou partes dele
        if any(ing_receita_lower in ing_user or ing_user in ing_receita_lower 
               for ing_user in ingredientes_usuario_lower):
            encontrados += 1
        else:
            faltantes += 1
    
    total = len(ingredientes_receita)
    score = (encontrados / total) * 100 if total > 0 else 0
    
    return score, encontrados, faltantes


def sugerir_receitas(receitas: List[Receita], 
                     ingredientes_usuario: List[str],
                     limite: int = 5) -> List[Dict]:
    """
    Sugere receitas baseado nos ingredientes disponíveis
    
    Args:
        receitas: Lista de receitas disponíveis
        ingredientes_usuario: Lista de ingredientes que o usuário possui
        limite: Máximo de sugestões a retornar
        
    Returns:
        Lista de dicts com receitas sugeridas, ordenadas por compatibilidade
    """
    if not receitas or not ingredientes_usuario:
        return []
    
    sugestoes = []
    
    for receita in receitas:
        score, encontrados, faltantes = calcular_score_compatibilidade(
            ingredientes_usuario, 
            receita.ingredientes
        )
        
        # Só inclui receitas com pelo menos 30% de compatibilidade
        if score >= 30:
            sugestoes.append({
                'receita': receita,
                'score': score,
                'encontrados': encontrados,
                'faltantes': faltantes,
                'total_ingredientes': len(receita.ingredientes),
                'avaliacao_numeral': receita.avaliacao
            })
    
    # Ordena por score (descendente) e depois por avaliação (descendente)
    sugestoes.sort(key=lambda x: (x['score'], x['avaliacao_numeral']), reverse=True)
    
    return sugestoes[:limite]


def exibir_sugestoes(sugestoes: List[Dict]) -> None:
    """
    Exibe as sugestões de forma formatada e amigável
    
    Args:
        sugestoes: Lista de sugestões retornadas por sugerir_receitas()
    """
    if not sugestoes:
        print("\n❌ Nenhuma receita encontrada com seus ingredientes.")
        print("   Tente adicionar mais ingredientes!")
        return
    
    print("\n" + "="*70)
    print("  💡 RECEITAS SUGERIDAS PARA VOCÊ")
    print("="*70)
    
    for idx, sugestao in enumerate(sugestoes, 1):
        receita = sugestao['receita']
        score = sugestao['score']
        encontrados = sugestao['encontrados']
        faltantes = sugestao['faltantes']
        avaliacao_str = "⭐" * receita.avaliacao if receita.avaliacao > 0 else "⭐" * 3
        
        # Determina a cor/emoji baseado no score
        if score >= 80:
            emoji = "🔥"
            status = "EXCELENTE"
        elif score >= 60:
            emoji = "✨"
            status = "BOM"
        elif score >= 40:
            emoji = "👍"
            status = "POSSÍVEL"
        else:
            emoji = "📌"
            status = "PARCIAL"
        
        print(f"\n{idx}. {emoji} {receita.nome.upper()}")
        print(f"   Compatibilidade: {score:.0f}% {status}")
        print(f"   Ingredientes: {encontrados}/{sugestao['total_ingredientes']} disponíveis " 
              f"(faltam {faltantes})")
        print(f"   Tempo: {receita.tempo_preparo} min | Avaliação: {avaliacao_str}")
        print(f"   ID: {receita.id}")
    
    print("\n" + "="*70)
    print(f"   {len(sugestoes)} receita(s) sugerida(s)")
    print("="*70)


def listar_ingredientes_que_faltam(receeta: Receita, 
                                   ingredientes_usuario: List[str]) -> List[str]:
    """
    Lista quais ingredientes faltam para preparar uma receita
    
    Args:
        receita: Receita para verificar
        ingredientes_usuario: Ingredientes disponíveis
        
    Returns:
        Lista de ingredientes que faltam
    """
    ingredientes_usuario_lower = [ing.lower().strip() for ing in ingredientes_usuario]
    faltam = []
    
    for ing_receita in receeta.ingredientes:
        ing_receita_lower = ing_receita.lower().strip()
        
        if not any(ing_receita_lower in ing_user or ing_user in ing_receita_lower 
                   for ing_user in ingredientes_usuario_lower):
            faltam.append(ing_receita)
    
    return faltam


def calcular_melhor_receita(receitas: List[Receita], 
                           ingredientes_usuario: List[str]) -> Optional[Dict]:
    """
    Retorna a melhor receita de uma lista baseada em compatibilidade e avaliação
    
    Args:
        receitas: Lista de receitas
        ingredientes_usuario: Ingredientes disponíveis
        
    Returns:
        Dict com melhor receita ou None se não houver
    """
    sugestoes = sugerir_receitas(receitas, ingredientes_usuario, limite=1)
    return sugestoes[0] if sugestoes else None
