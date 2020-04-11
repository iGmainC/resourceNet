from django.urls import path
from movie import views
urlpatterns = [
    path('',views.index),
    path('index/',views.index),
    path('postbox/',views.postbox)
    ]