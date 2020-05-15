import time
import random
import pygame


def CurrentTIme():
    return int(round(time.time() * 1000))


class Ball:

    def __init__(self, initial_position=None, velocity=1):
        if initial_position is None:
            initial_position = [0, 0]

        self.rect = pygame.Rect(initial_position[0], initial_position[1], 30, 30)
        self.initial_position = initial_position
        self.velocity = velocity
        self.movement = [0, 0]
        self.spawned = False

    def Reset(self):
        self.spawned = False
        self.movement = [0, 0]

    def IsSpawned(self):
        return self.spawned

    def Spawn(self):
        self.spawned = True

    def GetPosition(self):
        return [self.rect.x, self.rect.y]

    def SetPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def SetPositionX(self, x):
        self.rect.x = x

    def SetPositionY(self, y):
        self.rect.y = y

    def SetMovement(self, movement_vector):
        self.movement = movement_vector

    def SetMovementDirectionX(self, direction):
        self.movement[0] = direction

    def SetMovementDirectionY(self, direction):
        self.movement[1] = direction

    def Move(self):
        self.rect.x += self.movement[0] * self.velocity
        self.rect.y += self.movement[1] * self.velocity

    def Collide(self, obj):
        return self.rect.colliderect(obj.rect)


class Board:

    LEFT = 0
    RIGHT = 1
    NULL = 2

    def __init__(self, size=(500, 500), id=0, spawn_rate=125, player_vel=5, balls_vel=1, training=False):
        self.size = size
        self.balls = []
        self.player = Ball([int(size[0] / 2), int(size[1] - 50)], velocity=player_vel)
        self.spawn_rate = spawn_rate
        self.start_time = CurrentTIme()
        self.game_over = False
        self.score = 0
        self.id = id

        self.balls_velocity = balls_vel
        self.training = training

    def Reset(self):
        self.balls = []

        self.player.SetPosition(int(self.size[0] / 2), int(self.size[1] - 50))
        self.start_time = CurrentTIme()
        self.game_over = False
        self.score = 0

    def IsGameOver(self):
        return self.game_over

    def GetScore(self):
        return self.score

    def GetID(self):
        return self.id

    def Tick(self):
        elapsed_time = CurrentTIme() - self.start_time

        if elapsed_time > self.spawn_rate:
            if random.random() > 0.5:
                self.balls.append(Ball(velocity=self.balls_velocity))

            self.start_time = CurrentTIme()

        for ball in self.balls:
            position = ball.GetPosition()

            if not ball.IsSpawned():
                random_x = random.randrange(180, self.size[0] - 180, 30)

                ball.SetPosition(random_x, 0)
                ball.SetMovementDirectionY(1)
                ball.Spawn()

            elif position[1] >= self.size[1]:
                self.game_over = True

            ball.Move()

            if self.player.Collide(ball):
                ball_index = self.balls.index(ball)

                if ball_index == 0:
                    self.balls.pop(ball_index)
                    self.score += 1

                else:
                    self.game_over = True

    def MovePlayer(self, direction):
        position = self.player.GetPosition()

        if direction == self.LEFT:
            self.player.SetMovementDirectionX(-1)

        elif direction == self.RIGHT:
            self.player.SetMovementDirectionX(1)

        else:
            self.player.SetMovement([0, 0])

        if position[0] - 50 <= 0 or position[0] + 50 >= self.size[0]:
            if self.training:
                self.game_over = True

            else:
                self.player.SetMovementDirectionX(0)

        self.player.Move()

    def Get1DPositions(self):
        player_position = self.player.GetPosition()

        ball_position = [int(self.size[1] / 2), 0]

        if len(self.balls) > 0:
            ball_position = self.balls[0].GetPosition()

        return [player_position[0], ball_position[0]]

    def GetBallsPositions(self):
        return [ball.GetPosition() for ball in self.balls]

    def GetPlayerPosition(self):
        return self.player.GetPosition()


def CreateBoards(pop_size=5, board_size=(500, 500)):
    return [Board(size=board_size, id=i, training=True, spawn_rate=500) for i in range(pop_size)]


def ResetBoards(boards):
    for board in boards:
        board.Reset()

    return boards
