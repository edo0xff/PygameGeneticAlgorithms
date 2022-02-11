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

        self.Reset()

    def Reset(self):
        self.spawned = False
        self.movement = [0, 0]
        self.orientation = 'UP'
        self.moving = False

    def Rotate(self, direction):
        if direction < 0:
            if self.orientation == "UP":
                self.orientation = "LEFT"
            elif self.orientation == "LEFT":
                self.orientation = "DOWN"
            elif self.orientation == "DOWN":
                self.orientation = "RIGHT"
            elif self.orientation == "RIGHT":
                self.orientation = "UP"
        else:
            if self.orientation == "UP":
                self.orientation = "RIGHT"
            elif self.orientation == "RIGHT":
                self.orientation = "DOWN"
            elif self.orientation == "DOWN":
                self.orientation = "LEFT"
            elif self.orientation == "LEFT":
                self.orientation = "UP"

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

    def __init__(self, size=(1000, 1000), id=0, player_vel=5, balls_vel=1, training=False):
        self.id = id
        self.size = size
        self.player = Ball([0, 0], velocity=player_vel)

        self.Reset()

    def Reset(self):
        self.player.SetPosition(40, 40)
        self.start_time = CurrentTIme()
        self.game_over = False
        self.score = 0
        self.pos_history = []
        self.paths = []
        self.matrix = {'x': [], 'y': []}
        self.final_pos = [0,0]
        self.rotations = 0

    def IsGameOver(self):
        return self.game_over

    def GetScore(self):
        return self.score

    def GetID(self):
        return self.id

    def Tick(self):
        elapsed_time = CurrentTIme() - self.start_time
        player_position = self.player.GetPosition()

        if player_position == self.final_pos:
            self.player.SetMovement([0,0])
            self.moving = False

            if not player_position in self.paths:
                self.score += 1
                self.paths.append(player_position)
        else:
            if not player_position in self.pos_history:
                self.pos_history.append(player_position)
            self.player.Move()

    def MovePlayer(self, direction):
        self.player.SetMovement([0,0])
        position = self.player.GetPosition()

        self.final_pos = position

        # forward
        if direction == 0:
            if self.player.orientation == 'UP':
                self.player.SetMovementDirectionY(-1)
                self.final_pos[1] -= 20
            elif self.player.orientation == 'DOWN':
                self.player.SetMovementDirectionY(1)
                self.final_pos[1] += 20
            elif self.player.orientation == 'RIGHT':
                self.player.SetMovementDirectionX(1)
                self.final_pos[0] -= 20
            elif self.player.orientation == 'LEFT':
                self.player.SetMovementDirectionX(-1)
                self.final_pos[1] += 20

            self.rotations = 0

            self.paths.append(position)
            self.moving = True

        # rotate left
        elif direction == 1:
            self.player.Rotate(-1)
            self.rotations += 1

        # rotate right
        elif direction == 2:
            self.player.Rotate(1)
            self.rotations += 1

        if self.rotations >= 4:
            self.game_over = True

        if position[0] < 0 or position[0] > self.size[0]:
            self.game_over = True

        if position[1] < 0 or position[1] > self.size[1]:
            self.game_over = True

    def GetPlayerPosition(self):
        return self.player.GetPosition()

    def GetBoardMatrix(self):
        return self.matrix

    def GetSensorValues(self):
        # left, front, right
        sensors = [0, 0, 0]

        player_position = self.GetPlayerPosition()

        # y
        if (player_position[1] - 40) < 0:
            if self.player.orientation == "UP":
                sensors[1] = 1
            elif self.player.orientation == 'LEFT':
                sensors[2] = 1
            elif self.player.orientation == 'RIGHT':
                sensors[0] = 1

        elif (player_position[1] + 40) > self.size[1]:
            if self.player.orientation == "DOWN":
                sensors[1] = 1
            elif self.player.orientation == 'RIGHT':
                sensors[2] = 1
            elif self.player.orientation == 'LEFT':
                sensors[1] = 1

        #x
        if (player_position[0] + 40) > self.size[0]:
            if self.player.orientation == "UP":
                sensors[2] = 1
            elif self.player.orientation == 'RIGHT':
                sensors[1] = 1
            elif self.player.orientation == 'DOWN':
                sensors[0] = 1

        elif (player_position[0] - 40) < 0:
            if self.player.orientation == "UP":
                sensors[0] = 1
            elif self.player.orientation == 'LEFT':
                sensors[1] = 1
            elif self.player.orientation == 'DOWN':
                sensors[2] = 1

        if self.player.orientation == "UP":
            front_pos = [player_position[0], player_position[1] - 20]
        elif self.player.orientation == "DOWN":
            front_pos = [player_position[0], player_position[1] + 20]
        elif self.player.orientation == "LEFT":
            front_pos = [player_position[0] - 20, player_position[1]]
        elif self.player.orientation == "RIGHT":
            front_pos = [player_position[0] + 20, player_position[1]]

        if front_pos in self.paths:
            print('visited path in front of robot')
            sensors[1] = 1

        return sensors


def CreateBoards(pop_size=5, board_size=(500, 500)):
    return [Board(size=board_size, id=i, training=True) for i in range(pop_size)]


def ResetBoards(boards):
    for board in boards:
        board.Reset()

    return boards
