# Generated by Django 5.1.4 on 2025-03-19 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DormBuilding',
            fields=[
                ('d_building_id', models.AutoField(primary_key=True, serialize=False)),
                ('building_name', models.CharField(max_length=100)),
                ('building_loc', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('maint_req_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_date', models.DateField()),
                ('request_desc', models.TextField()),
                ('request_status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('pay_method_id', models.AutoField(primary_key=True, serialize=False)),
                ('pay_method_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('pay_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_rent', models.BooleanField(default=False)),
                ('electricity', models.BooleanField(default=False)),
                ('water', models.BooleanField(default=False)),
                ('amenities', models.BooleanField(default=False)),
                ('pay_type_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=100)),
                ('l_name', models.CharField(max_length=100)),
                ('m_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=20)),
                ('birthdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceLog',
            fields=[
                ('m_log_id', models.AutoField(primary_key=True, serialize=False)),
                ('repair_type', models.CharField(max_length=100)),
                ('repair_desc', models.TextField()),
                ('repair_status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('repair_date', models.DateField()),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='dormitory.maintenancerequest')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Partial', 'Partial'), ('Complete', 'Complete')], default='Pending', max_length=20)),
                ('pay_date', models.DateField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.paymentmethod')),
                ('pay_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.paymenttype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.student')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_number', models.IntegerField()),
                ('floor', models.IntegerField()),
                ('room_type', models.CharField(max_length=50)),
                ('room_capacity', models.IntegerField()),
                ('room_item', models.CharField(blank=True, max_length=255)),
                ('room_status', models.CharField(choices=[('Available', 'Available'), ('Occupied', 'Occupied'), ('Maintenance', 'Maintenance')], default='Available', max_length=20)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.dormbuilding')),
            ],
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.room'),
        ),
        migrations.CreateModel(
            name='RoomAssignment',
            fields=[
                ('r_assign_id', models.AutoField(primary_key=True, serialize=False)),
                ('d_building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.dormbuilding')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dormitory.payment')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.student')),
            ],
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.student'),
        ),
    ]
