#!/usr/bin/env python
"""Quick import test for the recipe manager"""
try:
    import models.receita
    print("✓ models.receita imported")
except Exception as e:
    print(f"✗ models.receita: {e}")
    exit(1)

try:
    import utils.storage
    print("✓ utils.storage imported")
except Exception as e:
    print(f"✗ utils.storage: {e}")
    exit(1)

try:
    import services.receita_service
    print("✓ services.receita_service imported")
except Exception as e:
    print(f"✗ services.receita_service: {e}")
    exit(1)

try:
    # Don't actually execute main, just import
    import main
    print("✓ main imported")
except Exception as e:
    print(f"✗ main: {e}")
    exit(1)

print("\n✓ All modules imported successfully!")
