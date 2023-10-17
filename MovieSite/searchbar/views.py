from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import django.contrib.auth as auth
from django.contrib import messages
from django.urls import reverse
from .models import Actor, Movie
import time
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.
from django.http import HttpResponse


def index(request):
    result = Movie.objects.all()
    total_number = len(result)
    movies = []
    for mov in result:
        movies.append([mov.name, mov.picutre_src, mov.id])
    paginator = Paginator(movies , 21)
    page = request.GET.get('page')
    try:
        res = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        res = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        res = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    # 决定页面渲染方式
    range_list = []
    if(res.paginator.num_pages > 7):
        if(res.number <= 4):
            range_list = list(range(1, res.number+3))
        elif(res.number >= res.paginator.num_pages - 3):
            range_list = list(range(res.number-2, res.paginator.num_pages+1))
        else:
            range_list = list(range(res.number-2, res.number+3))
    else:
        range_list = []
    context = {
        'all_movies': res,
        'Page': res,
        'range_list': range_list,
        'total_number': total_number,
        'keywords': "啊这就这不会吧不会吧",
        'limit': res.paginator.num_pages - 3
    }
    return render(request, 'result/result.html', context)


def actor(request):
    result = Actor.objects.all()
    total_number = len(result)
    actors = []
    for act in result:
        actors.append([act.name, act.picutre_src, act.id])
    paginator = Paginator(actors, 21)
    page = request.GET.get('page')
    try:
        res = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        res = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        res = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    # 决定页面渲染方式
    range_list = []
    if(res.paginator.num_pages > 7):
        if(res.number <= 4):
            range_list = list(range(1, res.number+3))
        elif(res.number >= res.paginator.num_pages - 3):
            range_list = list(range(res.number-2, res.paginator.num_pages+1))
        else:
            range_list = list(range(res.number-2, res.number+3))
    else:
        range_list = []
    context = {
        'all_actors': res,
        'Page': res,
        'range_list': range_list,
        'total_number': total_number,
        'keywords': "啊这就这不会吧不会吧",
        'limit': res.paginator.num_pages - 3
    }
    return render(request, 'result/result.html', context)


def find_result(request):
    keywords = request.POST.get('keywords')
    type = request.POST.get('search_type')
    if not keywords or not type:
        if type == 'Actors':
            return HttpResponseRedirect(reverse('actor'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('show_result', args=(keywords, type,)))


def show_result(request, keywords, type):
    # 搜索结果
    # 根据不同的类别进行搜索
    result = []
    start = time.perf_counter()
    keywords = keywords.strip()
    if(type == "Movies"):
        res_obj = Movie.objects.filter(
            Q(name__contains=keywords) |
            Q(actors_name_str__contains=keywords)
        )
        for text in res_obj:
            ind = text.actors_name_str.find(keywords)
            if ind >= len(text.actors_name_str) - 50:
                result.append((text.id, text.name, text.picutre_src, text.actors_name_str[-52:], "movie_detail"))
            else:
                if ind == -1:
                    ind += 1
                result.append((text.id, text.name, text.picutre_src, text.actors_name_str[ind:ind+50], "movie_detail"))
    elif(type == "Comments"):
        res_obj = Movie.objects.filter(
            Q(comments__contains=keywords)
        )
        for text in res_obj:
            comment = text.comments.replace("\n", " ")
            ind = comment.find(keywords)
            if ind >= len(comment) - 50:
                result.append((text.id, text.name, text.picutre_src, comment[-52:], "movie_detail"))
            else:
                if ind == -1:
                    ind += 1
                result.append((text.id, text.name, text.picutre_src, comment[ind:ind + 50], "movie_detail"))
    else:
        res_obj = Actor.objects.filter(
            Q(name__contains=keywords) |
            Q(movies_name_str__contains=keywords)
        )
        for text in res_obj:
            ind = text.movies_name_str.find(keywords)
            if ind >= len(text.movies_name_str) - 50:
                result.append((text.id, text.name, text.picutre_src, text.movies_name_str[-52:], "actor_detail"))
            else:
                if ind == -1:
                    ind += 1
                result.append((text.id, text.name, text.picutre_src, text.movies_name_str[ind:ind + 50], "actor_detail"))
    time_used = time.perf_counter() - start
    # 返回结果
    paginator = Paginator(result, 21)
    page = request.GET.get('page')
    try:
        res = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        res = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        res = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    # 决定页面渲染方式
    range_list = []
    if(res.paginator.num_pages > 7):
        if(res.number <= 4):
            range_list = list(range(1, res.number+3))
        elif(res.number >= res.paginator.num_pages - 3):
            range_list = list(range(res.number-2, res.paginator.num_pages+1))
        else:
            range_list = list(range(res.number-2, res.number+3))
    else:
        range_list = []
    context = {
        'num': len(result),
        'search_result': res,
        'Page': res,
        'range_list': range_list,
        'time_used': time_used,
        'keywords': keywords,
        'limit': res.paginator.num_pages - 3
    }
    return render(request, 'result/result.html', context)


def show_movie_detail(request, id_):
    try:
        movie = Movie.objects.get(id=id_)
    except BaseException:
        return HttpResponse('找不到该影片的信息')
    comments = movie.comments.split("\n")
    # 找到参演人员
    actor_name = []
    actor_picture_src = []
    actor_id = []
    for act in movie.actors.all():
        actor_name.append(act.name)
        actor_id.append(act.id)
        actor_picture_src.append(act.picutre_src)
    context = {
        'this_movie_name': movie.name,
        'introduction': movie.introduction,
        'picture_src': movie.picutre_src,
        'state': movie.state,
        'language': movie.language,
        'length': movie.length,
        'comments': comments,
        'actor': list(zip(actor_name, actor_id , actor_picture_src)),
    }
    return render(request, 'detail/detail.html', context)


def show_actor_detail(request, id_):
    try:
        actor = Actor.objects.get(id=id_)
    except BaseException:
        return HttpResponse('找不到该演员的信息')
    co_actors = actor.co_actors
    co_work_nums = actor.co_work_nums
    # 找出他的最高合伙10人
    co_list = co_actors.split(" ")
    actor_name = []
    actor_picture_src = []
    actor_id = []
    actor_num = []
    for aid in co_list:
        act = Actor.objects.get(id=aid)
        actor_name.append(act.name)
        actor_id.append(act.id)
        actor_picture_src.append(act.picutre_src)
    co_nums = co_work_nums.split(" ")
    for num in co_nums:
        actor_num.append(num)
    # 找到他参演的电影
    movie_name = []
    movie_picture_src = []
    movie_id = []
    for mov in actor.movie_set.all():
        movie_name.append(mov.name)
        movie_id.append(mov.id)
        movie_picture_src.append(mov.picutre_src)

    context = {
        'this_actor_name': actor.name,
        'introduction': actor.introduction,
        'picture_src': actor.picutre_src,
        'sex': actor.sex,
        'star': actor.star,
        'birthday': actor.birthday,
        'birthplace': actor.birthplace,
        'movie': list(zip(movie_name, movie_id, movie_picture_src)),
        'actor': list(zip(actor_name, actor_id, actor_picture_src, actor_num)),
    }
    return render(request, 'detail/detail.html', context)

