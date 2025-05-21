from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/students/add/', views.add_student, name='add_student'),
    path('api/rooms/assign/', views.assign_room, name='assign_room'),
    path('api/rooms/available/', views.get_available_rooms, name='get_available_rooms'),
]