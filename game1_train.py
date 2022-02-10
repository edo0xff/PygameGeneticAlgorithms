import os
import game1
import pygame
import genetics

BOARD_SIZE = (500, 600)
POPULATION_SIZE = 10

network = genetics.Network()

network.add(genetics.FCLayer(2, 20))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(20, 10))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(10, 2))
network.add(genetics.ActivationLayer(genetics.tanh))

population = genetics.CreatePopulation(network, pop_size=POPULATION_SIZE)
boards = game1.CreateBoards(pop_size=POPULATION_SIZE, board_size=BOARD_SIZE)
window = game1.Window(size=BOARD_SIZE)

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
            movement = AI.Inference(board.Get1DPositions())
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

        population = genetics.EvolvePopulation(population, 0.25)

        print(" [i] generation #%i evolved" % generation_count)

        boards = game1.ResetBoards(boards)

    window.Draw(boards[display_board], generation_count)
