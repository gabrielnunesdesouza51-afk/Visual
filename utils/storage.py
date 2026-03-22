"""
Módulo de persistência de dados em JSON
"""
import json
import os
from typing import List
from models.receita import Receita

ARQUIVO_RECEITAS = "receitas.json"

def carregar_receitas() -> List[Receita]:
    """
    Carrega receitas do arquivo JSON
    
    Returns:
        List[Receita]: Lista de receitas carregadas
    """
    try:
        if os.path.exists(ARQUIVO_RECEITAS):
            with open(ARQUIVO_RECEITAS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return [Receita.do_dict(item) for item in dados]
        return []
    except (json.JSONDecodeError, IOError) as e:
        print(f" Erro ao carregar receitas: {e}")
        return []

def salvar_receitas(receitas: List[Receita]) -> bool:
    """
    Salva receitas no arquivo JSON
    
    Args:
        receitas: Lista de receitas a salvar
        
    Returns:
        bool: True se sucesso, False caso contrário
    """
    try:
        dados = [receita.para_dict() for receita in receitas]
        with open(ARQUIVO_RECEITAS, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f" Erro ao salvar receitas: {e}")
        return False

def proxima_id(receitas: List[Receita]) -> int:
    """
    Calcula o próximo ID disponível
    
    Args:
        receitas: Lista de receitas atuais
        
    Returns:
        int: Próximo ID disponível
    """
    if not receitas:
        return 1
    return max(r.id for r in receitas) + 1
