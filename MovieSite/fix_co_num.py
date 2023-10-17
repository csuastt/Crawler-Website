from searchbar.models import *

all_actors = Actor.objects.all()
i = 0
for actor in all_actors:
    i += 1
    print(i)
    movies = actor.movie_set.all()
    # 完善co_actors
    co_actors_dict = {}
    for mov in movies:
        movie_actors = mov.actors.all()
        for act in movie_actors:
            if(act.id == actor.id):
                continue
            if(act.id in co_actors_dict):
                co_actors_dict[act.id] += 1;
            else:
                co_actors_dict[act.id] = 1;
    print(co_actors_dict)
    co_list = []
    co_nums = []
    for tup in sorted(co_actors_dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True):
        co_list.append(str(tup[0]))
        co_nums.append(str(tup[1]))
        if(len(co_list) == 10):
            break
    co_actors = " ".join(co_list)
    co_work_nums = " ".join(co_nums)
    actor.co_actors = co_actors
    actor.co_work_nums = co_work_nums
    # 保存
    actor.save()