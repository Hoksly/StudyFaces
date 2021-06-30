from ImageFunctions import generate_new_set, take_photos_and_their_names_from_directory
from GUI import Person, StartWindow
from GUIFunctions import give_folder_name
import pygame

pygame.init()

window = pygame.display.set_mode((600, 400))
W = StartWindow()

run = True
mode = 'Main'

if __name__ == '__main__':
    run = True

    while run:
        pygame.time.delay(1000 // 30)

        for el in pygame.event.get():
            if el.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = el.pos
                mode = W.collidepoint(mouse_pos)

            if el.type == pygame.QUIT or mode == 'Exit':
                run = False
        if mode == "Main":
            W.draw()

        if mode == 'Start':
            pass # Switch to start menu

        if mode == 'Settings':
            pass # Switch to settings

        pygame.display.update()

pygame.quit()