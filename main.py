from pygame import *
from random import uniform


BAKGROUND_COLOR = (200, 255, 255)
WINDOW_WIDTH = 600 
WINDOW_HEIGTH = 500
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGTH)
FPS = 60
RED_COLOR = (255, 0 , 0)



class Actor(sprite.Sprite):
    def __init__(self, filename: str, x: int, y: int, speed: int, width: int, heigth: int):
        super().__init__()
        self.image = transform.scale(
            image.load(filename), (width, heigth)
        )

        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Actor):
    def __init__(self, filename: str, x: int, y: int, speed: int, width: int, heigth: int, key_up, key_down):
        super().__init__(filename, x, y, speed, width, heigth)
        self.key_up = key_up
        self.key_down = key_down
    
    def update(self):
        pressed = key.get_pressed()
        if pressed[self.key_up] and self.rect.y > 5:
            self.rect.y -= self.speed
        if pressed[self.key_down] and self.rect.y < WINDOW_HEIGTH - 80:
            self.rect.y += self.speed

class Ball(Actor):
    def __init__(self, filename: str, x: int, y: int, speed: int, width: int, heigth: int):
        super().__init__(filename, x, y, speed, width, heigth)
        self.speed_x = self.speed * uniform(0.5, 1.5)
        self.speed_y = self.speed * uniform(0.5, 1.5)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def on_collide(self):
        if (self.speed_x > 0 and self.speed_y > 0) or (self.speed_x < 0 and self.speed_y < 0):
            self.speed_x *= -1
        else:
            self.speed_y *= -1

    @property
    def x_coord(self):
        return self.rect.x

    def check_borders(self):
        if self.rect.y > WINDOW_HEIGTH - 50 or self.rect.y < 0:
            self.speed_y *= -1
        

window = display.set_mode(WINDOW_SIZE)
display.set_caption('Ping-Pong')
clock = time.Clock()

font.init()
lose_font = font.Font(None, 35)
left_lose = lose_font.render('left player lost', True, RED_COLOR)
right_lose = lose_font.render('right player lost', True, RED_COLOR)

right_player = Player('resources/racket.png', 520, 200, 4, 50, 150, K_UP, K_DOWN)
left_player = Player('resources/racket.png', 30, 200, 4, 50, 150, K_w, K_s)
ball = Ball('resources/tenis_ball.png', 200, 200, 6, 50, 50)


game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:

        window.fill(BAKGROUND_COLOR)

        left_player.update()
        right_player.update()
        ball.update()

        if sprite.collide_rect(left_player, ball) or sprite.collide_rect(right_player, ball):
            ball.on_collide()
        ball.check_borders()

        if ball.x_coord < 0:
            finish = True
            window.blit(left_lose, (200, 200))
        
        if ball.x_coord > WINDOW_WIDTH:
            finish = True
            window.blit(right_lose, (200, 200))
        
        left_player.draw()
        right_player.draw()
        ball.draw()

    display.update()
    clock.tick(FPS) 