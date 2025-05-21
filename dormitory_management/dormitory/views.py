from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.db.models import Count
import datetime

def dashboard(request):
    """Main dashboard view"""
    buildings_count = DormBuilding.objects.count()
    rooms_count = Room.objects.count()
    students_count = Student.objects.count()
    maintenance_count = MaintenanceRequest.objects.filter(request_status='Pending').count()
    
    rooms = Room.objects.select_related('building').all()
    students = Student.objects.all()
    maintenance_requests = MaintenanceRequest.objects.select_related('room', 'student', 'room__building').all()
    payments = Payment.objects.select_related('student', 'pay_type', 'pay_method').all()
    
    context = {
        'buildings_count': buildings_count,
        'rooms_count': rooms_count,
        'students_count': students_count,
        'maintenance_count': maintenance_count,
        'rooms': rooms,
        'students': students,
        'maintenance_requests': maintenance_requests,
        'payments': payments,
    }
    
    return render(request, 'dormitory/index.html', context)

@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        student = Student.objects.create(
            f_name=data.get('firstName'),
            l_name=data.get('lastName'),
            m_name=data.get('middleName'),
            gender=data.get('gender'),
            email=data.get('email'),
            contact_number=data.get('contactNumber'),
            birthdate=data.get('birthdate')
        )
        
        return JsonResponse({
            'success': True,
            'student_id': student.student_id,
            'f_name': student.f_name,
            'l_name': student.l_name,
            'gender': student.gender,
            'contact_number': student.contact_number
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def assign_room(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        student_id = data.get('studentId').replace('S', '')
        building_id = data.get('buildingId').replace('B', '')
        room_id = data.get('roomId').replace('R', '')
        assignment_date = data.get('assignmentDate')
        payment_status = data.get('paymentStatus')
        
        student = Student.objects.get(student_id=student_id)
        building = DormBuilding.objects.get(d_building_id=building_id)
        room = Room.objects.get(room_id=room_id)
        
        room.room_status = 'Occupied'
        room.save()
        
        assignment = RoomAssignment.objects.create(
            student=student,
            d_building=building,
            room=room
        )
        
        return JsonResponse({'success': True, 'assignment_id': assignment.r_assign_id})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def get_available_rooms(request):
    if request.method == 'GET':
        building_id = request.GET.get('building_id')
        
        rooms = Room.objects.filter(
            building_id=building_id,
            room_status='Available'
        ).values('room_id', 'room_number', 'room_type')
        
        return JsonResponse({'rooms': list(rooms)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})