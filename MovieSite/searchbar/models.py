from django.db import models

# Create your models here.

from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    picutre_src = models.CharField(max_length=100)
    sex = models.CharField(max_length=20)
    star = models.CharField(max_length=20)
    birthday = models.CharField(max_length=20)
    birthplace = models.CharField(max_length=50)
    co_actors = models.CharField(max_length=500)
    co_work_nums = models.CharField(max_length=200, default="")
    movies_name_str = models.CharField(max_length=500, default="")
    url = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    定义存放影视资讯的model
    """
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    picutre_src = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    length = models.CharField(max_length=100)
    comments = models.TextField()
    actors = models.ManyToManyField(Actor)
    actors_name_str = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

