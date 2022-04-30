from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('studentLogin', views.studentLogin, name="studentLogin"),
    path('managerLogin', views.managerLogin, name="managerLogin"),
    path('instructorLogin', views.instructorLogin, name="instructorLogin"),
]