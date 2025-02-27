import pygame as pg
import math
from settings import *  # นำเข้าค่าตั้งค่าทั้งหมดจากไฟล์ settings


class RayCasting:
    def __init__(self, game):
        self.game = game  # อ้างอิงไปยังอ็อบเจ็กต์เกมหลัก
        self.ray_casting_result = []  # เก็บผลลัพธ์ของการคำนวณ Raycasting
        self.objects_to_render = []  # เก็บข้อมูลของวัตถุที่ต้องเรนเดอร์
        self.textures = self.game.object_renderer.wall_textures  # โหลดพื้นผิวของกำแพงจาก Object Renderer

    def get_objects_to_render(self):
        """สร้างรายการวัตถุที่ต้องเรนเดอร์จากผลลัพธ์ Raycasting"""
        self.objects_to_render = []  # ล้างข้อมูลก่อนเริ่มใหม่
        for ray, values in enumerate(self.ray_casting_result):  # วนลูปผ่านทุกค่าที่ได้จาก Raycasting
            depth, proj_height, texture, offset = values  # ดึงค่าความลึก, ความสูง, พื้นผิว, และตำแหน่ง texture

            if proj_height < HEIGHT:  # ถ้ากำแพงสูงน้อยกว่าความสูงของหน้าจอ
                # ดึงเฉพาะส่วนของ texture ตาม offset
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                # ปรับขนาด texture ให้เหมาะกับการฉายภาพ 3D
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)  # กำหนดตำแหน่งของกำแพงในเกม
            else:  # ถ้ากำแพงสูงกว่าหรือเท่ากับความสูงของหน้าจอ
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height  # ปรับขนาด texture ให้สัมพันธ์กับการฉายภาพ
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))  # ปรับขนาด texture ให้เต็มจอ
                wall_pos = (ray * SCALE, 0)  # วางตำแหน่งของกำแพงที่ด้านบนของหน้าจอ

            self.objects_to_render.append((depth, wall_column, wall_pos))  # เพิ่มกำแพงเข้าไปในรายการที่ต้องเรนเดอร์

    def ray_cast(self):
        """คำนวณ Raycasting เพื่อหากำแพงที่ผู้เล่นเห็น"""
        self.ray_casting_result = []  # ล้างข้อมูลก่อนคำนวณใหม่
        texture_vert, texture_hor = 1, 1  # เก็บค่าพื้นผิวที่ชนแนวตั้งและแนวนอน
        ox, oy = self.game.player.pos  # ตำแหน่งของผู้เล่น
        x_map, y_map = self.game.player.map_pos  # ตำแหน่งของผู้เล่นในตารางแผนที่

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001  # คำนวณมุมเริ่มต้นของ Ray
        for ray in range(NUM_RAYS):  # ยิงรังสีจำนวน NUM_RAYS
            sin_a = math.sin(ray_angle)  # คำนวณค่า sine ของมุมรังสี
            cos_a = math.cos(ray_angle)  # คำนวณค่า cosine ของมุมรังสี

            # คำนวณจุดตัดแนวนอน
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a  # คำนวณระยะห่างถึงจุดตัด
            x_hor = ox + depth_hor * cos_a  # คำนวณตำแหน่ง X ที่จุดตัด
            delta_depth = dy / sin_a  # คำนวณระยะห่างระหว่างแต่ละช่องของกริด
            dx = delta_depth * cos_a  # คำนวณการเปลี่ยนแปลง X ในแต่ละขั้นตอน

            for i in range(MAX_DEPTH):  # ตรวจสอบจุดตัดแนวนอน
                tile_hor = int(x_hor), int(y_hor)  # แปลงตำแหน่งเป็นช่องกริด
                if tile_hor in self.game.map.world_map:  # ถ้ามีสิ่งกีดขวาง (กำแพง)
                    texture_hor = self.game.map.world_map[tile_hor]  # ดึงค่า texture
                    break
                x_hor += dx  # เลื่อนไปยังตำแหน่งถัดไป
                y_hor += dy
                depth_hor += delta_depth  # เพิ่มระยะทาง

            # คำนวณจุดตัดแนวตั้ง
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a  # คำนวณระยะห่างถึงจุดตัด
            y_vert = oy + depth_vert * sin_a  # คำนวณตำแหน่ง Y ที่จุดตัด
            delta_depth = dx / cos_a  # คำนวณระยะห่างระหว่างแต่ละช่องของกริด
            dy = delta_depth * sin_a  # คำนวณการเปลี่ยนแปลง Y ในแต่ละขั้นตอน

            for i in range(MAX_DEPTH):  # ตรวจสอบจุดตัดแนวตั้ง
                tile_vert = int(x_vert), int(y_vert)  # แปลงตำแหน่งเป็นช่องกริด
                if tile_vert in self.game.map.world_map:  # ถ้ามีสิ่งกีดขวาง (กำแพง)
                    texture_vert = self.game.map.world_map[tile_vert]  # ดึงค่า texture
                    break
                x_vert += dx  # เลื่อนไปยังตำแหน่งถัดไป
                y_vert += dy
                depth_vert += delta_depth  # เพิ่มระยะทาง

            # เปรียบเทียบระยะทางระหว่างแนวนอนและแนวตั้ง
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # ปรับระยะให้ลดผลกระทบจาก Fishbowl Effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # คำนวณความสูงของกำแพงที่ฉายบนหน้าจอ
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # บันทึกค่าที่ได้จาก Raycasting
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE  # ปรับมุมรังสีสำหรับรอบถัดไป

    def update(self):
        """อัปเดต Raycasting ทุกเฟรม"""
        self.ray_cast()  # คำนวณ Raycasting
        self.get_objects_to_render()  # สร้างรายการวัตถุที่ต้องเรนเดอร์
