from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.db.models import Count
import datetime

def dashboard(request):
    """Main dashboard view"""
    # Always get fresh counts from database
    buildings_count = DormBuilding.objects.count()
    rooms_count = Room.objects.count()
    students_count = Student.objects.count()
    maintenance_count = MaintenanceRequest.objects.filter(request_status='Pending').count()
    
    # Get all data with related objects (efficient queries)
    buildings = DormBuilding.objects.all()
    rooms = Room.objects.select_related('building').all()
    students = Student.objects.all()
    maintenance_requests = MaintenanceRequest.objects.select_related('room', 'student', 'room__building').all()
    payments = Payment.objects.select_related('student', 'pay_type', 'pay_method').all()
    
    context = {
        'buildings_count': buildings_count,
        'rooms_count': rooms_count,
        'students_count': students_count,
        'maintenance_count': maintenance_count,
        'buildings': buildings,
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
        try:
            data = json.loads(request.body)
            
            student_id = data.get('studentId').replace('S', '')
            building_id = data.get('buildingId').replace('B', '')
            room_id = data.get('roomId').replace('R', '')
            assignment_date = data.get('assignmentDate')
            payment_status = data.get('paymentStatus')
            
            # Debug info
            print(f"Student ID: {student_id}, Building ID: {building_id}, Room ID: {room_id}")
            
            student = Student.objects.get(student_id=student_id)
            
            # Create building if it doesn't exist
            building, created = DormBuilding.objects.get_or_create(
                d_building_id=building_id,
                defaults={
                    'building_name': f'Building {building_id}',
                    'building_loc': 'Campus'
                }
            )
            
            # Check if room exists, create if not
            try:
                room = Room.objects.get(room_id=room_id)
            except Room.DoesNotExist:
                # Extract room number from room ID (assuming format like R001)
                room_number = int(room_id) % 100
                room = Room.objects.create(
                    room_id=room_id,
                    building=building,
                    room_number=room_number,
                    floor=1,
                    room_type="Single",
                    room_capacity=1,
                    room_status="Available"
                )
            
            # Set room status to Occupied
            room.room_status = 'Occupied'
            room.save()
            
            # Create assignment
            assignment = RoomAssignment.objects.create(
                student=student,
                d_building=building,
                room=room
            )
            
            return JsonResponse({'success': True, 'assignment_id': assignment.r_assign_id})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)})
    
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

@csrf_exempt
def get_room(request, room_id):
    room_id = room_id.replace('R', '')
    try:
        room = Room.objects.select_related('building').get(room_id=room_id)
        
        room_data = {
            'room_id': room.room_id,
            'building_name': room.building.building_name,
            'room_number': room.room_number,
            'floor': room.floor,
            'room_type': room.room_type,
            'room_capacity': room.room_capacity,
            'room_item': room.room_item,
            'room_status': room.room_status
        }
        
        return JsonResponse({'success': True, 'room': room_data})
    except Room.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Room not found'})

@csrf_exempt
def update_room(request, room_id):
    if request.method == 'POST':
        try:
            room_id = room_id.replace('R', '')
            room = get_object_or_404(Room, room_id=room_id)
            
            data = json.loads(request.body)
            
            room.room_number = data.get('roomNumber')
            room.floor = data.get('floor')
            room.room_type = data.get('roomType')
            room.room_capacity = data.get('roomCapacity')
            room.room_status = data.get('roomStatus')
            room.room_item = data.get('roomItems')
            
            room.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def get_student(request, student_id):
    student_id = student_id.replace('S', '')
    student = get_object_or_404(Student, student_id=student_id)
    
    student_data = {
        'student_id': student.student_id,
        'f_name': student.f_name,
        'l_name': student.l_name,
        'm_name': student.m_name,
        'gender': student.gender,
        'email': student.email,
        'contact_number': student.contact_number,
        'birthdate': student.birthdate.strftime('%Y-%m-%d')
    }
    
    return JsonResponse({'success': True, 'student': student_data})

@csrf_exempt
def update_student(request, student_id):
    if request.method == 'POST':
        try:
            student_id = student_id.replace('S', '')
            student = get_object_or_404(Student, student_id=student_id)
            
            data = json.loads(request.body)
            
            student.f_name = data.get('firstName')
            student.l_name = data.get('lastName')
            student.m_name = data.get('middleName')
            student.gender = data.get('gender')
            student.email = data.get('email')
            student.contact_number = data.get('contactNumber')
            student.birthdate = data.get('birthdate')
            
            student.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            student_id = student_id.replace('S', '')
            student = get_object_or_404(Student, student_id=student_id)
            
            # Check if student has room assignments and update room status
            assignments = RoomAssignment.objects.filter(student=student)
            for assignment in assignments:
                room = assignment.room
                room.room_status = 'Available'
                room.save()
            
            student.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})