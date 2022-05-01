from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #login urls
    path('studentIndex', views.studentIndex, name="studentIndex"),
    path('managerIndex', views.managerIndex, name="managerIndex"),
    path('instructorIndex', views.instructorIndex, name="instructorIndex"),
    path('studentLogin', views.studentLogin, name="studentLogin"),
    path('managerLogin', views.managerLogin, name="managerLogin"),
    path('instructorLogin', views.instructorLogin, name="instructorLogin"),
    #home page urls
    path('studentHome', views.studentHome, name="studentHome"),
    path('managerHome', views.managerHome, name="managerHome"),
    path('instructorHome', views.instructorHome, name="instructorHome"),
    #manager urls
    path('managerHome/addStudentPage', views.addStudentPage, name="managerHome/addStudentPage"),
    path('managerHome/addInstructorPage', views.addInstructorPage, name="managerHome/addInstructorPage"),
    path('managerHome/deleteStudentPage', views.deleteStudentPage, name="managerHome/deleteStudentPage"),
    
    path('managerHome/addStudent', views.addStudent, name="managerHome/addStudent"),
    path('managerHome/addInstructor', views.addInstructor, name="managerHome/addInstructor"),
    path('managerHome/deleteStudent', views.deleteStudent, name="managerHome/deleteStudent"),
    
    path('managerHome/viewInstructorsPage', views.viewInstructorsPage, name="managerHome/viewInstructorsPage"),
    
    
    path('toy', views.toy, name="toy")
]
