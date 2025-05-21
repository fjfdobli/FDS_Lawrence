from django.contrib import admin
from .models import *

admin.site.register(DormBuilding)
admin.site.register(Room)
admin.site.register(Student)
admin.site.register(RoomAssignment)
admin.site.register(PaymentType)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(MaintenanceLog)
admin.site.register(MaintenanceRequest)