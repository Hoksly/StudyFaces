from ImageFunctions import generate_new_set, take_photos_and_their_names_from_directory
from GUI import Person, StartWindow, MainWindow
from GUIFunctions import give_folder_name
import pygame
pygame.init()

window = pygame.display.set_mode((600, 400))
W = StartWindow()


def create_persons_list(folder):
    """

    :param folder: target folder
    :return: list which have GUI.Person types of data for all photos

    """
    photos_and_names = take_photos_and_their_names_from_directory(folder)
    persons_list = []
    for el in list(photos_and_names.keys()):
        persons_list.append(Person(photos_and_names[el], el))

    return persons_list


Main = MainWindow(create_persons_list('data/Persons/Test_set'))
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
            Main.draw()

        if mode == 'Settings':
            pass # Switch to settings

        pygame.display.update()


pygame.quit()

