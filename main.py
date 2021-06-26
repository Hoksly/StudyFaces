import pygame
import os
from ImageFunctions import take_gender_and_age
import random


sep = '/' # need update, specified to os
file_sep = '_' # separator between name and second name

# Russian names and second names
Russian_male_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_names_male_hard.txt'
Russian_female_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_names_female_hard.txt'
Russian_male_second_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_second_names_male_hard.txt'
Russian_female_second_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_second_names_female_hard.txt'

# Photos directory
Photo_dir = 'data/Persons'


def take_text_data_from_file(filename):
    """
    Takes data from a file, especially names and second names.

    :param filename: file name
    :return: list of names or second names
    """

    file = open(filename, 'r')
    data = []

    while True:
        line = file.readline()
        if line == '':
            break
        data.append(line[0:-1])

    return data


def take_photos_and_their_names_from_directory(folder):
    """

    :param folder: folder in which are target photos
    :return: dictionary type:  photo_name: pygame_photo_object

    Ideas to improvement:
    1) Some photos can have same name. This situation is needed to be fixed.
    """

    photos_and_names = {}
    for photo in os.listdir(folder):
        name = photo[0:photo.rindex('.')]
        pygame_photo = pygame.image.load(folder + sep + photo)

        photos_and_names.update({name:pygame_photo})

    return photos_and_names


def put_some_photos_in_folder(folder_name, n):
    """
    :param folder_name: target folder
    :param n:quantity of photos
    :return: None
    """
    pass


def give_names_to_photos_in_folder(folder, diffiicult = 'hard', language = 'russian'):
    """
    Uses function recognize_sex to recognize sex, and after that gives a
    random name and second name to a photo.

    :param language: language of new set
    :param diffiicult: types of names (casual or rare)
    :param folder: target folder
    :return: None
    """

    male_names = ['Jhon']
    male_second_names = ['Johnson']
    female_names = ['Joanna']
    female_second_names = ['Johnson']

    #name = 'Jhon'
    #second_name = "Johnston"

    if diffiicult == 'hard' and language == 'russian':
        male_names = take_text_data_from_file(Russian_male_names_hard_file)
        male_second_names = take_text_data_from_file(Russian_male_second_names_hard_file)
        female_names = take_text_data_from_file(Russian_female_names_hard_file)
        female_second_names = take_text_data_from_file(Russian_female_second_names_hard_file)

    for photo in os.listdir(folder):
        gender, age = take_gender_and_age(folder + sep + photo)

        if gender == 'Male':
            name = random.choice(male_names)
            second_name = random.choice(male_second_names)
        else:
            name = random.choice(female_names)
            second_name = random.choice(female_second_names)
        new_filename = name + file_sep + second_name

        os.rename(folder + sep + photo, folder + sep + new_filename + '.jpeg')


def generate_new_set(set_name, n):
    """
    :param set_name -  name of new set, in which will be placed all of data
            n - quantity of new photos in this set
    :return: Nothing

    Creates a new folder(os.mkdir), then downloads some new photos (n, func - put_some_new_photos_in_folder)
    then gives them a name (func gives_names_to_photos_in_folder). Then process is finished.

    """

    return None