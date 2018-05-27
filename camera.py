import cv2
from FaceRecognizer.Services.UserManager import UserManager


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.userManager=UserManager()
        self.last_frame=None;
        self._classificador = cv2.CascadeClassifier('frontalface.xml')
        self._altura = 220
        self._largura = 220
        self._font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self._lbphClassifier = cv2.face.LBPHFaceRecognizer_create()
        self._lbphClassifier.read('../FaceRecognizer/Dependencies/classifierLbph.yml')

    def __del__(self):
        self.video.release()
    
    # def get_frame(self):
    #
    #     imagem, frame = self.video.read()
    #
    #     imagem_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #
    #     faces_classificadas = self._classificador.detectMultiScale(imagem_cinza)
    #
    #     for x, y, l, a in faces_classificadas:
    #         cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
    #         self.last_frame = imagem_cinza[y:(y + a), x:(x + l)]
    #     ret, jpeg = cv2.imencode('.jpg', frame)
    #
    #     return jpeg.tobytes()

    def recognition(self):

        imagem, frame = self.video.read()

        imagem_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces_classificadas = self._classificador.detectMultiScale(imagem_cinza)

        for x, y, l, a in faces_classificadas:
            imagem_face = cv2.resize(imagem_cinza[y:(y + a), x:(x + l)], (self._largura, self._altura))

            cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 0, 255), 2)

            id, confianca = self._lbphClassifier.predict(imagem_face)

            if (id > 0):
                user = self.userManager.get_user_by_id(id)
                cv2.rectangle(frame, (x, y), (x + l, y + a), (0, 255, 0), 2)
                cv2.putText(frame, str(id), (x, y + (a + 30)), self._font, 2, (0, 255, 0))
                cv2.putText(frame, user.get_name(), (x, y + (a + 50)), self._font, 2, (0, 255, 0))

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode sssit into JPEG in order to correctly display the
        # video stream.


