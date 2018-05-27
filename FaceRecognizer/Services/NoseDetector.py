"""Classe responsável pela detecção do nariz."""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2

class NoseDetector():
    _haarCascadeNose = 'FaceRecognizer/Dependencies/nose.xml'
    _grayNose = None

    def __init__(self):

        """Instancia um objeto do tipo NoseDetector.

        Ao fazer isso, preenche-se o seguinte campo:

        self._classifierNose = define o classificador do nariz."""

        self._classifierNose = cv2.CascadeClassifier(self._haarCascadeNose)

    def validation_nose(self, face):

        """Valida a presença de nariz na face capturada.

        Parâmetro = face: face capturada pelo OpenCV."""

        self.detect_nose(face)
        nose=self.get_nose(face)
        if(nose!=()):
            return True
        return False

    def detect_nose(self, face):

        """Detecta o nariz.

        Parâmetro= face: face capturada pelo OpenCV."""

        self._grayNose=self._classifierNose.detectMultiScale(face)

    def get_nose(self, face):

        """Define e retorna a área que compreende o nariz.

        Parâmetro= face: face capturada pelo OpenCV."""

        for mx, my, ml, ma in self._grayNose:
            nose=face[my:(my + ma), mx:(mx + ml)]
            return nose