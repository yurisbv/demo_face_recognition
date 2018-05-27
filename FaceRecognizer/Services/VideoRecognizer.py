"""Classe responsável por realizar o reconhecimento facial em vídeos com extensão aceita pelo OpenCV."""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2

import cv2.face

from FaceRecognizer.Services.FaceDetector import FaceDetector
from FaceRecognizer.Services.UserManager import UserManager

class VideoRecognizer(object):
    """Variáveis=
    _lbphClassifier: classificador do algoritmo LBPH responsável por reconhecer faces atravésdo arquivo YML salvo como: Depencencies/classifierLbph.yml – Default: None;
    _ids: lista com os identificadores dos usuários reconhecidos – Inteiro;
    _threshold_limit: Valor que garante a credibilidade do reconhecimento facial. Se a face for superior ao número dessa variável, o reconhecimento não será validado – Inteiro – Default: 110;
    _id_final: Identificador mais confiável ao término do processo de reconhecimento facial – Inteiro – Default: 0;
    _userManager: Controle do usuário – FaceRecognizer.Services.UserManager."""

    _lbphClassifier=None
    _ids=None
    _threshold_limit = 110
    _id_final = 0
    _userManager = UserManager()

    def __init__(self, threshold=110):
        """Instancia o objeto do tipo VideoRecognizer.

        Parâmetro= threshold: valor passado para ser comparado com o _threshold_limit – Inteiro – Default: 110.

        Ao fazer isso, preenchem-se os campos:

        _lbphClassifier: configura a variável para trabalhar com o algoritmo de reconhecimento facial LPBH;
        _set_threshold_limit: configura o valor do _threshold_limit;
        """

        try:
            self._lbphClassifier = cv2.face.LBPHFaceRecognizer_create()
            self._set_threshold_limit(threshold)
        except:
            print('error value')

    def recognizer(self, video, max_faces=50, min_faces=5, duration=None):

        """Método empregado para reconhecer as faces detectadas no vídeo.

        Parâmetros= video: endereço do arquivo de vídeo;
                    max_faces: quantidade máxima de faces reconhecidas – Inteiro – Default: 50;
                    min_faces: quantidade mínima de faces reconhecidas – Inteiro – Default: 5;
                    duration: duração do vídeo – Float – Default: None.


        Retorno= Caso haja algum erro no processo de reconhecimento facial ou no de detecção de faces, o método apenas terá a sua execução interrompida;
                 Caso o reconhecimento facial seja executado com sucesso, o método look_for_user será acionado."""

        try:
            self._faceDetection = FaceDetector(max_faces, min_faces, duration)
            image_faces=self._faceDetection.detect_video(video)
            if(image_faces==False):
                return
            return self.look_for_user(image_faces)
        except:
            print('Error to recognize user')
            return


    def look_for_user(self, image_faces):
        """Método responsável por identificar o usuário presente nas faces – image_faces.

        Parâmetro= image_faces: lista com as faces detectadas.

        Retorno= Em caso de existência do arquivo classifierLbpt.yml e do consequente reconhecimento do usuário, o retorno será o identificador da pessoa classificada;
                Caso não haja o arquivo classifierLbpt.yml, será exibia a mensagem 'Yml not found' e a execução do método será interrompida;
                Se houver o arquivo classifierLbpt.yml, mas o usuário não for reconhecido, o retorno será None."""
        try:
            self._lbphClassifier.read('FaceRecognizer/Dependencies/classifierLbph.yml')
            self._identify_user(image_faces)
            return self._id_final
        except:
            print('Yml not found')
            return

    def _identify_user(self, image_faces):

        """Realiza a identificação do usuário.

        Parâmetro= image_faces: lista com as faces detectadas."""

        self._process_face(image_faces)
        self._get_id_final()

    def _get_id_final(self):

        """Retorna o identificador pertencente ao usuário identificado com maior credibilidade.

        Retorno= Em caso de não identificação do usuário, o retorno será None.
                 Caso haja o usuário seja reconhecido, será retornado o valor do identificador."""

        if (self._id_final > 0):
            print(self._id_final)
            return self._id_final
        print('user not found')
        self._id_final=None

    def _process_face(self, image_faces):

        """Verifica se as faces passadas por parâmetro estão registradas no sistema.

        Parâmetro= image_faces: lista com as faces detectadas."""

        for face in image_faces:
            id, confianca = self._lbphClassifier.predict(face)
            print(confianca)
            self._validate_min_confianca_and_id_final(id, confianca)

    def _validate_min_confianca_and_id_final(self, id, confidence):

        """Verifica se o usuário foi identificado e preenche os valores de _threshold_limit e _id_final.

        Parâmetros= id: identificador do usuário reconhecido – Inteiro;
                    confidence: valor que garante a credibilidade do reconhecimento."""

        if (id > 0):
            if (self._threshold_limit > confidence):
                self._set_threshold_limit(confidence)
                self._set_id_final(id)
                print(id)

    def _set_id_final(self, id):

        """Preenche o valor de _id_final.

        Parâmetro= id: identificador do usuário reconhecido – Inteiro."""

        if id and isinstance(id, int):
            self._id_final=id

    def _set_threshold_limit(self, threshold):

        """Preenche o valor de _threshold_limit.

        Parâmetro= threshold: valor que garante a credibilidade do reconhecimento."""

        if id and isinstance(id, float):
            self._threshold_limit = threshold