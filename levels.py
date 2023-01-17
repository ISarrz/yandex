import pygame, math, sys
import technic,  entity, interface

tile_width = tile_height = 30

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.name = 'Tile'
        self.tile_images = {
            'wall': technic.load_image('wall.png', 1),
            'empty': technic.load_image('empty.png', 1),
            'portal': technic.load_image('portal.png', -1),
            'aptechka': technic.load_image('objects/aptechka.png', -1)
        }
        super().__init__(all_sprites)
        self.image = self.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
           tile_width * pos_x, tile_height * pos_y)

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
                bots.append(entity.Enemy(all_sprites, (x * tile_width, (y + 2) * tile_height), level))
                bots_group.add(bots[-1])
    return a * tile_width, b * tile_height

def start_level(level):

    global size, gaming, screen, health, player, player_group, all_sprites, horizontal_borders, vertical_borders, pulya
    global pulya_group, cont, exit_group, wall_group, all_sprites, bots_group, aptechka_group, bots, camera, timer, fire, prtls
    global hirt, kill
    pygame.init()
    size = (600, 600)
    gaming = True
    font = pygame.font.Font('data/fonts/Old-Soviet.otf', 30)
    answer = 0
   
    aptechka_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bots_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    # Игрок
    health = []
    player = entity.Player(all_sprites, generate_level(load_level(level)), level)
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
        health.append(entity.Health((x, y)))
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
            player.update((-math.sqrt(player_speed ** 2 / 2), math.sqrt(player_speed ** 2 / 2)))
            check = False
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.update((math.sqrt(player_speed ** 2 / 2), -math.sqrt(player_speed ** 2 / 2)))
            check = False    
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.update((math.sqrt(player_speed ** 2 / 2), math.sqrt(player_speed ** 2 / 2)))
            check = False
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            player.update((-math.sqrt(player_speed ** 2 / 2), -math.sqrt(player_speed ** 2 / 2)))
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
        try:
            
            camera.update(player)
            for sprite in all_sprites:
                if sprite.name != 'Health':
                    camera.apply(sprite)
            screen.fill(pygame.Color('WHITE'))
            all_sprites.draw(screen)
            tt = pygame.time.get_ticks() - interface.start_time
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
        except Exception:
            pass
    # answer 1 - некст левел, 2 - повтор, 0 - конец
    return answer

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