import pygame
import os
import sys
from math import sqrt
import random
import sqlite3

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
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = load_image("player/player_right1.png")
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

    def update(self, new_pos):
        if self.last_move2[0] != new_pos[0] or self.last_move2[1] != new_pos[1]:
            self.change_image_for_moving(new_pos)
        else:
            self.animation_moving()
        if new_pos[1] != 0:
            if not pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y += new_pos[1]
                self.last_move[1] = new_pos[1]
                self.last_move2 = new_pos
            else:
                self.rect.y -= self.last_move[1]
        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x += new_pos[0]
                self.last_move[0] = new_pos[0]
                self.last_move2 = new_pos
            else:
                self.rect.x -= self.last_move[0]

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

    def strike(self, speed):
        pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (speed[0], speed[1]), player=True))
        pulya_group.add(pulya[-1])

    def find_path(self, dest):
        dest_x, dest_y = dest[0], dest[1]
        delta_x = dest_x - self.rect.centerx
        delta_y = dest_y - self.rect.centery
        dist = sqrt(delta_x ** 2 +  delta_y ** 2)
        time = dist / self.speed_shooting
        speed_x = delta_x / time
        speed_y = delta_y / time
        return speed_x, speed_y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.speed = 4
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


    def __call__(self, tick, player_pos):
        player_x = player_pos[0]
        player_y = player_pos[1]
        if tick - self.last_tick > self.cooldown:
            self.strike(self.find_path(player_pos))
            self.last_tick = tick
        
        delta_x = player_x - self.rect.centerx
        delta_y = player_y - self.rect.centery
        dist = sqrt(delta_x ** 2 +  delta_y ** 2)
        if self.last_pos == self.rect.center:
            pass
        else:
            self.last_pos = self.rect.center

        if dist > self.distance:
            time = dist / self.speed
            speed_x = delta_x / time
            speed_y = delta_y / time
            self.update((speed_x, speed_y))
    """
    def check_on_shooting(self):
        if self.health:
            if pygame.sprite.spritecollideany(self, pulya_group):
                print('ok')
                self.health -= 1
        else:
            delet = bots.pop(bots.index(self))
            all_sprites.remove(delet)
            bots_group.remove(delet)
            """


    def update(self, new_pos):
        if self.last_move2[0] != new_pos[0] or self.last_move2[1] != new_pos[1]:
            self.change_image_for_moving(new_pos)
        else:
            self.animation_moving()
        if new_pos[1] != 0:
            if not pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y += new_pos[1]
                self.last_move[1] = new_pos[1]
                self.last_move2 = new_pos
                self.last_pos = (self.last_pos[0], new_pos[1])
            else:
                self.rect.y -= self.last_move[1]
        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x += new_pos[0]
                self.last_move[0] = new_pos[0]
                self.last_move2 = new_pos
                self.last_pos = (new_pos[0], self.last_pos[1])
            else:
                self.rect.x -= self.last_move[0]

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
        pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (speed[0], speed[1]), player=False))
        pulya_group.add(pulya[-1])

    def find_path(self, dest):
        dest_x = dest[0]
        dest_y = dest[1]
        delta_x = dest_x - self.rect.centerx
        delta_y = dest_y - self.rect.centery
        dist = sqrt(delta_x ** 2 +  delta_y ** 2)
        time = dist / self.speed_shooting
        speed_x = delta_x / time
        speed_y = delta_y / time
        return speed_x, speed_y


class Shooting(pygame.sprite.Sprite):
    def __init__(self, group, pos, where, player):
        super().__init__(group)
        self.image = load_image('objects\pulya.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.player = player
        self.rect.y = pos[1] + 20
        self.where = where

    def update(self):
        if not self.player:
            if pygame.sprite.spritecollideany(self, player_group):
                if health:
                    health[-1].update(0)
                else:
                    pygame.quit()
                
                delet = pulya.pop(pulya.index(self))
                all_sprites.remove(delet)
                pulya_group.remove(delet)
        else:
            who = pygame.sprite.spritecollideany(self, bots_group)
            if who:
                if who.health:
                    print('ok')
                    who.health -= 1
                    delet = pulya.pop(pulya.index(self))
                    all_sprites.remove(delet)
                    pulya_group.remove(delet)
                if who.health == 0:
                    delet = bots.pop(bots.index(who))
                    all_sprites.remove(delet)
                    bots_group.remove(delet)

                
        if not pygame.sprite.spritecollideany(self, horizontal_borders) and not pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect.x += self.where[0]
            self.rect.y += self.where[1]
        else:
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
        
        #cur.execute(f"INSERT INTO RECORDS (name, time, score) VALUES ('{name}', '{time}', {score});")
        #con.commit()
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


pygame.init()

size = (1000, 1000)
gaming = True
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('WHITE'))

all_sprites = pygame.sprite.Group()
# Меню
pygame.display.set_caption('ZEON')
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

# Игрок
health = []
player_group = pygame.sprite.Group()
player = Player(all_sprites, (40, 50))
player_group.add(player)

# Боты
enemy = Enemy(all_sprites, (500, 500))
bots = []
bots_group = pygame.sprite.Group()
bots_group.add(enemy)
bots.append(enemy)
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
x, y = 10, 10
for _ in range(10):
    health.append(Health((x, y)))
    x += 30
pygame.display.flip()
fps = 110  # количество кадров в секунду
clock = pygame.time.Clock()
cont = False
player_speed = 3


shoot_tick = 0
# Музыка



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

    pulya_group.update()
    screen.fill(pygame.Color('WHITE'))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
