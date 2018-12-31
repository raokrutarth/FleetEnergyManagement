import json
import os



DATAFILE = os.path.abspath('./energy_usage.json')

class FileOps:

    @staticmethod
    def save_entry(new_entry):
        json_file = open(DATAFILE, 'a+')
        try:
            data = json.load(json_file)
            data['entries'].append(new_entry)
        except:
            data = {'entries': [new_entry]}
        json.dump(data, json_file)
        json_file.close()

    @staticmethod
    def read():
        try:
            with open(DATAFILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return ''
