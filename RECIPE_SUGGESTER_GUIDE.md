# 💡 Sistema de Sugestão Inteligente de Receitas

## 📌 Visão Geral

O **Sistema de Sugestão Inteligente** analisa os ingredientes que você possui e recomenda receitas baseado em compatibilidade, avaliação e disponibilidade de ingredientes.

---

## ✨ Características

### 🎯 Algoritmo Inteligente
- **Análise de Compatibilidade**: Calcula o percentual de ingredientes disponíveis para cada receita
- **Ordenação Inteligente**: Prioriza receitas com maior compatibilidade e avaliação
- **Filtro Mínimo**: Apenas mostra receitas com pelo menos 30% de compatibilidade

### 📊 Scoring Detalhado
- **Compatibilidade 80%+** 🔥 EXCELENTE - Quase todos os ingredientes disponíveis
- **Compatibilidade 60-79%** ✨ BOM - Maioria dos ingredientes disponíveis
- **Compatibilidade 40-59%** 👍 POSSÍVEL - Alguns ingredientes disponíveis
- **Compatibilidade 30-39%** 📌 PARCIAL - Poucos ingredientes, mas viável

### 💪 Funcionalidades
1. ✅ Sugere receitas baseado em ingredientes que você possui
2. ✅ Mostra score de compatibilidade para cada receita
3. ✅ Lista quantos ingredientes faltam
4. ✅ Leva em conta avaliação/rating da receita
5. ✅ Permite ver ingredientes específicos que faltam por receita

---

## 🚀 Como Usar

### Via Menu Principal

```
Abra a aplicação:
$ python main.py

No menu, escolha a opção:
✨ IA & SUGESTÕES
  16. Sugerir receitas por ingredientes
```

### Passo a Passo

1. **Selecione a opção 16** no menu principal
2. **Digite seus ingredientes** um por linha:
   ```
   chocolate em pó
   leite
   óleo
   fermento
   [deixe em branco e pressione Enter para terminar]
   ```
3. **Veja as sugestões** com scores de compatibilidade
4. **Escolha uma receita** para ver quais ingredientes faltam

---

## 🧠 Como Funciona

### Algoritmo de Compatibilidade

```
Score = (Ingredientes Encontrados / Total de Ingredientes) × 100
```

**Exemplo:**
```
Sua lista: [leite, óleo, açúcar, ovo, sal]
Receita: [leite, ovos, sal, manteiga]

Encontrados: leite, ovos, sal = 3
Total: 4
Score = (3/4) × 100 = 75% ✨ BOM
```

### Busca de Ingredientes

O sistema é **inteligente na busca**:
- ✅ Casa parcial ("ov" encontra "ovos")
- ✅ Busca bidirecional ("chocolate em pó" ≈ "chocolate")
- ✅ Case-insensitive (maiúscula/minúscula não importa)
- ✅ Ignora espaços extras

---

## 📋 Exemplo de Uso

### Sessão Completa

```
Escolha uma opção: 16

============================================================
  💡 SUGESTÃO INTELIGENTE DE RECEITAS
============================================================

Digite os ingredientes que você possui:
(Digite um ingrediente por linha, deixe em branco para terminar)
> leite condensado
> chocolate em pó
> manteiga
> 

 Processando...

============================================================
  💡 RECEITAS SUGERIDAS PARA VOCÊ
============================================================

1. 🔥 BRIGADEIRO CLÁSSICO
   Compatibilidade: 75% BOM
   Ingredientes: 3/4 disponíveis (faltam 1)
   Tempo: 20 min | Avaliação: ⭐⭐⭐⭐⭐
   ID: 1

2. 👍 BOLO DE CHOCOLATE
   Compatibilidade: 43% POSSÍVEL
   Ingredientes: 3/7 disponíveis (faltam 4)
   Tempo: 60 min | Avaliação: ⭐⭐⭐⭐
   ID: 3

============================================================
   2 receita(s) sugerida(s)
============================================================

Deseja ver os ingredientes que faltam para alguma receita?
Digite o ID da receita (ou deixe em branco para voltar): 1

 Ingredientes que faltam para 'Brigadeiro Clássico':
  - chocolate granulado
```

---

## 🔧 Estrutura Técnica

### Arquivo: `services/recipe_suggester.py`

#### Funções Principais

##### `calcular_score_compatibilidade()`
```python
def calcular_score_compatibilidade(ingredientes_usuario: List[str], 
                                   ingredientes_receita: List[str]) -> Tuple[float, int, int]
```
- **Parâmetros:**
  - `ingredientes_usuario`: Lista de ingredientes disponíveis
  - `ingredientes_receita`: Lista de ingredientes da receita
- **Retorna:** (score_percentual, encontrados, faltantes)

##### `sugerir_receitas()`
```python
def sugerir_receitas(receitas: List[Receita], 
                     ingredientes_usuario: List[str],
                     limite: int = 5) -> List[Dict]
```
- **Parâmetros:**
  - `receitas`: Lista de todas as receitas
  - `ingredientes_usuario`: Ingredientes disponíveis
  - `limite`: Máximo de sugestões (padrão 5)
- **Retorna:** Lista de sugestões ordenadas por score + avaliação

##### `exibir_sugestoes()`
```python
def exibir_sugestoes(sugestoes: List[Dict]) -> None
```
- Exibe as sugestões de forma formatada e colorida

##### `listar_ingredientes_que_faltam()`
```python
def listar_ingredientes_que_faltam(receita: Receita, 
                                   ingredientes_usuario: List[str]) -> List[str]
```
- Retorna lista de ingredientes que faltam para uma receita

##### `calcular_melhor_receita()`
```python
def calcular_melhor_receita(receitas: List[Receita], 
                           ingredientes_usuario: List[str]) -> Optional[Dict]
```
- Retorna a única melhor receita (compatibilidade + avaliação)

---

## 📊 Dados de Resposta

Cada sugestão retornada contém:

```python
{
    'receita': Receita,        # Objeto da receita
    'score': float,            # Compatibilidade %
    'encontrados': int,        # Ingredientes encontrados
    'faltantes': int,          # Ingredientes faltando
    'total_ingredientes': int, # Total de ingredientes
    'avaliacao_numeral': int   # Avaliação 0-5
}
```

---

## 🧪 Testes

Execute os testes do sistema:

```bash
python test_recipe_suggester.py
```

### Testes Inclusos

1. ✅ Cálculo de compatibilidade
2. ✅ Geração de sugestões
3. ✅ Lista de ingredientes faltantes
4. ✅ Cálculo da melhor receita
5. ✅ Tratamento de lista vazia

---

## 🎯 Casos de Uso

### Caso 1: Decidindo o que cozinhar
```
Você abre a geladeira, ve: leite, ovos, farinha, açúcar
Executa a sugestão → encontra receitas com esses ingredientes
```

### Caso 2: Aproveitando ingredientes
```
Comprou chocolate, manteiga, leite
Quer descobrir que receitas fazer
→ Sistema sugere as melhores opções
```

### Caso 3: Planejamento de compras
```
Vê uma receita com 30% compatibilidade
Confere quais 3 ingredientes precisam ser comprados
→ Decide se vale a pena
```

---

## 🚀 Futuras Melhorias

### Versão 2.0
- 🎨 Integração com interface gráfica
- 📱 API REST para mobile
- 🔄 Sincronização com listas de supermercado
- 🤖 IA com machine learning para preferências pessoais
- 📊 Gráficos de compatibilidade
- 💾 Salvar sugestões favoritas
- 🌐 Dados de receitas online

### Versão 3.0
- 👥 Sugestões colaborativas (com amigos)
- 📸 Reconhecimento de ingredientes por foto
- 🛒 Integração com e-commerce
- 🍽️ Geração de cardápios semanais

---

## 📖 Exemplo de Integração

### Usando no seu código

```python
from models.receita import Receita
from services.recipe_suggester import sugerir_receitas, exibir_sugestoes
from utils.storage import carregar_receitas

# Carrega receitas
receitas = carregar_receitas()

# Ingredientes disponíveis
meus_ingredientes = ["leite", "ovos", "farinha", "açúcar"]

# Gera sugestões
sugestoes = sugerir_receitas(receitas, meus_ingredientes, limite=5)

# Exibe resultado
exibir_sugestoes(sugestoes)
```

---

## ✅ Checklist de Implementação

- ✅ Algoritmo de compatibilidade
- ✅ Sistema de scoring
- ✅ Integração com menu principal
- ✅ Função de exibição formatada
- ✅ Testes unitários
- ✅ Documentação completa
- ✅ Tratamento de erros
- ✅ Input validation

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique que seus ingredientes estão bem digitados
2. Tente com apenas 2-3 ingredientes primeiro
3. Execute os testes: `python test_recipe_suggester.py`
4. Abra uma issue no GitHub

---

**Desenvolvido com ❤️ para ajudar você a descobrir novas receitas!**
