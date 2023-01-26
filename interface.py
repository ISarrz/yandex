import pygame, sys, sqlite3, levels

def menu():
    global start_time
    pygame.init()
    pygame.mixer.music.load("data/sounds/main_menu_theme.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    Menu().menu(True)
    pygame.quit()
    start_time = pygame.time.get_ticks()


class Menu:
    def __init__(self) -> None:
        punkts = [[400, 250, u'Играть', (255, 255, 255), (176, 5, 5), 0],
          [340, 400, u'Статистика', (255, 255, 255), (176, 5, 5), 1],
          [400, 550, u'Выход', (250, 250, 30), (176, 5, 5), 2]]
        pygame.init()

        size = (1000, 1000)
        screen = pygame.display.set_mode(size)
        
        self.punkts = punkts
        self.screen = screen

    def menu(self, esc):
        running = True
        font_menu = pygame.font.Font('data/fonts/Purisa.ttf', 60)
        punkt = -1
        while running:
            mp = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            for i in self.punkts:
                if (mp[0] > i[0] and mp[0] < i[0] + 155) and mp[1] > i[1] and (mp[1] < i[1] + 50):
                    punkt = i[5]
                    break
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
      
            if keys[pygame.K_ESCAPE] and not esc:
                sys.exit()

            if pygame.mouse.get_pressed()[0]:
                if punkt == 0:
                    running = False
                elif punkt == 1:
                    
                    rec = Records()
                    rec.records()
                    pass
                elif punkt == 2:
                    sys.exit()
            if not esc:
                esc = False

            self.screen.fill((163, 160, 160))
            for i in self.punkts:
                if punkt == i[5]:
                    self.screen.blit(font_menu.render(i[2], True, i[4]), (i[0], i[1]))
                else:
                    self.screen.blit(font_menu.render(i[2], True, i[3]), (i[0], i[1]))

            self.screen.blit(self.screen, (0, 0))
            pygame.display.flip()
        

class Records:
    def __init__(self) -> None:
        pygame.init()

        size = (1000, 1000)
        screen = pygame.display.set_mode(size)
        self.screen = screen
        
    def records(self):
        done = True
        pygame.font.init()
        pygame.font.get_init()
        sc = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption('ZEON')

        font = pygame.font.Font('data/fonts/Old-Soviet.otf', 30)
        con = sqlite3.connect('data/game.sqlite')
        cur = con.cursor()

        text1 = font.render('№', True, (0, 0, 0))
        text2 = font.render('Никнейм', True, (0, 0, 0))
        text3 = font.render('Время', True, (0, 0, 0))
        text4 = font.render('Счёт', True, (0, 0, 0))

        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()
        textRect4 = text4.get_rect()

        BLACK = (0, 0, 0)
        textRect1.center = (20, 30)
        textRect2.center = (200, 30)
        textRect3.center = (600, 30)
        textRect4.center = (900, 30)

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
                    
                    quit()
                pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            if keys[pygame.K_ESCAPE]:
                self.screen.blit(self.screen, (0, 0))
                pygame.display.flip()
                done = False
                
                Menu().menu(True)

            self.screen.blit(self.screen, (0, 0))
            pygame.display.flip()


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
        self.window = screen

    def menu(self):
        global timer
        time = levels.timer
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
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()
            clock.tick(30)

