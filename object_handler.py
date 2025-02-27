from sprite_object import *  # นำเข้าโมดูลที่เกี่ยวข้องกับวัตถุ Sprite
from npc import *  # นำเข้าโมดูลที่เกี่ยวข้องกับ NPC
from random import choices, randrange  # นำเข้า choices และ randrange สำหรับการสุ่ม


class ObjectHandler:
    def __init__(self, game):  # คอนสตรักเตอร์สำหรับคลาส ObjectHandler
        self.game = game  # เก็บอ้างอิงไปยังอ็อบเจ็กต์เกมหลัก
        self.sprite_list = []  # รายการเก็บ Sprite ทั้งหมด
        self.npc_list = []  # รายการเก็บ NPC ทั้งหมด
        self.npc_sprite_path = 'resources/sprites/npc/'  # กำหนด path ของ sprite NPC
        self.static_sprite_path = 'resources/sprites/static_sprites/'  # กำหนด path ของ sprite แบบ static
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'  # กำหนด path ของ sprite แบบเคลื่อนไหว
        add_sprite = self.add_sprite  # กำหนด alias สำหรับฟังก์ชัน add_sprite
        add_npc = self.add_npc  # กำหนด alias สำหรับฟังก์ชัน add_npc
        self.npc_positions = {}  # เก็บตำแหน่งของ NPC

        # จำนวน NPC ที่จะเกิดขึ้นในเกม
        self.enemies = 20  # จำนวนศัตรูที่ต้องการ spawn
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]  # รายชื่อประเภทของ NPC ที่เป็นไปได้
        self.weights = [70, 20, 10]  # น้ำหนักของแต่ละประเภทในการสุ่ม spawn (เปอร์เซ็นต์)
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}  # กำหนดพื้นที่ห้าม spawn NPC
        self.spawn_npc()  # เรียกใช้ฟังก์ชัน spawn_npc() เพื่อสร้าง NPC

        # สร้าง Sprite
        add_sprite(AnimatedSprite(game))  # สร้าง Sprite แรกที่ตำแหน่งเริ่มต้น
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))  # สร้าง Sprite ที่ตำแหน่ง (1.5, 1.5)
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))  # และอื่นๆ ตามลำดับ
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        
        # สร้าง Sprite ไฟสีแดงจาก path ที่กำหนด
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        
        # สร้าง Sprite เพิ่มเติม
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

    def spawn_npc(self):  # ฟังก์ชันสำหรับสร้าง NPC
        for i in range(self.enemies):  # วนลูปตามจำนวนศัตรูที่กำหนด
            npc = choices(self.npc_types, self.weights)[0]  # เลือกประเภท NPC แบบสุ่ม
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)  # กำหนดตำแหน่งแบบสุ่ม
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):  # ตรวจสอบว่าตำแหน่งถูกต้อง
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)  # หากไม่ถูกต้องให้สุ่มใหม่
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))  # เพิ่ม NPC ที่ตำแหน่งที่ถูกต้อง

    def check_win(self):  # ฟังก์ชันตรวจสอบว่าผู้เล่นชนะหรือไม่
        if not len(self.npc_positions):  # หากไม่มี NPC เหลืออยู่
            self.game.object_renderer.win()  # แสดงหน้าจอชนะ
            pg.display.flip()  # อัปเดตหน้าจอแสดงผล
            pg.time.delay(1500)  # รอ 1.5 วินาที
            self.game.new_game()  # เริ่มเกมใหม่

    def update(self):  # ฟังก์ชันอัปเดตสถานะของวัตถุทั้งหมดในเกม
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}  # อัปเดตตำแหน่ง NPC ที่ยังมีชีวิต
        [sprite.update() for sprite in self.sprite_list]  # อัปเดต sprite ทั้งหมด
        [npc.update() for npc in self.npc_list]  # อัปเดต NPC ทั้งหมด
        self.check_win()  # เรียกใช้ฟังก์ชันตรวจสอบว่าผู้เล่นชนะหรือไม่

    def add_npc(self, npc):  # ฟังก์ชันเพิ่ม NPC ลงในรายการ
        self.npc_list.append(npc)  # เพิ่ม NPC ที่รับมาเข้าไปในรายการ

    def add_sprite(self, sprite):  # ฟังก์ชันเพิ่ม Sprite ลงในรายการ
        self.sprite_list.append(sprite)  # เพิ่ม Sprite ที่รับมาเข้าไปในรายการ
