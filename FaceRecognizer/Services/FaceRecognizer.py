"""Classe responsável por lidar com as dependências fundamentais ao processo de reconhecimento facial."""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import cv2
from FaceRecognizer.Services.FileManager import FileManager

class FaceRecognizer(object):

    """Variável=
    _fileManager: Serviço responsável por gerenciar os arquivos do sistema – FaceRecognizer.Services.FileManager"""

    _fileManager = FileManager()

    def __init__(self, radius=5, neighbours=10, grade_x=8, grade_y=8, threshold=110):

        """Instanciar o objeto de FaceRecognizer.

        Parâmetros= radius: valor equivalente ao raio ao redor do pixel central – Float;
                    neighbours: quantidade mínima de vizinhos a serem verificados – Inteiro;
                    grade_x: valor referentes ao número de célucas na horizontal – Default: 8;
                    grade_y: valor referentes ao número de célucas na vertical – Default: 8;
                    threshold: valor passado para garantir maior credibilidade ao processo de reconhecimento facial – Inteiro – Default: 110."""

        self._lbphClassifier = cv2.face.LBPHFaceRecognizer_create(radius, neighbours, grade_x, grade_y, threshold)

    def trainining(self):

        """Método responsável por treinar o arquivo classifierLbph.yml, caso não exista, ou, do contrário, por atualizar as informações"""

        if(self._fileManager.is_valid_yml()==True):
            self.update_classifier_lbph()
        else:
            self.train_classifier_lbph()

    def update_classifier_lbph(self):

        """Atualizar as informações contidas no arquivo classifierLbph.yml"""

        self._ids, self._faces = self._fileManager.get_ids_faces()
        self._lbphClassifier.read('FaceRecognizer/Dependencies/classifierLbph.yml')
        self._lbphClassifier.update(self._faces, self._ids)
        self._lbphClassifier.write('FaceRecognizer/Dependencies/classifierLbph.yml')

    def train_classifier_lbph(self):

        """Treinar o arquivo classifierLbph.yml"""

        self._ids, self._faces = self._fileManager.get_ids_faces()
        self._lbphClassifier.train(self._faces, self._ids)
        self._lbphClassifier.write('FaceRecognizer/Dependencies/classifierLbph.yml')