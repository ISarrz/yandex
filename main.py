import pygame

screen = pygame.display.set_mode((500, 500))
gaming = True
while gaming:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            gaming = False
pygame.quit()
