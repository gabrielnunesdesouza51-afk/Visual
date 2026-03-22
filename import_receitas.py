"""
Script para importar receitas de um dataset público para o Gerenciador de Receitas
Sem necessidade de APIs pagas ou autenticação
"""
import sys
import os
import json
import csv
from datetime import datetime
from pathlib import Path

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.receita import Receita
from utils.storage import salvar_receitas, carregar_receitas, proxima_id

# ==================== DATASET DE RECEITAS REAIS ====================
# Receitas brasileiras e internacionais populares para popular o app
RECEITAS_PADRAO = [
    {
        "nome": "Brigadeiro Clássico",
        "categoria": "Sobremesa",
        "ingredientes": ["leite condensado", "chocolate em pó", "manteiga", "chocolate granulado"],
        "modo_preparo": "Misture leite condensado, chocolate em pó e manteiga em uma panela. Cozinhe em fogo médio, mexendo sempre até desgrudar da panela. Coloque em prato manteigado, esfrie e passe na manteiga e chocolate. Enrole em papel e refrigere.",
        "porcoes": 20,
        "tempo_preparo": 20,
        "categoria_culinaria": "Sobremesa"
    },
    {
        "nome": "Feijoada à Brasileira",
        "categoria": "Salgado",
        "ingredientes": ["feijão preto", "carne seca", "costela de porco", "linguiça", "bacon", "cebola", "alho", "louro", "sal"],
        "modo_preparo": "Cozinhe o feijão até ficar macio. Em outra panela, refogue cebola e alho, adicione as carnes e refogue bem. Misture o feijão cozido com a carne, tempere com sal e folhas de louro. Deixe cozinhar por 1 hora em fogo baixo.",
        "porcoes": 8,
        "tempo_preparo": 180,
        "categoria_culinaria": "Salgado"
    },
    {
        "nome": "Bolo de Chocolate",
        "categoria": "Doce",
        "ingredientes": ["2 xícaras farinha de trigo", "2 xícaras açúcar", "4 ovos", "1 xícara chocolate em pó", "1 xícara leite", "1/2 xícara óleo", "1 colher sopa fermento"],
        "modo_preparo": "Misture os ingredientes secos (farinha, açúcar, chocolate, fermento). Em outra tigela, bata os ovos com leite e óleo. Combine as duas misturas. Despeje em forma untada e asse a 180°C por 40-45 minutos.",
        "porcoes": 12,
        "tempo_preparo": 60,
        "categoria_culinaria": "Doce"
    },
    {
        "nome": "Macarrão à Carbonara",
        "categoria": "Salgado",
        "ingredientes": ["macarrão", "ovos", "bacon", "queijo pecorino", "sal", "pimenta preta"],
        "modo_preparo": "Cozinhe o macarrão. Enquanto isso, frite o bacon cortado. Bata os ovos com queijo ralado. Misture o macarrão quente com o bacon, tire do fogo e adicione a mistura de ovo. Tempere com sal e pimenta.",
        "porcoes": 4,
        "tempo_preparo": 30,
        "categoria_culinaria": "Salgado"
    },
    {
        "nome": "Bruschetta Italiana",
        "categoria": "Aperitivo",
        "ingredientes": ["pão italiano", "tomate fresco", "alho", "manjericão", "azeite", "sal", "pimenta"],
        "modo_preparo": "Corte o pão e toste no forno. Passe alho fresco nas fatias. Misture tomate cortado com alho, manjericão e azeite. Coloque sobre o pão tostado. Tempere com sal e pimenta.",
        "porcoes": 6,
        "tempo_preparo": 15,
        "categoria_culinaria": "Aperitivo"
    },
    {
        "nome": "Sushi de Salmão",
        "categoria": "Japonês",
        "ingredientes": ["arroz para sushi", "alga nori", "salmão fresco", "abacate", "cenoura", "pepino", "gengibre", "wasabi", "molho de soja"],
        "modo_preparo": "Cozinhe o arroz e tempere com vinagre de arroz. Coloque o alga nori em um tapete de bambu, espalhe o arroz, adicione os ingredientes no centro e enrole firmemente. Corte com faca molhada.",
        "porcoes": 6,
        "tempo_preparo": 45,
        "categoria_culinaria": "Japonês"
    },
    {
        "nome": "Frango Parmegiana",
        "categoria": "Salgado",
        "ingredientes": ["peito de frango", "molho de tomate", "queijo mozzarela", "queijo parmesão", "farinha de trigo", "ovo", "óleo", "sal"],
        "modo_preparo": "Bata o frango, passe em ovo e farinha, frite. Coloque em refratário, cubra com molho de tomate e queijo. Asse a 180°C por 20 minutos até ficar gratin.",
        "porcoes": 4,
        "tempo_preparo": 50,
        "categoria_culinaria": "Salgado"
    },
    {
        "nome": "Pavê de Chocolate",
        "categoria": "Sobremesa",
        "ingredientes": ["biscoito doce", "chocolate em pó", "achocolatado em pó", "leite", "manteiga", "açúcar"],
        "modo_preparo": "Misture achocolatado com leite. Mergulhe biscoitos nesta mistura e alterne camadas com creme de chocolate. Finalize com chocolate em pó ralado. Refrigere por 4 horas.",
        "porcoes": 8,
        "tempo_preparo": 30,
        "categoria_culinaria": "Sobremesa"
    },
    {
        "nome": "Salada Grega",
        "categoria": "Salada",
        "ingredientes": ["tomate", "pepino", "cebola roxa", "azeitona preta", "queijo feta", "azeite", "orégano", "sal", "limão"],
        "modo_preparo": "Corte os vegetais em cubos. Misture com azeitona, queijo feta cortado, azeite, suco de limão e orégano. Tempere com sal. Coma gelado como entrada ou acompanhamento.",
        "porcoes": 4,
        "tempo_preparo": 15,
        "categoria_culinaria": "Salada"
    },
    {
        "nome": "Ratatouille Provençal",
        "categoria": "Vegetariano",
        "ingredientes": ["berinjela", "abobrinha", "tomate", "pimentão", "cebola", "alho", "azeite", "tomilho", "sal"],
        "modo_preparo": "Corte os vegetais em rodelas. Refogue cebola e alho em azeite, adicione os vegetais em camadas, tempere com tomilho, sal e pimenta. Cozinhe em fogo baixo por 45 minutos.",
        "porcoes": 6,
        "tempo_preparo": 60,
        "categoria_culinaria": "Vegetariano"
    },
    {
        "nome": "Tarta de Maçã",
        "categoria": "Doce",
        "ingredientes": ["massa podre pronta", "maçã", "açúcar", "canela", "suco de limão", "farinha de amêndoa", "manteiga"],
        "modo_preparo": "Forneie a massa. Fatiar maçãs, tempere com canela, suco de limão e açúcar. Arrume na massa em camadas. Polvilhe farinha de amêndoa e manteiga em dots. Asse a 200°C por 35-40 minutos.",
        "porcoes": 8,
        "tempo_preparo": 70,
        "categoria_culinaria": "Doce"
    }
]

# ==================== FUNÇÕES ====================

def importar_receitas_padrao() -> int:
    """
    Importa as receitas padrão incluídas no script
    
    Returns:
        int: Número de receitas importadas
    """
    print("\n" + "="*70)
    print("📥 IMPORTANDO RECEITAS PADRÃO")
    print("="*70)
    
    receitas_existentes = carregar_receitas()
    proximo_id = proxima_id(receitas_existentes)
    
    receitas_importadas = []
    
    for receita_dados in RECEITAS_PADRAO:
        try:
            receita = Receita(
                id=proximo_id,
                nome=receita_dados.get("nome", "Receita sem nome"),
                categoria=receita_dados.get("categoria", "Outro"),
                ingredientes=receita_dados.get("ingredientes", []),
                modo_preparo=receita_dados.get("modo_preparo", "Sem instruções"),
                porcoes=receita_dados.get("porcoes", 1),
                tempo_preparo=receita_dados.get("tempo_preparo", 0),
                avaliacao=0,
                calorias=0,
                favorita=False,
                data=datetime.now().strftime("%d/%m/%Y %H:%M")
            )
            
            receitas_importadas.append(receita)
            proximo_id += 1
            
            print(f"  ✅ {receita.nome} ({receita.tempo_preparo} min)")
            
        except Exception as e:
            print(f"  ❌ Erro ao processar receita: {e}")
    
    if receitas_importadas:
        todas_receitas = receitas_existentes + receitas_importadas
        if salvar_receitas(todas_receitas):
            print(f"\n✅ {len(receitas_importadas)} receita(s) importada(s) com sucesso!")
            print(f"📊 Total de receitas no app: {len(todas_receitas)}")
            return len(receitas_importadas)
        else:
            print("\n❌ Erro ao salvar receitas")
            return 0
    
    return 0

def importar_de_csv(arquivo_csv: str) -> int:
    """
    Importa receitas de um arquivo CSV
    
    Esperado: coluna 'name' ou 'nome', 'ingredients' ou 'ingredientes', 
              'instructions' ou 'modo_preparo'
    
    Args:
        arquivo_csv: Caminho do arquivo CSV
        
    Returns:
        int: Número de receitas importadas
    """
    if not os.path.exists(arquivo_csv):
        print(f"❌ Arquivo não encontrado: {arquivo_csv}")
        return 0
    
    print(f"\n📖 Lendo arquivo: {arquivo_csv}")
    
    receitas_existentes = carregar_receitas()
    proximo_id = proxima_id(receitas_existentes)
    receitas_importadas = []
    
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            
            for linha in leitor:
                try:
                    # Tenta diferentes nomes de coluna
                    nome = linha.get('name') or linha.get('nome') or linha.get('title')
                    
                    if not nome:
                        continue
                    
                    ingredientes_str = linha.get('ingredients') or linha.get('ingredientes') or ""
                    if isinstance(ingredientes_str, str):
                        # Se for string, tenta dividir por vírgula ou quebra de linha
                        ingredientes = [i.strip() for i in ingredientes_str.replace('\n', ',').split(',') if i.strip()]
                    else:
                        ingredientes = [str(ingredientes_str).strip()]
                    
                    modo_preparo = linha.get('instructions') or linha.get('modo_preparo') or "Sem instruções"
                    
                    tempo_str = linha.get('minutes') or linha.get('tempo_preparo') or "0"
                    try:
                        tempo_preparo = int(tempo_str)
                    except:
                        tempo_preparo = 0
                    
                    porcoes_str = linha.get('servings') or linha.get('porcoes') or "1"
                    try:
                        porcoes = int(porcoes_str)
                    except:
                        porcoes = 1
                    
                    categoria = linha.get('category') or linha.get('cuisine') or linha.get('categoria') or "Outro"
                    
                    receita = Receita(
                        id=proximo_id,
                        nome=nome,
                        categoria=categoria,
                        ingredientes=ingredientes,
                        modo_preparo=modo_preparo,
                        porcoes=porcoes,
                        tempo_preparo=tempo_preparo,
                        data=datetime.now().strftime("%d/%m/%Y %H:%M")
                    )
                    
                    receitas_importadas.append(receita)
                    proximo_id += 1
                    print(f"  ✅ {receita.nome}")
                    
                except Exception as e:
                    print(f"  ⚠️ Erro em linha: {e}")
                    continue
        
        if receitas_importadas:
            todas_receitas = receitas_existentes + receitas_importadas
            if salvar_receitas(todas_receitas):
                print(f"\n✅ {len(receitas_importadas)} receita(s) importada(s) do CSV!")
                return len(receitas_importadas)
        
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
    
    return 0

def importar_de_json(arquivo_json: str) -> int:
    """
    Importa receitas de um arquivo JSON
    
    Args:
        arquivo_json: Caminho do arquivo JSON
        
    Returns:
        int: Número de receitas importadas
    """
    if not os.path.exists(arquivo_json):
        print(f"❌ Arquivo não encontrado: {arquivo_json}")
        return 0
    
    print(f"\n📖 Lendo arquivo: {arquivo_json}")
    
    receitas_existentes = carregar_receitas()
    proximo_id = proxima_id(receitas_existentes)
    receitas_importadas = []
    
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            
            # Se for lista de objetos
            if isinstance(dados, list):
                items = dados
            else:
                # Se for um objeto com uma chave de lista
                items = dados.get('recipes') or dados.get('receitas') or [dados]
            
            for item in items:
                try:
                    nome = item.get('name') or item.get('nome') or item.get('title')
                    
                    if not nome:
                        continue
                    
                    ingredientes = item.get('ingredients') or item.get('ingredientes') or []
                    if isinstance(ingredientes, str):
                        ingredientes = [i.strip() for i in ingredientes.split(',') if i.strip()]
                    
                    modo_preparo = item.get('instructions') or item.get('modo_preparo') or "Sem instruções"
                    tempo_preparo = int(item.get('minutes') or item.get('tempo_preparo') or 0)
                    porcoes = int(item.get('servings') or item.get('porcoes') or 1)
                    categoria = item.get('category') or item.get('cuisine') or item.get('categoria') or "Outro"
                    
                    receita = Receita(
                        id=proximo_id,
                        nome=nome,
                        categoria=categoria,
                        ingredientes=ingredientes,
                        modo_preparo=modo_preparo,
                        porcoes=porcoes,
                        tempo_preparo=tempo_preparo,
                        data=datetime.now().strftime("%d/%m/%Y %H:%M")
                    )
                    
                    receitas_importadas.append(receita)
                    proximo_id += 1
                    print(f"  ✅ {receita.nome}")
                    
                except Exception as e:
                    print(f"  ⚠️ Erro ao processar item: {e}")
                    continue
        
        if receitas_importadas:
            todas_receitas = receitas_existentes + receitas_importadas
            if salvar_receitas(todas_receitas):
                print(f"\n✅ {len(receitas_importadas)} receita(s) importada(s) do JSON!")
                return len(receitas_importadas)
        
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
    
    return 0

def exibir_menu():
    """Exibe menu de importação"""
    print("\n" + "="*70)
    print("🍳 IMPORTADOR DE RECEITAS - GERENCIADOR DE RECEITAS")
    print("="*70)
    print("\nEscolha uma opção:\n")
    print("  1️⃣  Importar receitas padrão (11 receitas incluídas)")
    print("  2️⃣  Importar de arquivo CSV")
    print("  3️⃣  Importar de arquivo JSON")
    print("  0️⃣  Sair")
    print("\n" + "="*70)

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("  🍳 BEM-VINDO AO IMPORTADOR DE RECEITAS 👨‍🍳")
    print("="*70)
    print("\nEste script importa receitas para seu Gerenciador de Receitas")
    print("a partir de datasets públicos e gratuitos.\n")
    
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            importar_receitas_padrao()
            input("\n\nPressione ENTER para continuar...")
            
        elif opcao == "2":
            caminho = input("\nDigite o caminho do arquivo CSV: ").strip()
            if caminho:
                importar_de_csv(caminho)
            input("\n\nPressione ENTER para continuar...")
            
        elif opcao == "3":
            caminho = input("\nDigite o caminho do arquivo JSON: ").strip()
            if caminho:
                importar_de_json(caminho)
            input("\n\nPressione ENTER para continuar...")
            
        elif opcao == "0":
            print("\n👋 Até logo!\n")
            break
            
        else:
            print("\n❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
