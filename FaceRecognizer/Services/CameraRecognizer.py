"""Classe responsável pelo uso de uma câmera no processo de Reconhecimento Facial"""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2
from FaceRecognizer.Services.UserManager import UserManager


class CameraRecognizer(object):
    def __init__(self):
        """Instanciar o objeto do tipo CameraRecognizer.

        Ao fazer isso, preenchem-se os seguintes campos:
        self._userManager = Controle do usuário – FaceRecognizer.Services.UserManager;
        self._height = Altura – valor numérico;
        self._width = Largura – valor numérico;
        self._font = tipo de fonte usado no preenchimento do nome e do identificador do usuário reconhecido;
        self._lbphClassifier = classificador de face que utiliza o algoritmo de reconhecimento facial LBPH. Só será preenchido se o arquivo .yml existir.
        """

        self.userManager=UserManager()
        self._classifier= cv2.CascadeClassifier('FaceRecognizer/Dependencies/frontalface.xml')
        self._height = 220
        self._width = 220
        self._font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self._lbphClassifier = cv2.face.LBPHFaceRecognizer_create()
        try:
            self._lbphClassifier.read('FaceRecognizer/Dependencies/classifierLbph.yml')
        except:
            print('No YML')
            self._lbphClassifier=None

    def recognition(self, cameraService, scaleFactor=1.1, minNeighbors=9, minSize=(140, 140)):

        """Identificar os usuários através de sua face.

        Parâmetros = cameraService: instância responsável por configurar a câmera empregada – FaceRecognizer.Services.CameraService;
                     scaleFactor: valor equivalente ao raio ao redor do pixel central – Float – Default: 1.1;
                     minNeighbors: quantidade mínima de vizinhos a serem verificados – Inteiro – Default: 9;
                     minSize: valores referentes aos números de célucas na horizontal e vertical, respectivamente – Default: (140, 140).

        Retorno = imagem reconhecida pelo OpenCv convertida em bytes, caso haja sucesso na excução do método. Se houver erro, nada será retornado."""

        try:

            cameraService.read()

            faces_classificadas = self._classifier.detectMultiScale(cameraService.gray_image, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)

            for x, y, l, a in faces_classificadas:
                imagem_face = cv2.resize(cameraService.gray_image[y:(y + a), x:(x + l)], (self._width, self._height))

                cv2.rectangle(cameraService.frame, (x, y), (x + l, y + a), (0, 0, 255), 2)

                id, confianca = self._lbphClassifier.predict(imagem_face)

                if (id > 0):
                    user = self.userManager.get_user_by_id(id)
                    cv2.rectangle(cameraService.frame, (x, y), (x + l, y + a), (0, 255, 0), 2)
                    cv2.putText(cameraService.frame, str(id), (x, y + (a + 30)), self._font, 2, (0, 255, 0))
                    cv2.putText(cameraService.frame, user.get_name(), (x, y + (a + 50)), self._font, 2, (0, 255, 0))

            ret, jpeg = cv2.imencode('.jpg', cameraService.frame)

            return jpeg.tobytes()
        except:
            cameraService.stop_cam()
            print('Erro ao carregar o reconhecimento facial')
            return


    def get_lbph_classifier(self):

        """retorna o classificador lbph"""

        return self._lbphClassifier



