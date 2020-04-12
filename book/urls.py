from django.urls import path
from book import views
urlpatterns = [
    path('',views.index),
    path('index/',views.index),
    path('postbox/',views.postbox)
    ]