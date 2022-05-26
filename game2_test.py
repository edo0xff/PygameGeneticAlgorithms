import game2
import pygame
import genetics

BOARD_SIZE = (600, 600)

board = game2.Board(size=BOARD_SIZE)
window = game2.Window(size=BOARD_SIZE, fps=60, title="A nice Neural Network is playing")

network = genetics.Network()

network.add(genetics.FCLayer(4, 20))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(20, 20))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(20, 20))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(20, 10))
network.add(genetics.ActivationLayer(genetics.tanh))
network.add(genetics.FCLayer(10, 3))
network.add(genetics.ActivationLayer(genetics.tanh))

network.LoadState("./model.json")

player = genetics.Genome(network)

playing = True

board.player.SetPosition(300,300)

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

    if not playing:
        continue

    net_input = board.GetSensorValues()

    if not board.player.moving:
        movement = player.Inference(net_input)
        board.MovePlayer(movement)

    board.Tick()

    if board.IsGameOver():
        board.Reset()

    window.Draw(board)
