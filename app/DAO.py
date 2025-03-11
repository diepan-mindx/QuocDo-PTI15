import json as j
class DAO:
    root_path = 'data/'
    @classmethod
    def load_json_data(cls,entity_name):
        data = list()
        # mo file json
        file_path = cls.root_path + entity_name + '.json'
        with open(file_path, 'r') as json_file:
            # gan du lieu json
            data = j.load(json_file) # chuye du lieu tu json thanh python obj
        return data
    @classmethod
    def save_json_data(cls,entity_name, update_list):
        # ghi de du lieu json 
        file_path = cls.root_path + entity_name + '.json'
        with open (file_path, 'w') as  json_file:
            j.dump(update_list, json_file)
        print('successful writing!')
        