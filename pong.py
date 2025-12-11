import random


class Frame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[" " for _ in range(width)] for _ in range(height)]

    def render(self, step=None, reward=None):
        """Render the frame to the terminal"""
        # Clear the terminal (works on most systems)
        print("\033c", end="")
        
        # Build the frame as a string
        frame_str = ""
        for row in self.pixels:
            frame_str += "".join(row) + "\n"
        
        print(frame_str)
        if step is not None and reward is not None:
            print(f"Step: {step}, Reward: {reward}")


class Paddle:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.width = 1
        self.height = height


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])


class PongGame:
    def __init__(self, width, height, paddle_height, limits):
        self.width = width
        self.height = height
        self.frame = Frame(width, height)
        self.paddle1 = Paddle(x=0, y=height // 2, height=paddle_height)
        self.paddle2 = Paddle(x=width - 1, y=height // 2, height=paddle_height)
        self.ball = Ball(x=width // 2, y=height // 2)
        self.limits = limits
        self.step = 0
        self.reward = 0

    def forward(self):
        self.ball.x += self.ball.speed_x
        self.ball.y += self.ball.speed_y

        self.check_hit()

        if self.ball.speed_x < 0:
            distance_to_paddle1 = self.ball.x - self.paddle1.x
            time_to_paddle1 = distance_to_paddle1 / abs(self.ball.speed_x)
            predicted_y1 = self.ball.y + self.ball.speed_y * time_to_paddle1
            self.paddle1.y = max(
                min(int(predicted_y1), self.height - self.paddle1.height // 2),
                self.paddle1.height // 2,
            )

    def reset(self):
        if self.step >= self.limits:
            raise Exception("Game Over")
        
        self.step += 1
        self.ball = Ball(x=self.width // 2, y=self.height // 2)

    def check_hit(self):
        # hit first paddle
        if self.ball.x == self.paddle1.x + self.paddle1.width:
            if (
                self.ball.y <= self.paddle1.y + self.paddle1.height // 2
                and self.ball.y >= self.paddle1.y - self.paddle1.height // 2
            ):
                self.ball.speed_x = -self.ball.speed_x
            else:
                self.reset()
        # hit second paddle
        if self.ball.x == self.paddle2.x - self.paddle2.width:
            if (
                self.ball.y <= self.paddle2.y + self.paddle2.height // 2
                and self.ball.y >= self.paddle2.y - self.paddle2.height // 2
            ):
                self.ball.speed_x = -self.ball.speed_x
                self.reward += 1
            else:
                self.reset()
        # hit top wall
        if self.ball.y == 0:
            self.ball.speed_y = -self.ball.speed_y
        # hit bottom wall
        if self.ball.y == self.frame.height - 1:
            self.ball.speed_y = -self.ball.speed_y

    def draw(self):
        """Draw the game state to the frame"""
        # Clear the frame
        self.frame.pixels = [[" " for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw paddles
        for i in range(self.paddle1.height):
            paddle1_y = self.paddle1.y - self.paddle1.height // 2 + i
            if 0 <= paddle1_y < self.height:
                self.frame.pixels[paddle1_y][self.paddle1.x] = "|"
        
        for i in range(self.paddle2.height):
            paddle2_y = self.paddle2.y - self.paddle2.height // 2 + i
            if 0 <= paddle2_y < self.height:
                self.frame.pixels[paddle2_y][self.paddle2.x] = "|"
        
        # Draw ball
        if 0 <= self.ball.y < self.height and 0 <= self.ball.x < self.width:
            self.frame.pixels[self.ball.y][self.ball.x] = "O"
        
        # Draw boundaries
        for x in range(self.width):
            self.frame.pixels[0][x] = "-"
            self.frame.pixels[self.height - 1][x] = "-"
