from django.urls import path
from . import views
from.views import home,add_student

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path("", home, name='home'),
    path("",views.index,name='index'),
    # path('index', views.index, name='index'),
    path("add-student/", add_student, name='add_student'),
    path('students/', views.view_students, name='view_students'),
    path('update-student/<int:id>/', views.update_student, name='update_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('report/<int:id>/',views.student_report,name='student_report'),
]