import interface
import levels


all_levels = [ 'level_1.txt', 'level_2.txt', 'level_3.txt']
tile_width = tile_height = 30
# Запуск Меню

interface.menu()

for i in all_levels:
    answer = levels.start_level(i)
    if answer == 2:
        while answer == 2:
            answer = levels.start_level(i)
    if answer == 1 and i == all_levels[-1]:
        end = interface.End()

