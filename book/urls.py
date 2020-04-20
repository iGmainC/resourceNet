from django.urls import path
from book import views
urlpatterns = [
    path('',views.index,name="index"),
    path('index/',views.index),
    path('detail/<id>/',views.detail,name='detail'),
    path('postbox/',views.postbox),
    path('about/',views.about,name="about"),
    path('page=<int:page_num>/',views.page,name="page"),
    path("push/",views.push,name="push")
    ]
