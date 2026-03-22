#!/usr/bin/env python
"""Test script to validate all Python module syntax"""
import py_compile
import sys
import os

def test_syntax(filename):
    """Test if a Python file has valid syntax"""
    try:
        py_compile.compile(filename, doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)

if __name__ == "__main__":
    files_to_check = [
        "models/receita.py",
        "utils/storage.py",
        "services/receita_service.py",
        "main.py"
    ]
    
    all_valid = True
    for filename in files_to_check:
        valid, error = test_syntax(filename)
        if valid:
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename}")
            print(f"  Error: {error}")
            all_valid = False
    
    if all_valid:
        print("\n✓ All files have valid syntax!")
        sys.exit(0)
    else:
        print("\n✗ Some files have syntax errors!")
        sys.exit(1)
