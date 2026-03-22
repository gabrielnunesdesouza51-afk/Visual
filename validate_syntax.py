#!/usr/bin/env python
"""Validador de sintaxe para os novos arquivos"""
import py_compile
import sys

files_to_check = [
    "main.py",
    "services/recipe_suggester.py",
    "test_recipe_suggester.py"
]

all_valid = True
print("\n" + "="*60)
print("VALIDAÇÃO DE SINTAXE")
print("="*60)

for filename in files_to_check:
    try:
        py_compile.compile(filename, doraise=True)
        print(f"✅ {filename}")
    except py_compile.PyCompileError as e:
        print(f"❌ {filename}")
        print(f"   Erro: {e}")
        all_valid = False

print("="*60)

if all_valid:
    print("✅ TODOS OS ARQUIVOS TÊM SINTAXE VÁLIDA!")
    sys.exit(0)
else:
    print("❌ ALGUNS ARQUIVOS TÊM ERROS DE SINTAXE!")
    sys.exit(1)
