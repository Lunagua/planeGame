#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""游戏主程序"""

import pygame
from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        """游戏初始化:
                1.创建游戏的窗口
                2.创建游戏的时钟
                3.调用私有方法，精灵和精灵组的创建
                4.设置定时器事件，- 创建敌机  1s"""

        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, CREATE_ENEMY_TIME)
        pygame.time.set_timer(HERO_FIRE_EVENT, HERO_FIRE_TIME)
        pygame.time.set_timer(SUPPLY_VISIT_EVENT,SUPPLY_TIME)

    def start_game(self):
        """游戏开始:
        1.设置刷新帧率
        2.事件监听
        3.碰撞检测
        4.更新/绘制精灵组
        5.更新显示"""
        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()

    def __create_sprites(self):
        """创建精灵和精灵组"""
        # 创建背景精灵和精灵组
        self.back_ground = pygame.sprite.Group(Background(), Background(True))
        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        # 创建补给精灵组
        self.supply_group = pygame.sprite.Group()

    def __event_handler(self):
        """事件监听"""

        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵，并将敌机精灵假如敌机精灵组
                self.enemy_group.add(Enemy())
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            elif event.type == SUPPLY_VISIT_EVENT:
                self.supply = Supply()
                self.supply_group.add(self.supply)

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 3
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -3
        elif keys_pressed[pygame.K_UP]:
            self.hero.move_up_and_down = -3
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.move_up_and_down = 3
        else:
            self.hero.speed = 0
            self.hero.move_up_and_down = 0

    def __check_collide(self):
        """碰撞检测"""
        # 1.子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 2.敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            PlaneGame.__game_over()
        # 3.英雄获得补给
        supply = pygame.sprite.spritecollide(self.hero, self.supply_group, True)
        if len(supply) > 0:
            self.supply.kill()
            self.hero.add_supply()

    def __update_sprites(self):
        """更新精灵组"""
        self.back_ground.update()
        self.back_ground.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.supply_group.update()
        self.supply_group.draw(self.screen)

    @staticmethod
    def __game_over():
        """游戏结束"""
        print("游戏结束...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    # 启动游戏
    game.start_game()
