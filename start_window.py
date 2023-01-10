import pygame
import os

pygame.init()
size = 400, 400
screen = pygame.display.set_mode(size)
screen.fill((0, 200, 15))
font = pygame.font.Font(None, 50)
text = font.render('Начать игру', True, (170, 0, 20))
text_x = size[0] // 2 - text.get_width() // 2
text_y = size[1] // 2 - text.get_height() // 2
text_w = text.get_width()
text_h = text.get_height()
screen.blit(text, (text_x, text_y))
pygame.draw.rect(screen, (120, 0, 120), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
pygame.display.flip()
start = True
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            pos = event.pos
            if text_x <= pos[0] <= text_x + text_w and text_y <= pos[1] <= text_y + text_h:
                os.startfile('1.py')
pygame.quit()