"""Classe responsável pela detecção da boca."""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2

class MouthDetector():

    _haarCascadeMouth = 'FaceRecognizer/Dependencies/mouth.xml'
    _grayMouth = None

    def __init__(self):

        """Instancia um objeto do tipo MouthDetector.

        Ao fazer isso, preenche-se o seguinte campo:

        self._classifierMouth = define o classificador da boca."""

        self._classifierMouth = cv2.CascadeClassifier(self._haarCascadeMouth)

    def validation_mouth(self, face):

        """Valida a presença de boca na face capturada.

        Parâmetro = face: face capturada pelo OpenCV."""

        self.detect_mouth(face)
        mouth=self.get_mouth(face)
        if(mouth!=()):
            return True
        return False

    def detect_mouth(self, face):

        """Detecta a boca.

        Parâmetro= face: face capturada pelo OpenCV."""

        self._grayMouth=self._classifierMouth.detectMultiScale(face)

    def get_mouth(self, face):

        """Define e retorna a área que compreende a boca.

        Parâmetro= face: face capturada pelo OpenCV."""

        for mx, my, ml, ma in self._grayMouth:
            mouth=face[my:(my + ma), mx:(mx + ml)]
            return mouth