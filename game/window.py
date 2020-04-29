import pygame


class Window:

    PLAYER_COLOR = (0, 255, 255)
    ENEMY_COLOR = (250, 92, 0)
    LINE_COLOR = (0, 255, 0)
    TEXT_COLOR = (0, 255, 0)
    FOOD_COLOR = (255, 255, 255)
    BALL_RADIUS = 20

    def __init__(self, size=(500, 500), fps=None, title="Genetic Algorithms - PyGame"):
        self.fps = fps
        self.size = size
        self.clock = pygame.time.Clock()

        pygame.init()

        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont("monospace", 15)

        self.highest_score = 0

        pygame.display.set_caption(title)

    def Draw(self, board, generation):
        board_id = board.GetID()
        board_score = board.GetScore()
        enemies = board.GetEnemiesPositions()
        player_position = board.GetPlayerPosition()

        self.screen.fill((0, 0, 0))

        i = 0
        for enemy_position in enemies:
            relative_position = int((enemy_position[1] * 100) / self.size[1])

            if relative_position < 0:
                relative_position = 0

            relative_position = int((255 * relative_position) / 100)
            color = (0, relative_position % 255, 0)

            if relative_position > 50:
                first_point = enemy_position

                if i + 1 == len(enemies):
                    second_point = player_position

                else:
                    second_point = enemies[i + 1]

                pygame.draw.line(self.screen, color, first_point, second_point)

            pygame.draw.circle(self.screen, color, enemy_position, self.BALL_RADIUS)

            i += 1

        pygame.draw.circle(self.screen, self.ENEMY_COLOR, enemies[-1], self.BALL_RADIUS)
        pygame.draw.circle(self.screen, self.PLAYER_COLOR, player_position, self.BALL_RADIUS)

        label = self.font.render("Gen %i Net #%i Score %i" % (generation, board_id, board_score), 1,
                                 (255, 255, 0))

        self.screen.blit(label, (20, 20))

        label = self.font.render("Highest Score %i" % self.highest_score, 1,
                                 (255, 255, 0))

        self.screen.blit(label, (20, 40))

        if board_score > self.highest_score:
            self.highest_score = board_score

        pygame.display.flip()

        if self.fps:
            self.clock.tick(self.fps)
