import os
import pygame
import genetics
import game

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

BOARD_SIZE = (500, 400)
POP_SIZE = 20
FPS = 60

population = genetics.CreatePopulation(pop_size=POP_SIZE)
boards = game.CreateBoards(pop_size=POP_SIZE, board_size=BOARD_SIZE)
window = game.Window(size=BOARD_SIZE, fps=FPS)

generation = 0
display_board = 0
game_over_boards = 0

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        i = 0
        for board in boards:
            if not board.IsGameOver():
                neural_net = population[i]

                movement = neural_net.MovementPrediction(board.Get1DPositions())
                board.MovePlayer(movement)

                board.Tick()

                if board.IsGameOver():
                    game_over_boards += 1
                    population[i].SetFitness(board.GetScore())

            elif display_board == i:
                display_board += 1

            i += 1

        if game_over_boards == len(boards):
            print(" [i] Evolving networks")

            generation += 1
            display_board = 0
            game_over_boards = 0

            population, boards = genetics.SortPopulation(population, boards)

            population = genetics.EvolvePopulation(population)
            boards = game.ResetBoards(boards)

            print(" [i] generation #%i evolved" % generation)

        window.Draw(boards[display_board])

except KeyboardInterrupt:
    pass
