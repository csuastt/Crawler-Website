import json
import os

# path = r"./movie_json/"
path = r"./actor_json/"
file_list = os.listdir(path)
data_list = []
for file in file_list:
    f = open(path + file, encoding="utf-8")
    new_data = json.load(f)
    ok = True
    for data in data_list:
        if(
            # data["name"] == new_data["name"] and
            # data["introduction"] == new_data["introduction"] and
            # data["pictures_index"] == new_data["pictures_index"]
            data["url"] == new_data["url"]
        ):
            ok = False
            break
    f.close()
    if(ok):
        data_list.append(new_data)
    else:
        os.remove(path + file)
print(len(data_list))