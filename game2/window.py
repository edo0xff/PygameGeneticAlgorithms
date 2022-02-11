import pygame

class Window:

    BALL_RADIUS = 20
    BALL_COLOR = (255, 0, 89)
    TEXT_COLOR = (150, 92, 250)

    def __init__(self, size=(1000, 1000), fps=None, title="Genetic Algorithms - PyGame"):
        self.fps = fps
        self.size = size
        self.clock = pygame.time.Clock()

        pygame.init()

        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont("monospace", 15)

        self.highest_score = 0

        pygame.display.set_caption(title)

    def Draw(self, board, generation=0):
        board_id = board.GetID()
        board_score = board.GetScore()
        player_position = board.GetPlayerPosition()

        if board_score > self.highest_score:
            self.highest_score = board_score

        self.screen.fill((0, 0, 0))

        for position in board.pos_history:
            pygame.draw.circle(self.screen, (0,0,255), position, self.BALL_RADIUS)

        # cross
        if board.player.orientation == 'UP' or board.player.orientation == 'DOWN':
            pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0] - 40, player_position[1]), 4)
            pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0] + 40, player_position[1]), 4)

            if board.player.orientation == 'UP':
                pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0], player_position[1] - 40), 4)
            else:
                pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0], player_position[1] + 40), 4)

        if board.player.orientation == 'RIGHT' or board.player.orientation == 'LEFT':
            pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0], player_position[1] - 40), 4)
            pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0], player_position[1] + 40), 4)

            if board.player.orientation == 'RIGHT':
                pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0] + 40, player_position[1]), 4)
            else:
                pygame.draw.line(self.screen, (0, 255, 0), player_position, (player_position[0] - 40, player_position[1]), 4)

        pygame.draw.circle(self.screen, self.BALL_COLOR, player_position, self.BALL_RADIUS)

        label = self.font.render("Gen %i Net #%i Score %i" % (generation, board_id, board_score), 1,
                                 self.TEXT_COLOR)

        self.screen.blit(label, (20, 20))

        label = self.font.render("Highest Score %i" % self.highest_score, 1,
                                 self.TEXT_COLOR)

        self.screen.blit(label, (20, 40))

        pygame.display.flip()

        if self.fps:
            self.clock.tick(self.fps)
