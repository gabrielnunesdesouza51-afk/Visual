"""
Modelo de Receita com validação de dados
"""
from datetime import datetime
from typing import List, Dict

class Receita:
    """Classe que representa uma receita culinária"""
    
    def __init__(self, id: int, nome: str, categoria: str, ingredientes: List[str],
                 modo_preparo: str, porcoes: int, tempo_preparo: int,
                 avaliacao: int = 0, calorias: int = 0, favorita: bool = False,
                 data: str = None):
        """
        Inicializa uma receita
        
        Args:
            id: Identificador único
            nome: Nome da receita
            categoria: Categoria (Doce, Salgado, etc)
            ingredientes: Lista de ingredientes
            modo_preparo: Modo de preparação
            porcoes: Número de porções
            tempo_preparo: Tempo em minutos
            avaliacao: Nota de 0-5
            calorias: Total de calorias
            favorita: Se é uma receita favorita
            data: Data de criação
        """
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo
        self.porcoes = porcoes
        self.tempo_preparo = tempo_preparo
        self.avaliacao = avaliacao
        self.calorias = calorias
        self.favorita = favorita
        self.data = data or datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def para_dict(self) -> Dict:
        """Converte a receita para um dicionário (para JSON)"""
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "ingredientes": self.ingredientes,
            "modo_preparo": self.modo_preparo,
            "porcoes": self.porcoes,
            "tempo_preparo": self.tempo_preparo,
            "avaliacao": self.avaliacao,
            "calorias": self.calorias,
            "favorita": self.favorita,
            "data": self.data
        }
    
    @staticmethod
    def do_dict(dados: Dict) -> 'Receita':
        """Cria uma receita a partir de um dicionário com robustez"""
        # Campos obrigatórios
        try:
            id_val = dados.get('id')
            nome_val = dados.get('nome')
            categoria_val = dados.get('categoria')
            ingredientes_val = dados.get('ingredientes', [])
            modo_preparo_val = dados.get('modo_preparo')
            porcoes_val = dados.get('porcoes')
            tempo_preparo_val = dados.get('tempo_preparo')
            
            # Validar campos obrigatórios
            if not all([id_val is not None, nome_val, categoria_val, 
                       ingredientes_val, modo_preparo_val, 
                       porcoes_val is not None, tempo_preparo_val is not None]):
                raise ValueError("Campos obrigatórios ausentes ou inválidos")
            
            # Campos opcionais com defaults
            avaliacao_val = dados.get('avaliacao', 0)
            calorias_val = dados.get('calorias', 0)
            favorita_val = dados.get('favorita', False)
            data_val = dados.get('data')
            
            # Validar tipos
            if not isinstance(ingredientes_val, list):
                ingredientes_val = [str(ingredientes_val)]
            
            if not isinstance(avaliacao_val, int):
                avaliacao_val = 0
            
            if not isinstance(calorias_val, int):
                calorias_val = 0
            
            if not isinstance(favorita_val, bool):
                favorita_val = False
            
            return Receita(
                id=int(id_val),
                nome=str(nome_val),
                categoria=str(categoria_val),
                ingredientes=[str(ing) for ing in ingredientes_val],
                modo_preparo=str(modo_preparo_val),
                porcoes=int(porcoes_val),
                tempo_preparo=int(tempo_preparo_val),
                avaliacao=avaliacao_val,
                calorias=calorias_val,
                favorita=favorita_val,
                data=data_val
            )
        except (ValueError, TypeError, KeyError) as e:
            raise ValueError(f"Erro ao converter dicionário para Receita: {e}")
    
    def __repr__(self):
        return f"<Receita(id={self.id}, nome={self.nome}, categoria={self.categoria})>"
