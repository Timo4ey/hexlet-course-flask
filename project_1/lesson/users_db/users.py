import json
from .paths import Paths


class Users:
    id = 0

    def __new__(cls, *args, **kwargs):
        cls.id += 1
        instance = super().__new__(cls)
        return instance

    def __init__(self, name, email) -> None:
        self.id = self.id
        self.name = name
        self.email = email

    def output(self):
        return {
                'id': self.id,
                'nickname': self.name,
                'email': self.email
                }

    @property
    def get_id(self):
        return self.id

    @get_id.setter
    def get_id(self, num):
        self.id = num


class UserMaker:
    def __init__(self, data: Users) -> None:
        self.data = data
        self.paths = Paths()
        self.path = self.paths.set_cur_dir()
        self.data_dir = self.paths.get_data_dir()
        self.file = None

    def read_json_file(self):
        directory = self.data_dir
        with open(f'{directory}/users.json', 'r') as f:
            file_ = f.read()
            if len(file_) == 0:
                return ''
            return json.loads(file_)

    def write_into_json(self, new_data):
        directory = self.data_dir
        with open(f'{directory}/users.json', 'w') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

    def gen_user(self):
        self.paths.check_file()
        out = self.data.output()
        filedata = self.read_json_file()

        if isinstance(filedata, dict | str):
            filedata = []
        filedata.append(out)
        self.write_into_json(filedata)
