"""
Módulo de persistência de dados em JSON
"""
import json
import os
from typing import List
from models.receita import Receita

# Tenta múltiplos locais para encontrar o arquivo
ARQUIVO_RECEITAS = "receitas.json"
LOCAIS_POSSIVEIS = [
    "receitas.json",
    "data/receitas.json",
    "./receitas.json",
    os.path.join(os.path.dirname(__file__), "..", "receitas.json"),
    os.path.join(os.path.dirname(__file__), "..", "data", "receitas.json")
]

def _encontrar_arquivo():
    """Encontra o arquivo de receitas em locais possíveis"""
    for local in LOCAIS_POSSIVEIS:
        if os.path.exists(local):
            return local
    return ARQUIVO_RECEITAS  # Retorna padrão se nenhum encontrado

ARQUIVO_RECEITAS = _encontrar_arquivo()

def carregar_receitas() -> List[Receita]:
    """
    Carrega receitas do arquivo JSON com robustez
    
    Returns:
        List[Receita]: Lista de receitas carregadas (vazio se nenhuma encontrada)
    """
    try:
        arquivo_correto = _encontrar_arquivo()
        
        if not os.path.exists(arquivo_correto):
            return []
        
        with open(arquivo_correto, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            
            if not isinstance(dados, list):
                print(f" ⚠️  Aviso: Formato JSON inesperado em {arquivo_correto}")
                return []
            
            # Validar e converter cada receita com robustez
            receitas = []
            for item in dados:
                try:
                    receita = Receita.do_dict(item)
                    receitas.append(receita)
                except (KeyError, TypeError, ValueError) as e:
                    print(f" ⚠️  Aviso: Erro ao carregar receita: {e}")
                    continue
            
            return receitas
            
    except json.JSONDecodeError as e:
        print(f" ❌ Erro: JSON inválido em {arquivo_correto}: {e}")
        return []
    except IOError as e:
        print(f" ❌ Erro ao ler arquivo: {e}")
        return []
    except Exception as e:
        print(f" ❌ Erro inesperado ao carregar receitas: {e}")
        return []

def salvar_receitas(receitas: List[Receita]) -> bool:
    """
    Salva receitas no arquivo JSON com robustez
    
    Args:
        receitas: Lista de receitas a salvar
        
    Returns:
        bool: True se sucesso, False caso contrário
    """
    try:
        arquivo_correto = _encontrar_arquivo()
        
        # Criar diretório se não existir
        diretorio = os.path.dirname(arquivo_correto)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)
        
        dados = [receita.para_dict() for receita in receitas]
        
        with open(arquivo_correto, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        return True
        
    except IOError as e:
        print(f" ❌ Erro ao salvar receitas: {e}")
        return False
    except Exception as e:
        print(f" ❌ Erro inesperado ao salvar: {e}")
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


def criar_receitas_iniciais() -> List[Receita]:
    """
    Cria um conjunto de receitas iniciais para demonstração
    
    Returns:
        List[Receita]: Lista com receitas iniciais
    """
    receitas_init = [
        Receita(
            id=1,
            nome="Brigadeiro Clássico",
            categoria="Sobremesa",
            ingredientes=["leite condensado", "chocolate em pó", "manteiga", "chocolate granulado"],
            modo_preparo="Misture leite condensado, chocolate em pó e manteiga em uma panela. Cozinhe em fogo médio, mexendo sempre até desgrudar da panela. Coloque em prato manteigado, esfrie e passe na manteiga e chocolate. Enrole em papel e refrigere.",
            porcoes=20,
            tempo_preparo=20,
            avaliacao=5,
            calorias=150
        ),
        Receita(
            id=2,
            nome="Macarrão à Carbonara",
            categoria="Salgado",
            ingredientes=["macarrão", "ovos", "bacon", "queijo pecorino", "sal", "pimenta preta"],
            modo_preparo="Cozinhe o macarrão. Enquanto isso, frite o bacon cortado. Bata os ovos com queijo ralado. Misture o macarrão quente com o bacon, tire do fogo e adicione a mistura de ovo. Tempere com sal e pimenta.",
            porcoes=4,
            tempo_preparo=30,
            avaliacao=4,
            calorias=400
        ),
        Receita(
            id=3,
            nome="Bolo de Chocolate",
            categoria="Doce",
            ingredientes=["farinha de trigo", "açúcar", "ovos", "chocolate em pó", "leite", "óleo", "fermento"],
            modo_preparo="Misture os ingredientes secos. Em outra tigela, bata os ovos com leite e óleo. Combine as misturas. Despeje em forma untada e asse a 180°C por 40-45 minutos.",
            porcoes=12,
            tempo_preparo=60,
            avaliacao=4,
            calorias=250
        )
    ]
    return receitas_init
