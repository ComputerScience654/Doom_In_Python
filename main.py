import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from uxui import *
from npc import SoldierNPC, CacoDemonNPC, CyberDemonNPC, Vasago  # นำเข้า NPC ทั้งหมด

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Shotgun(self)  # Default weapon
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        self.boss_spawned = False
        pg.mixer.music.play(-1)
        self.spawn_initial_npcs()  # สร้าง NPC เริ่มต้น

    def spawn_initial_npcs(self):
        def get_random_position():
            while True:
                pos = (randint(1, 20), randint(1, 20))
                if pos not in self.map.world_map:
                    return pos

        # สร้าง SoldierNPC 10 ตัวสุ่มเกิดทั่วแมพ
        for _ in range(10):
            pos = get_random_position()
            npc = SoldierNPC(self, pos=pos)
            self.object_handler.npc_positions.add(npc.map_pos)
            self.object_handler.npc_list.append(npc)

        # สร้าง CacoDemonNPC 10 ตัวสุ่มเกิดทั่วแมพ
        for _ in range(10):
            pos = get_random_position()
            npc = CacoDemonNPC(self, pos=pos)
            self.object_handler.npc_positions.add(npc.map_pos)
            self.object_handler.npc_list.append(npc)

        # สร้าง CyberDemonNPC 3 ตัวสุ่มเกิดทั่วแมพ
        for _ in range(3):
            pos = get_random_position()
            npc = CyberDemonNPC(self, pos=pos)
            self.object_handler.npc_positions.add(npc.map_pos)
            self.object_handler.npc_list.append(npc)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.weapon = Shotgun(self)
                elif event.key == pg.K_2:
                    self.weapon = Plasmarifle(self)
                elif event.key == pg.K_3:
                    self.weapon = Rifle(self)
                elif event.key == pg.K_4:
                    self.weapon = SuperShotgun(self)
                elif event.key == pg.K_0:
                    self.weapon = fist(self)
                elif event.key == pg.K_9:
                    self.weapon = bfg(self)

    def check_spawn_boss(self):
        if not self.boss_spawned and not self.object_handler.npc_positions:
            boss_class = choice([Vasago])
            boss = boss_class(self)
            self.object_handler.npc_positions.add(boss.map_pos)  # Use add instead of append
            self.object_handler.npc_list.append(boss)  # Add boss to npc_list
            self.boss_spawned = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    main_menu(game)
