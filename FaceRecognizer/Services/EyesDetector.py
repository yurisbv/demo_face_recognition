"""Classe responsável pela detecção dos olhos."""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2

class EyesDetector():
    _haarCascadeLeftEye = 'FaceRecognizer/Dependencies/lefteye.xml'
    _haarCascadeRightEye = 'FaceRecognizer/Dependencies/righteye.xml'
    _grayLeftEye = None
    _grayRightEye = None

    def __init__(self):
        """Instancia um objeto do tipo EyesDetector.

        Ao fazer isso, preenchem-se os seguintes campos:

        self._classifierLeftEye = define o classificador do olho esquerdo;
        self.classifierRightEye = define o classificador do olho direito."""

        self._classifierLeftEye = cv2.CascadeClassifier(self._haarCascadeLeftEye)
        self._classifierRightEye = cv2.CascadeClassifier(self._haarCascadeRightEye)

    def validation_eyes(self, face):

        """Valida a presença de olhos na face capturada.

        Parâmetro = face: face capturada."""

        self.detect_left_eye(face)
        self.detect_right_eye(face)
        left_eye=self.get_left_eye(face)
        right_eye=self.get_right_eye(face)
        if(left_eye!=() and right_eye!=()):
            return True
        return False

    def detect_left_eye(self, face):

        """Detecta o olho esquerdo.

        Parâmetro= face: face capturada pelo OpenCV."""

        self._grayLeftEye=self._classifierLeftEye.detectMultiScale(face)

    def detect_right_eye(self, face):

        """Detecta o olho direito.

        Parâmetro= face: face capturada pelo OpenCV."""

        self._grayRightEye=self._classifierRightEye.detectMultiScale(face)

    def get_left_eye(self, face):

        """Define e retorna a área que compreende o olho esquerdo.

        Parâmetro= face: face capturada pelo OpenCV."""

        for ox, oy, ol, oa in self._grayLeftEye:
            left_eye=face[oy:(oy + oa), ox:(ox + ol)]
            return left_eye

    def get_right_eye(self, face):

        """Define e retorna a área que compreende o olho direito.

        Parâmetro= face: face capturada pelo OpenCV."""

        for ox, oy, ol, oa in self._grayRightEye:
            right_eye=face[oy:(oy + oa), ox:(ox + ol)]
            return right_eye