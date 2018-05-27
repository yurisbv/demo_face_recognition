from FaceRecognizer.Services.FaceRecognizer import FaceRecognizer
from FaceRecognizer.Services.FileManager import FileManager
from FaceRecognizer.Services.UserManager import UserManager
from FaceRecognizer.Services.FaceDetector import FaceDetector
from FaceRecognizer.Services.VideoRecognizer import VideoRecognizer
from FaceRecognizer.Services.FaceRecognizer import FaceRecognizer

userManager = UserManager()

faceDetector = FaceDetector(maxfaces=50, minfaces=10)

# userManager.delete_user(12)

# userManager.create_user(4, 'Champs')
# # #
# userManager.create_user(5, 'Jefferson')
# # #
# userManager.create_user(17, 'Andressa')
#
videoRecognizer = VideoRecognizer()

faceRecognizer = FaceRecognizer()
#
# userManager.create_user(35, 'testando')
# usuario=userManager.get_user_by_id(17)
# # # # # #
# usuario=userManager.get_user_by_id(16)
# faceDetector.detect('andressa.avi', usuario, faceRecognizer)


#userManager.delete_user(4)


# fileManager = FileManager()
# #
# fileManager.get_images()

# faceRecognizer.trainining()
#
videoRecognizer.recognizer('reconhecedor09.avi', max_faces=50, min_faces=20)
# faceRecognizer.local_recognizer(userManager)

#if(file.is_valid_directory(user,'users')==True):
    #file.create_directory(user, 'users')
    #file.generate_user_info(user.get_id(), user.get_create_at(), 'users')
#else:
    #print('Não criou')

