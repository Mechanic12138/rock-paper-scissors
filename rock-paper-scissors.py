# coding=utf-8
import random
import pygame
import cv2
from aip import AipBodyAnalysis
from threading import Thread
import time

APP_ID = '*****'
API_KEY = '*****'
SECRET_KEY = '*****'


def zlyb():
    global youwin, pcwin, cont
    screen.fill(0)
    pygame.display.update()
    youwin = 0
    pcwin = 0
    flag1 = 1
    cont = 0
    starting_screen('再来一把嘛')


def gameover():
    screen.fill([0, 0, 0])
    pygame.display.update()
    if youwin == 2:
        wenzi1 = font.render('恭喜你，你拿下两场胜利，游戏结束', True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
        screen.blit(wenzi1, (SCREEN_WIDTH // 2 - wenzi1.get_width() // 2, 150))
        pygame.display.update()
        pygame.time.wait(2000)  # 暂停2s
        zlyb()
    if pcwin == 2:
        wenzi2 = font.render('恭喜你，你输了两场，游戏结束', True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
        screen.blit(wenzi2, (SCREEN_WIDTH // 2 - wenzi2.get_width() // 2, 150))
        pygame.display.update()
        pygame.time.wait(2000)  # 暂停2s
        zlyb()


def yunsuan(player):
    global youwin, pcwin, cont
    screen.fill(0)
    pygame.display.update()
    computer = random.randint(0, 2)
    if computer == 0:
        computer1 = "石头"
    elif computer == 1:
        computer1 = "布"
    else:
        computer1 = "剪刀"
    if player == 0:
        player1 = "石头"
    elif player == 1:
        player1 = "布"
    else:
        player1 = "剪刀"
    display()
    wenzi3 = font.render('你出的是%s' % player1, True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
    screen.blit(wenzi3, (SCREEN_WIDTH // 2 - wenzi3.get_width() // 2, 100))
    if (player == 0 and computer == 2) or (player == 1 and computer == 0) or (player == 2 and computer == 1):
        wenzi1 = font.render('电脑出的是%s,你赢了' % computer1, True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
        screen.blit(wenzi1, (SCREEN_WIDTH // 2 - wenzi1.get_width() // 2, 150))
        pygame.display.update()
        pygame.time.wait(2000)  # 暂停2s
        youwin = youwin + 1
        if youwin == 2:
            gameover()
        else:
            moshi()
    elif player == computer:
        wenzi2 = font.render('电脑出的是%s,这把是平局' % computer1, True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
        screen.blit(wenzi2, (SCREEN_WIDTH // 2 - wenzi2.get_width() // 2, 150))
        pygame.display.update()
        pygame.time.wait(2000)  # 暂停2s
        moshi()
    else:
        wenzi2 = font.render('电脑出的是%s,你输了' % computer1, True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
        screen.blit(wenzi2, (SCREEN_WIDTH // 2 - wenzi2.get_width() // 2, 150))
        pygame.display.update()
        pygame.time.wait(2000)  # 暂停2s
        pcwin += 1
        if pcwin == 2:
            gameover()
        else:
            moshi()


capture = cv2.VideoCapture(0)  # 0为默认摄像头


def camera():
    global flag1
    while flag1 == 1:
        # 获得图片
        ret, frame = capture.read()
        # cv2.imshow(窗口名称, 窗口显示的图像)
        # 显示图片
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    exit()


def gesture_recognition():
    global flag1
    gesture_client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
    # 第一个参数ret 为True 或者False,代表有没有读取到图片

    # 第二个参数frame表示截取到一帧的图片

    while True:
        time.sleep(3.00)
        # 调用摄像头
        ret, frame = capture.read()
        # 图片格式转换
        image = cv2.imencode('.jpg', frame)[1]
        gesture = gesture_client.gesture(image)  # AipBodyAnalysis内部函数
        words = gesture['result'][0]['classname']
        flag1 = 0
        return words


def tuxiang():
    global flag1
    screen.fill(0)
    pygame.display.update()
    flag1 = 1
    Thread(target=camera).start()  # 引入线程防止在识别的时候卡死
    player = gesture_recognition()
    cv2.destroyAllWindows()
    if player == 'Fist':
        yunsuan(0)
    elif player == 'Five':
        yunsuan(1)
    elif player == 'Two':
        yunsuan(2)
    else:
        wenzi = font.render('没有识别出来你出的是什么，下次请把手靠近摄像头，但不要太近', True, [255, 255, 255])
        screen.blit(wenzi, [200, 300])
        pygame.display.update()
        time.sleep(2)
        moshi()


def sbxz():
    screen.fill([0, 0, 0])
    display()
    pygame.display.update()
    bu = pygame.image.load('bu.jpg')
    screen.blit(bu, [150, 150])
    shitou = pygame.image.load('shitou.jpg')
    screen.blit(shitou, [400, 150])
    jiandao = pygame.image.load('jiandao.jpg')
    screen.blit(jiandao, [660, 150])
    pygame.display.update()
    button1 = Button('出布', [255, 0, 0], 200, 450, centered_x=False)
    button2 = Button('出石头', [255, 255, 255], 430, 450, centered_x=False)
    button3 = Button('出剪刀', [255, 255, 255], 680, 450, centered_x=False)

    button1.display()
    button2.display()
    button3.display()
    pygame.display.update()

    while True:

        if button1.check_click(pygame.mouse.get_pos()):
            button1 = Button('出布', [255, 0, 0], 200, 450, centered_x=False)
        else:
            button1 = Button('出布', [255, 255, 255], 200, 450, centered_x=False)

        if button2.check_click(pygame.mouse.get_pos()):
            button2 = Button('出石头', [255, 0, 0], 430, 450, centered_x=False)
        else:
            button2 = Button('出石头', [255, 255, 255], 430, 450, centered_x=False)
        if button3.check_click(pygame.mouse.get_pos()):
            button3 = Button('出剪刀', [255, 0, 0], 680, 450, centered_x=False)
        else:
            button3 = Button('出剪刀', [255, 255, 255], 680, 450, centered_x=False)

        button1.display()
        button2.display()
        button3.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if button1.check_click(pygame.mouse.get_pos()):
                yunsuan(1)
            if button2.check_click(pygame.mouse.get_pos()):
                yunsuan(0)
            if button3.check_click(pygame.mouse.get_pos()):
                yunsuan(2)


class Button(object):
    def __init__(self, text, color, x=None, y=None, **kwargs):
        self.surface = font.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = SCREEN_WIDTH // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['centered_y']:
            self.y = SCREEN_HEIGHT // 2 - self.HEIGHT // 2
        else:
            self.y = y

    def display(self):
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False

    def getract(self):
        return self.getract()


def moshi():
    global cont
    screen.fill(0)
    cont += 1
    display()
    pygame.display.update()
    moshi_1 = font.render('选择你的游玩模式', True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
    screen.blit(moshi_1, (SCREEN_WIDTH // 2 - moshi_1.get_width() // 2, 150))
    button1 = Button('鼠标选择', [255, 0, 0], None, 220, centered_x=True)
    button2 = Button('图像识别(正在开发ing，你点了也没用)', [255, 255, 255], None, 270, centered_x=True)

    button1.display()
    button2.display()

    pygame.display.update()

    while True:

        if button1.check_click(pygame.mouse.get_pos()):
            button1 = Button('鼠标选择', [255, 0, 0], None, 220, centered_x=True)
        else:
            button1 = Button('鼠标选择', [255, 255, 255], None, 220, centered_x=True)

        if button2.check_click(pygame.mouse.get_pos()):
            button2 = Button('图像识别(正在开发ing，你点了也没用)', [255, 0, 0], None, 270, centered_x=True)
        else:
            button2 = Button('图像识别(正在开发ing，你点了也没用)', [255, 255, 255], None, 270, centered_x=True)

        button1.display()
        button2.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if button1.check_click(pygame.mouse.get_pos()):
                sbxz()
            if button2.check_click(pygame.mouse.get_pos()):
                tuxiang()


def display():
    # 绘制游戏得分
    font = pygame.font.Font('C:\Windows\Fonts\STKAITI.TTF', 50)  # 字体以及字号
    player = font.render('you win:%s' % str(youwin), True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
    rect1 = player.get_rect()  # 把属性赋值给rect1
    rect1.left = 0  # 调整属性
    pc = font.render('pc win:%s' % str(pcwin), True, [255, 255, 255])  # 显示的内容，抗锯齿，字体颜色，背景色
    rect2 = player.get_rect()  # 把属性赋值给rect2
    rect2.right = screen.get_rect().right  # 调整属性
    zongshu = font.render('这是第%s把' % str(cont), True, [255, 255, 255])
    screen.blit(player, rect1)  # 显示内容
    screen.blit(pc, rect2)  # 显示内容
    screen.blit(zongshu, [400, 0])
    pygame.display.update()  # 更新屏幕


def caiquan():
    moshi()
    # 处理游戏退出
    # 从消息队列中循环取
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


class Wenzi:
    def __init__(self, text, color, x, y):
        self.display = font.render(text, False, color)
        self.y = y
        self.x = x

    def fanhui(self):
        return self


def starting_screen(txt):
    game_title = font.render(txt, True, [255, 255, 255])

    screen.blit(game_title, (SCREEN_WIDTH // 2 - game_title.get_width() // 2, 150))

    play_button = Button('Play', [255, 255, 255], None, 350, centered_x=True)
    exit_button = Button('Exit', [255, 255, 255], None, 400, centered_x=True)

    play_button.display()
    exit_button.display()

    pygame.display.update()

    while True:

        if play_button.check_click(pygame.mouse.get_pos()):
            play_button = Button('Play', [255, 0, 0], None, 350, centered_x=True)
        else:
            play_button = Button('Play', [255, 255, 255], None, 350, centered_x=True)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('Exit', [255, 0, 0], None, 400, centered_x=True)
        else:
            exit_button = Button('Exit', [255, 255, 255], None, 400, centered_x=True)

        play_button.display()
        exit_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                screen.fill([0, 0, 0])
                pygame.display.update()
                caiquan()
            if exit_button.check_click(pygame.mouse.get_pos()):
                screen.fill([0, 0, 0])  # 清除屏幕，内容为颜色
                pygame.display.update()
                tuichu = font.render('bye', True, [255, 255, 255])
                screen.blit(tuichu, (500, 340))  # 先宽，后高
                pygame.display.update()
                pygame.time.wait(2000)
                exit()


youwin = 0
pcwin = 0
flag1 = 1
cont = 0
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 680
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('石头剪刀布')
font = pygame.font.Font('C:\Windows\Fonts\STKAITI.TTF', 50)  # 字体以及字号
starting_screen('玩游戏嘛')
