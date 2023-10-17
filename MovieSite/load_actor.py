import json
import os
from searchbar.models import *

path = "./actor_json/"
file_list = os.listdir(path)

for file in file_list:
    f = open(path + file, encoding="utf-8")
    data = json.load(f)
    new_one = Actor(
        name = data["name"],
        introduction = data["intro"],
        picutre_src = data["pictures_index"],
        sex = data["sex"],
        star = data["star"],
        birthday = data["birthday"],
        birthplace = data["birthplace"], 
        url = data["url"],
    )
    new_one.save()