import json
import os.path

class FileOps:
    '''
        {
            id: 1,
            entries: [
                "2018-08-24T00:00:00Z": 45,
                "2018-08-24T00:15:00Z": 43,
                "2018-08-24T00:30:00Z": 43
            ]
        }
    '''

    datafile = './energy_usage.json'

    @staticmethod
    def save_entry(new_entry):

        json_file = open(FileOps.datafile, 'r+')
        try:
            data = json.load(json_file)
            data['entries'].append(new_entry)
        except:
            data = {'entries': [new_entry]}
        json.dump(json.dumps(data), json_file)
        json_file.close()

    @staticmethod
    def read():
        try:
            with open(FileOps.datafile, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return ''
