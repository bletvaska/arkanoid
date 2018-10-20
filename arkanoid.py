WIDTH = 480
HEIGHT = 640
TITLE = 'Arkanoid'

class Ball(Actor):
    def __init__(self):
        super().__init__('ball-blue')
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.dx = 1
        self.dy = 1
        self.speed = 5

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        if self.right > WIDTH:
            self.dx *= -1

        if self.left < 0:
            self.dx *= -1

        if self.top < 0:
            self.dy *= -1

        if self.bottom > HEIGHT:
            self.dy *= -1

        for actor in actors:
            if isinstance(actor, Brick) and self.colliderect(actor):
                actors.remove(actor)
                self.dy *= -1



class Brick(Actor):
    def __init__(self):
        super().__init__('brick-red')


class Paddle(Actor):
    def __init__(self):
        super().__init__('paddle-blue')
        self.bottom = HEIGHT
        self.x = WIDTH / 2
        self.speed = 5

    def update(self):
        if keyboard.z:
            self.x -= self.speed
            if self.left < 0:
                self.left = 0

        if keyboard.x:
            self.x += self.speed
            if self.right > WIDTH:
                self.right = WIDTH


actors = []

ball = Ball()
paddle = Paddle()

actors.append(ball)
actors.append(paddle)

for row in range(5):
    for col in range(7):
        brick = Brick()
        brick.left = col * brick.width
        brick.top = row * brick.height
        actors.append(brick)

def draw():
    screen.clear()
    for actor in actors:
        actor.draw()

def update():
    ball.update()
    paddle.update()


