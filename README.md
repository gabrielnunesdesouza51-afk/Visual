# Gerenciador de Receitas - Sistema Profissional

Um aplicativo CLI (Command Line Interface) profissional para gerenciar receitas culinárias com arquitetura escalável e modular.

## Arquitetura do Projeto

O projeto foi refatorado em uma estrutura profissional com separação clara de responsabilidades:

```
project/
├── models/
│   ├── __init__.py
│   └── receita.py           # Classe de modelo para Receita
├── services/
│   ├── __init__.py
│   └── receita_service.py   # Lógica de negócio e funções reutilizáveis
├── utils/
│   ├── __init__.py
│   └── storage.py           # Persistência de dados em JSON
├── main.py                   # Aplicação principal e CLI
└── receitas.json            # Arquivo de dados (criado automaticamente)
```

## Componentes Principais

### 1. **models/receita.py**
Classe `Receita` que representa uma receita culinária com:
- Atributos: id, nome, categoria, ingredientes, modo_preparo, porcoes, tempo_preparo, avaliacao, calorias, favorita, data
- Métodos: `para_dict()` (serialização), `do_dict()` (desserialização), `__repr__()`
- Type hints completos

### 2. **utils/storage.py**
Camada de persistência com funções:
- `carregar_receitas()`: Carrega receitas do JSON
- `salvar_receitas()`: Salva receitas no JSON
- `proxima_id()`: Gera próximo ID disponível
- Tratamento robusto de erros

### 3. **services/receita_service.py**
Serviços e lógica de negócio:
- **Validação**: `validar_numero()` com range checking
- **Seleção**: `selecionar_receita()` com interface interativa
- **Display**: `exibir_lista_simples()` com formatação em tabela
- **Processamento**: 
  - `extrair_quantidade()` - Parse de quantidades (ex: "2 ovos" → 2x ovos)
  - `calcular_calorias_ingrediente()` - Cálculo com tabela e fallback estimativas
  - `gerar_lista_compras_agregada()` - Agregação de ingredientes
- **Filtragem**: `filtrar_receitas()` com múltiplos critérios
- **Top**: `top_receitas()` - Receitas melhores avaliadas
- **Confirmação**: `confirmar_acao()` - Loop de confirmação do usuário

**Tabela de Calorias**: 25+ ingredientes com valores padrão

### 4. **main.py**
Aplicação CLI com 16 operações:

**GERENCIAR (1-5)**:
- ✅ Adicionar receita com validação
- ✅ Listar todas as receitas
- ✅ Ver detalhes completos
- ✅ Editar receita existente
- ✅ Deletar receita (com confirmação)

**BUSCAR E FILTRAR (6-9)**:
- ✅ Buscar por ingrediente
- ✅ Buscar por nome
- ✅ Listar por categoria
- ✅ Filtrar por tempo de preparo

**ANÁLISE (10-15)**:
- ✅ Avaliar receita (1-5 estrelas)
- ✅ Calcular calorias (total e por porção)
- ✅ Gerar lista de compras (com agregação e arquivo)
- ✅ Top receitas (melhores avaliadas)
- ✅ Favoritar/Desfavoritar
- ✅ Listar favoritas

## Melhorias Implementadas

1. **OOP Design**: Classe `Receita` replaces dictionaries
2. **Type Hints**: Tipagem em todas as funções
3. **Validação**: Input validation com retry loops
4. **Reutilização**: Helper functions em service layer
5. **Calorias Aprimoradas**: 
   - Parser de quantidade com regex
   - Tabela de 25+ ingredientes
   - Estimativas por categoria (verduras, carnes, doces)
6. **Lista de Compras Inteligente**: Agregação automática de quantidades
7. **Emojis UX**: ⭐ para avaliações, ❤️ para favoritas
8. **Confirmação Delete**: Proteção contra exclusões acidentais
9. **Persistência**: Arquivo JSON com error handling
10. **Code Style**: Docstrings, comentários, formatação profissional

## Uso

```bash
# Executar aplicação
python main.py

# Testar imports
python test_imports.py

# Validar sintaxe
python test_syntax.py
```

## Estrutura de Dados (receitas.json)

```json
[
  {
    "id": 1,
    "nome": "Bolo de Chocolate",
    "categoria": "Doce",
    "ingredientes": ["2 ovos", "100g farinha"],
    "modo_preparo": "Misture e asse...",
    "porcoes": 4,
    "tempo_preparo": 30,
    "avaliacao": 5,
    "calorias": 1200,
    "favorita": true,
    "data": "15/01/2024 10:30"
  }
]
```

## Funcionalidades Avançadas

- **Agregação de Ingredientes**: Combines "2 ovos" + "3 ovos" = "5 ovos"
- **Cálculo de Calorias**: Multiplica quantidade × valor calórico
- **Multi-Critério Filtragem**: tempo, categoria, nome, rating, favorita
- **Export Lista Compras**: Arquivo txt com timestamp
- **Avaliação em Estrelas**: 1-5 com display visual ⭐

## Próximos Passos

Possíveis melhorias futuras:
- [ ] Banco de dados (SQLite/PostgreSQL)
- [ ] Interface gráfica (Tkinter/PyQt)
- [ ] API REST (Flask/FastAPI)
- [ ] Busca avançada com índices
- [ ] Sync em nuvem
- [ ] Testes automatizados (pytest)
- [ ] Documentação Sphinx

## Tecnologias

- **Python** 3.12.7
- **JSON** para persistência
- **Regex** para parsing de quantidades
- **Type Hints** para máxima clareza

---

**Desenvolvido com padrões profissionais de engenharia de software.**
