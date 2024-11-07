import context
from src.agent import func


# Para o ruff não remover o import do context
context.foo()


def test_func():
    assert func() == 1
