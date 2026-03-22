# 🍳 Recipe Manager CLI

A professional-grade command-line application for managing recipes with advanced search, filtering, and organization features. Built with Python using object-oriented programming and modular architecture.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Examples](#-examples)
- [Technologies](#-technologies)
- [Future Improvements](#-future-improvements)

---

## ✨ Features

### 🍔 Core Recipe Management
- ✅ **Add Recipes** - Create new recipes with ingredients, preparation steps, and metadata
- ✅ **Edit Recipes** - Modify existing recipes with validation
- ✅ **Delete Recipes** - Remove recipes with confirmation prompt
- ✅ **View Details** - Display complete recipe information including ingredients and instructions

### 🔍 Search & Filter
- 🔎 **Search by Name** - Find recipes by partial name matching
- 🥕 **Search by Ingredient** - Discover recipes containing specific ingredients
- 📂 **Filter by Category** - Organize recipes by type (Doce, Salgado, Bebida, Sobremesa)
- ⏱️ **Filter by Preparation Time** - Find quick recipes by maximum cook time

### ⭐ Analytics & Features
- 🌟 **Rating System** - Rate recipes from 1-5 stars
- ❤️ **Favorites** - Mark and quickly access favorite recipes
- 🏆 **Top Recipes** - View highest-rated recipes
- 🔥 **Calorie Calculator** - Calculate total and per-portion calories
- 🛒 **Smart Shopping List** - Generate aggregated ingredient list with quantities

### 🎨 User Experience
- 💬 **Input Validation** - Robust error handling and type checking
- ⚠️ **Confirmation Dialogs** - Prevent accidental data loss
- 📱 **Clean Interface** - Professional CLI design with emoji indicators
- 💾 **Data Persistence** - Automatic JSON-based storage

---

## 🗂️ Project Structure

```
recipe-manager/
├── main.py                      # Application entry point & menu system
├── models/
│   ├── __init__.py
│   └── receita.py              # Receita class (OOP model)
├── services/
│   ├── __init__.py
│   └── receita_service.py      # Business logic & utilities
├── utils/
│   ├── __init__.py
│   └── storage.py              # JSON persistence layer
├── receitas.json               # Data file (auto-generated)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/gabrielnunesdesouza51-afk/Visual.git
cd Visual
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

---

## 🚀 Usage

### Starting the Application

```bash
$ python main.py

==================================================
  🍽️  BEM-VINDO AO GERENCIADOR DE RECEITAS! 👨‍🍳
==================================================

 Começar adicionando sua primeira receita!

============================================================
  🍴 GERENCIADOR DE RECEITAS 🍳
============================================================

 GERENCIAR RECEITAS
  1️⃣   Adicionar receita
  2️⃣   Listar todas as receitas
  3️⃣   Ver detalhes de receita
  4️⃣   Editar receita
  5️⃣   Deletar receita

 🔍 BUSCAR E FILTRAR
  6️⃣   Buscar por ingrediente
  7️⃣   Buscar por nome
  8️⃣   Listar por categoria
  9️⃣   Filtrar por tempo de preparo

 📊 ANÁLISE E FERRAMENTAS
  🔟  Avaliar receita
  1️⃣1️⃣  Calcular calorias
  1️⃣2️⃣  Gerar lista de compras
  1️⃣3️⃣  Top receitas
  1️⃣4️⃣  Favoritar receita
  1️⃣5️⃣  Listar favoritas

  0️⃣   Sair
============================================================

Escolha uma opção: 
```

### Main Menu Options

| Option | Action |
|--------|--------|
| 1-5 | Manage recipes (add, list, view, edit, delete) |
| 6-9 | Search and filter recipes |
| 10-15 | Analytics and tools |
| 0 | Exit application |

---

## 📝 Examples

### Example 1: Adding a Recipe

```
Digite uma opção: 1

============================================================
   ADICIONAR RECEITA
============================================================
Nome da receita: Brigadeiro

Categoria (Doce, Salgado, Bebida, Sobremesa): Sobremesa

Ingredientes (uma por linha, deixe em branco para terminar):
   leite condensado
   chocolate em pó
   manteiga
   

Modo de preparo:
> Cozinhe o leite condensado com chocolate e manteiga em fogo médio até ficar 
  pegajoso. Coloque em um prato manteigado e espere esfriar.

Número de porções: 12

Tempo de preparo (minutos): 15

 Receita 'Brigadeiro' adicionada com sucesso!
```

### Example 2: Listing All Recipes

```
Digite uma opção: 2

RECEITAS:
============================================================
ID | Nome                  | Tempo | Avaliação  | Favorita
============================================================
1  | Brigadeiro           | 15min | ⭐⭐⭐⭐⭐ | ❤️
2  | Macarrão à Carbonara | 20min | ⭐⭐⭐⭐   |
3  | Bolo de Chocolate    | 45min | ⭐⭐⭐     |
```

### Example 3: Searching by Ingredient

```
Digite uma opção: 6

 Digite o ingrediente a buscar: chocolate

 2 receita(s) encontrada(s):
 - Brigadeiro (15 min)
 - Bolo de Chocolate (45 min)
```

### Example 4: Viewing Top Recipes

```
Digite uma opção: 13

 TOP RECEITAS (Melhor Avaliadas)
============================================================
 1. Brigadeiro ⭐⭐⭐⭐⭐ (15 min)
 2. Macarrão à Carbonara ⭐⭐⭐⭐ (20 min)
 3. Bolo de Chocolate ⭐⭐⭐ (45 min)
```

---

## 🛠️ Technologies

### Core Technologies
- **Python 3.8+** - Programming language
- **JSON** - Data storage format
- **OOP** - Object-oriented programming principles

### Architecture Patterns
- **Modular Design** - Separated concerns (models, services, utils)
- **Business Logic Layer** - Service layer for recipe operations
- **Data Persistence** - JSON-based file storage
- **Input Validation** - Type checking and error handling

### Key Libraries (Built-in)
- `json` - Data serialization
- `os` - File operations
- `sys` - System utilities
- `datetime` - Timestamp management
- `typing` - Type hints

---

## 🔮 Future Improvements

### Planned Features
- 🌐 **Database Integration** - Replace JSON with SQLite/PostgreSQL
- 🎨 **GUI Interface** - PyQt or Tkinter desktop application
- 📊 **Data Visualization** - Charts and statistics dashboard
- 🔐 **User Authentication** - Multi-user support with login
- ☁️ **Cloud Sync** - Sync recipes across devices
- 📱 **REST API** - Web API for mobile app integration

### Code Enhancements
- ✨ Add Rich library for colored terminal output
- 📋 Implement pagination for large recipe lists
- 🔎 Add fuzzy search capabilities
- 💾 Add data export to CSV/PDF formats
- 🧪 Comprehensive unit tests

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Gabriel Nunes de Souza**
- GitHub: [@gabrielnunesdesouza51-afk](https://github.com/gabrielnunesdesouza51-afk)

---

## 💡 Tips & Best Practices

### Before Using
1. Create a Virtual Environment to isolate dependencies
2. Keep the `receitas.json` file by backing it up regularly
3. Use meaningful recipe names for easier searching

### While Using
- Use arrow keys to navigate when prompted
- Leave fields blank in edit mode to keep existing values
- Mark your favorite recipes for quick access
- Regularly check the top recipes to find your best meals

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this project and submit pull requests with improvements.

---

**Made with ❤️ for food lovers and Python enthusiasts**
