import game
import genetics
import pygame


BOARD_SIZE = (500, 600)
SONG_BIT_RATE = 44100
SONG_BPM = 107

board = game.Board(size=BOARD_SIZE, balls_vel=5, player_vel=10, spawn_rate=SONG_BPM)
window = game.Window(size=BOARD_SIZE, fps=60, title="A nice Neural Network is playing")
player = genetics.Genome()

player.network.LoadState("./model.json")

pygame.mixer.pre_init(SONG_BIT_RATE, -16, 2, 2048)
pygame.mixer.init()

pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play(-1)

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

    window.Draw(board)
