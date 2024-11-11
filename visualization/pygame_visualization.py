import sys
import os
import pygame
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.model import ForestFire
from src.agent import TreeCell, Water, Fireman, River

# Cores para os agentes e elementos do ambiente
COLORS = {
    "Fine": (0, 170, 0),  # Verde (árvore saudável)
    "On Fire": (255, 69, 0),  # Vermelho escuro (fogo)
    "Burned Out": (0, 0, 0),  # Preto (árvore queimada)
    "Water": (0, 191, 255),  # Azul claro (águas do rio)
    "River": (70, 130, 180),  # Azul mais escuro para o rio
    "Fireman": (255, 255, 0),  # Amarelo (bombeiro)
    "Land": (139, 69, 19),  # Marrom para a terra (áreas sem árvores)
}

# Configurações da tela
WIDTH, HEIGHT = 1000, 1000  # Dimensões da janela em pixels
CELL_SIZE = 10  # Tamanho de cada célula em pixels
FPS = 20  # Frames por segundo para a animação

# Inicializar o pygame
pygame.init()

# Inicializar o relógio
clock = pygame.time.Clock()


def get_cell_color(agent):
    """
    Retorna a cor associada ao agente baseado no seu estado.
    """
    if isinstance(agent, TreeCell):
        if agent.condition > 0.7:
            return COLORS["Fine"]
        elif agent.condition > 0:
            fire_intensity = 255 - int(agent.condition * 255)  # Intensidade do fogo
            return (fire_intensity, fire_intensity // 2, 0)
        else:
            return COLORS["Burned Out"]

    elif isinstance(agent, Water):
        return COLORS["Water"]

    elif isinstance(agent, River):
        return COLORS["River"]

    elif isinstance(agent, Fireman):
        return COLORS["Fireman"] if agent.condition > 0 else COLORS["Burned Out"]

    return COLORS["Land"]  # Para células vazias (terra)


def draw_grid(screen, model):
    """
    Desenha a grade completa na tela com base no estado do modelo.
    """
    for x in range(model.grid.width):
        for y in range(model.grid.height):
            cell = model.grid[x][y]
            if cell:
                agent = cell[0]
                color = get_cell_color(agent)

                # Desenhar a célula (retângulo) na tela
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )


def handle_events():
    """
    Lida com todos os eventos (como sair, pressionamento de teclas) durante a simulação.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def update_game(model):
    """
    Avança o modelo no tempo, incluindo a propagação do fogo e os efeitos da água.
    """
    model.step()


def init_game(tree_density, water_density):
    """
    Inicializa a tela do pygame, o modelo de incêndio na floresta e outros componentes necessários.
    """
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação de Incêndio na Floresta")
    
    # Inicializa o modelo de incêndio na floresta com densidade de árvores e água controladas
    model = ForestFire(
        width=WIDTH // CELL_SIZE,
        height=HEIGHT // CELL_SIZE,
        tree_density=tree_density,  # Densidade das árvores
        water_density=water_density,  # Densidade das águas (rios)
    )
    return screen, model


def main():
    # Densidade de árvores e água, ajustadas para melhorar a interação
    tree_density = 0.9  
    water_density = 0.1

    # Inicializar o jogo
    screen, model = init_game(tree_density, water_density)

    running = True
    while running:
        # Lidar com os eventos
        running = handle_events()

        # Avançar o modelo (interação entre fogo e água)
        update_game(model)

        # Limpar a tela
        screen.fill((0, 0, 0))

        # Desenhar a grade com base no estado do modelo
        draw_grid(screen, model)

        # Atualizar a tela
        pygame.display.flip()

        # Limitar para 20 quadros por segundo (para animação suave)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
