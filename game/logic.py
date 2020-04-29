import time
import random
import pygame


class Ball:

    def __init__(self, initial_position=None, velocity=1):
        if initial_position is None:
            initial_position = [-1, -1]

        self.rect = pygame.Rect(initial_position[0], initial_position[1], 30, 30)
        self.initial_position = initial_position
        self.position = initial_position
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
        return self.position

    def SetPosition(self, x, y):
        self.position = [x, y]
        self.rect.x = x
        self.rect.y = y

    def SetPositionX(self, x):
        self.position[0] = x
        self.rect.x = x

    def SetPositionY(self, y):
        self.position[1] = y
        self.rect.y = y

    def SetMovement(self, movement_vector):
        self.movement = movement_vector

    def SetMovementDirectionX(self, direction):
        self.movement[0] = direction

    def SetMovementDirectionY(self, direction):
        self.movement[1] = direction

    def Move(self):
        self.position[0] += self.movement[0] * self.velocity
        self.position[1] += self.movement[1] * self.velocity
        self.rect.x += self.movement[0] * self.velocity
        self.rect.y += self.movement[1] * self.velocity

    def Collide(self, obj):
        return self.rect.colliderect(obj.rect)


class Board:

    LEFT = 0
    RIGHT = 1
    NULL = 2

    def __init__(self, size=(500, 500), id=0, number_of_enemies=10, spawn_rate=15, player_vel=5, balls_vel=1, training=False):
        self.size = size
        self.balls = [Ball(velocity=balls_vel), Ball(velocity=balls_vel)]
        self.player = Ball([int(size[0] / 2), int(size[1] - 50)], velocity=player_vel)
        self.number_of_enemies = number_of_enemies
        self.spawn_rate = spawn_rate
        self.start_time = time.time()
        self.game_over = False
        self.score = 0
        self.id = id

        self.balls_velocity = balls_vel
        self.training = training

    def Reset(self):
        self.balls = [Ball(velocity=self.balls_velocity), Ball(velocity=self.balls_velocity)]

        self.player.SetPosition(int(self.size[0] / 2), int(self.size[1] - 50))
        self.start_time = time.time()
        self.game_over = False
        self.score = 0

    def IsGameOver(self):
        return self.game_over

    def GetScore(self):
        return self.score

    def GetID(self):
        return self.id

    def Tick(self, key_pressed=True):
        if (time.time() - self.start_time) > self.spawn_rate and len(self.balls) < self.number_of_enemies:
            self.balls.append(Ball(velocity=self.balls_velocity))
            self.start_time = time.time()

        for ball in self.balls:
            position = ball.GetPosition()

            if not ball.IsSpawned():
                random_x = random.randrange(150, self.size[0] - 150, 30)
                random_y = random.randrange(-1000, -100, 50)

                ball.SetPosition(random_x, random_y)
                ball.SetMovementDirectionY(1)
                ball.Spawn()

            elif position[1] >= self.size[1]:
                self.game_over = True

            ball.Move()

            if self.player.Collide(ball) and key_pressed:
                ball.spawned = False
                self.score += 1

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

        enemy_positions = []

        for ball in self.balls:
            enemy_positions.append(ball.GetPosition())

        def SortByNearest(enemy):
            return enemy[1]

        enemy_positions = sorted(enemy_positions, key=SortByNearest)
        positions = [player_position[0], enemy_positions[-1][0]]

        return positions

    def GetEnemiesPositions(self):
        positions = [ball.GetPosition() for ball in self.balls]

        def SortingKey(e):
            return e[1]

        return sorted(positions, key=SortingKey)

    def GetPlayerPosition(self):
        return self.player.GetPosition()


def CreateBoards(pop_size=5, board_size=(500, 500)):
    boards = []

    for i in range(pop_size):
        boards.append(Board(size=board_size, id=i, training=True))

    return boards


def ResetBoards(boards):
    for i in range(len(boards)):
        boards[i].Reset()

    return boards
