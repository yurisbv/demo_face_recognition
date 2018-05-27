"""Classe que possibilita instanciar um Usuário do sistema."""

__author__="Jefferson Luis e Yuri Soares"
__version__="1.0"
__email__="jefferson16luis@hotmail.com / yurisbv@gmail.com"

class User(object):

    def set_name(self, name):
        """adicionar o nome do usuário.

        Parâmetros= name: nome do usuário."""

        self._name=name

    def set_id(self, id):
        """adicionar o id do usuário.

        Parâmetros= id: id do usuário."""

        self._id=id

    def set_create_at(self, create_at):
        """adicionar o momento de criação do usuário.

        Parâmetros= create_at: momento em que o usuário foi criado."""

        self._create_at=create_at

    def set_last_change(self, last_change):
        """adicionar o momento em que o usuário foi alterado.

        Parâmetros= last_change: momento em que o usuário foi alterado."""

        self._last_change=last_change

    def get_name(self):
        """Retornar o nome do usuário"""

        return self._name

    def get_id(self):
        """Retornar o id do usuário"""
        return self._id

    def get_create_at(self):
        """Retornar a data de criação do usuário"""
        return self._create_at

    def get_last_change(self):
        """Retornar a data de alteração do usuário"""
        return self._last_change

    def get_json(self):
        """Retornar o nome e o id do usuário como json"""
        obj = {'id': self._id, 'name': self._name}
        return obj


