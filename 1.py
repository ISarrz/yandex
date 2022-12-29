import pygame
import os
import sys


def load_image(name, colorkey=None):
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


class Hero(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = load_image("mario.png")
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
        else:
            self.rect.y -= self.last_move[1]
        print(self.last_move)


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
hero = Hero(all_sprites, (10, 10))
all_sprites.draw(screen)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(5, 5, size[0] - 5, 5)
Border(5, size[1] - 5, size[0] - 5, size[1] - 5)
Border(5, 5, 5, size[1] - 5)
Border(size[0] - 5, 5, size[0] - 5, size[1] - 5)
pygame.display.flip()
fps = 50  # количество кадров в секунду
clock = pygame.time.Clock()
cont = False
while gaming:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gaming = False
        if event.type == pygame.KEYDOWN:
            new_key = event.key
            if new_key == pygame.K_UP:
                hero.update((0, -1))
            if new_key == pygame.K_DOWN:
                hero.update((0, 1))
            if new_key == pygame.K_LEFT:
                hero.update((-1, 0))
            if new_key == pygame.K_RIGHT:
                hero.update((1, 0))
            last_key = new_key
            cont = True
        if event.type == pygame.KEYUP:
            cont = False
    if cont:
        print('go')
        if last_key == pygame.K_UP:
            hero.update((0, -1))
        if last_key == pygame.K_DOWN:
            hero.update((0, 1))
        if last_key == pygame.K_LEFT:
            hero.update((-1, 0))
        if last_key == pygame.K_RIGHT:
            hero.update((1, 0))
    screen.fill(pygame.Color('WHITE'))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
