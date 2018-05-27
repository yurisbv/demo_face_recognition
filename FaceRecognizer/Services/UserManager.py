

from datetime import datetime

from FaceRecognizer.Entities.User import User
from FaceRecognizer.Services.FileManager import FileManager


class UserManager(object):

    file_manager = FileManager()

    def create_user(self, id, name):
        user = User()
        user.set_id(id)
        user.set_name(name)
        user.set_create_at(datetime.now())
        if not self.validate_user(user):
            print('usuário já existente')
            return False
        self.file_manager.create_directory(user)
        self.file_manager.generate_all_users_text(user.get_id())
        self.file_manager.generate_user_info_text(user.get_id(), user.get_name(), user.get_create_at())
        return user

    def validate_user(self, user):
        return self.file_manager.is_valid_directory(user)

    def get_user_by_id(self, id_user):
        try:
            user = User()
            text=self.file_manager.read_user_info_text(id_user)
            user.set_id(text[0])
            user.set_name(text[1])
            user.set_create_at(text[2])
            if len(text) == 4:
                user.set_last_change(text[3])
            return user
        except:
            print('User not found')

    def delete_user(self, id_user):
        self.file_manager.delete_directory(id_user)

    def edit_user_name(self, id_user, name='',):
        user = self.get_user_by_id(id_user)
        user.set_last_change(datetime.now())
        if name != '':
            user.set_name(name)
            self.file_manager.generate_user_info_text(user.get_id(), user.get_name(), user.get_create_at(), user.get_last_change())