from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import os
# from GUI import SEP as sep
import string

sep = '/'
persons_data_dir = 'data' + sep + 'Persons'


def give_folder_name():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    return filename[0:filename.rindex(sep)]


def check_input(set_name, number_of_members, lang, age, gender, mode = 'new'):

    """

    :param set_name: name of future set
    :param number_of_members: number of photos in future set
    :param lang: language of set
    :param age: ? of people in set
    :param gender: gender of people in set
    :param mode: can be 'new' or 'addition'
    :return: set of bool for all of arguments, which means, that it should or not to be corrected,
            if all corrected, set of setting to create a new set
    """

    set_name_correct = False
    number_of_members_correct = True
    lang_correct = False
    age_correct = True
    gender_correct = False

    lang_ret = 'rus'
    age_ret = -1
    gender_ret = 0

    folders = os.listdir(persons_data_dir)
    if mode == 'new' and set_name not in folders:
        set_name_correct = True
        for el in set_name:
            if el not in string.printable:
                set_name_correct = False

    try:
        for el in str(number_of_members):
            if el not in string.digits:
                number_of_members_correct = False
    except TypeError:
        number_of_members_correct = False
    #print(lang, lang_correct)
    if lang in ('Rus', 'rus', 'RUS'):
        lang_ret = 'rus'
        lang_correct = True

    elif lang in ('Eng', 'ENG', 'eng'):
        lang_ret = 'eng'
        lang_correct = True
    # '(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)'
    #print(lang, lang_correct)
    try:
        for el in str(age):
            if el not in string.digits:
                age_correct = False
    except TypeError:
        age_correct = False

    if age_correct:
        age = int(age)
        if age in range(2):
            age_ret = '0-2'
        elif age in range(4, 6):
            age_ret = '4-6'
        elif age in range(4, 7):
            age_ret = '4-6'
        elif age in range(7, 14):
            age_ret = '8-12'
        elif age in range(14, 23):
            age_ret = '15-20'
        elif age in range(23, 35):
            age_ret = '25-32'
        elif age in range(35, 45):
            age_ret = '38-43'
        elif age in range(45, 60):
            age_ret = '45-53'
        elif age in range(60, 100):
            age_ret = '60-100'

        if gender in ('M', 'm', 'male', 'Male'):
            gender_correct = True
            gender_ret = 'm'
        elif gender in ('F', 'f', 'female', 'Female'):
            gender_correct = True
            gender_ret = 'f'
        elif gender == 0:
            gender_correct = True
            gender_ret = 0

        print(set_name_correct, number_of_members_correct, lang_correct, age_correct, gender_correct)
        print(set_name, int(number_of_members) if number_of_members_correct else 0, lang_ret, age_ret, gender_ret)
        return ((set_name_correct, number_of_members_correct, lang_correct, age_correct, gender_correct),
                (set_name, int(number_of_members) if number_of_members_correct else 0, lang_ret, age_ret if age_ret != -1 else 0, gender_ret))


