import numpy as np
import time
from pong import PongGame


def main():

    game = PongGame(
        width=50,
        height=20,
        paddle_height=3,
        limits=1000,
    )
    
    try:
        while True:
            game.forward()
            game.draw()
            game.frame.render(game.step, game.reward)
            time.sleep(0.1)  # Add a small delay to make it visible
    except Exception as e:
        print(f"Game ended: {e}")
        game.draw()
        game.frame.render(game.step, game.reward)

    return game


if __name__ == "__main__":
    main()
