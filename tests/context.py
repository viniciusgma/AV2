import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Para o ruff não remover o import do context
def foo():
    pass
