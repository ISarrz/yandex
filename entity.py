import technic
import pygame, math
import levels, technic

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, level):
        super().__init__(group)
        self.name = 'Player'
        self.level = level
        self.image = technic.load_image("player/player_left1.png", -1)
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
        if pygame.sprite.spritecollideany(self, levels.aptechka_group):
            self_group = pygame.sprite.Group()
            self_group.add(self) 
            col = pygame.sprite.groupcollide(self_group, levels.aptechka_group, False, False)
            ban = []
            for i in col.items():
                obj = i[1][0]
                ban.append(obj)
            for i in ban:
                levels.aptechka_group.remove(i)
                levels.all_sprites.remove(i)
            x = levels.health[-1].rect.x + 30
            y = levels.health[-1].rect.y
            for i in range(10 - len(levels.health)):
                levels.health.append(Health((x, y)))
                x += 30
        if pygame.sprite.spritecollideany(self, levels.exit_group) and len(levels.bots) <= 0:
            self.finish = True
        if pygame.sprite.spritecollideany(self, levels.wall_group):
            self.come_back()
        else:
            self.last_pos = [self.rect.x, self.rect.y]

    def update(self, new_pos):
        if self.last_move2[0] != new_pos[0] or self.last_move2[1] != new_pos[1]:
            self.change_image_for_moving(new_pos)
        else:
            self.animation_moving()
        if new_pos[1] != 0:
            if not pygame.sprite.spritecollideany(self, levels.wall_group):
                self.rect.y += new_pos[1]
                self.check_on_collide()
                self.last_move[1] = new_pos[1]
                self.last_move2 = new_pos
        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, levels.wall_group):
                self.rect.x += new_pos[0]
                self.check_on_collide()
                self.last_move[0] = new_pos[0]
                self.last_move2 = new_pos

    def animation_stop(self):
        if self.now_image[0] == 'left':
            self.image = technic.load_image('player/player_left.png')
        if self.now_image[0] == 'right':
            self.image = technic.load_image('player/player_right.png')
        if self.now_image[0] == 'down':
            self.image = technic.load_image('player/player_down.png')
        if self.now_image[0] == 'up':
            self.image = technic.load_image('player/player_up.png')

    def animation_moving(self):
        if self.now_image[1][-5] == '2':
            self.image = technic.load_image(self.images[self.now_image[0]][0])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][0]]
        else:
            self.image = technic.load_image(self.images[self.now_image[0]][1])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][1]]
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.check_on_collide()

    def change_image_for_moving(self, new_pos):
        if new_pos[0] > 0:
            self.image = technic.load_image('player/player_right1.png')
            self.now_image = ['right', 'player/player_right1.png']
        if new_pos[0] < 0:
            self.image = technic.load_image('player/player_left1.png')
            self.now_image = ['left', 'player/player_left1.png']
        if new_pos[1] > 0:
            self.image = technic.load_image('player/player_down1.png')
            self.now_image = ['down', 'player/player_down1.png']
        if new_pos[1] < 0:
            self.image = technic.load_image('player/player_up1.png')
            self.now_image = ['up', 'player/player_up1.png']
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.check_on_collide()

    def strike(self, speed):
        levels.pulya.append(Shooting(levels.all_sprites, (self.rect.x, self.rect.y), (speed[0], speed[1]), self.level, player=True))
        levels.pulya_group.add(levels.pulya[-1])

    def find_path(self, dest):
        dest_x, dest_y = dest[0], dest[1]
        delta_x = dest_x - self.rect.centerx
        delta_y = dest_y - self.rect.centery
        dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
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
        self.image = technic.load_image("enemy\enemy_right1.png")
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
        dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
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
        if pygame.sprite.spritecollideany(self, levels.exit_group) and len(levels.bots) <= 0:
            self.finish = True
        if pygame.sprite.spritecollideany(self, levels.wall_group):
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
            if not pygame.sprite.spritecollideany(self, levels.wall_group):
                self.rect.y += new_pos[1]
                self.check_on_collide()
                self.last_move[1] = new_pos[1]
                self.last_move2 = new_pos
        if new_pos[0] != 0:
            if not pygame.sprite.spritecollideany(self, levels.wall_group):
                self.rect.x += new_pos[0]
                self.check_on_collide()
                self.last_move[0] = new_pos[0]
                self.last_move2 = new_pos

    def animation_stop(self):
        if self.now_image[0] == 'left':
            self.image = technic.load_image('enemy\enemy_left.png')
        if self.now_image[0] == 'right':
            self.image = technic.load_image('enemy\enemy_right.png')
        if self.now_image[0] == 'down':
            self.image = technic.load_image('enemy\enemy_down.png')
        if self.now_image[0] == 'up':
            self.image = technic.load_image('enemy\enemy_up.png')

    def animation_moving(self):
        if self.now_image[1][-5] == '2':
            self.image = technic.load_image(self.images[self.now_image[0]][0])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][0]]
        else:
            self.image = technic.load_image(self.images[self.now_image[0]][1])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][1]]
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.check_on_collide()

    def change_image_for_moving(self, new_pos):
        if new_pos[0] > 0 and new_pos[0] > abs(new_pos[1]):
            self.image = technic.load_image('enemy\enemy_right1.png')
            self.now_image = ['right', 'enemy\enemy_right1.png']
        if new_pos[0] < 0 and abs(new_pos[0]) > abs(new_pos[1]):
            self.image = technic.load_image('enemy\enemy_left1.png')
            self.now_image = ['left', 'enemy\enemy_left1.png']
        if new_pos[1] > 0 and abs(new_pos[1]) > abs(new_pos[0]):
            self.image = technic.load_image('enemy\enemy_down1.png')
            self.now_image = ['down', 'enemy\enemy_down1.png']
        if new_pos[1] < 0 and abs(new_pos[1]) > abs(new_pos[0]):
            self.image = technic.load_image('enemy\enemy_up1.png')
            self.now_image = ['up', 'enemy\enemy_up1.png']
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.check_on_collide()

    def strike(self, speed):
        levels.pulya.append(Shooting(levels.all_sprites, (self.rect.x, self.rect.y), (speed[0], speed[1]), self.level, player=True))
        levels.pulya_group.add(technic.pulya[-1])

    def find_path(self, dest):
        dest_x, dest_y = dest[0], dest[1]
        delta_x = dest_x - self.rect.centerx
        delta_y = dest_y - self.rect.centery
        dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
        time = dist / self.speed_shooting
        speed_x = delta_x / time
        speed_y = delta_y / time
        return speed_x, speed_y

    def animation_moving(self):
        if self.now_image[1][-5] == '2':
            self.image = technic.load_image(self.images[self.now_image[0]][0])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][0]]
        else:
            self.image = technic.load_image(self.images[self.now_image[0]][1])
            self.now_image = [self.now_image[0], self.images[self.now_image[0]][1]]
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

   

    def strike(self, speed):
        levels.pulya.append(Shooting(levels.all_sprites, (self.rect.x, self.rect.y), (speed[0], speed[1]), self.level, player=False))
        levels.pulya_group.add(levels.pulya[-1])

    def find_path(self, dest):
        dest_x = dest[0]
        dest_y = dest[1]
        delta_x = dest_x - self.rect.centerx
        delta_y = dest_y - self.rect.centery
        dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
        time = dist / self.speed_shooting
        if time:
            speed_x = delta_x / time
            speed_y = delta_y / time
            return speed_x, speed_y


class Shooting(pygame.sprite.Sprite):
    def __init__(self, group, pos, where, level, player):
        global fire
        super().__init__(group)
        levels.fire.play()
        self.name = 'Shooting'
        self.level = level
        self.image = technic.load_image('objects\pulya.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.player = player
        self.rect.y = pos[1] + 20
        self.where = where

    def update(self):
        check = False
        if not self.player:
            if pygame.sprite.spritecollideany(self, levels.player_group):
                if levels.health:
                    levels.health[-1].update(0)
                else:
                    pygame.quit()

                delet = levels.pulya.pop(levels.pulya.index(self))
                levels.all_sprites.remove(delet)
                levels.pulya_group.remove(delet)
                check = True
            elif pygame.sprite.spritecollideany(self, levels.wall_group):
                delet = levels.pulya.pop(levels.pulya.index(self))
                levels.all_sprites.remove(delet)
                levels.pulya_group.remove(delet)
                check = True
        else:
            who = pygame.sprite.spritecollideany(self, levels.bots_group)
            if pygame.sprite.spritecollideany(self, levels.wall_group):
                delet = levels.pulya.pop(levels.pulya.index(self))
                levels.all_sprites.remove(delet)
                levels.pulya_group.remove(delet)
                check = True
            elif who:
                if who.health:
                    who.health -= 1
                    print(-1)
                    delet = levels.pulya.pop(levels.pulya.index(self))
                    levels.all_sprites.remove(delet)
                    levels.pulya_group.remove(delet)
                    check = True
                if who.health == 0:
                    levels.kill.play()
                    delet = levels.bots.pop(levels.bots.index(who))
                    levels.all_sprites.remove(delet)
                    levels.bots_group.remove(delet)
                    check = True
                if len(levels.bots) == 0:
                    levels.generate_finish(levels.load_level(self.level))

        if not pygame.sprite.spritecollideany(self, levels.horizontal_borders) and not pygame.sprite.spritecollideany(self,
                                                                                                               levels.vertical_borders):
            self.rect.x += self.where[0]
            self.rect.y += self.where[1]
        else:
            if not check:
                delet = levels.pulya.pop(levels.pulya.index(self))
                levels.all_sprites.remove(delet)
                levels.pulya_group.remove(delet)


class Health(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(levels.all_sprites)
        self.name = 'Health'
        self.image = technic.load_image('objects\health.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, action):
        if action == 1 and 1 <= len(levels.health) <= 9:  # здесь будет какая-то хилка
            levels.health.append(Health((levels.health[-1].rect.x + 30, 10)))
        if action == 0 and len(levels.health) >= 1:
            levels.hirt.play()
            delet = levels.health.pop(-1)
            levels.all_sprites.remove(delet)
        if len(levels.health) == 0:
            levels.kill.play()
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


