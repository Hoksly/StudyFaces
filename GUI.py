import tkinter as tk
import pygame

sep = '/'
data_folder = 'data' + sep + 'GUI' + sep

window = pygame.display.set_mode((600, 400))

'''
class MainWindow:
    def __init__(self, width, height, background = data_folder + sep +'background.png' ):
        """

        :param drawer: tkinter.Tk
        :param width:
        :param height:
        :param background:
        """
        self.width = width
        self.height = height
        # self.window = pygame.display.set_mode((self.width, self.height))
        self.background= pygame.image.load(background)
        self.FPS = 30

    def draw(self):
        window.blit(self.background, (0, 0))


Window = MainWindow(600, 400)
'''

background = pygame.image.load(data_folder + 'background.png')


class Person:
    def __init__(self, image, name):
        """

        :param image: pygame scaled image
        :param name: name of person
        """

        self.image = image
        self.name = name

    def compare_name(self, input_name):
        """ Needs to be upgraded"""

        if self.name == input_name:
            return True

    def draw(self, x, y):
        window.blit(self.image, (x, y))


def draw(current_person = 'Nothing'):
    window.blit(background, (0, 0))
    # current_person.draw()

    pygame.display.update()


class Icon:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image)

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(point)


class StartWindow:
    def __init__(self, bg_image = data_folder + 'background.png'):
        self.background = pygame.image.load(bg_image)
        self.start_icon = Icon(200, 80 - 5, 200, 50, data_folder + 'start.png')
        self.settings_icon = Icon(200, 160 - 5, 200, 50, data_folder + "settings.png")
        self.exit_icon = Icon(200, 240, 200 - 5, 50, data_folder + "exit.png")

    def collidepoint(self, point):
        start = self.start_icon.collidepoint(point)
        settings = self.settings_icon.collidepoint(point)
        exit = self.exit_icon.collidepoint(point)

        res = "Main"
        if start:
            res = 'Start'
        elif settings:
            res = 'Settings'
        elif exit:
            res = 'Exit'

        return res

    def draw(self):
        window.blit(self.background, (0, 0))
        self.settings_icon.draw()
        self.start_icon.draw()
        self.exit_icon.draw()


if __name__ == '__main__':
    run = True

    while run:
        pygame.time.delay(1000 // 30)
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                run = False

        draw()
