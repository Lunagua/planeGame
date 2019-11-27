#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""游戏工具模块"""
import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)  # 定义屏幕大小的常量
FRAME_PER_SEC = 60  # 刷新帧率
CREATE_ENEMY_EVENT = pygame.USEREVENT  # 创建敌机的定时器常量
CREATE_ENEMY_TIME = 1000  # 创建敌机的时间间隔，毫秒
HERO_FIRE_EVENT = pygame.USEREVENT + 1  # 英雄发射子弹事件
HERO_FIRE_TIME = 500  # 英雄发射子弹时间间隔，毫秒
HERO_RECT_Y = 120  # 英雄飞机出场位置
SUPPLY_VISIT_EVENT = pygame.USEREVENT + 2  # 补给出现定时器常量
SUPPLY_TIME = 10000  # 补给出现时间间隔


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()

        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向运动
        self.rect.y += self.speed


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 1.调用父类方法，设置image&speed
        super().__init__('./resources/images/me1.png', 0)
        # 2.设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - HERO_RECT_Y
        # 3.创建子弹的精灵组
        self.bullets = pygame.sprite.Group()
        # 4.英雄子弹加强属性
        self.more_bullets = 1
        self.move_up_and_down = 0

    def update(self):
        # 英雄在水平方向移动
        self.rect.x += self.speed
        # 控制英雄不能离开屏幕
        if self.rect.right > SCREEN_RECT.right + self.rect.width / 2:
            self.rect.right = SCREEN_RECT.right + self.rect.width / 2
        if self.rect.x < -self.rect.width / 2:
            self.rect.x = -self.rect.width / 2
        # 英雄在垂直方向移动
        self.rect.y += self.move_up_and_down
        # 控制英雄不能离开屏幕
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_RECT.height - self.rect.height / 2:
            self.rect.y = SCREEN_RECT.height - self.rect.height / 2

    def fire(self):
        """发射子弹"""
        if self.more_bullets == 4:
            bullet1 = BulletStrengthen()
            bullet2 = BulletStrengthen1()
            # 2.设置子弹精灵的位置
            bullet1.rect.bottom = self.rect.y
            bullet1.rect.centerx = self.rect.centerx - 10
            bullet2.rect.bottom = self.rect.y
            bullet2.rect.centerx = self.rect.centerx + 10
            # 3.将精灵添加到精灵组
            self.bullets.add(bullet1)
            self.bullets.add(bullet2)
        for i in range(-self.more_bullets // 2, self.more_bullets // 2 + 1):
            # 1.创建子弹精灵
            bullet = Bullet()
            # 2.设置子弹精灵的位置
            bullet.rect.bottom = self.rect.y
            bullet.rect.centerx = self.rect.centerx + 5 * i
            # 3.将精灵添加到精灵组
            self.bullets.add(bullet)

    def add_supply(self):
        if self.more_bullets < 4:
            self.more_bullets += 1


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__('./resources/images/bullet1.png', -2)

    def update(self):
        # 1. 调用父类方法，让子弹沿垂直方向飞行
        super().update()
        # 2.子弹飞出屏幕后，销毁子弹
        if self.rect.bottom < 0:
            self.kill()


class BulletStrengthen(GameSprite):
    """加强版子弹"""

    def __init__(self):
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__('./resources/images/bullet2.png', -2)

    def update(self):
        # 1. 调用父类方法，让子弹沿垂直方向飞行
        super().update()
        self.rect.x += self.speed/2
        # 2.子弹飞出屏幕后，销毁子弹
        if self.rect.bottom < 0:
            self.kill()


class BulletStrengthen1(GameSprite):
    """加强版子弹"""

    def __init__(self):
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__('./resources/images/bullet2.png', -2)

    def update(self):
        # 1. 调用父类方法，让子弹沿垂直方向飞行
        super().update()
        self.rect.x -= self.speed/2
        # 2.子弹飞出屏幕后，销毁子弹
        if self.rect.bottom < 0:
            self.kill()


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__('./resources/images/enemy1.png')
        # 2.指定敌机的初始随机速度
        self.speed = random.randint(1, 3)
        # 3.指定敌机的初始随机位置
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.rect.bottom = 0  # self.rect.y = -self.rect.height

    def update(self):
        # 1.调用父类方法，保持垂直方向的飞行
        super().update()
        # 2.判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # kill可以将精灵充所以的精灵组中移出，精灵就会被自动销毁
            self.kill()


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        # 1.调用父类方法实现精灵的创建（image/rect/speed）
        super().__init__('./resources/images/background.png')
        # 2.判断是否交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        """
        1.调用父类的方法实现
        2.判断图像是否移出屏幕，如果移出，则将图像设置到屏幕上方
        """
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Supply(GameSprite):
    def __init__(self):
        super().__init__('./resources/images/bullet_supply.png')
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        super().update()
        self.rect.x += random.randint(-5, 5)
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = SCREEN_RECT.height
        if self.rect.centerx < 0:
            self.rect.centerx = SCREEN_RECT.width
        if self.rect.centerx > SCREEN_RECT.width:
            self.rect.centerx = 0
