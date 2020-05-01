import os
import game
import pygame
import genetics

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

BOARD_SIZE = (500, 600)
POPULATION_SIZE = 10

population = genetics.CreatePopulation(pop_size=POPULATION_SIZE)
boards = game.CreateBoards(pop_size=POPULATION_SIZE, board_size=BOARD_SIZE)
window = game.Window(size=BOARD_SIZE)

done_boards = 0
display_board = 0
generation_count = 1

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

    if not playing:

        save = input(" [?] Do you wanna save model state? (y/n)")

        if save == "y":
            population[display_board].network.SaveState('./model.json')

        continue

    for AI, board in zip(population, boards):

        if not board.IsGameOver():
            movement = AI.MovementPrediction(board.Get1DPositions())
            board.MovePlayer(movement)

            board.Tick()

            if board.IsGameOver():
                done_boards += 1
                AI.SetFitness(board.GetScore())

        elif display_board == boards.index(board):
            display_board += 1

    if done_boards == len(boards):

        generation_count += 1
        display_board = 0
        done_boards = 0

        print(" [i] Evolving %i networks" % len(population))

        population = genetics.EvolvePopulation(population)

        print(" [i] generation #%i evolved" % generation_count)

        boards = game.ResetBoards(boards)

    window.Draw(boards[display_board], generation_count)
