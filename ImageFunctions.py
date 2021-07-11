import cv2
import pygame
import os
import requests
import random
import string
from time import sleep
# from GUI import SEP as sep

sep = '/'

def __highlightface(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            # cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, faceBoxes


faceProto = "data/cv2data/opencv_face_detector.pbtxt"
faceModel = "data/cv2data/opencv_face_detector_uint8.pb"
ageProto = "data/cv2data/age_deploy.prototxt"
ageModel = "data/cv2data/age_net.caffemodel"
genderProto = "data/cv2data/gender_deploy.prototxt"
genderModel = "data/cv2data/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)


def take_gender_and_age(IMAGE):
    video = cv2.VideoCapture(IMAGE)
    padding = 20
    hasFrame, frame = video.read()
    resultImg, faceBoxes = __highlightface(faceNet, frame)
    if not faceBoxes:
        print("No face detected:", IMAGE)
        return None, None

    for faceBox in faceBoxes[0:1]:
        face = frame[max(0, faceBox[1] - padding):
                     min(faceBox[3] + padding, frame.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                    :min(faceBox[2] + padding, frame.shape[1] - 1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        # print(f'Gender: {gender}')

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        # print(f'Age: {age[1:-1]} years')

        return gender, age[1:-1]


# need update, specified to os
file_sep = '_'  # separator between name and second name

# Russian names and second names
Russian_male_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_names_male_hard.txt'
Russian_female_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_names_female_hard.txt'
Russian_male_second_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_second_names_male_hard.txt'
Russian_female_second_names_hard_file = 'data' + sep + 'Names' + sep + 'Russian' + sep + 'Russian_second_names_female_hard.txt'

# Photos directory
Photo_dir = 'data/Persons'

# url for persons
_url = 'https://thispersondoesnotexist.com/image'

# For functions usage
NEW_FILES = []


def generate_random_name(n):
    if n == 1:
        return random.choice(string.ascii_letters)
    else:
        return random.choice(string.ascii_letters) + generate_random_name(n - 1)


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


def take_photos_and_their_names_from_directory(folder, image_size=(200, 200)):
    """

    :param image_size: size in which photo will be shown in GUI
    :param folder: folder in which are target photos
    :return: dictionary type:  photo_name: pygame_photo_object

    Ideas to improvement:
    1) Some photos can have same name. This situation is needed to be fixed.
    2) Critical! Image needs to be scaled! *Solved*
    """

    photos_and_names = {}
    for photo in os.listdir(folder):
        name = photo[0:photo.rindex('.')]
        pygame_photo = pygame.image.load(folder + sep + photo)
        pygame_photo = pygame.transform.scale(pygame_photo, image_size)

        photos_and_names.update({name: pygame_photo})

    return photos_and_names


def put_some_photos_in_folder(folder_name, n, target_age=0, target_gender=0):
    """
    :param target_gender: can take 'Male' or 'Female' or 0
    :param target_age: can be '0-2', '4-6', '8-12', '15-20', '25-32', '38-43', '48-53', '60-100' or 0
    :param folder_name: target folder
    :param n:quantity of photos
    :return: None
    """
    _headers = {'User-Agent': 'Mozzila/5.0'}

    while n > 0:
        sleep(1.5)

        photo = requests.get(_url, headers=_headers).content
        filename = folder_name + sep + generate_random_name(8)

        file = open(filename, 'wb')
        file.write(photo)

        NEW_FILES.append(folder_name + sep + filename)
        file.close()
        if target_age == 0 and target_gender == 0:
            n -= 1
        else:
            destroy = False
            gender, age = take_gender_and_age(filename)
            if target_age != age and target_age != 0:
                destroy = True
            if target_gender != gender and target_gender != 0:
                destroy = True
            if destroy:
                os.remove(filename)
            else:
                n -= 1


def give_names_to_photos_in_folder(folder, difficult='hard', language='russian', mode='all'):
    """
    Uses function recognize_sex to recognize sex, and after that gives a
    random name and second name to a photo.

    :param mode: rename all files or only some of them
    :param language: language of new set
    :param difficult: types of names (casual or rare)
    :param folder: target folder
    :return: None
    """

    male_names = ['Jhon']
    male_second_names = ['Johnson']
    female_names = ['Joanna']
    female_second_names = ['Johnson']

    # name = 'Jhon'
    # second_name = "Johnston"

    if difficult == 'hard' and language == 'rus':
        male_names = take_text_data_from_file(Russian_male_names_hard_file)
        male_second_names = take_text_data_from_file(Russian_male_second_names_hard_file)
        female_names = take_text_data_from_file(Russian_female_names_hard_file)
        female_second_names = take_text_data_from_file(Russian_female_second_names_hard_file)

    for photo in os.listdir(folder) if mode == 'all' else NEW_FILES:
        gender, age = take_gender_and_age(folder + sep + photo) if mode == 'all' else take_gender_and_age(photo)

        if gender == 'Male':
            name = random.choice(male_names)
            second_name = random.choice(male_second_names)
        else:
            name = random.choice(female_names)
            second_name = random.choice(female_second_names)
        new_filename = name + file_sep + second_name

        os.rename(folder + sep + photo, folder + sep + new_filename + '.jpeg')


def generate_new_set(set_name, n, mode='new', difficult='hard', language='rus', age = 0, gender = 0):
    """
    :param gender: gender of new set (beta)
    :param age: target age for new set (beta)
    :param difficult: difficulty of new set
    :param language: language of set, can be 'rus' or 'eng'
    :param mode: new set or for addition. Can take values 'new' or 'addition'
    :param set_name -  name of new set, in which will be placed all of data
            n - quantity of new photos in this set
    :return: Nothing

    Creates a new folder(os.mkdir), then downloads some new photos (n, func - put_some_new_photos_in_folder)
    then gives them a name (func gives_names_to_photos_in_folder). Then process is finished.

    """
    folder = Photo_dir + sep + set_name
    destroy = False
    try:
        os.mkdir(folder)

    except:
        pass

    try:
        put_some_photos_in_folder(folder, n, target_age=age, target_gender=gender)
    except:
        destroy = True
        print('Error in put_some_photos_in_folder, line 246 ImageFunctions.py')

    try:
        give_names_to_photos_in_folder(folder, mode='all' if mode == 'new' else 'addition', language=language,
                                       difficult=difficult)
    except:
        print('Error in give_names_to_photos_in_folder, line 251 ImageFunctions.py')
        destroy = True

    if destroy:
        os.rmdir(folder)
        assert (ValueError('Something goes wrong, please, report this bug: https://github.com/hoksly/StudyFaces'))
        return False

    return True
