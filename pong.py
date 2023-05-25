import numpy as np
import pygame as pg
import sys
import time

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
        self._vector = np.array(init)

    @property
    def vector(self):
        return self._vector
    
    @vector.setter
    def vector(self, vec):
        self._vector = vec
    
    @property
    def x(self):
        return self._vector[0]
    
    @x.setter
    def x(self, x):
        self._vector[0] = x
    
    @property
    def y(self):
        return self._vector[1]
    
    @y.setter
    def y(self, y):
        self._vector[1] = y

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
    def __init__(self, paddles, init_pos, init_vel, init_accel=[0,0], radius=BALL_RADIUS):
        super().__init__(init_pos, init_vel, init_accel)
        self.init_pos = init_pos
        self.paddles = paddles
        self.radius = radius
        self.bound_volume = 0
        self.point_flag = None

    def move(self):
        delta_pos = self.vel.vector * DELTA_TIME
        self.pos.vector += delta_pos

        self.bound_volume = pg.Rect((self.pos.x-self.radius, self.pos.y+self.radius), (self.radius, self.radius))

        # 壁の跳ね返り
        if self.pos.y <= 0.0 or self.pos.y >= 700.0:
            print("REFLECTION!!!")
            self.vel.y = -self.vel.y

        elif self.pos.x <=0:
            print("player2 point_flag")
            self.point_flag = "player2"
            # プレイヤー１に加点
            # リセット
        
        elif self.pos.x >= 1000:
            print("player1 point_flag")
            self.point_flag = "player1"
            # プレイヤー２に加点
            # リセット
            

        # パドルの跳ね返り
        for pdl in self.paddles:
            if self.bound_volume.colliderect(pdl.rect):
                print("REFLECTION!!!")
                self.vel.x = -self.vel.x
            
        #print(f"BALL POSITON: {self.pos.y}")
        #print(f"BALL VELOCTIY: {self.vel.y}")

    def draw(self, window):
        # print("draw ball")
        pg.draw.circle(window, WHITE, self.pos.vector, self.radius)
    
    def reset(self, reset_pos):
        self.pos.vector = reset_pos
        print("reset ball")

class Paddle(Object):
    def __init__(self, init_pos, player):
        super().__init__(init_pos, [0,0], [0,0])
        self.init_pos = init_pos
        self.player = player
        self.rect = pg.Rect(init_pos, (PADDLE_WIDTH, PADDLE_HEIGHT))
        # print(self.player.name)
        # print(self.player.command)

    def move(self):
        # print(f"{self.player.name}'s command {self.player.command} recieved")
        if self.player.command == "UP":
            self.pos.y -= 10 # パドルを上に動かす
            print(self.pos.y)

        elif self.player.command == "DOWN":
            self.pos.y += 10 # パドルを下に動かす
            print(self.pos.y)

        else: pass
            # print("no command recieved")
        self.player.command = None

        self.rect = pg.Rect((self.pos.x, self.pos.y), (PADDLE_WIDTH, PADDLE_HEIGHT))
        # self.rect = self.rect.move_ip(self.pos.x, self.pos.y)
        # print(f"{self.player.name}'s PADDLE POSITION: {self.pos.x, self.pos.y}")

    def draw(self, window):
        # print("draw paddle")
        pg.draw.rect(window, WHITE, self.rect)

    def reset(self, reset_pos):
        self.pos.y = reset_pos[1]
        print(self.player.name + " " + "init_pos:" + " " + str(self.init_pos))
        print("reset" + " " + self.player.name + " " + "paddle")

class Player():
    def __init__(self, name, up_key, down_key):
        self.name = name
        self.up_key = up_key
        self.down_key = down_key
        self.command = None
        self.point = 0

    def control_paddle(self, pressed_key):  # Paddleインスタンスに制御信号(UP, DOWN)を送る
        if pressed_key[self.up_key]:
            self.command = "UP"
            # print(f"{self.name} comamnd: {self.command}")

        elif pressed_key[self.down_key] == True:
            self.command = "DOWN"
            # print(f"{self.name} comamnd: {self.command}")

        else: pass
            #print("no commands")

    def add_point(self):
        print(self.name + " " + "add point")
        self.point += 1

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
        self.paddle1 = Paddle(PADDLE_INIT_POS1, self.player1)
        self.paddle2 = Paddle(PADDLE_INIT_POS2, self.player2)
        self.ball = Ball([self.paddle1, self.paddle2], BALL_INIT_POS, BALL_INIT_VEL)
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

    def reset(self):
        if self.ball.point_flag == None:
            return 

        # プレイヤーに加点
        elif self.ball.point_flag == "player1":
            self.player1.add_point()
            self.ball.point_flag = None

        elif self.ball.point_flag == "player2":
            self.player2.add_point()
            self.ball.point_flag = None

        for obj in self.objects:    # オブジェクトの位置をリセット
            obj.reset(obj.init_pos)

        time.sleep(1)
        print("sleep 1 sec")


    def loop(self): # メインループ
        self.check_event()
        self.update()
        self.draw()
        self.reset()

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