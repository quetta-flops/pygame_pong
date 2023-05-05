import numpy as np
import pygame as pg
import sys

WINDOW_SIZE = (1000, 700)
WINDOW_TITLE = "PONG"
DELTA_TIME = 0.01
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_INIT_POS1 = (100.0, 300.0)
PADDLE_INIT_POS2 = (900.0, 300.0)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 70

BALL_RADIUS = 5
BALL_INIT_POS = (500.0, 350.0)
BALL_INIT_VEL = (5.0, 5.0)

PLAYER1_NAME = "Player_1"
PLAYER1_UP_KEY = pg.K_w
PLAYER1_DOWN_KEY = pg.K_s
PLAYER2_NAME = "Player_2"
PLAYER2_UP_KEY = pg.K_i
PLAYER2_DOWN_KEY = pg.K_k

class Vec2D():
    def __init__(self, init=[0, 0]):
        self.__vector = np.array(init)

    @property
    def vector(self):
        return self.__vector
    
    @vector.setter
    def vector(self, vec):
        self.__vector = vec
    
    @property
    def x(self):
        return self.__vector[0]
    
    @x.setter
    def x(self, x):
        self.__vector[0] = x
    
    @property
    def y(self):
        return self.__vector[1]
    
    @y.setter
    def y(self, y):
        self.__vector[1] = y

class Object():
    def __init__(self, init_pos, init_vel, init_accel):
        self.pos = Vec2D(init_pos)
        self.vel = Vec2D(init_vel)
        self.accel = Vec2D(init_accel)

    def move():
        pass

    def draw():
        pass

class Ball(Object):
    def __init__(self, init_pos, init_vel, init_accel=[0,0], radius=BALL_RADIUS):
        super().__init__(init_pos, init_vel, init_accel)
        self.radius = radius

    def move(self):
        delta_pos = self.vel.vector * DELTA_TIME
        self.pos.vector += delta_pos

        # 跳ね返り
        if self.pos.y <= 0.0 or self.pos.y >= 700.0:
            print("REFLECTION!!!")
            self.vel.y = -self.vel.y

        elif self.pos.x <=0 or self.pos.x >= 1000:
            print("REFLECTION!!!")
            self.vel.x = -self.vel.x
            
        #print(f"BALL POSITON: {self.pos.y}")
        #print(f"BALL VELOCTIY: {self.vel.y}")

    def draw(self, window):
        # print("draw ball")
        pg.draw.circle(window, WHITE, self.pos.vector, self.radius)

class Paddle(Object):
    def __init__(self, init_pos, player):
        super().__init__(init_pos, [0,0], [0,0])
        self.player = player
        self.rect = pg.Rect(init_pos, (PADDLE_WIDTH, PADDLE_HEIGHT))

    def move(self):
        if self.player.command == "UP":
            print(f"{self.player.name}'s command {self.player.command} recieved")
            # self.pos.y += 1 # パドルを上に動かす
            self.rect.move(0, 1)

        elif self.player.command == "DOWN":
            print(f"{self.player.name}'s DOWN command {self.player.command} recieved")
            #s elf.pos.y -= 1 # パドルを下に動かす
            self.rect.move(0, -1)

        else: pass #print("no command recieved")

        # print(f"{self.player.name}'s PADDLE POSITION: {self.pos.x, self.pos.y}")

    def draw(self, window):
        # print("draw paddle")
        pg.draw.rect(window, WHITE, self.rect)

class Player():
    def __init__(self, name, up_key, down_key):
        self.name = name
        self.up_key = up_key
        self.down_key = down_key
        self.command = None

    def control_paddle(self, pressed_key):
        if pressed_key[self.up_key]:
            self.command = "UP"
            print(f"{self.name} comamnd: UP")

        elif pressed_key[self.down_key] == True:
            self.command = "DOWN"
            print(f"{self.name} comamnd: DOWN")

        else: print("no commands")

        self.command = None

class Game():
    def __init__(self):
        print("pygame初期化、window生成")
        pg.init()
        pg.key.set_repeat(50, 50)
        self.window = pg.display.set_mode(WINDOW_SIZE)
        self.title = pg.display.set_caption(WINDOW_TITLE)
        self.is_dead = False

        self.player1 = Player(PLAYER1_NAME, PLAYER1_UP_KEY, PLAYER1_DOWN_KEY)
        self.player2 = Player(PLAYER2_NAME, PLAYER2_UP_KEY, PLAYER2_DOWN_KEY)

        # ステージ生成
        self.ball = Ball(BALL_INIT_POS, BALL_INIT_VEL)
        self.paddle1 = Paddle(PADDLE_INIT_POS1, self.player1)
        self.paddle2 = Paddle(PADDLE_INIT_POS2, self.player2)
        self.objects = [self.ball, self.paddle1, self.paddle2]
        
    def check_event(self):
        pressed_key = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_dead = True # 終了フラグ

            if event.type == pg.KEYDOWN:    # キーボード入力処理
                # pressed_key = pg.key.name(event.key)   # 入力されたキーの名前
                pressed_key = pg.key.get_pressed()
                self.player1.control_paddle(pressed_key)
                self.player2.control_paddle(pressed_key)

            #if event.type == pg.MOUSEMOTION:
            #    x, y = event.pos
            #    print(x, y)

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f"mouse button pushed at {x, y}")

    def update(self):
        for obj in self.objects:
            obj.move()

    def draw(self):
        for obj in self.objects:
            obj.draw(self.window)
        pg.display.update()
        self.window.fill(BLACK)
        

    def loop(self): # メインループ
        self.check_event()
        self.update()
        self.draw()

    def quit(self): # 終了処理
        pg.quit()
        sys.exit()

def main():
    game = Game()
    while(not game.is_dead):
        game.loop()

    game.quit()

if __name__ == "__main__":
     main()