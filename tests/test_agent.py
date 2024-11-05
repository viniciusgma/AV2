import context

from src.agent import func


def test_func():
    assert func() == 1


# Para o ruff não remover o import do context
context.foo()
