import pygame as pg
from settings import *  # นำเข้าตัวแปรค่าต่าง ๆ จากไฟล์ settings
import os  # ใช้สำหรับจัดการเส้นทางไฟล์
from collections import deque  # ใช้สำหรับสร้างรายการที่สามารถหมุนได้ (rotate)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # กำหนด path ของไฟล์สคริปต์ปัจจุบัน
IMAGE_PATH = os.path.join(BASE_DIR, "resources", "sprites", "weapon", "shotgun", "0.png")  # กำหนด path ของไฟล์รูปภาพ




class SpriteObject:
    def __init__(self, game, path, pos=(10, 10), scale=0.8, shift=0.15):
        absolute_path = os.path.join(os.path.dirname(__file__), path)  # กำหนด path ของไฟล์ sprite
        self.image = pg.image.load(absolute_path).convert_alpha()  # โหลดภาพและทำให้พื้นหลังโปร่งใส


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game  # อ้างอิงไปยังอ็อบเจ็กต์เกมหลัก
        self.player = game.player  # อ้างอิงไปยังผู้เล่น
        self.x, self.y = pos  # กำหนดตำแหน่งของ sprite
        self.image = pg.image.load(path).convert_alpha()  # โหลดภาพ sprite และทำให้พื้นหลังโปร่งใส
        self.IMAGE_WIDTH = self.image.get_width()  # ความกว้างของภาพ sprite
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2  # ครึ่งหนึ่งของความกว้าง
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()  # อัตราส่วนกว้างต่อสูงของภาพ
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1  # ค่าตัวแปรที่ใช้ในคำนวณ
        self.sprite_half_width = 0  # ครึ่งหนึ่งของความกว้าง sprite หลังการฉายภาพ
        self.SPRITE_SCALE = scale  # อัตราส่วนการขยาย sprite
        self.SPRITE_HEIGHT_SHIFT = shift  # การเลื่อน sprite ในแนวตั้ง

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE  # คำนวณขนาดของ sprite บนหน้าจอ
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj  # กำหนดความกว้างและความสูงของ sprite

        image = pg.transform.scale(self.image, (proj_width, proj_height))  # ปรับขนาดภาพ sprite ให้เหมาะสม

        self.sprite_half_width = proj_width // 2  # คำนวณค่าครึ่งหนึ่งของความกว้าง
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT  # คำนวณการเลื่อนแนวตั้ง
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift  # คำนวณตำแหน่งของ sprite บนหน้าจอ

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))  # เพิ่ม sprite เข้าไปในรายการที่ต้องแสดงผล

    def get_sprite(self):
        dx = self.x - self.player.x  # คำนวณระยะห่างแกน X ระหว่าง sprite กับผู้เล่น
        dy = self.y - self.player.y  # คำนวณระยะห่างแกน Y ระหว่าง sprite กับผู้เล่น
        self.dx, self.dy = dx, dy  # กำหนดค่า dx และ dy
        self.theta = math.atan2(dy, dx)  # คำนวณมุมระหว่าง sprite กับผู้เล่น

        delta = self.theta - self.player.angle  # หาค่าความต่างของมุม
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):  # ปรับค่ามุมหาก sprite อยู่ด้านหลังผู้เล่น
            delta += math.tau  

        delta_rays = delta / DELTA_ANGLE  # คำนวณจำนวนเรย์ที่เบี่ยงเบน
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE  # คำนวณตำแหน่งของ sprite บนหน้าจอ

        self.dist = math.hypot(dx, dy)  # คำนวณระยะห่างระหว่าง sprite กับผู้เล่น
        self.norm_dist = self.dist * math.cos(delta)  # ปรับระยะทางให้ลดผลกระทบของ Fishbowl Effect
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()  # แสดง sprite หากอยู่ในมุมมองของผู้เล่น

    def update(self):
        self.get_sprite()  # อัปเดตตำแหน่งของ sprite


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)  # เรียกใช้ตัวสร้างของ SpriteObject
        self.animation_time = animation_time  # กำหนดระยะเวลาการเปลี่ยนภาพของ animation
        self.path = path.rsplit('/', 1)[0]  # แยก path ของไฟล์ภาพเพื่อใช้โหลดชุดภาพ
        self.images = self.get_images(self.path)  # โหลดภาพทั้งหมดในโฟลเดอร์
        self.animation_time_prev = pg.time.get_ticks()  # บันทึกเวลาเริ่มต้นของ animation
        self.animation_trigger = False  # กำหนดค่าเริ่มต้นให้ animation ยังไม่ทำงาน

    def update(self):
        super().update()  # เรียกใช้งาน update ของ SpriteObject
        self.check_animation_time()  # ตรวจสอบว่า animation ควรเปลี่ยนเฟรมหรือไม่
        self.animate(self.images)  # อัปเดตภาพ animation

    def animate(self, images):
        if self.animation_trigger:  # ถ้าถึงเวลาที่ต้องเปลี่ยนภาพ
            images.rotate(-1)  # หมุนรายการภาพไปข้างหน้า
            self.image = images[0]  # ใช้ภาพใหม่เป็นภาพปัจจุบัน

    def check_animation_time(self):
        self.animation_trigger = False  # กำหนดให้ animation ยังไม่เปลี่ยนภาพ
        time_now = pg.time.get_ticks()  # ได้เวลาปัจจุบันของเกม
        if time_now - self.animation_time_prev > self.animation_time:  # ถ้าเวลาที่ผ่านไปมากกว่ากำหนด
            self.animation_time_prev = time_now  # อัปเดตเวลาล่าสุดของ animation
            self.animation_trigger = True  # เปิดใช้งาน animation

    def get_images(self, path):
        images = deque()  # สร้าง deque เพื่อเก็บภาพ sprite
        for file_name in os.listdir(path):  # วนลูปผ่านไฟล์ทั้งหมดในโฟลเดอร์
            if os.path.isfile(os.path.join(path, file_name)):  # ตรวจสอบว่าเป็นไฟล์ภาพหรือไม่
                img = pg.image.load(path + '/' + file_name).convert_alpha()  # โหลดภาพและทำให้พื้นหลังโปร่งใส
                images.append(img)  # เพิ่มภาพเข้าไปใน deque
        return images  # ส่งคืนรายการภาพที่โหลดเสร็จแล้ว
