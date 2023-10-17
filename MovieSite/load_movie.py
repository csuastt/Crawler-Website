import json
import os
from searchbar.models import *

path = "./movie_json/"
file_list = os.listdir(path)
i = 0
for file in file_list:
    i += 1
    print(i)
    f = open(path + file, encoding="utf-8")
    data = json.load(f)
    new_one = Movie(
        name = data["name"],
        introduction = data["introduction"],
        picutre_src = data["pictures_index"],
        state = data["state"],
        language = data["language"],
        length = data["length"]
    )
    # 设置好评论
    comments = ''
    for comment in data["comments"]:
        if(comments == ''):
            comments = comment
        else:
            comments = comments + '\n' + comment
    new_one.comments = comments
    # 设置好演员字符串
    actors_name_str = ''
    for act in data["actors"]:
        if(actors_name_str == ''):
            actors_name_str = act[1]
        else:
            actors_name_str = actors_name_str + ' ' + act[1]
    new_one.actors_name_str = actors_name_str
    new_one.save()
    # 设置好演员与其关系的关系
    all_actors = Actor.objects.all()
    for act in data["actors"]:
        act_url = act[0]
        ok = False
        for actor in all_actors:
            if actor.url == act_url:
                ok = True
                new_one.actors.add(actor)
                break
        if(not ok):
            new_actor = Actor(name = act[1], url = act[0])
            new_actor.save()
            new_one.actors.add(new_actor)
    new_one.save()