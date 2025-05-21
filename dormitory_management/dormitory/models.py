from django.db import models

class DormBuilding(models.Model):
    d_building_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=100)
    building_loc = models.CharField(max_length=255)
    
    def __str__(self):
        return self.building_name
    
class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    building = models.ForeignKey(DormBuilding, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    floor = models.IntegerField()
    room_type = models.CharField(max_length=50)
    room_capacity = models.IntegerField()
    room_item = models.CharField(max_length=255, blank=True)
    room_status = models.CharField(max_length=20, 
        choices=[
            ('Available', 'Available'),
            ('Occupied', 'Occupied'),
            ('Maintenance', 'Maintenance')
        ], 
        default='Available'
    )
    
    def __str__(self):
        return f"{self.building.building_name} - Room {self.room_number}"

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, 
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ]
    )
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    birthdate = models.DateField()
    
    def __str__(self):
        return f"{self.f_name} {self.l_name}"

class RoomAssignment(models.Model):
    r_assign_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    d_building = models.ForeignKey(DormBuilding, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.student} - {self.room}"

class PaymentMethod(models.Model):
    pay_method_id = models.AutoField(primary_key=True)
    pay_method_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.pay_method_name

class PaymentType(models.Model):
    pay_type_id = models.AutoField(primary_key=True)
    room_rent = models.BooleanField(default=False)
    electricity = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    amenities = models.BooleanField(default=False)
    pay_type_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        types = []
        if self.room_rent: types.append("Room Rent")
        if self.electricity: types.append("Electricity")
        if self.water: types.append("Water")
        if self.amenities: types.append("Amenities")
        return ", ".join(types) or "No type specified"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pay_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    pay_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, 
        choices=[
            ('Pending', 'Pending'),
            ('Partial', 'Partial'),
            ('Complete', 'Complete')
        ],
        default='Pending'
    )
    pay_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.student}"

class MaintenanceLog(models.Model):
    m_log_id = models.AutoField(primary_key=True)
    maintenance = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE, related_name='logs')
    repair_type = models.CharField(max_length=100)
    repair_desc = models.TextField()
    repair_status = models.CharField(max_length=20, 
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )
    repair_date = models.DateField()
    
    def __str__(self):
        return f"Maintenance Log {self.m_log_id}"

class MaintenanceRequest(models.Model):
    maint_req_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    request_date = models.DateField()
    request_desc = models.TextField()
    request_status = models.CharField(max_length=20, 
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )
    
    def __str__(self):
        return f"Maintenance Request {self.maint_req_id} - {self.room}"