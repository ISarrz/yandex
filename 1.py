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
        self.image = load_image("player_1.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.last_move = [0, 0]

    def update(self, new_pos):
        if not pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect.x += new_pos[0]
            self.last_move = new_pos
        else:
            self.rect.x -= self.last_move[0]
        if not pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect.y += new_pos[1]
            self.last_move = new_pos
        else:
            self.rect.y -= self.last_move[1]
        print(self.last_move)


class Health(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = load_image('health.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def down(self):
        del self

    def update(self, action):
        if action == 1: #здесь будет какая-то хилка
            health.append(Health((health[-1].rect.x + 10, 10)))
        else:
            health[-1].down()



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
size = (500, 500)
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
x, y = 10, 10
for _ in range(10):
    health.append(Health((x, y)))
    x += 30
pygame.display.flip()
fps = 60  # количество кадров в секунду
clock = pygame.time.Clock()
cont = False
player_speed = 3
while gaming:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.update((0, -player_speed))
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.update((0, player_speed))
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.update((-player_speed, 0))
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.update((player_speed, 0))
    if keys[pygame.K_DELETE]:
        health[-1].update(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gaming = False

    screen.fill(pygame.Color('WHITE'))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
