import game1
import genetics
import pygame


BOARD_SIZE = (500, 600)

board = game1.Board(size=BOARD_SIZE, balls_vel=5, player_vel=10, spawn_rate=125)
window = game1.Window(size=BOARD_SIZE, fps=60, title="A nice Neural Network is playing")

network = genetics.Network()

network.add(genetics.FCLayer(2, 20))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(20, 10))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(10, 2))
network.add(genetics.ActivationLayer(genetics.tanh))

player = genetics.Genome(network)

player.network.LoadState("./model.json")

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

    if not playing:
        continue

    movement = player.Inference(board.Get1DPositions())
    board.MovePlayer(movement)

    board.Tick()

    if board.IsGameOver():
        board.Reset()

    window.Draw(board)
