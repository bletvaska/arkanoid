#!/usr/bin/env python3
import pgzrun
# from pgzrun.actor import Actor
# from pgzrun import keyboard

WIDTH = 640
HEIGHT = 600
TITLE = 'Arkanoid'

actors = []
score = 0
lives = 3
state = 'SERVICE'


class Paddle(Actor):
    def __init__(self):
        super().__init__('paddle-blue')
        self.bottom = HEIGHT
        self.x = WIDTH/2
        self.speed = 7

    def update(self):
        if keyboard.z:
            self.left -= self.speed
            if self.left < 0:
                self.left = 0

        if keyboard.x:
            self.right += self.speed
            if self.right > WIDTH:
                self.right = WIDTH



class Ball(Actor):
    def __init__(self, paddle):
        super().__init__('ball-blue')
        self.paddle = paddle
        self.x = WIDTH/2
        self.speed = 10
        self.dx = 1
        self.dy = -1

    def _service(self):
        self.midbottom = self.paddle.midtop
        self.dy = -1

    def update(self):
        # update ball movement
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # check the borders
        if self.right > WIDTH:
            self.right = WIDTH
            self.dx *= -1

        if self.left < 0:
            self.left = 0
            self.dx *= -1

        if self.top < 0:
            self.top = 0
            self.dy *= -1

        if self.colliderect(self.paddle):
            self.dy *= -1

        if self.bottom > HEIGHT:
            global lives
            lives -= 1
            self._service()
            return

        for actor in actors:
            # remove brick, if in colision
            if isinstance(actor, Brick) and self.colliderect(actor):
                actors.remove(actor)
                self.dy *= -1
                global score
                score += 100
                break


class Brick(Actor):
    def __init__(self, color):
        super().__init__(f'brick-{color}')

    def update(self):
        pass


def draw():
    screen.clear()
    screen.blit('background', (0, (HEIGHT-480)/2))

    # draw all actors
    bricks = 0
    for actor in actors:
        if isinstance(actor, Brick):
            bricks += 1
        actor.draw()

    # draw hid
    screen.draw.text(f'SCORE: {score}', (0,0))
    screen.draw.text(f'LIVES: {lives}', right=WIDTH, top=0)

    # check number of bricks
    if bricks == 0:
        screen.draw.text('Well Done', (WIDTH/2, HEIGHT/2))
        while True:
            pass


def update():
    # escape to exit
    if keyboard.escape:
        exit()

    # update every actor
    for actor in actors:
        actor.update()


def main():
    paddle = Paddle()
    actors.append(paddle)

    ball = Ball(paddle)
    ball.bottom = paddle.top
    actors.append(ball)

    colors = ('red', 'green', 'purple', 'yellow', 'grey')
    for row in range(10):
        for col in range(len(colors)):
            brick = Brick(colors[col])
            brick.left = row * brick.width
            brick.top = col * brick.height
            actors.append(brick)

    pgzrun.go()

main()
