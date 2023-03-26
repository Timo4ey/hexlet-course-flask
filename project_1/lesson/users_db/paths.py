import os
import json


class Paths:
    def __init__(self) -> None:
        self.dir = os.path.abspath(__file__)

    def set_cur_dir(self):
        self.dir = os.path.dirname(__file__)

    @classmethod
    def read_json(cls):
        path = os.path.join(os.path.dirname(__file__), 'data/users.json')
        with open(path, 'r') as f:
            return json.loads(f.read())

    def get_data_dir(self):
        return os.path.join(self.dir, 'data')

    def check_file(self):
        directory = self.get_data_dir()
        check_dir = os.listdir(directory)
        if not check_dir:
            with open(f'{directory}/users.json', 'w') as f:
                f.write({})
