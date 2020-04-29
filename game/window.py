import pygame


class Window:

    PLAYER_COLOR = (0, 0, 255)
    ENEMY_COLOR = (255, 0, 0)
    LINE_COLOR = (0, 255, 0)
    FOOD_COLOR = (255, 255, 255)
    BALL_RADIUS = 20

    def __init__(self, size=(500, 500), fps=60):
        self.size = size
        self.clock = pygame.time.Clock()
        self.fps = fps

        pygame.init()

        self.screen = pygame.display.set_mode(size)

        pygame.display.set_caption("GA Game")

    def Draw(self, board):

        enemies = board.GetEnemiesPositions()
        player_position = board.GetPlayerPosition()

        self.screen.fill((0, 0, 0))

        for enemy_position in enemies:
            if not enemy_position == [-1, -1]:
                pygame.draw.line(self.screen, self.LINE_COLOR, player_position, enemy_position)
                pygame.draw.circle(self.screen, self.ENEMY_COLOR, enemy_position, self.BALL_RADIUS)

        pygame.draw.circle(self.screen, self.PLAYER_COLOR, player_position, self.BALL_RADIUS)

        pygame.display.flip()
