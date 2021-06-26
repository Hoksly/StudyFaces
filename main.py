import pygame
import os
from ImageFunctions import take_gender_and_age

# global_data

# Is it right place to initialize it here?
Russian_names = []
American_names = []
American_second_names = []
Russian_second_names = []


def take_text_data_from_file(file):
    """
    Takes data from a file, especially names and second names.

    :param file: file name
    :return: list of names or second names
    """
    data = []

    return data


def take_photos_and_their_names_from_directory(folder):
    """

    :param folder: folder in which are target photos
    :return: dictionary type:  photo_name: pygame_photo_object

    Ideas to improvement:
    1) Some photos can have same name. This situation is needed to be fixed.
    """

    photos_and_names = {}

    return photos_and_names


def put_some_photos_in_folder(folder_name, n):
    """

    :param folder_name: target folder
    :param n:quantity of photos
    :return: Nothing
    """
    pass


def give_names_to_photos_in_folder(folder):
    """
    Uses function recognize_sex to recognize sex, and after that gives a
    random name and second name to a photo.

    :param folder: target folder
    :return: Nothing
    """

    '''  
    # Need to understand where initialize it  
    Russian_names = []
    American_names = []
    American_second_names = []
    Russian_second_names = []
    '''
    pass


def generate_new_set(set_name, n):
    """
    :param set_name -  name of new set, in which will be placed all of data
            n - quantity of new photos in this set
    :return: Nothing

    Creates a new folder(os.mkdir), then downloads some new photos (n, func - put_some_new_photos_in_folder)
    then gives them a name (func gives_names_to_photos_in_folder). Then process is finished.

    """

    return None