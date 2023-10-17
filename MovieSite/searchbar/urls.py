from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('actor/', views.actor, name='actor'),
    path('find/', views.find_result, name="find_result"),
    path('movie_detail/<str:id_>', views.show_movie_detail, name='show_movie_detail'),
    path('actor_detail/<str:id_>', views.show_actor_detail, name='show_actor_detail'),
    path('?keyword=<str:keywords>?type=<str:type>', views.show_result, name="show_result"),
]