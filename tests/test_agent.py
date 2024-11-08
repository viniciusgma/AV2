import context
import pytest
from mesa import Model
from mesa.space import MultiGrid
from tree import (
    TreeCell,
)  # Replace with the correct import path for your TreeCell class

# Para o ruff não remover o import do context
context.foo()


class FireModel(Model):
    """A simple model for testing TreeCell fire spread."""

    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = None  # Not needed for this test


@pytest.fixture
def setup_forest():
    """Fixture to set up a 3x3 grid with a central tree on fire."""
    model = FireModel(3, 3)

    # Create TreeCell agents and place them on the grid
    trees = {}
    for x in range(3):
        for y in range(3):
            tree = TreeCell((x, y), model)
            model.grid.place_agent(tree, (x, y))
            trees[(x, y)] = tree

    # Set the center tree on fire
    trees[(1, 1)].condition = "On Fire"
    return model, trees


def test_fire_spread(setup_forest):
    """Test that fire spreads to neighbors and the center tree burns out."""
    model, trees = setup_forest

    # Step the center tree (1, 1), which should spread fire to neighbors
    trees[(1, 1)].step()

    # Check that the center tree has burned out
    assert trees[(1, 1)].condition == "Burned Out"

    # Check that neighboring trees are on fire
    for pos in [(0, 1), (1, 0), (1, 2), (2, 1)]:
        assert trees[pos].condition == "On Fire"

    # Non-neighboring trees should still be fine
    for pos in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        assert trees[pos].condition == "Fine"


def test_no_spread_when_fine(setup_forest):
    """Test that trees do not spread fire when they are fine."""
    model, trees = setup_forest

    # Step all trees except the center (1, 1), which is on fire
    for pos, tree in trees.items():
        if pos != (1, 1):
            tree.step()

    # Ensure no fire has spread from fine trees
    for pos, tree in trees.items():
        if pos != (1, 1):
            assert tree.condition == "Fine"
