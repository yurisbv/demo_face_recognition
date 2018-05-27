"""Classe responsável por configurar a câmera utilizada nos processos de detecção e reconhecimento facial"""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2

class CameraService(object):
    """Variáveis=
    frame: imagem vetorial capturada pela câmera e processada pelo OpenCV;
    gray_image: frame em escala de cinza;
    image: boolean que valida o frame capturado."""

    gray_image=None
    frame=None
    image=None

    def __init__(self, cam=None):

        """Instancia um objeto do tipo CameraService

        Parâmetro= cam: tipo de câmera utilizado."""

        self.set_cam(cam)

    def set_cam(self, cam):

        """Adicionar camera ao método VideoCapture, que permite a captura de imagens através do dispositivo de registor de imagens indicado.

        Parâmetro= cam: tipo de câmera utilizado."""

        if (cam == None):
            self.cam = cv2.VideoCapture(0)
        else:
            self.cam = cv2.VideoCapture(cam)

    def read(self):

        """Capturar imagem – frame – e, via OpenCv, convertê-la para cinza.

        A variável image indica a validade do frame capturado."""

        if (self.cam.isOpened() == True):
            self.image, self.frame = self.cam.read()

            self.gray_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def stop_cam(self):

        """Parar a câmera e limpar a câmera instanciada."""

        if(self.cam!=None):
            self.cam.release()
            cv2.destroyAllWindows()