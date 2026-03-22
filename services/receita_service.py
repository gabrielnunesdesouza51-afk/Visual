"""
Serviços de negócio para gerenciamento de receitas
"""
import re
from typing import List, Optional, Tuple
from models.receita import Receita
from utils.storage import salvar_receitas, proxima_id

# Tabela de calorias por ingrediente
TABELA_CALORIAS = {
    "ovo": 70, "ovos": 70, "leite": 60, "açúcar": 400, "farinha": 360,
    "manteiga": 717, "óleo": 884, "sal": 0, "pão": 250, "presunto": 145,
    "queijo": 400, "tomate": 18, "alface": 15, "cebola": 40, "alho": 149,
    "frango": 165, "carne": 250, "peixe": 100, "arroz": 130, "feijão": 76,
    "batata": 77, "cenoura": 41, "maçã": 52, "banana": 89, "chocolate": 535,
    "café": 0, "chá": 0, "agua": 0, "pimenta": 251
}

def validar_numero(valor: str, minimo: int = 0, maximo: int = None) -> Optional[int]:
    """
    Valida se um valor é um número válido
    
    Args:
        valor: String a validar
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
        
    Returns:
        int ou None se inválido
    """
    try:
        num = int(valor)
        if num >= minimo and (maximo is None or num <= maximo):
            return num
        return None
    except ValueError:
        return None

def selecionar_receita(receitas: List[Receita], acao: str = "selecionar") -> Optional[Receita]:
    """
    Permite ao usuário selecionar uma receita pelo ID
    
    Args:
        receitas: Lista de receitas disponíveis
        acao: Ação a realizar (para mensagem)
        
    Returns:
        Receita ou None se cancelado
    """
    if not receitas:
        print("\n Nenhuma receita disponível!")
        return None
    
    exibir_lista_simples(receitas)
    
    while True:
        entrada = input(f"\nDigite o ID da receita para {acao} (0 para cancelar): ")
        
        if entrada == "0":
            return None
        
        id_receita = validar_numero(entrada)
        if id_receita is None:
            print(" ID inválido!")
            continue
        
        for receita in receitas:
            if receita.id == id_receita:
                return receita
        
        print(f" Receita com ID {id_receita} não encontrada!")

def exibir_lista_simples(receitas: List[Receita]) -> None:
    """Exibe lista resumida de receitas"""
    # DEBUG: Validar entrada
    print(f"\n[DEBUG] exibir_lista_simples() recebeu:")
    print(f"[DEBUG] - Tipo: {type(receitas).__name__}")
    print(f"[DEBUG] - Total: {len(receitas)} receitas")
    
    if not receitas:
        print("\n❌ Nenhuma receita registrada!")
        return
    
    print(f"\n[DEBUG] Iterando sobre lista para exibir...")
    print(f"\n{'ID':<4} {'Nome':<25} {'Categoria':<15} {'':<4} {'':<6}")
    print("-" * 70)
    
    contagem = 0
    for r in receitas:
        contagem += 1
        # DEBUG: Validar tipo de cada item
        if not isinstance(r, Receita):
            print(f"[DEBUG] ⚠️  Item {contagem} não é Receita, é {type(r).__name__}")
            continue
        
        estrela = f"{'⭐' * r.avaliacao}" if r.avaliacao > 0 else ""
        nome_trunc = r.nome[:24] if len(r.nome) > 24 else r.nome
        tempo_str = f"{r.tempo_preparo}min"
        print(f"{r.id:<4} {nome_trunc:<25} {r.categoria:<15} {estrela:<4} {tempo_str:<6}")
    
    print(f"\n[DEBUG] Iteração completa: {contagem} receitas exibidas")

def extrair_quantidade(ingrediente: str) -> Tuple[int, str]:
    """
    Extrai a quantidade de um ingrediente (ex: '2 ovos' -> (2, 'ovos'))
    
    Args:
        ingrediente: String do ingrediente
        
    Returns:
        Tupla (quantidade, ingrediente_limpo)
    """
    match = re.match(r'(\d+)\s*([a-záàâãéèêíïóôõöúçñA-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+)', ingrediente.strip())
    
    if match:
        quantidade = int(match.group(1))
        nome = match.group(2).strip()
        return quantidade, nome
    
    return 1, ingrediente.strip()

def calcular_calorias_ingrediente(ingrediente: str) -> int:
    """
    Calcula calorias de um ingrediente
    
    Args:
        ingrediente: Nome do ingrediente
        
    Returns:
        int: Calorias estimadas
    """
    quantidade, nome = extrair_quantidade(ingrediente)
    nome_lower = nome.lower()
    
    for chave, valor in TABELA_CALORIAS.items():
        if chave in nome_lower:
            return valor * quantidade
    
    # Se não encontrar, retorna estimativa baseada em tipo
    if any(x in nome_lower for x in ['verdura', 'vegetál', 'legume', 'alface']):
        return 20 * quantidade
    elif any(x in nome_lower for x in ['carne', 'frango', 'peixe']):
        return 150 * quantidade
    elif any(x in nome_lower for x in ['doce', 'açúcar', 'chocolate']):
        return 300 * quantidade
    
    return 100 * quantidade  # Padrão

def gerar_lista_compras_agregada(receitas_selecionadas: List[Receita]) -> dict:
    """
    Gera lista de compras com ingredientes agregados
    
    Args:
        receitas_selecionadas: Receitas para gerar lista
        
    Returns:
        Dict com ingredientes agregados
    """
    ingredientes_dict = {}
    
    for receita in receitas_selecionadas:
        for ingrediente in receita.ingredientes:
            quantidade, nome = extrair_quantidade(ingrediente)
            
            if nome in ingredientes_dict:
                ingredientes_dict[nome] += quantidade
            else:
                ingredientes_dict[nome] = quantidade
    
    return ingredientes_dict

def filtrar_receitas(receitas: List[Receita], criterio: str, valor) -> List[Receita]:
    """
    Filtra receitas por diferentes critérios
    
    Args:
        receitas: Lista de receitas
        criterio: Tipo de filtro ('tempo', 'categoria', 'nome', 'rating')
        valor: Valor a filtrar
        
    Returns:
        Lista de receitas filtradas
    """
    if criterio == 'tempo':
        return [r for r in receitas if r.tempo_preparo <= valor]
    elif criterio == 'categoria':
        return [r for r in receitas if r.categoria.lower() == valor.lower()]
    elif criterio == 'nome':
        return [r for r in receitas if valor.lower() in r.nome.lower()]
    elif criterio == 'favorita':
        return [r for r in receitas if r.favorita]
    elif criterio == 'rating':
        return sorted([r for r in receitas if r.avaliacao > 0], 
                     key=lambda x: x.avaliacao, reverse=True)
    
    return receitas

def top_receitas(receitas: List[Receita], quantidade: int = 5) -> List[Receita]:
    """
    Retorna as receitas melhor avaliadas
    
    Args:
        receitas: Lista de receitas
        quantidade: Quantas receitas retornar
        
    Returns:
        Lista das melhores receitas
    """
    com_avaliacao = [r for r in receitas if r.avaliacao > 0]
    return sorted(com_avaliacao, key=lambda x: x.avaliacao, reverse=True)[:quantidade]

def confirmar_acao(mensagem: str = "Tem certeza?") -> bool:
    """
    Pede confirmação do usuário
    
    Args:
        mensagem: Mensagem de confirmação
        
    Returns:
        bool: True se confirmou
    """
    while True:
        resposta = input(f"\n{mensagem} (s/n): ").lower().strip()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'não', 'nao']:
            return False
        else:
            print(" Digite 's' para sim ou 'n' para não!")
