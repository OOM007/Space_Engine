import json
import os

from Code import Engine_controle
from Code.Body_Functions import *

class Load:
    def load_file(self, file_name):
        a = os.path.split(os.getcwd())[0]
        os.listdir(a)
        f = open(file_name)
        data = json.load(f)
        f.close()
        return data

    def config_with_file(self, data, Engine, Camera):
        list_of_objects = []

        for d in data["planets"]:
            print(d)
            list_of_objects.append(Planet(d['Position'], d["Vector"], d["Mass"], d["type"], d["size"], d["ID"], Engine, Camera))

        if list_of_objects != None:
            print("File loaded successful")

        return list_of_objects

    def save_controle(self, planet_list, fileDirectory):
        savingFile = {
            "planets": [],
            "settings": []
        }

        for bodys in planet_list:
            bodyFile = {
                "Position": [bodys.position.x, bodys.position.y],
                "Vector": [-bodys.vector.x, -bodys.vector.y],
                "Mass": bodys.mass,
                "type": bodys.type,
                "size": bodys.size,
                "ID": bodys.ID}

            savingFile["planets"].append(bodyFile)

        with open(fileDirectory, "w") as fd:
            json.dump(savingFile, fd)