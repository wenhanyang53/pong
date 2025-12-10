import numpy as np
from pong import PongGame


def main():

    game = PongGame(
        width=200,
        height=200,
        paddle_height=5,
        limits=1000,
    )
    while True:
        game.forward()

    return game


if __name__ == "__main__":
    main()
