import os

BASE_PATH = "" #Path where the files are created
MAIN_FOLDER ="dblp" # Name of the folder


def checkMainFolder():
    '''
    create main folder, if non existent
    :return:
    '''
    return createFolder(BASE_PATH,MAIN_FOLDER)


def createFolder(path,name):
    '''
    creates folder if non existent
    :param path: path to folder
    :param name: name of folder
    :return: path of new folder
    '''
    main_path = os.path.join(path, name)
    os.makedirs(main_path, exist_ok=True)
    return main_path

def createFile(path,name):
    main_path = os.path.join(path, name)
