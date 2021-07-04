import tkinter as tk
import pygame
import os
pygame.init()
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


class MainWindow:
    def __init__(self, persons_list, bg_image = data_folder + 'background.png'):
        self.background = pygame.image.load(bg_image)

        self.user_text = ''
        self.persons_list = persons_list

        self.score = 0
        self.input_rect = pygame.Rect(350, 200, 140, 32)
        self.current_person = 0
        self.image = self.persons_list[self.current_person].image
        self.m_mode = 0
        self.was_answer_right = True
        # debug print
        # print(os.getcwd() + sep + data_folder + 'ChelseaMarket-Regular.ttf')

        self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', 32)

    def update_input(self, event):
        if event.type == pygame.KEYDOWN:

            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                self.user_text = self.user_text[:-1]

            elif event.key == pygame.K_RETURN:
                self.m_mode += 1
                if self.persons_list[self.current_person].compare_name(self.user_text):
                    self.score += 1
                    self.was_answer_right = True

                self.was_answer_right = False

                self.user_text = self.persons_list[self.current_person].name

                if self.m_mode % 2 == 0:
                    if self.current_person < len(self.persons_list) - 1:
                        self.current_person += 1
                        self.image = self.persons_list[self.current_person].image
                        self.user_text = ''
                        self.was_answer_right = True

                        return '', self.score

                    return 'Finish', self.score

            else:
                self.user_text += event.unicode

    def draw(self):
        window.blit(self.background, (0, 0))

        pygame.draw.rect(window, pygame.Color('lightblue'), self.input_rect)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255)if self.was_answer_right else (255, 0, 0))
        window.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        self.input_rect.w = max(100, text_surface.get_width() + 10)

        self.persons_list[self.current_person].draw(100, 100)


class FinalScreen:
    def __init__(self, score, all_score, failed, bg_image = data_folder + 'background.png'):
        """

        :param score: final score, int
        :param failed: failed answers (names), list
        """
        self.score = score
        self.failed_answers = failed
        self.background = pygame.image.load(bg_image)
        self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', 32)
        self.all_score = all_score

    def draw(self):
        window.blit(self.background, (0, 0))
        score_text = self.font.render('Your final score: ' + '{}/{}'.format(self.score, self.all_score), True, (255, 255, 255))
        window.blit(score_text, (300 - score_text.get_width()/2, 100))

        failed_answers_text = []

        failed_answers_text.append(self.font.render('Failed:', True, (255, 255, 255)))
        y = 105
        y += score_text.get_height()

        for answer in self.failed_answers:
            failed_answers_text.append(self.font.render(answer, True, (255, 0, 0)))

        for text in failed_answers_text:
            window.blit(text, (300 - text.get_width()/2, y))
            y += text.get_height()


if __name__ == '__main__':
    run = True
    # Window = MainWindow([Person(pygame.transform.scale(pygame.image.load('data/Persons/Test_set/Герман_Болдырев.jpeg'), (200, 200)), 'GG')])
    Window = FinalScreen(2, 16, ['gg', 'GG'])
    while run:
        pygame.time.delay(1000 // 30)
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                run = False
            # Window.update_input(el)

        Window.draw()

        pygame.display.update()
