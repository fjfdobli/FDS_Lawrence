from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/students/add/', views.add_student, name='add_student'),
    path('api/students/<str:student_id>/', views.get_student, name='get_student'),
    path('api/students/<str:student_id>/update/', views.update_student, name='update_student'),
    path('api/students/<str:student_id>/delete/', views.delete_student, name='delete_student'),
    path('api/rooms/assign/', views.assign_room, name='assign_room'),
    path('api/rooms/available/', views.get_available_rooms, name='get_available_rooms'),
    path('api/rooms/<str:room_id>/', views.get_room, name='get_room'),
    path('api/rooms/<str:room_id>/update/', views.update_room, name='update_room'),
]