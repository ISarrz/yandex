import pygame 
import sqlite3

def menu(self):
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
            cur.executemany(f"INSERT INTO RECORDS (name, time, score) VALUES('{text}', '{time}', {score});")
            con.commit()
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


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()