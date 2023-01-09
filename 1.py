import pygame
import os
import sys


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
        self.image = load_image("player_right1.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.last_move = [0, 0]
        self.last_move2 = [0, 0]
        self.speed_shooting = 10
        self.now_image = ['right', 'player_right1.png']
        self.images = {
            'down': ['player_down1.png', 'player_down2.png'],
            'up': ['player_up1.png', 'player_up2.png'],
            'right': ['player_right1.png', 'player_right2.png'],
            'left': ['player_left1.png', 'player_left2.png']
        }

    def update(self, new_pos):
        if self.last_move2[0] != new_pos[0] or self.last_move2[1] != new_pos[1]:
            self.change_image_for_moving(new_pos)
            print('no')
        else:
            print('ok')
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
            self.image = load_image('player_left.png')
        if self.now_image[0] == 'right':
            self.image = load_image('player_right.png')
        if self.now_image[0] == 'down':
            self.image = load_image('player_down.png')
        if self.now_image[0] == 'up':
            self.image = load_image('player_up.png')

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
            self.image = load_image('player_right1.png')
            self.now_image = ['right', 'player_right1.png']
        if new_pos[0] < 0:
            self.image = load_image('player_left1.png')
            self.now_image = ['left', 'player_left1.png']
        if new_pos[1] > 0:
            self.image = load_image('player_down1.png')
            self.now_image = ['down', 'player_down1.png']
        if new_pos[1] < 0:
            self.image = load_image('player_up1.png')
            self.now_image = ['up', 'player_up1.png']
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def strike(self):
        if self.now_image[0] == 'right':
            #self.image = load_image('player_right_s.png')
            pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (self.speed_shooting, 0)))
        if self.now_image[0] == 'left':
            #self.image = load_image('player_left_s.png')
            pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (-self.speed_shooting, 0)))
        if self.now_image[0] == 'down':
            #self.image = load_image('player_down_s.png')
            pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (0, self.speed_shooting)))
        if self.now_image[0] == 'up':
            #self.image = load_image('player_up_s.png')
            pulya.append(Shooting(all_sprites, (self.rect.x, self.rect.y), (0, -self.speed_shooting)))
        pulya_group.add(pulya[-1])


class Shooting(pygame.sprite.Sprite):
    def __init__(self, group, pos, where):
        super().__init__(group)
        self.image = load_image('pulya.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] + 20
        self.where = where

    def update(self):
        print(self.rect.center)
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
        self.image = load_image('health.png')
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


pygame.init()
size = (1000, 1000)
gaming = True
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('WHITE'))
all_sprites = pygame.sprite.Group()
player = Player(all_sprites, (40, 50))
all_sprites.draw(screen)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(5, 40, size[0] - 5, 40)
Border(5, size[1] - 5, size[0] - 5, size[1] - 5)
Border(5, 40, 5, size[1] - 5)
Border(size[0] - 5, 40, size[0] - 5, size[1] - 5)
health = []
pulya_group = pygame.sprite.Group()
pulya = []
x, y = 10, 10
for _ in range(10):
    health.append(Health((x, y)))
    x += 30
print(health)
pygame.display.flip()
fps = 110  # количество кадров в секунду
clock = pygame.time.Clock()
cont = False
player_speed = 3
while gaming:
    keys = pygame.key.get_pressed()
    check = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.update((0, -player_speed))
        check = False
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.update((0, player_speed))
        check = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.update((-player_speed, 0))
        check = False
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.update((player_speed, 0))
        check = False
    """
    if keys[pygame.BUTTON_LEFT]:
        player.strike()
    """
    if check:
        player.animation_stop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gaming = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                gaming = health[-1].update(0)
            if event.key == pygame.K_EQUALS:
                gaming = health[-1].update(1)
            if event.key == pygame.K_SPACE:
                player.strike()
    pulya_group.update()
    screen.fill(pygame.Color('WHITE'))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
