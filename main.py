from ImageFunctions import generate_new_set, take_photos_and_their_names_from_directory
from GUI import Person, StartWindow, MainWindow, FinalScreen, MiddleScreen, ChooseSetScreen, CreateNewSetScreen
from GUIFunctions import give_folder_name
import pygame
pygame.init()

window = pygame.display.set_mode((600, 400))



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


Main = None
W = StartWindow()
Final_Score_Screen = FinalScreen()
MiddleScreen = MiddleScreen()
Chose_Screen = ChooseSetScreen()
NewSetScreen = CreateNewSetScreen()
run = True
mode = 'Main'

if __name__ == '__main__':
    run = True

    while run:
        #print(mode)
        pygame.time.delay(1000 // 30)

        for el in pygame.event.get():
            if mode == 'Create New Set':
                NewSetScreen.clicks(el)
            if el.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = el.pos
                if mode == 'Main':
                    mode = W.collidepoint(mouse_pos)

                elif mode == 'Start':
                    mode = MiddleScreen.clicks(el.pos)

                elif mode == 'Chose Set':
                    folder = Chose_Screen.clicks(el.pos)
                    if folder != 'Chose Set':
                        Main = MainWindow(create_persons_list('data/Persons/' + folder))
                        mode = 'In Game'
            if mode == 'In Game':
                mode = Main.update_input(el)

            if el.type == pygame.QUIT or mode == 'Exit':
                run = False
        if mode == "Main":
            W.draw()

        elif mode == 'Start':
            MiddleScreen.draw()

        elif mode == 'In Game':
            Main.draw()

        elif mode == 'Chose Set':
            Chose_Screen.draw()
        elif mode == 'Create New Set':
            NewSetScreen.draw()

        elif mode == 'Settings':
            pass # Switch to settings

        elif mode == 'Finish':
            if Final_Score_Screen.get_status():
                score, all_score, failed = Main.return_data()
                Final_Score_Screen.update_data(score, all_score, failed)
            else:
                Final_Score_Screen.draw()

        pygame.display.update()


pygame.quit()

