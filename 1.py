import pygame
import os
import sys
from math import sqrt
import random

bots = []


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, level):
        super().__init__(group)
        self.level = level
        self.image = load_image("player/player_left1.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.cooldown = 500
        self.rect.y = pos[1]
        self.last_move = [0, 0]
        self.last_move2 = [0, 0]
        self.speed_shooting = 10
        self.now_image = ['right', 'player/player_right1.png']
        self.images = {
            'down': ['player/player_down1.png', 'player/player_down2.png'],
            'up': ['player/player_up1.png', 'player/player_up2.png'],
            'right': ['player/player_right1.png', 'player/player_right2.png'],
            'left': ['player/player_left1.png', 'player/player_left2.png']
        }
        self.last_pos = [pos[0], pos[1]]
        self.finish = False

    def come_back(self):
        self.rect.x = self.last_pos[0]
        self.rect.y = self.last_pos[1]
        pygame.display.flip()

    def check_on_collide(self):
        if pygame.sprite.spritecollideany(self, exit_group):
            self.finish = True
        if pygame.sprite.spritecollideany(self, wall_group):
            self.come_back()
        else:
            self.last_pos = [self.rect.x, self.rect.y]

    def update(self, new_pos):
        if self.last_move2[0] != new_pos[0] or self.last_move2[1] != new_pos[1]:
            self.change_image_for_moving(new_pos)
        else:
            self.animation_moving()
        if new_pos[1] != 0:
            if not pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y += new_pos[1]
            self.check_on_collide()

        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x += new_pos[0]

    def animation_stop(self):
        if self.now_image[0] == 'left':
            self.image = load_image('player/player_left.png')
        if self.now_image[0] == 'right':
            self.image = load_image('player/player_right.png')
        if self.now_image[0] == 'down':
            self.image = load_image('player/player_down.png')
        if self.now_image[0] == 'up':
            self.image = load_image('player/player_up.png')

    def animation_moving(self):
        if self.now_image[1][-5] == '2':
            self.image = load_image(self.images[self.now_image[0]][0])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][0]]
        else:
            self.image = load_image(self.images[self.now_image[0]][1])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][1]]
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_image_for_moving(self, new_pos):
        if new_pos[0] > 0:
            self.image = load_image('player/player_right1.png')
            self.now_image = ['right', 'player/player_right1.png']
        if new_pos[0] < 0:
            self.image = load_image('player/player_left1.png')
            self.now_image = ['left', 'player/player_left1.png']
        if new_pos[1] > 0:
            self.image = load_image('player/player_down1.png')
            self.now_image = ['down', 'player/player_down1.png']
        if new_pos[1] < 0:
            self.image = load_image('player/player_up1.png')
            self.now_image = ['up', 'player/player_up1.png']
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.check_on_collide()

    def strike(self, speed):
        pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (speed[0], speed[1]), self.level, player=True))
        pulya_group.add(pulya[-1])

    def find_path(self, dest):
        dest_x, dest_y = dest[0], dest[1]
        delta_x = dest_x - self.rect.centerx
        delta_y = dest_y - self.rect.centery
        dist = sqrt(delta_x ** 2 + delta_y ** 2)
        time = dist / self.speed_shooting
        speed_x = delta_x / time
        speed_y = delta_y / time
        return speed_x, speed_y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, pos, level):
        super().__init__(group)
        self.speed = 4
        self.level = level
        self.image = load_image("enemy\enemy_right1.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.cooldown = 700
        self.rect.y = pos[1]
        self.distance = 300
        self.last_tick = 0
        self.last_move = [0, 0]
        self.last_move2 = [0, 0]
        self.speed_shooting = 10
        self.last_pos = self.rect.center
        self.now_image = ['right', 'enemy\enemy_right1.png']
        self.images = {
            'down': ['enemy\enemy_down1.png', 'enemy\enemy_down2.png'],
            'up': ['enemy\enemy_up1.png', 'enemy\enemy_up2.png'],
            'right': ['enemy\enemy_right1.png', 'enemy\enemy_right2.png'],
            'left': ['enemy\enemy_left1.png', 'enemy\enemy_left2.png']
        }

        self.health = 3
        self.last_pos = [pos[0], pos[1]]

    def __call__(self, tick, player_pos):
        player_x = player_pos[0]
        player_y = player_pos[1]
        if tick - self.last_tick > self.cooldown:
            self.strike(self.find_path(player_pos))
            self.last_tick = tick

        delta_x = player_x - self.rect.centerx
        delta_y = player_y - self.rect.centery
        dist = sqrt(delta_x ** 2 + delta_y ** 2)
        if self.last_pos == self.rect.center:
            pass
        else:
            self.last_pos = self.rect.center

        if dist > self.distance:
            time = dist / self.speed
            speed_x = delta_x / time
            speed_y = delta_y / time
            self.update((speed_x, speed_y))

    def come_back(self):
        self.rect.x = self.last_pos[0]
        self.rect.y = self.last_pos[1]

    def check_on_collide(self):
        if pygame.sprite.spritecollideany(self, wall_group) or pygame.sprite.spritecollideany(self,
                                                                                              horizontal_borders) or pygame.sprite.spritecollideany(
            self,
            vertical_borders):
            self.come_back()
        else:
            self.last_pos = [self.rect.x, self.rect.y]

    def update(self, new_pos):
        if self.last_move2[0] != new_pos[0] or self.last_move2[1] != new_pos[1]:
            self.change_image_for_moving(new_pos)
        else:
            self.animation_moving()
        if new_pos[1] != 0:
            if not pygame.sprite.spritecollideany(self, wall_group) and not pygame.sprite.spritecollideany(self,
                                                                                                           horizontal_borders):
                self.rect.y += new_pos[1]
            self.check_on_collide()

        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, wall_group) and not pygame.sprite.spritecollideany(self,
                                                                                                           vertical_borders):
                self.rect.x += new_pos[0]
            self.check_on_collide()

    def animation_stop(self):
        if self.now_image[0] == 'left':
            self.image = load_image('enemy\enemy_left.png')
        if self.now_image[0] == 'right':
            self.image = load_image('enemy\enemy_right.png')
        if self.now_image[0] == 'down':
            self.image = load_image('enemy\enemy_down.png')
        if self.now_image[0] == 'up':
            self.image = load_image('enemy\enemy_up.png')

    def animation_moving(self):
        if self.now_image[1][-5] == '2':
            self.image = load_image(self.images[self.now_image[0]][0])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][0]]
        else:
            self.image = load_image(self.images[self.now_image[0]][1])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][1]]
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_image_for_moving(self, new_pos):
        if new_pos[0] > 0:
            self.image = load_image('enemy\enemy_right1.png')
            self.now_image = ['right', 'enemy\enemy_right1.png']
        if new_pos[0] < 0:
            self.image = load_image('enemy\enemy_left1.png')
            self.now_image = ['left', 'enemy\enemy_left1.png']
        if new_pos[1] > 0:
            self.image = load_image('enemy\enemy_down1.png')
            self.now_image = ['down', 'enemy\enemy_down1.png']
        if new_pos[1] < 0:
            self.image = load_image('enemy\enemy_up1.png')
            self.now_image = ['up', 'enemy\enemy_up1.png']
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def strike(self, speed):
        pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (speed[0], speed[1]), self.level, player=False))
        pulya_group.add(pulya[-1])

    def find_path(self, dest):
        dest_x = dest[0]
        dest_y = dest[1]
        delta_x = dest_x - self.rect.centerx
        delta_y = dest_y - self.rect.centery
        dist = sqrt(delta_x ** 2 + delta_y ** 2)
        time = dist / self.speed_shooting
        speed_x = delta_x / time
        speed_y = delta_y / time
        return speed_x, speed_y


class Shooting(pygame.sprite.Sprite):
    def __init__(self, group, pos, where, level, player):
        super().__init__(group)
        self.level = level
        self.image = load_image('objects\pulya.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.player = player
        self.rect.y = pos[1] + 20
        self.where = where

    def update(self):
        check = False
        if not self.player:
            if pygame.sprite.spritecollideany(self, player_group):
                if health:
                    health[-1].update(0)
                else:
                    pygame.quit()

                delet = pulya.pop(pulya.index(self))
                all_sprites.remove(delet)
                pulya_group.remove(delet)
                check = True
            elif pygame.sprite.spritecollideany(self, wall_group):
                delet = pulya.pop(pulya.index(self))
                all_sprites.remove(delet)
                pulya_group.remove(delet)
                check = True
        else:
            who = pygame.sprite.spritecollideany(self, bots_group)
            if pygame.sprite.spritecollideany(self, wall_group):
                delet = pulya.pop(pulya.index(self))
                all_sprites.remove(delet)
                pulya_group.remove(delet)
                check = True
            elif who:
                if who.health:
                    who.health -= 1
                    print(-1)
                    delet = pulya.pop(pulya.index(self))
                    all_sprites.remove(delet)
                    pulya_group.remove(delet)
                    check = True
                if who.health == 0:
                    delet = bots.pop(bots.index(who))
                    all_sprites.remove(delet)
                    bots_group.remove(delet)
                    check = True
                print(1)
                if len(bots) == 0:
                    generate_finish(load_level(self.level))

        if not pygame.sprite.spritecollideany(self, horizontal_borders) and not pygame.sprite.spritecollideany(self,
                                                                                                               vertical_borders):
            self.rect.x += self.where[0]
            self.rect.y += self.where[1]
        else:
            if not check:
                delet = pulya.pop(pulya.index(self))
                all_sprites.remove(delet)
                pulya_group.remove(delet)


class Health(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = load_image('objects\health.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, action):
        if action == 1 and 1 <= len(health) <= 9:  # здесь будет какая-то хилка
            health.append(Health((health[-1].rect.x + 30, 10)))
        if action == 0 and len(health) >= 1:
            delet = health.pop(-1)
            all_sprites.remove(delet)
        if len(health) == 0:
            return 0
        return 1

    class Camera:
        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            obj.rect.x += self.dx
            obj.rect.y += self.dy

        def update(self, target):
            self.dx = -(target.rect.x + target.rect.w // 2)
            self.dy = -(target.rect.y + target.rect.h // 2)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


tile_width = tile_height = 30


class Menu:
    def __init__(self, window, punkts) -> None:
        self.punkts = punkts
        self.window = window

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], True, (222, 27, 27)), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], True, i[3]), (i[0], i[1]))

    def menu(self, esc):
        done = True
        font_menu = pygame.font.Font('data/fonts/Purisa.ttf', 60)
        punkt = -1
        while done:

            screen.fill((66, 62, 62))
            mp = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
                    break

            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            if keys[pygame.K_ESCAPE] and not esc:
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                if punkt == 0:
                    done = False
                elif punkt == 1:
                    rec = Records(window=screen, menu=self)
                    rec.records()
                    pass
                elif punkt == 2:
                    sys.exit()
            if not esc:
                esc = False

            self.window.blit(screen, (0, 0))
            pygame.display.flip()


class Records:
    def __init__(self, window, menu) -> None:
        self.punkts = punkts
        self.window = window
        self.menu = menu

    def records(self):
        done = True
        font_menu = pygame.font.Font('data/fonts/Old-Soviet.otf', 60)
        punkt = 0
        while done:
            keys = pygame.key.get_pressed()
            screen.fill((66, 62, 62))
            mp = pygame.mouse.get_pos()

            # self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            if keys[pygame.K_ESCAPE]:
                self.window.blit(screen, (0, 0))
                pygame.display.flip()
                done = False
                self.menu.menu(True)

            self.window.blit(screen, (0, 0))
            pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.tile_images = {
            'wall': load_image('wall.png', 1),
            'empty': load_image('empty.png', 1),
            'portal': load_image('portal.png', -1)
        }
        super().__init__(all_sprites)
        self.image = self.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    a, b = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                wall_group.add(Tile('wall', x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                a, b = x, y
            elif level[y][x] == 'x':
                Tile('empty', x, y)

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'x':
                bots.append(Enemy(all_sprites, (x * tile_width, y * tile_height), level))
                bots_group.add(bots[-1])
    return a * tile_width, b * tile_height


def generate_finish(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '?':
                exit_group.add(Tile('portal', x, y))


pygame.init()
size = (1000, 1000)
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('BLACK'))

# Меню


pygame.mixer.music.load("data/sounds/main_menu_theme.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

punkts = [(400, 250, u'Game', (255, 255, 255), (250, 30, 2530), 0),
          (340, 400, u'Statisticks', (255, 255, 255), (250, 30, 2530), 1),
          (400, 550, u'Quit', (250, 250, 30), (250, 30, 2530), 2)]
game = Menu(punkts=punkts, window=screen)
game.menu(False)

pygame.mixer.music.load("data/sounds/game_theme.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

all_levels = ['level_1.txt', 'level_2.txt', 'level_3.txt']


def start_level(level):
    global size, gaming, screen, health, player, player_group, all_sprites, horizontal_borders, vertical_borders, pulya
    global pulya_group, cont, exit_group, wall_group, all_sprites, bots_group
    size = (1470, 930)

    gaming = True
    next_level = False
    all_sprites = pygame.sprite.Group()
    bots_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('BLACK'))
    # Игрок
    health = []
    player = Player(all_sprites, generate_level(load_level(level)), level)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Боты

    all_sprites.draw(screen)

    # Стены

    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    Border(5, 40, size[0] - 5, 40)
    Border(5, size[1] - 5, size[0] - 5, size[1] - 5)
    Border(5, 40, 5, size[1] - 5)
    Border(size[0] - 5, 40, size[0] - 5, size[1] - 5)

    pulya_group = pygame.sprite.Group()
    pulya = []

    pygame.display.flip()
    fps = 110  # количество кадров в секунду
    clock = pygame.time.Clock()
    cont = False
    player_speed = 3

    shoot_tick = 0

    x, y = 10, 10
    for _ in range(10):
        health.append(Health((x, y)))
        x += 30
    while gaming:

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        now_tick = pygame.time.get_ticks()

        check = True
        # Боты
        for i in bots:
            i(now_tick, player.rect.center)

        # Игрок

        if click[0] and now_tick - shoot_tick > player.cooldown:
            player.strike(player.find_path((mouse[0], mouse[1])))
            shoot_tick = pygame.time.get_ticks()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.update((0, -player_speed))
            check = False
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.update((0, player_speed))
            check = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.update((-player_speed, 0))
            check = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.update((player_speed, 0))
            check = False

        if check:
            player.animation_stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or len(health) == 0:
                gaming = False
            if player.finish:
                gaming = False
                next_level = True
        pulya_group.update()
        screen.fill(pygame.Color('BLACK'))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    return next_level


for i in all_levels:
    answer = start_level(i)
    if not answer:
        break
