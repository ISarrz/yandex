import pygame
import os
import sys
from math import sqrt
import random
import sqlite3


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

            screen.fill((163, 160, 160))
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
        pygame.font.init()
        pygame.font.get_init()
        sc = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption('ZEON')

        font = pygame.font.Font('data/fonts/Old-Soviet.otf', 30)
        con = sqlite3.connect('data/game.sqlite')
        cur = con.cursor()

        # Render the texts that you want to display
        text1 = font.render('№', True, (0, 0, 0))
        text2 = font.render('Никнейм', True, (0, 0, 0))
        text3 = font.render('Время', True, (0, 0, 0))
        text4 = font.render('Счёт', True, (0, 0, 0))

        # create a rectangular object for the
        # text surface object
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()
        textRect4 = text4.get_rect()

        BLACK = (0, 0, 0)
        textRect1.center = (20, 30)
        textRect2.center = (200, 30)
        textRect3.center = (600, 30)
        textRect4.center = (900, 30)

        # cur.execute(f"INSERT INTO RECORDS (name, time, score) VALUES ('{name}', '{time}', {score});")
        # con.commit()
        while done:
            keys = pygame.key.get_pressed()
            sc.fill((163, 160, 160))
            sc.blit(text1, textRect1)
            sc.blit(text2, textRect2)
            sc.blit(text3, textRect3)
            sc.blit(text4, textRect4)
            cur.execute("select * from RECORDS order by score desc limit 15")
            res = cur.fetchall()
            count = 1
            for i in res:
                number, name, time, score = list(i)
                number = font.render(str(count), True, (0, 0, 0))
                number1 = text1.get_rect().center = (10, 60 * count)

                name = font.render(name, True, (0, 0, 0))
                name1 = text1.get_rect().center = (100, 60 * count)

                time = font.render(time, True, (0, 0, 0))
                time1 = text1.get_rect().center = (600, 60 * count)

                score = font.render(str(score), True, (0, 0, 0))
                score1 = text1.get_rect().center = (900, 60 * count)

                pygame.draw.line(sc, BLACK, [2, 60 * count], [1000, 60 * count], 3)
                sc.blit(number, number1)
                sc.blit(name, name1)
                sc.blit(time, time1)
                sc.blit(score, score1)
                count += 1

            pygame.draw.line(sc, BLACK, [2, 2], [2, 1000], 3)
            pygame.draw.line(sc, BLACK, [2, 2], [1000, 2], 3)

            pygame.draw.line(sc, BLACK, [50, 2], [50, 1000], 3)
            pygame.draw.line(sc, BLACK, [500, 2], [500, 1000], 3)
            pygame.draw.line(sc, BLACK, [800, 2], [800, 1000], 3)
            pygame.draw.line(sc, BLACK, [998, 2], [998, 1000], 3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                pygame.display.update()
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
        self.name = 'Player'
        self.level = level
        self.image = load_image("player/player_left1.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.cooldown = 500
        self.rect.y = pos[1]
        self.last_move = [0, 0]
        self.last_move2 = [0, 0]
        self.speed_shooting = 7
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
        if pygame.sprite.spritecollideany(self, aptechka_group):
            self_group = pygame.sprite.Group()
            self_group.add(self) 
            col = pygame.sprite.groupcollide(self_group, aptechka_group, False, False)
            ban = []
            for i in col.items():
                obj = i[1][0]
                ban.append(obj)
            for i in ban:
                aptechka_group.remove(i)
                all_sprites.remove(i)
            x = health[-1].rect.x + 30
            y = health[-1].rect.y
            for i in range(10 - len(health)):
                health.append(Health((x, y)))
                x += 30
        if pygame.sprite.spritecollideany(self, exit_group) and len(bots) <= 0:
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
                self.last_move[1] = new_pos[1]
                self.last_move2 = new_pos
        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x += new_pos[0]
                self.check_on_collide()
                self.last_move[0] = new_pos[0]
                self.last_move2 = new_pos

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
        self.check_on_collide()

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
        self.name = 'Enemy'
        self.speed = 3
        self.level = level
        self.image = load_image("enemy\enemy_right1.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.cooldown = 400
        self.rect.y = pos[1]
        self.distance = 200
        self.max_distance = 300
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
        delta_x = player_x - self.rect.centerx
        delta_y = player_y - self.rect.centery
        dist = sqrt(delta_x ** 2 + delta_y ** 2)
        if (tick - self.last_tick > self.cooldown) and (dist < self.max_distance):
            self.strike(self.find_path(player_pos))
            self.last_tick = tick
        if self.last_pos == self.rect.center:
            pass
        else:
            self.last_pos = self.rect.center

        if dist > self.distance and dist < self.max_distance:
            time = dist / self.speed
            speed_x = delta_x / time
            speed_y = delta_y / time
            self.update((speed_x, speed_y))

    def come_back(self):
        self.rect.x = self.last_pos[0]
        self.rect.y = self.last_pos[1]
        pygame.display.flip()

    def check_on_collide(self):
        if pygame.sprite.spritecollideany(self, exit_group) and len(bots) <= 0:
            self.finish = True
        if pygame.sprite.spritecollideany(self, wall_group):
            self.come_back()
        else:
            self.last_pos = [self.rect.x, self.rect.y]

    def update(self, new_pos):
        self.check_on_collide()
        if abs (self.last_move2[0] - new_pos[0]) >= 0.5 or abs(self.last_move2[1] - new_pos[1]) >= 0.5:
            self.change_image_for_moving(new_pos)
        else:
            self.animation_moving()
        if new_pos[1] != 0:
            if not pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y += new_pos[1]
                self.check_on_collide()
                self.last_move[1] = new_pos[1]
                self.last_move2 = new_pos
        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x += new_pos[0]
                self.check_on_collide()
                self.last_move[0] = new_pos[0]
                self.last_move2 = new_pos

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
        self.check_on_collide()

    def change_image_for_moving(self, new_pos):
        if new_pos[0] > 0 and new_pos[0] > abs(new_pos[1]):
            self.image = load_image('enemy\enemy_right1.png')
            self.now_image = ['right', 'enemy\enemy_right1.png']
        if new_pos[0] < 0 and abs(new_pos[0]) > abs(new_pos[1]):
            self.image = load_image('enemy\enemy_left1.png')
            self.now_image = ['left', 'enemy\enemy_left1.png']
        if new_pos[1] > 0 and abs(new_pos[1]) > abs(new_pos[0]):
            self.image = load_image('enemy\enemy_down1.png')
            self.now_image = ['down', 'enemy\enemy_down1.png']
        if new_pos[1] < 0 and abs(new_pos[1]) > abs(new_pos[0]):
            self.image = load_image('enemy\enemy_up1.png')
            self.now_image = ['up', 'enemy\enemy_up1.png']
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
        if time:
            speed_x = delta_x / time
            speed_y = delta_y / time
            return speed_x, speed_y


class Shooting(pygame.sprite.Sprite):
    def __init__(self, group, pos, where, level, player):
        global fire
        super().__init__(group)
        fire.play()
        self.name = 'Shooting'
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
                    kill.play()
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
        self.name = 'Health'
        self.image = load_image('objects\health.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, action):
        if action == 1 and 1 <= len(health) <= 9:  # здесь будет какая-то хилка
            health.append(Health((health[-1].rect.x + 30, 10)))
        if action == 0 and len(health) >= 1:
            hirt.play()
            delet = health.pop(-1)
            all_sprites.remove(delet)
        if len(health) == 0:
            kill.play()
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
        self.name = 'Border'
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


tile_width = tile_height = 30


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.name = 'Tile'
        self.tile_images = {
            'wall': load_image('wall.png', 1),
            'empty': load_image('empty.png', 1),
            'portal': load_image('portal.png', -1),
            'aptechka': load_image('objects/aptechka.png', -1)
        }
        super().__init__(all_sprites)
        self.image = self.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class End():
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.music.load("data/sounds/main_menu_theme.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        size = (1000, 1000)
        screen = pygame.display.set_mode(size)
        screen.fill(pygame.Color('BLACK'))
        self.menu()
        self.punkts = punkts
        self.window = screen

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], True, (222, 27, 27)), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], True, i[3]), (i[0], i[1]))

    def menu(self):
        global timer
        time = timer
        h, m, s, ml = map(int, time.split(':'))
        h *= 60 * 60 * 1000
        m *=  60 * 1000
        s *= 1000
        score = max(0, 1000000 - h - m - s)
        size = (1000, 1000)
        screen = pygame .display.set_mode(size)
        font = pygame.font.Font('data/fonts/Old-Soviet.otf', 30)
        con = sqlite3.connect('data/game.sqlite')
        cur = con.cursor()
        clock = pygame .time.Clock()
        input_box = pygame.Rect(400, 280, 100, 50)
        color_inactive = pygame .Color((0, 0, 0))
        color_active = pygame .Color((207, 48, 48))
        color = color_inactive
        active = False
        text = ''
        done = False


        text1 = font.render('Введите никнейм', True, (0, 0, 0))
        textRect1 = text1.get_rect()
        textRect1.center = (200, 300)

        text2 = font.render('Время', True, (0, 0, 0))
        textRect2 = text2.get_rect()
        textRect2.center = (100, 200)

        text3 = font.render(f'{time}', True, (0, 0, 0))
        textRect3 = text3.get_rect()
        textRect3.center = (500, 200)

        text4 = font.render('Счёт', True, (0, 0, 0))
        textRect4 = text4.get_rect()
        textRect4.center = (90, 100)

        text5 = font.render(f'{score}', True, (0, 0, 0))
        textRect5 = text5.get_rect()
        textRect5.center = (500, 100)

        text6 = font.render('Enter - для сохранения', True, (0, 0, 0))
        textRect6 = text6.get_rect()
        textRect6.center = (500, 400)

        text7 = font.render('Сохранено', True, (207, 48, 48))
        textRect7 = text7.get_rect()
        textRect7.center = (500, 600)

        save = False
        while not done:
            keys = pygame.key.get_pressed()
            for event in pygame .event.get():
                if event.type == pygame .QUIT:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                if event.type == pygame .MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame .K_RETURN:
                            text = ''
                        elif event.key == pygame .K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            if keys[pygame.K_RETURN]:
                save = True
                cur.execute(f"INSERT INTO RECORDS (name, time, score) VALUES('{text}', '{time}', {score});")
                con.commit()
            if keys[pygame.K_ESCAPE]:
                sys.exit()
            screen.fill((163, 160, 160))
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            if save:
                screen.blit(text7, textRect7)
            screen.blit(text1, textRect1)
            screen.blit(text2, textRect2)
            screen.blit(text3, textRect3)
            screen.blit(text4, textRect4)
            screen.blit(text5, textRect5)
            screen.blit(text6, textRect6)
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame .draw.rect(screen, color, input_box, 2)
            pygame .display.flip()
            clock.tick(30)

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def generate_level(level):
    global bots
    bots = []
    a, b = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y + 2)
            elif level[y][x] == '#':
                wall_group.add(Tile('wall', x, y + 2))
            elif level[y][x] == '@':
                Tile('empty', x, y + 2)
                a, b = x, y
            elif level[y][x] == 'x':
                Tile('empty', x, y + 2)
            elif level[y][x] == '+':
                aptechka_group.add(Tile('aptechka', x, y + 2))
            elif level[y][x] == '?':
                portal = Tile('empty', x, y + 2)
                exit_group.add(portal)
                all_sprites.add(portal)


    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'x':
                bots.append(Enemy(all_sprites, (x * tile_width, (y + 2) * tile_height), level))
                bots_group.add(bots[-1])
    return a * tile_width, b * tile_height

def generate_finish(level):
    ban = []
    for i in exit_group:
        ban.append(i)
        x, y = i.rect.centerx, i.rect.centery
        portal = Tile('portal', 0,  0)
        portal.rect.centerx = x
        portal.rect.centery = y
        exit_group.add(portal)
        all_sprites.add(portal)
    for i in ban:
        all_sprites.remove(i)
        exit_group.remove(i)

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, target, dx, dy):
        self.dx = 0
        self.dy = 0
        self.x = target.rect.centerx + dx 
        self.y = target.rect.centery + dy 
        
    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        
    
    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.centerx - self.x)
        self.dy = -(target.rect.centery - self.y)
        
    

def start_level(level):
    global size, gaming, screen, health, player, player_group, all_sprites, horizontal_borders, vertical_borders, pulya
    global pulya_group, cont, exit_group, wall_group, all_sprites, bots_group, aptechka_group, bots, camera, timer, fire, prtls
    global hirt, kill
    pygame.init()
    size = (600, 600)
    gaming = True
    font = pygame.font.Font('data/fonts/Old-Soviet.otf', 30)
    answer = 0
    start_time = pygame.time.get_ticks()
    aptechka_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bots_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
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


    pulya_group = pygame.sprite.Group()
    pulya = []

    pygame.display.flip()
    fps = 110  # количество кадров в секунду
    clock = pygame.time.Clock()
    cont = False
    player_speed = 4

    shoot_tick = 0

    x, y = 10, 10
    for _ in range(10):
        health.append(Health((x, y)))
        x += 30
    pygame.mixer.music.load("data/sounds/game_theme.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    die = pygame.mixer.Sound("data/sounds/die.ogg")
    fire = pygame.mixer.Sound("data/sounds/fire.ogg")
    prtls = pygame.mixer.Sound("data/sounds/prtls.ogg")
    hirt = pygame.mixer.Sound("data/sounds/hirt.ogg")
    kill = pygame.mixer.Sound("data/sounds/kill.ogg")
    if level == 'level_1.txt':
        dx = -450
        dy = -900
    elif level == 'level_2.txt':
        dx = -450
        dy = -650
    elif level == 'level_3.txt':
        dx = -450
        dy = -1200
        player.cooldown = 100
    camera = Camera(player, dx, dy)
    camera.update(player)
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
        if keys[pygame.K_ESCAPE]:
            sys.exit()    
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            player.update((-sqrt(player_speed ** 2 / 2), sqrt(player_speed ** 2 / 2)))
            check = False
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.update((sqrt(player_speed ** 2 / 2), -sqrt(player_speed ** 2 / 2)))
            check = False    
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.update((sqrt(player_speed ** 2 / 2), sqrt(player_speed ** 2 / 2)))
            check = False
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            player.update((-sqrt(player_speed ** 2 / 2), -sqrt(player_speed ** 2 / 2)))
            check = False
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.update((0, player_speed))
            check = False
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.update((-player_speed, 0))
            check = False
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            player.update((0, -player_speed))
            check = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.update((player_speed, 0))
            check = False

        if len(health) == 0:
            gaming = False
            answer = 2
            die.play()
            return answer
        if check:
            player.animation_stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gaming = False
                sys.exit()
            if player.finish:
                gaming = False
                answer = 1
                prtls.play()
                return answer

        pulya_group.update()
        camera.update(player)
        for sprite in all_sprites:
            if sprite.name != 'Health':
                camera.apply(sprite)
        screen.fill(pygame.Color('WHITE'))
        all_sprites.draw(screen)
        tt = pygame.time.get_ticks() - start_time
        h = tt // 1000 // 60 //60 % 60
        m = tt// 1000 // 60 % 60
        s = tt // 1000 % 60
        mil = tt % 1000
        timer = f'{h}:{m}:{s}:{mil}'
        time = font.render(timer, True, (0, 0, 0))
        time1 = time.get_rect().center = (400, 10)
        screen.blit(time, time1)
        pygame.display.flip()
        clock.tick(fps)

        
    #pygame.quit()
    # answer 1 - некст левел, 2 - повтор, 0 - конец
    return answer


# Меню

pygame.init()
pygame.mixer.music.load("data/sounds/main_menu_theme.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
size = (1000, 1000)
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('BLACK'))
punkts = [(400, 250, u'Game', (255, 255, 255), (250, 30, 2530), 0),
          (340, 400, u'Statisticks', (255, 255, 255), (250, 30, 2530), 1),
          (400, 550, u'Quit', (250, 250, 30), (250, 30, 2530), 2)]
game = Menu(punkts=punkts, window=screen)
game.menu(False)


all_levels = [ 'level_1.txt', 'level_2.txt', 'level_3.txt']

for i in all_levels:
    answer = start_level(i)
    if answer == 2:
        while answer == 2:
            answer = start_level(i)
    if answer == 1 and i == all_levels[-1]:
        print('конец')
        end = End()

