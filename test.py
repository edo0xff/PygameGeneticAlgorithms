import game
import genetics
import pygame


board_size = (500, 400)

board = game.Board(size=board_size, balls_vel=3, player_vel=8)
window = game.Window(size=board_size, fps=60, title="A nice Neural Network is playing")
player = genetics.Subject()

player.network.load_state("./model.json")

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

    if not playing:
        continue

    movement = player.MovementPrediction(board.Get1DPositions())
    board.MovePlayer(movement)

    board.Tick()

    if board.IsGameOver():
        board.Reset()

    window.Draw(board, 0)