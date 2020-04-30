import game
import pygame


board_size = (500, 400)

board = game.Board(size=board_size, balls_vel=3)
window = game.Window(size=board_size, fps=60, title="You are playing")

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

    if not playing:
        continue

    mouse_position = pygame.mouse.get_pos()
    key = pygame.key.get_pressed()

    board.player.SetPositionX(mouse_position[0])
    board.Tick(key[pygame.K_q])

    if board.IsGameOver():
        board.Reset()

    window.Draw(board, 0)