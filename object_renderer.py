import pygame as pg  # นำเข้าไลบรารี pygame
from settings import *  # นำเข้าค่าตั้งค่าทั้งหมดจาก settings


class ObjectRenderer:
    def __init__(self, game):  # ฟังก์ชันเริ่มต้นของ ObjectRenderer
        self.game = game  # เก็บอ้างอิงไปยังอ็อบเจ็กต์เกมหลัก
        self.screen = game.screen  # ใช้หน้าจอของเกม
        self.wall_textures = self.load_wall_textures()  # โหลดพื้นผิวของกำแพง
        self.sky_image = self.get_texture('resources/textures/city.png', (WIDTH, HALF_HEIGHT))  # โหลดภาพท้องฟ้า
        self.sky_offset = 0  # ตำแหน่งการเลื่อนของท้องฟ้า
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)  # โหลดภาพเลือดหน้าจอ
        self.digit_size = 90  # ขนาดของตัวเลข
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)  # โหลดภาพตัวเลข
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))  # สร้างดิกชันนารีสำหรับตัวเลข
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)  # โหลดภาพ Game Over
        self.win_image = self.get_texture('resources/textures/win.png', RES)  # โหลดภาพชนะเกม

    def draw(self):  # ฟังก์ชันวาดทุกองค์ประกอบบนหน้าจอ
        self.draw_background()  # วาดพื้นหลัง
        self.render_game_objects()  # แสดงอ็อบเจ็กต์ในเกม
        self.draw_player_health()  # แสดงค่าพลังชีวิตของผู้เล่น

    def win(self):  # ฟังก์ชันแสดงภาพเมื่อผู้เล่นชนะ
        self.screen.blit(self.win_image, (0, 0))  # แสดงภาพชนะเต็มหน้าจอ

    def game_over(self):  # ฟังก์ชันแสดงภาพเมื่อผู้เล่นแพ้
        self.screen.blit(self.game_over_image, (0, 0))  # แสดงภาพ Game Over เต็มหน้าจอ

    def draw_player_health(self):  # ฟังก์ชันแสดงค่าพลังชีวิตของผู้เล่น
        health = str(self.game.player.health)  # แปลงค่าพลังชีวิตเป็นข้อความ
        for i, char in enumerate(health):  # วนลูปแสดงตัวเลขพลังชีวิต
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))  # แสดงตัวเลขที่ตำแหน่งที่เหมาะสม
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))  # แสดงสัญลักษณ์พลังชีวิตเต็ม

    def player_damage(self):  # ฟังก์ชันแสดงเอฟเฟกต์เลือดเมื่อผู้เล่นได้รับความเสียหาย
        self.screen.blit(self.blood_screen, (0, 0))  # แสดงภาพเลือดเต็มหน้าจอ

    def draw_background(self):  # ฟังก์ชันวาดพื้นหลังและพื้นดิน
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH  # คำนวณการเลื่อนของท้องฟ้า
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))  # วาดท้องฟ้า
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))  # วาดท้องฟ้าซ้ำให้เต็มหน้าจอ
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))  # วาดพื้นดิน

    def render_game_objects(self):  # ฟังก์ชันแสดงอ็อบเจ็กต์ในเกม
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)  # เรียงลำดับอ็อบเจ็กต์ตามระยะลึก
        for depth, image, pos in list_objects:  # วนลูปแสดงอ็อบเจ็กต์
            self.screen.blit(image, pos)  # วาดอ็อบเจ็กต์ที่ตำแหน่งที่กำหนด

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):  # ฟังก์ชันโหลดและปรับขนาดพื้นผิว
        texture = pg.image.load(path).convert_alpha()  # โหลดรูปภาพและแปลงให้รองรับ alpha
        return pg.transform.scale(texture, res)  # ปรับขนาดรูปภาพ

    def load_wall_textures(self):  # ฟังก์ชันโหลดพื้นผิวของกำแพง
        return {
            1: self.get_texture('resources/textures/11.png'),  # โหลดพื้นผิวของกำแพงหมายเลข 1
            2: self.get_texture('resources/textures/22.png'),  # โหลดพื้นผิวของกำแพงหมายเลข 2
            3: self.get_texture('resources/textures/33.jpg'),  # โหลดพื้นผิวของกำแพงหมายเลข 3
            4: self.get_texture('resources/textures/44.png'),  # โหลดพื้นผิวของกำแพงหมายเลข 4
            5: self.get_texture('resources/textures/5.png'),  # โหลดพื้นผิวของกำแพงหมายเลข 5
        }
