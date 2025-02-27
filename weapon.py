from sprite_object import *
import pygame as pg
from collections import deque
import time

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()

class Shotgun(Weapon):
    def __init__(self, game):
        super().__init__(game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90)
        self.damage = 50
        self.shot_sound = pg.mixer.Sound('resources/sound/shotgun1.wav')  # โหลดเสียงปืน

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
                if self.frame_counter == 1:  # เล่นเสียงปืนเมื่อเริ่มอนิเมชั่น
                    self.shot_sound.play()

class Plasmarifle(Weapon):
    def __init__(self, game):
        super().__init__(game, path='resources/sprites/weapon/plasmarifle/0.png', scale=5, animation_time=100)
        self.damage = 25
        self.shot_sound = pg.mixer.Sound('resources/sound/plasmarifle.mp3')  # โหลดเสียงปืน

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
                if self.frame_counter == 1:  # เล่นเสียงปืนเมื่อเริ่มอนิเมชั่น
                    self.shot_sound.play()

class Rifle(Weapon):
    def __init__(self, game):
        super().__init__(game, path='resources/sprites/weapon/rifle/0.png', scale=3, animation_time=80)
        self.damage = 40
        self.shot_sound = pg.mixer.Sound('resources/sound/rifle.wav')  # โหลดเสียงปืน

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
                if self.frame_counter == 1:  # เล่นเสียงปืนเมื่อเริ่มอนิเมชั่น
                    self.shot_sound.play()

class SuperShotgun(Weapon):
    def __init__(self, game):
        super().__init__(game, path='resources/sprites/weapon/supershotgun/0.png', scale=5, animation_time=120)
        self.damage = 150
        self.shot_sound = pg.mixer.Sound('resources/sound/supers.wav')  # โหลดเสียงปืน

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
                if self.frame_counter == 1:  # เล่นเสียงปืนเมื่อเริ่มอนิเมชั่น
                    self.shot_sound.play()