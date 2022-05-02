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
    #add student
    path('managerHome/addStudentPage', views.addStudentPage, name="managerHome/addStudentPage"),
    path('managerHome/addStudent', views.addStudent, name="managerHome/addStudent"),
    #add instructor
    path('managerHome/addInstructorPage', views.addInstructorPage, name="managerHome/addInstructorPage"),
    path('managerHome/addInstructor', views.addInstructor, name="managerHome/addInstructor"),
    #delete student
    path('managerHome/deleteStudentPage', views.deleteStudentPage, name="managerHome/deleteStudentPage"),
    path('managerHome/deleteStudent', views.deleteStudent, name="managerHome/deleteStudent"),
    #view instructors
    path('managerHome/viewInstructorsPage', views.viewInstructorsPage, name="managerHome/viewInstructorsPage"),
    #view students
    path('managerHome/viewStudentsPage', views.viewStudentsPage, name="managerHome/viewStudentsPage"),
    #view grades
    path('managerHome/viewGradesPage', views.viewGradesPage, name="managerHome/viewGradesPage"),
    #view courses of instructor
    path('managerHome/viewCoursesInsPage', views.viewCoursesInsPage, name="managerHome/viewCoursesInsPage"),
    
    
    path('toy', views.toy, name="toy")
]
