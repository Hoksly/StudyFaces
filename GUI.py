import os
import string
import pygame
from ImageFunctions import generate_new_set
from GUIFunctions import check_input
from time import sleep

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

        if '_' in name:
            self.name = name.split('_')
        elif ' ' in name:
            self.name = name.split()
        else:
            assert ValueError("Error with file {}, it must contain '_' or ' ' separator between name and second name"
                              " ".format(name))

    def compare_name(self, input_name: str):
        # print(self.name, input_name.split(), self.name == input_name.split())
        return self.name == input_name.split()

    def get_name(self):
        return ' '.join(self.name)

    def draw(self, x, y):
        window.blit(self.image, (x, y))


def draw(current_person='Nothing'):
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
    def __init__(self, bg_image=data_folder + 'background.png'):
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
    def __init__(self, persons_list, bg_image=data_folder + 'background.png'):
        self.background = pygame.image.load(bg_image)

        self.user_text = ''
        self.printed_text = ''
        self.persons_list = persons_list

        self.score = 0
        self.input_rect = pygame.Rect(350, 200, 140, 32)
        self.current_person = 0
        self.last_person = len(self.persons_list)
        self.image = self.persons_list[self.current_person].image
        self.m_mode = 0
        self.was_answer_right = True

        self.failed = []

        # debug print
        # print(os.getcwd() + sep + data_folder + 'ChelseaMarket-Regular.ttf')

        self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', 32)

    def update_input(self, event):
        if event.type == pygame.KEYDOWN:

            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                self.printed_text = self.printed_text[:-1]
                self.user_text = self.user_text[:-1]

            elif event.key == pygame.K_RETURN:

                self.m_mode += 1
                if self.persons_list[self.current_person].compare_name(self.user_text):
                    self.score += 1
                    self.was_answer_right = True
                    self.m_mode += 1

                elif self.m_mode % 2 == 0:
                    self.failed.append(self.persons_list[self.current_person].get_name())

                self.was_answer_right = False

                self.printed_text = self.persons_list[self.current_person].get_name()

                if self.m_mode % 2 == 0:
                    if self.current_person < len(self.persons_list) - 1:
                        self.current_person += 1
                        self.image = self.persons_list[self.current_person].image
                        self.user_text = ''
                        self.printed_text = ''
                        self.was_answer_right = True


                    else:
                        print('here')
                        return 'Finish'

            else:
                self.user_text += event.unicode
                self.printed_text += event.unicode

        return 'In Game'

    def draw(self):
        window.blit(self.background, (0, 0))

        pygame.draw.rect(window, pygame.Color('lightblue'), self.input_rect)
        text_surface = self.font.render(self.printed_text, True,
                                        (255, 255, 255) if self.was_answer_right else (255, 0, 0))
        window.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        self.input_rect.w = max(100, text_surface.get_width() + 10)

        self.persons_list[self.current_person].draw(100, 100)

    def return_data(self):
        return self.score, self.last_person, self.failed


class FinalScreen:
    def __init__(self, bg_image=data_folder + 'background.png'):
        """

        :param score: final score, int
        :param failed: failed answers (names), list
        """
        self.score = None
        self.failed_answers = None
        self.all_score = None

        self.created = True
        self.background = pygame.image.load(bg_image)
        self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', 32)

    def update_data(self, score, all_score, failed):
        """
        Need to be initialize a bit later
        :param score: int
        :param all_score: int
        :param failed: list
        :return:
        """
        self.score = score
        self.failed_answers = failed
        self.all_score = all_score
        self.created = False

    def get_status(self):
        return self.created

    def draw(self):
        window.blit(self.background, (0, 0))
        score_text = self.font.render('Your final score: ' + '{}/{}'.format(self.score, self.all_score), True,
                                      (255, 255, 255))
        window.blit(score_text, (300 - score_text.get_width() / 2, 100))

        failed_answers_text = []

        failed_answers_text.append(self.font.render('Failed:', True, (255, 255, 255)))
        y = 105
        y += score_text.get_height()

        for answer in self.failed_answers:
            failed_answers_text.append(self.font.render(answer, True, (255, 0, 0)))

        for text in failed_answers_text:
            window.blit(text, (300 - text.get_width() / 2, y))
            y += text.get_height()


class Object:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y

    def draw(self):
        window.blit(self.image, (self.x, self.y))


'''
class Text(Icon):
    def __init__(self, x, y, text, width=200, height=50):
        self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', 32)
        text_surface = self._render_text(text)

        super(Text, self).__init__(x, y, width, height, text_surface)

    def _render_text(self, text):
        return self.font.render(text, True, (255, 255, 255))
'''


class Label:
    def __init__(self, text, x, y, width=200, height=50, text_size=32, align='center', color=(255, 255, 255)):
        self.background = pygame.Rect((x, y), (width, height))
        self.font = self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', text_size)
        self.input = text
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.align = align

        self.text = self._render_text(text)


    def _render_text(self, text):
        return self.font.render(text, True, self.color)

    def draw(self):
        self.background.width = max(self.background.width, self.text.get_width() + 5)
        pygame.draw.rect(window, pygame.Color('lightblue'), self.background)
        if self.align == 'center':
            label_x = self.x + (self.width - self.text.get_width()) / 2
            label_y = self.y + (self.height - self.text.get_height()) / 2

        elif self.align == 'right':
            label_x = self.x
            label_y = self.y + (self.height - self.text.get_height()) / 2
        else:
            label_x = self.x
            label_y = self.y

        window.blit(self.text, (label_x, label_y))

    def _collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(point)

    def update_input(self, event):
        pass


class ClickAbleLabel(Label):
    def __init__(self, x, y, text, func, text_size=32, width=200, height=50):
        super().__init__(text=text, x=x, y=y, text_size=text_size, width=width, height=height)
        self.click_function = func

    def click_on(self, point):
        if self._collidepoint(point):

            if self.click_function:
                return self.click_function()
            else:
                return self.input


class Screen:
    def __init__(self, bg_image=data_folder + 'background.png'):
        self.background = pygame.image.load(bg_image)
        self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', 32)
        self.objects = []

    def draw(self):
        window.blit(self.background, (0, 0))

        for obj in self.objects:
            obj.draw()


'''
# Not in usage, for now
def give_folder_name(name):
    return name
'''


class ChooseSetScreen(Screen):
    def __init__(self, set_folder='data/Persons'):
        super().__init__()
        self.set_folder = set_folder
        self.all_sets = os.listdir(set_folder)
        self.mode = 'Chose Set'
        x = 200
        y = 0
        for folder in self.all_sets:
            self.objects.append(ClickAbleLabel(x, y, folder, None, 30, height=30))
            y += 35

    def clicks(self, point):
        for obj in self.objects:
            mode = obj.click_on(point)
            if mode:
                self.mode = mode

        return self.mode

    def draw(self):
        super().draw()


class TextInput:
    def __init__(self, x, y, width=140, height=32, mode='all', text_size=32, color=(255, 255, 255)):
        self.user_text = ''
        self.x = x
        self.y = y
        self.input_rect = pygame.Rect(x, y, width, height)
        self.mode = mode
        self.font = self.font = pygame.font.SysFont(data_folder + 'ChelseaMarket-Regular.ttf', text_size)
        self.color = color

    def update_input(self, event):
        if event.type == pygame.KEYDOWN:

            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                self.user_text = self.user_text[:-1]
            elif event.key != pygame.K_RETURN:
                if self.mode == 'numbers':
                    self.user_text += event.unicode if event.unicode in string.digits else ''
                elif self.mode == 'letters':
                    self.user_text += event.unicode if event.unicode in string.ascii_letters else ''
                else:
                    self.user_text += event.unicode

    def return_value(self):
        return self.user_text

    def draw(self):
        pygame.draw.rect(window, pygame.Color('lightblue'), self.input_rect)
        text_surface = self.font.render(self.user_text, True,
                                        self.color)
        window.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)


def create_new_set():
    pass


class CreateNewSetScreen(Screen):
    def __init__(self):
        super().__init__()
        self.level = 1

        self.objects.append(Label('Name of new set:', 100, 100, align='right', height=32, text_size=30))
        self.objects.append(TextInput(350, 100, height=32, text_size=32))

        self.objects.append(Label('Number of humans:', 100, 150, align='right', height=32, text_size=30))
        self.objects.append(TextInput(350, 150, height=32, text_size=32))

        self.objects.append(Label('Language (Eng, Rus):', 100, 200, align='right', height=32, text_size=30))
        self.objects.append(TextInput(350, 200, height=32, text_size=32))

        self.objects.append(Label('Age (beta):', 100, 250, align='right', height=32, text_size=30))
        self.objects.append(TextInput(350, 250, height=32, text_size=32))

        self.objects.append(Label('Gender (beta):', 100, 300, align='right', height=32, text_size=30))
        self.objects.append(TextInput(350, 300, height=32, text_size=32))

        self.objects.append(ClickAbleLabel(200, 350, 'Confirm', create_new_set))

        self.run = True
        self.finished = False

    """
    Neds to be upgraded, when input is incorrect. Faced bug with same photos, about 3-4 same photos in one dir 
    (solved with time.sleep).
    """

    def clicks(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.objects[-1]._collidepoint(event.pos):
                set_name = self.objects[1].return_value()
                number_of_members = self.objects[3].return_value() if self.objects[3].return_value() != '' else 10
                lang = self.objects[5].return_value() if self.objects[5].return_value() != '' else 'rus'
                age = self.objects[7].return_value() if self.objects[7].return_value() != '' else 0  # beta
                gender = self.objects[9].return_value() if self.objects[9].return_value() != '' else 0  # beta

                right, res = check_input(set_name, number_of_members, lang, age, gender)
                self.run = True
                for i in range(5):
                    if not right[i]:
                        self.objects[1 + i*2].color = (255, 0, 0)
                        self.run = False

                if self.run:
                    print(set_name, number_of_members, lang, age, gender)
                    self.finished = generate_new_set(set_name, int(number_of_members), language=lang, age=age, gender=gender)

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                self.level -= 1 if self.level > 1 else 0
            elif event.key == pygame.K_DOWN:
                self.level += 1 if self.level < 9 else 0
            else:
                self.objects[self.level].update_input(event)

        return 'Create New Set' if not self.finished else 'Chose Set'


# Functions for MiddleScreen class
def go_to_chose_set():
    return "Chose Set"


def go_to_create_new_set():
    return "Create New Set"


class MiddleScreen(Screen):
    def __init__(self):
        super().__init__()
        self.objects.append(ClickAbleLabel(200, 100, 'Chose set', go_to_chose_set))
        self.objects.append(ClickAbleLabel(200, 200, 'Create new set', go_to_create_new_set))
        self.mode = 'Start'

    def clicks(self, point):
        for obj in self.objects:
            mode = obj.click_on(point)
            if mode:
                self.mode = mode
        return self.mode


class CreateRandomSetScreen:
    def __init__(self):
        pass


if __name__ == '__main__':
    run = True
    # Window = MainWindow([Person(pygame.transform.scale(pygame.image.load('data/Persons/Test_set/Герман_Болдырев.jpeg'), (200, 200)), 'GG')])
    # Window = FinalScreen()
    # Window.update_data(2, 16, ['gg', 'GG'])
    # Window = MiddleScreen()
    Window = CreateNewSetScreen()
    while run:
        pygame.time.delay(1000 // 30)
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                run = False
            Window.clicks(el)
            if el.type == pygame.MOUSEBUTTONDOWN:
                pass
            # Window.update_input(el)

        Window.draw()

        pygame.display.update()
