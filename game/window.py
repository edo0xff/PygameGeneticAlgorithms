import pygame


def ColorFade(color1, color2, percent):
    percent = percent / 100
    color3 = [0, 0, 0]

    color3[0] = int((color2[0] - color1[0]) * percent)
    color3[1] = int((color2[1] - color1[1]) * percent)
    color3[2] = int((color2[2] - color1[2]) * percent)

    return color3


class Window:

    BALL_RADIUS = 20
    BALL_COLOR = (255, 0, 89)
    TEXT_COLOR = (150, 92, 250)
    PLAYER_COLOR = (0, 168, 252)
    NEAREST_BALL_COLOR = (150, 92, 250)

    def __init__(self, size=(500, 500), fps=None, title="Genetic Algorithms - PyGame"):
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
        balls_positions = board.GetBallsPositions()
        player_position = board.GetPlayerPosition()

        if board_score > self.highest_score:
            self.highest_score = board_score

        self.screen.fill((0, 0, 0))

        i = 0
        for ball_position in balls_positions:
            relative_position = int((ball_position[1] * 100) / self.size[1])

            if relative_position < 0:
                relative_position = 0

            color = ColorFade((0, 0, 0), self.BALL_COLOR, relative_position)

            current_ball_index = balls_positions.index(ball_position)

            if relative_position > 50 and current_ball_index == 0:
                pygame.draw.line(self.screen, self.NEAREST_BALL_COLOR, ball_position, player_position)

            if relative_position > 50 and current_ball_index + 1 < len(balls_positions):
                second_point = balls_positions[current_ball_index + 1]

                pygame.draw.line(self.screen, color, ball_position, second_point)

            pygame.draw.circle(self.screen, color, ball_position, self.BALL_RADIUS)

            i += 1

        if len(balls_positions) > 0:
            pygame.draw.circle(self.screen, self.NEAREST_BALL_COLOR, balls_positions[0], self.BALL_RADIUS)

        pygame.draw.circle(self.screen, self.PLAYER_COLOR, player_position, self.BALL_RADIUS)

        label = self.font.render("Gen %i Net #%i Score %i" % (generation, board_id, board_score), 1,
                                 self.TEXT_COLOR)

        self.screen.blit(label, (20, 20))

        label = self.font.render("Highest Score %i" % self.highest_score, 1,
                                 self.TEXT_COLOR)

        self.screen.blit(label, (20, 40))

        pygame.display.flip()

        if self.fps:
            self.clock.tick(self.fps)
