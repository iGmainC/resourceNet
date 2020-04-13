from django.urls import path
from book import views
urlpatterns = [
    path('',views.index),
    path('index/',views.index),
    path('detail/<id>/',views.detail,name='detail'),
    path('postbox/',views.postbox)
    ]
