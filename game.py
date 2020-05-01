import game
import pygame


BOARD_SIZE = (500, 600)

board = game.Board(size=BOARD_SIZE, balls_vel=5, spawn_rate=125)
window = game.Window(size=BOARD_SIZE, fps=60, title="You are playing")

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

    if not playing:
        continue

    mouse_position = pygame.mouse.get_pos()

    board.player.SetPositionX(mouse_position[0])
    board.Tick()

    if board.IsGameOver():
        board.Reset()

    window.Draw(board)
