# 📥 Guia de Importação de Receitas

Este script (`import_receitas.py`) permite popular seu **Gerenciador de Receitas** com dados reais sem necessidade de APIs pagas.

---

## 🚀 Opções de Uso

### 1️⃣ Importar Receitas Padrão (mais fácil)

Já vem com **11 receitas reais** brasileiras e internacionais:

```bash
python import_receitas.py
# Escolha opção 1
```

**Receitas incluídas:**
- Brigadeiro Clássico
- Feijoada à Brasileira
- Bolo de Chocolate
- Macarrão à Carbonara
- Bruschetta Italiana
- Sushi de Salmão
- Frango Parmegiana
- Pavê de Chocolate
- Salada Grega
- Ratatouille Provençal
- Tarta de Maçã

---

### 2️⃣ Importar de Arquivo CSV

Use para datasets públicos do Kaggle ou GitHub.

**Formato esperado:**
```csv
name,ingredients,instructions,minutes,servings,category
Brigadeiro,"leite condensado, chocolate em pó, manteiga","Misture e cozinhe em fogo médio...",20,12,Sobremesa
```

**Colunas reconhecidas:**
- `name` ou `nome` ou `title` → Nome da receita
- `ingredients` ou `ingredientes` → Lista de ingredientes (separados por vírgula)
- `instructions` ou `modo_preparo` → Modo de preparo
- `minutes` ou `tempo_preparo` → Tempo em minutos
- `servings` ou `porcoes` → Número de porções
- `category`, `cuisine` ou `categoria` → Categoria

**Como usar:**
```bash
python import_receitas.py
# Escolha opção 2
# Digite o caminho: caminho/para/seu/arquivo.csv
```

---

### 3️⃣ Importar de Arquivo JSON

Use para dados estruturados em formato JSON.

**Formato aceito:**
```json
[
  {
    "name": "Brigadeiro",
    "ingredients": ["leite condensado", "chocolate em pó", "manteiga"],
    "instructions": "Misture e cozinhe...",
    "minutes": 20,
    "servings": 12,
    "category": "Sobremesa"
  }
]
```

Ou com wrapper:
```json
{
  "recipes": [
    { "name": "Brigadeiro", ... }
  ]
}
```

**Como usar:**
```bash
python import_receitas.py
# Escolha opção 3
# Digite o caminho: caminho/para/seu/arquivo.json
```

---

## 🌐 Datasets Públicos Recomendados

### 📊 Kaggle (Gratuito, sem API necessária)

1. **"What's Cooking?" Dataset**
   - URL: https://www.kaggle.com/competitions/whats-cooking/data
   - Formato: JSON
   - +39k receitas de cuisines variadas

2. **"Recipe Dataset"**
   - URL: https://www.kaggle.com/datasets/d4xbx/recipes-dataset
   - Formato: CSV
   - Receitas populares em inglês

3. **"Brazilian Recipes"**
   - URL: https://www.kaggle.com/datasets/search?q=brazilian+recipes
   - Receitas brasileiras

### 🔧 Como Baixar do Kaggle (sem pagar):

1. Acesse: https://www.kaggle.com/datasets
2. Busque por "recipes" ou "receitas"
3. Clique em **"Download"** (botão à direita)
4. Selecione o arquivo (CSV ou JSON)
5. Salve na pasta do seu projeto
6. Use `import_receitas.py` para importar!

### 💾 Outros Repositórios Públicos

- **GitHub:** Busque por "recipe dataset" em Public Repositories
- **Zenodo:** https://zenodo.org (datasets científicos abertos)
- **UC Irvine ML:** https://archive.ics.uci.edu/ml/

---

## 📋 Workflow Completo

```bash
# 1. Clonar/acessar seu projeto
cd c:\Users\Pai\Desktop\visual

# 2. Importar receitas padrão (mais fácil!)
python import_receitas.py
# → Escolha 1
# → Pronto! 11 receitas adicionadas

# 3. Verificar receitas importadas
python main.py
# → Menu → Opção 2 (Listar todas as receitas)

# 4. (Opcional) Importar mais dados de um CSV/JSON
python import_receitas.py
# → Escolha 2 ou 3
# → Digite caminho do arquivo
```

---

## ⚙️ Características Técnicas

✅ **Sem APIs pagas** - Funciona totalmente offline  
✅ **Suporte a múltiplos formatos** - CSV, JSON e receitas padrão  
✅ **Mapeamento automático** - Reconhece várias nomenclaturas de colunas  
✅ **Tratamento de erros** - Continua mesmo se algumas receitas falharem  
✅ **IDs automáticos** - Gera IDs únicos sem conflitos  
✅ **Integrado** - Usa as classes e funções do seu app  

---

## 🆘 Troubleshooting

### ❌ "Erro ao salvar receitas"
- Verifique se `receitas.json` não está aberto em outro programa
- Teste as permissões na pasta

### ❌ "Arquivo não encontrado"
- Use caminho absoluto: `C:\Users\Pai\Desktop\visual\dados.csv`
- Ou coloque o arquivo na pasta do projeto e use só o nome dele

### ❌ "Nenhuma receita importada"
- Verifique se o CSV/JSON tem as colunas corretas
- Veja exemplo de formato na seção acima

### ❌ "Receitas duplicadas"
- Isso não acontece! O script incrementa IDs automaticamente
- Se rodar 2x as receitas padrão, terá 22 receitas (não duplica conteúdo)

---

## 💡 Próximos Passos

1. **Importar receitas padrão:** `python import_receitas.py` → opção 1
2. **Testar no menu:** `python main.py` → opção 2 (listar)
3. **Criar receitas favoritas:** `python main.py` → opção 14 (favoritar)
4. **Avaliar receitas:** `python main.py` → opção 10 (avaliar)
5. **Gerar lista de compras:** `python main.py` → opção 12

---

## 📧 Suporte

Dúvidas? Verifique:
- Estrutura do CSV/JSON nos exemplos acima
- Console do VS Code (erros aparecem lá)
- Permissões de arquivo/pasta

**Bom apetite! 🍳👨‍🍳**
