"""Classe responsável pelo gerenciamento dos arquivos do sistema"""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

import codecs
import os
import cv2
import numpy as np
import re


class FileManager(object):

    def create_directory(self, user):

        """Criar a pasta que armazenará os dados dos usuários cadastrados.
        O nome da pasta de cada utilizador será o próprio id.
        Caso a pasta users não exista, este método fará a sua criação.


        Parâmetros: User = Usuário."""

        if os.path.isdir('FaceRecognizer/users'):
           os.makedirs( 'FaceRecognizer/users/' + str(user.get_id()))
        else:
            os.makedirs('FaceRecognizer/users')
            os.makedirs('FaceRecognizer/users/' + str(user.get_id()))

    def delete_directory(self, id):

        """Excluí todas as informações do usuário, através do id passado.

        Parâmetros= id: id do usuário."""

        self.clear_photos(id)
        os.remove('FaceRecognizer/users/' + str(id) + '/' + str(id) + '.txt')
        os.removedirs('FaceRecognizer/users/' + str(id))
        self.remove_user_in_users_text(id)

    def is_valid_directory(self, user):

        """Verifica a existência do diretório referente ao usuário passado por parâmetro.

        Parâmetros= User: Usuário.

        Retorno= True: Pasta do usuário não criada.
                 False: Pasta do usuário já criada."""

        if os.path.isdir('FaceRecognizer/users/' + str(user.get_id())):
            return False
        return True

    def is_valid_yml(self):

        """Verifica se o arquivo com a extensão .yml já foi criado.

        Retorno= True: Se o arquivo .yml existir.
                 False: Se o arquivo .yml não existir."""

        path = [os.path.join('FaceRecognizer/Dependencies', f) for f in os.listdir('FaceRecognizer/Dependencies')]
        for yml in path:
            if 'yml' in yml:
                return True

        return False

    def generate_user_info_text(self, id_user, name, create_at_user, last_change=''):

        """Cria ou atualiza o arquivo com a extensão .txt responsável por armazenar todas as informações referentes ao usuário.

        Parâmetros= id_user: id do usuário;
                    name: nome do usuário;
                    create_at_user: data de criação do usuário;
                    last_change: data de modificação do usuário."""

        with codecs.open( 'FaceRecognizer/users/' + str(id_user) + '/' + str(id_user) + '.txt', 'w', encoding='utf-8') as file:
            text = str(id_user) + '\n' + \
                   name + '\n' + \
                   str(create_at_user) + '\n' + \
                   str(last_change)
            file.write(text)
            file.close()


    def generate_all_users_text(self, id_user):

        """Cria ou atualiza o arquivo com extensão .txt responsável por armazenar todos os ids dos usuários cadastrados no sistema.

        Parâmetros= id_user: id do usuário."""

        try:
            self.update_all_users_txt(id_user)
        except IOError:
            self.write_all_users_txt(id_user)

    def update_all_users_txt(self, id_user):

        """Atualiza o arquivo com extensão .txt responsável por armazenar todos os ids dos usuários cadastrados no sistema.

        Parâmetros= id_user: id do usuário."""

        file = open('FaceRecognizer/users/users.txt', 'r')
        text = file.readlines()
        text.append(str(id_user) + '\n')
        file = open('FaceRecognizer/users/users.txt', 'w')
        file.writelines(text)
        file.close()

    def write_all_users_txt(self, id_user):

        """Cria o arquivo com extensão .txt responsável por armazenar todos os ids dos usuários cadastrados no sistema.

        Parâmetros= id_user: id do usuário."""

        file = open('FaceRecognizer/users/users.txt', 'w')
        text = str(id_user) + '\n'
        file.write(text)
        file.close()

    def remove_user_in_users_text(self, id_user):

        """Remove o id do usuário do arquivo com a extensão .txt responsável por armazenar os ids dos usuários cadastrados no sistema.

        Parâmetros= id_user: id do usuário."""

        try:
            file = open('FaceRecognizer/users/users.txt', 'r')
            text = file.readlines()
            new_text = self.rewrite_users_text(id_user, text, file)
            file = open('FaceRecognizer/users/users.txt', 'w')
            file.writelines(new_text)
        except IOError:
            print('no file')
            raise

    def rewrite_users_text(self, id_user, text, file):

        """Reescreve o arquivo com a extensão .txt responsável por armazenar os ids dos usuários cadastrados no sistema.

        Parâmetros= id_user: id do usuário;
                    text: conteúdo do arquivo a ser reescrito;
                    file: arquivo a ser alterado.

        Retorno= new_text: vetor de String com as informações do usuário atualizadas."""

        new_text = file.readlines()
        new_text.clear()
        for line in text:
            if (line == str(id_user) + '\n'):
                continue
            new_text.append(line)
        return new_text

    def read_user_info_text(self, id_user):

        """Lê as informações presentes no arquivo com a extensão .txt responsável por armazenar as informações do usuário.

        Parâmetros= id_user: id do usuário.

        Retorno= text: vetor de String com as informações do usuário."""

        text=[]
        with codecs.open('FaceRecognizer/users/' + str(id_user) + '/' + str(id_user) + '.txt', 'r', encoding='utf-8') as file:
            for line in file.readlines():
               text.append(line.replace('\n', ''))
            file.close()
            return text

    def read_all_users_text(self):

        """Lê o arquivo com a extensão .txt responsável por armazenar todos os ids dos usuários cadastrados.

        Retorno= text: vetor de String com as informações de todos os usuários registrados no sistema."""

        file = open('FaceRecognizer/users/users.txt', 'r')
        text = file.readlines()
        file.close()
        return text

    def get_last_id(self):

        """Retorna o último id cadastrado no sistema"""

        try:
            file = open('FaceRecognizer/users/users.txt', 'r')
            text = file.readlines()
            file.close()
            print(text[len(text)-1])
            return text[len(text)-1]
        except:
            return 0

    def save_image(self, image_faces, user):

        """Salva as imagens que contêm as faces dos usuários cadastrados na pasta de cada utilizador.

        Parâmetros= image_faces: Faces dos usuários
                    user: Usuário do sistema – FaceRecognizer.Entities.User"""

        for i, face in enumerate(image_faces):
            cv2.imwrite("FaceRecognizer/users/" + str(user.get_id()) + "/" + str(i) + ".jpg", face)

    def clear_photos(self, id):

        """Excluir todas as fotos do usuário cadastrado no sistema.

        Parâmetros= id: id do usuário."""

        userPath = [os.path.join('FaceRecognizer/users/'+str(id), p) for p in os.listdir('FaceRecognizer/users/'+str(id))]
        for image in userPath:
            if ('.txt' in image):
                continue
            os.remove(image)

    def get_faces(self, id):

        """Retorna todas as faces do usuários cadastrados no sistema

        Parâmetros= id: id do usuário."""

        faces=[]
        userPath = [os.path.join('FaceRecognizer/users/'+str(id), p) for p in os.listdir('FaceRecognizer/users/'+str(id))]
        for image in userPath:
            if ('.txt' in image):
                continue
            faces.append(image)

        return faces

    def get_ids_faces(self):

        "Retorna os ids e as faces de cada usuário cadastrado no sistema."

        ids=[]
        faces=[]
        usersPath = [os.path.join('FaceRecognizer/users', f) for f in os.listdir('FaceRecognizer/users')]

        for user in usersPath:
            if('.txt' in user):
                continue
            userPath = [os.path.join(user, p) for p in os.listdir(user)]
            id=self.generate_int_id(user)
            for image in userPath:
                # self.rotateImage(image, 90)
                if('.txt' in image):
                    continue
                image_face = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2GRAY)
                ids.append(id)
                faces.append(image_face)

        return np.array(ids), faces

    def generate_int_id(self, user):

        """Converte o nome da pasta do usuário em um valor inteiro.

        Paramêtros= user: nome da pasta do usuário.

        Retorno= id: identificador do usuário – Inteiro."""

        filtro = re.compile('([0-9]+)')
        string_id = filtro.findall(user)
        id=''.join(string_id)
        return int(id)

    # def rotateImage(image, angle):
    #     try:
    #         image_center = tuple(np.array(image.shape[1::-1]) / 2)
    #         rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    #         result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    #         return result
    #     except:
    #         print('erro ao rotacionar')
