"""Classe responsável por executar a detecção facial."""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2
import os
import datetime
import numpy as np

from moviepy.editor import VideoFileClip

from FaceRecognizer.Entities.User import User
from FaceRecognizer.Services.EyesDetector import EyesDetector
from FaceRecognizer.Services.FileManager import FileManager
from FaceRecognizer.Services.MouthDetector import MouthDetector
from FaceRecognizer.Services.NoseDetector import NoseDetector


class FaceDetector(object):
    """Variáveis=
    _haarcascade: arquivo .xml essencial para a detecção de faces;
    _maxfaces: valor máximo de faces a serem registrada pelo sistema – Inteiro – Default: 50;
    _minfaces: valor mínimo de faces a serem registrada pelo sistema – Inteiro – Default: 5;
    _duration: tempo limite de duração do vídeo – Float – Default: None;
    _video: arquivo de vídeo em formato válido pelo OpenCV – .AVI testado – Default: None;
    _classifier: Utiliza o _haarcascade para gerar um classificador responsável por identificar faces;
    _user: FaceRecognizer.Entities.User;
    _file_manager: FaceRecognizer.Services.FileManager;
    _eyeDetector: FaceRecognizer.Services.EyesDetector;
    _mouthDetector: FaceRecognizer.Services.MouthDetector;
    _noseDetector: FaceRecognizer.Services.NoseDetector;
    _faces: Vetor de faces detectadas pelo OpenCV;
    _last_frame: Último frame identificado pelo OpenCV;
    _jpeg: Imagem capturada pelo OpenCV convertida no formato JPG."""

    _haarCascade = 'FaceRecognizer/Dependencies/frontalface.xml'
    _maxfaces = 50
    _minfaces = 5
    _duration=None
    _video = None
    _classifier = None
    _user = User()
    _file_manager = FileManager()
    _eyeDetector = EyesDetector()
    _mouthDetector = MouthDetector()
    _noseDetector = NoseDetector()
    _faces=[]
    _last_frame=None
    _jpeg=None

    def __init__(self, maxfaces=50, minfaces=5, duration=None):

        """Instancia o objeto do tipo FaceDetector.

        Parâmetros: maxfaces: número máximo de faces – Inteiro – Default: 50;
                    minfaces: número mínimo de faces – Inteiro – Default: 5;
                    duration: duração máxima do vídeo – Float – Default: None.

        Ao fazer isso, preenchem-se os seguintes campos:

        _classifier = variável recebe o classificador do OpenCV através de passagem por parâmetro do _haarCascade;
        _set_min_faces = método responsável por definir o valor mínimo de faces detectadas no vídeo;
        _set_max_faces = método resposável por definir o valor máximo de faces detectadas no vídeo;
        _set_duration = método responsável por definir a duração máxima do vídeo."""

        self._classifier = cv2.CascadeClassifier(self._haarCascade)
        self._set_min_faces(minfaces)
        self._set_max_faces(maxfaces)
        self._set_duration(duration)

    def detect_video(self, video, user=None, faceRecognizer=None):
        """Método criado para detectar as faces válidas, através de vídeo aceito pelo OpenCV.

        Parâmetros= video: Arquivo de vídeo;
                    user: Usuário do sistema – FaceRecognizer.Entities.User;
                    faceRecognizer: Serviço responsável pelo reconhecimento facial – FaceRecognizer.Services.FaceRecognizer."""

        try:
            image_faces = []
            self._start_detection(video, user)
            while True:
                try:
                    image, frame = self._video.read()
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                except:
                    print('Vídeo inválido')
                    return False
                detected_face = self._detect_faces(frame_gray)

                if(detected_face!=()):
                    image_faces=self._add_image_faces(detected_face, image_faces, frame_gray)

                if len(image_faces) == self._maxfaces:
                    if(user!=None):
                        self.validate_image_faces_to_create(faceRecognizer, image_faces, user)
                        break
                    else:
                        image_faces=self._validate_image_faces_to_recognizer(image_faces)
                        return image_faces

            self._stop_video_process()
        except:
            print('Erro ao executar o método de detecção')

    def detect_camera(self, cameraService, scaleFactor=1.1, minNeighbors=9, minSize=(140, 140)):

        """Método criado para detectar faces através de câmera configurada no OpenCV e retornar a face detectada em forma de bytes.

        Parâmetros= cameraService: Serviço responsável por gerenciar o tipo de câmera a ser utilizado – FaceRecognizer.Services.CameraService;
                    scaleFactor: valor equivalente ao raio ao redor do pixel central – Float;
                    minNeighbors: quantidade mínima de vizinhos a serem verificados – Inteiro;
                    minSize: valores referentes aos números de célucas na horizontal e vertical, respectivamente.

        Retorno= Imagem .JPG convertida em bytes."""

        classified_faces = self.classifier_camera_faces(cameraService, scaleFactor, minNeighbors, minSize)

        if(classified_faces!=[]):
            frame=self.draw_rectangle_camera_faces(classified_faces, cameraService)

            ret, self._jpeg = cv2.imencode('.jpg', frame)

        return self._jpeg.tobytes()

    def classifier_camera_faces(self, cameraService, scaleFactor=1.1, minNeighbors=9, minSize=(140, 140)):

        """Método criado para detectar as faces classificadas pelo _classifier.

        Parâmetros= cameraService: Serviço responsável por gerenciar o tipo de câmera a ser utilizado – FaceRecognizer.Services.CameraService;
                    scaleFactor: valor equivalente ao raio ao redor do pixel central – Float;
                    minNeighbors: quantidade mínima de vizinhos a serem verificados – Inteiro;
                    minSize: valores referentes aos números de célucas na horizontal e vertical, respectivamente.

        Retorno= faces classificadas, caso o cameraService esteja em pleno funcionamento;
                 lista vazia, caso haja algum problema com o cameraService."""

        cameraService.read()

        if(cameraService.cam.isOpened()==True):
            classified_faces = self._classifier.detectMultiScale(cameraService.gray_image, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)

            return classified_faces
        return []

    def draw_rectangle_camera_faces(self, classified_faces, cameraService):

        """Desenhar um retângulo vermelho na face detectada.

        Parâmetros= classified_faces: faces classificadas pelo _classifier;
                    cameraService: Serviço responsável por gerenciar o tipo de câmera a ser utilizado – FaceRecognizer.Services.CameraService.

        Retorno= cameraService.frame: frame com o retângulo vermelho já desenhado."""

        for x, y, l, a in classified_faces:
            cv2.rectangle(cameraService.frame, (x, y), (x + l, y + a), (0, 0, 255), 2)
            self.set_last_frame(cameraService.gray_image[y:(y + a), x:(x + l)])
        return cameraService.frame


    def _start_detection(self, video, user):

        """Verifica a consistência dos valores de _minfaces e _maxfaces, preenche a variável user e invoca o método _set_video

        Parâmetros= video: video: Arquivo de vídeo;
                    user: Usuário do sistema – FaceRecognizer.Entities.User.

        Retorno= Caso haja inconsistência nos valores de _minfaces e _maxfaces, o método executará um retorno."""

        if (self._validate_number_of_faces(self._minfaces, self._maxfaces) == False):
            print('min>max')
            return
        else:
            self._user = user
            self._set_video(video)

    def validate_image_faces_to_create(self, faceRecognizer, image_faces, user):

        """Verifica se as faces capturadas não estão registradas no sistema e inicia o processo de salvamento de imagens através do método _prepare_to_save_faces.

        Parâmetros= faceRecognizer: Serviço responsável por gerenciar o reconhecimento facial – FaceRecognizer.Services.FaceRecognizer;
                    image_faces: Lista com todas as faces, em escala de cinza, capturadas do usuário pelo OpenCV;
                    user: Usuário do sistema – FaceRecognizer.Entities.User.

        Retorno= Caso as imagens já tenham sido registradas, executa um retorno."""

        if (faceRecognizer is not None and faceRecognizer.look_for_user(image_faces) is not None):
            print('Imagens já registradas')
            return
        self._prepare_to_save_faces(image_faces, user)


    def _validate_image_faces_to_recognizer(self, image_faces):

        """Verifica se as faces capturadas são superiores à quantidade mínima estipulada pela variável _minfaces.

        Parâmetros= image_faces: Lista com todas as faces, em escala de cinza, capturadas do usuário pelo OpenCV.

        Retorno= Caso o número de faces capturadas e validadas seja inferior ao valor da variável _minfaces, executa um retorno.
                 Caso Caso o número de faces capturadas e validadas seja superior ao valor da variável _minfaces, retorna image_faces."""

        image_faces = self._validation_face(image_faces)
        self._stop_video_process()
        if (len(image_faces) <= self._minfaces):
            print('faces inválidas')
            return

        return image_faces

    def _detect_faces(self, frame_gray, scaleFactor=1.1, minNeighbors=9, minSize=(140, 140)):

        """Recebe um frame em escala de cinza e verifica se há uma face nele.

        Parâmetros= frame_gray: frame capturado pelo OpenCV e convertido em escala de cinza;
                    scaleFactor: valor equivalente ao raio ao redor do pixel central – Float;
                    minNeighbors: quantidade mínima de vizinhos a serem verificados – Inteiro;
                    minSize: valores referentes aos números de célucas na horizontal e vertical, respectivamente.

        Retorno= face detectada pelo método _classifier.detectMultiScale – detected_face."""

        detected_face = self._classifier.detectMultiScale(frame_gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
        return detected_face

    def _transform_detected_face_in_face(self, frame_gray, detected_face):

        """Converte as dimensões do frame em escala de cinza em valores que delimitam a presença de face na área capturada.

        Parâmetros= frame_gray: frame capturado pelo OpenCV e convertido em escala de cinza;
                    detected_face: face detectada pelo OpenCV.

        Retorno= frame em escala de cinza convertido em face – frame_gray[y, x]"""

        for x, y, l, a in detected_face:
            return frame_gray[y:(y + a), x:(x + l)]

    def _validation_face_components(self, face):

        """Método responsável por validar a presença de olhos, boca e nariz na face capturada pelo OpenCV.

        Parâmetros= face: frame em escala de cinza convertido em face – frame_gray[y, x].

        Retorno= Caso todos os componentes da face sejam detectados, retorna True.
                 Caso não seja encontrado ao menos um componente da face, retorna False."""

        if(self._eyeDetector.validation_eyes(face) == True and self._mouthDetector.validation_mouth(face)==True and self._noseDetector.validation_nose(face)==True):
            return True
        else:
            return False

    def _validation_face(self, image_faces):

        """Elimina as faces repetidas das faces capturadas.

        Por faces repetidas, compreendem-se aqueças em que a posição é exatamente a mesma.

        Por exemplo, tentativa de gravar um vídeo de autenticação utilizando uma fotografia de um usuário validado no sistema.

        Parâmetros= image_faces: Lista com todas as faces, em escala de cinza, capturadas do usuário pelo OpenCV.

        Retorno= Lista com as imagens validadas por este método – new_image_faces."""

        try:
            count=0
            index=0
            new_image_faces=[]
            for face1 in self._faces:
                for face2 in self._faces:
                    if(np.all(face1==face2)):
                        count+=1
                if(count==1):
                    new_image_faces.append(image_faces[index])
                    index += 1
                count=0
        except:
            print('erro ao validar face' + ' ' + str(index))

        return new_image_faces

    def _add_image_faces(self, detected_face, image_faces, frame_gray):

        """Caso o frame em escala de cinza contenha todos os componentes de uma face, ele será adicionado a uma lista de faces.

        Parâmetros= detected_face: face detectada pelo OpenCV;
                    image_faces: Lista com todas as faces capturadas do usuário pelo OpenCV;
                    frame_gray: frame capturado pelo OpenCV e convertido em escala de cinza.

        Retorno= Lista com todas as faces em escala de cinza."""

        if (self._validation_face_components(self._transform_detected_face_in_face(frame_gray, detected_face))):
            self._faces.append(detected_face)
            image_faces.append(self._transform_detected_face_in_face(frame_gray, detected_face))

        return image_faces

    def _prepare_to_save_faces(self, image_faces, user):

        """Verifica se as faces capturadas estão aptas a serem salvas e executa, ou não, o armazenamento das imagens.

        Caso o fluxo principal seja cumprido, será exibida a mensagem: 'sucesso ao salvar faces'.

        Do contrário, o seguinte aviso será indicado: 'fracasso ao salvar faces'.

        Parâmetros= image_faces: Lista com todas as faces, em escala de cinza, capturadas do usuário pelo OpenCV;
                    user: Usuário do sistema – FaceRecognizer.Entities.User."""


        image_faces = self._validation_face(image_faces)
        if (len(image_faces) >= self._minfaces):
            self._file_manager.clear_photos(user.get_id())
            self._file_manager.save_image(image_faces, user)
            print('sucesso ao salvar faces')
        else:
            print('fracasso ao salvar faces')

    def _validate_number_of_faces(self, minfaces, maxfaces):

        """Verificia a validade dos valores de minfaces e maxfaces.

        Parâmetros= minfaces: quantidade mínima de faces – Inteiro;
                    maxfaces: quantidade máxima de faces – Inteiro.

        Retorno: Caso minfaces seja maior que maxfaces, retorna False.
                 Caso maxfaces seja maior que minfaces, retorna True."""

        if(minfaces > maxfaces):
            return False
        return True

    def _set_video(self, video):

        """Instanciar arquivo de vídeo ao OpenCV, caso a duração respeite o valor estipulado previamente em _duration.

        Este método também exibe a duração do vídeo.

        Parâmetro= video: Arquivo de vídeo."""

        videoClip=VideoFileClip(video)
        if(self._duration is None or videoClip.duration<=self._duration):
            self._video = cv2.VideoCapture(video)
        print(videoClip.duration)

    def _stop_video_process(self):

        """Limpar os registros do arquivo de vídeo do sistema."""

        self._video.release()
        cv2.destroyAllWindows()

    def _set_min_faces(self, minfaces):

        """Verifica a consistência de minfaces e preenche a variável _minfaces.

        Parâmetros= minfaces: quantidade mínima de faces – Inteiro."""

        if minfaces and isinstance(minfaces, int):
            self._minfaces=minfaces

    def _set_max_faces(self, maxfaces):

        """Verifica a consistência de maxfaces e preenche a variável _maxfaces.

        Parâmetros= maxfaces: quantidade máxima de faces – Inteiro."""

        if maxfaces and isinstance(maxfaces, int):
            self._maxfaces = maxfaces

    def _set_duration(self, duration):

        """Verifica a consistência de duration e preenche a variável _duration.

        Parâmetros= duration: duração máxima do vídeo – Float."""

        if duration is not None and duration and isinstance(duration, float):
            self._duration=duration

    def get_last_frame(self):

        """Retornar o último frame capturado pela câmera."""

        return self._last_frame

    def set_last_frame(self, frame):

        """Adiconar último frame capturado pela câmera à variável _last_frame.

        Parâmetros= frame: Último frame capturado pela câmera."""

        self._last_frame=frame