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
        """Cria uma receita a partir de um dicionário"""
        return Receita(
            id=dados['id'],
            nome=dados['nome'],
            categoria=dados['categoria'],
            ingredientes=dados['ingredientes'],
            modo_preparo=dados['modo_preparo'],
            porcoes=dados['porcoes'],
            tempo_preparo=dados['tempo_preparo'],
            avaliacao=dados.get('avaliacao', 0),
            calorias=dados.get('calorias', 0),
            favorita=dados.get('favorita', False),
            data=dados.get('data')
        )
    
    def __repr__(self):
        return f"<Receita(id={self.id}, nome={self.nome}, categoria={self.categoria})>"
