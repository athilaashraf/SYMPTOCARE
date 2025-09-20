from django.db import models

# Create your models here.
class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class hospital_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    hospitalname=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    post=models.CharField(max_length=100)
    latitude=models.FloatField()
    longitude=models.FloatField()
    logo=models.FileField()
    contact=models.BigIntegerField()
    email=models.CharField(max_length=100)

class doctor_table(models.Model):
    HOSPITAL=models.ForeignKey(hospital_table,on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    doctorname=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    image=models.FileField()
    place=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    post=models.CharField(max_length=100)




class user_table(models.Model):
    LOGIN=models.ForeignKey(login_table, on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    image=models.FileField()
    place=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    post=models.CharField(max_length=100)
    age=models.BigIntegerField()
    gender=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)

class department(models.Model):
    department_name=models.CharField(max_length=100)
    department_details=models.CharField(max_length=300)



class schedule_table(models.Model):
    DOCTOR=models.ForeignKey(doctor_table, on_delete=models.CASCADE)
    # doctor=models.CharField(max_length=100)
    # department=models.CharField(max_length=100)
    date=models.DateField()
    fromtime=models.CharField(max_length=10)
    totime=models.CharField(max_length=10)

class booking_table(models.Model):
    USER=models.ForeignKey(user_table, on_delete=models.CASCADE)
    SCHEDULE=models.ForeignKey(schedule_table, on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    time=models.TimeField()
    patientname = models.CharField(max_length=300,default='pending')
    age = models.CharField(max_length=300,default='pending')
    place = models.CharField(max_length=300,default='pending')
    token = models.CharField(max_length=300,default='pending')
    status = models.CharField(max_length=300,default='pending')


class prescription_table(models.Model):
    BOOKING=models.ForeignKey(booking_table,on_delete=models.CASCADE)
    prescription=models.CharField(max_length=300)
    medicine=models.CharField(max_length=300)
    instruction = models.CharField(max_length=300)
    duration = models.CharField(max_length=100)

class rating_table(models.Model):
    DOCTOR = models.ForeignKey(doctor_table, on_delete=models.CASCADE)
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    rating=models.CharField(max_length=100)
    review=models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()


class leave_table(models.Model):
    DOCTOR = models.ForeignKey(doctor_table, on_delete=models.CASCADE)
    reason=models.CharField(max_length=200)
    date=models.CharField(max_length=100)
    time=models.TimeField()


class disease_table(models.Model):
    DEPARTMENT=models.ForeignKey(department, on_delete=models.CASCADE)
    diseasename=models.CharField(max_length=1000)
    causes=models.CharField(max_length=1300)
    howtoprevent=models.CharField(max_length=1300)

class symptom_table(models.Model):
    DISEASE = models.ForeignKey(disease_table, on_delete=models.CASCADE)
    symptom=models.CharField(max_length=200)





class slot_table(models.Model):
    BOOKING = models.ForeignKey(booking_table, on_delete=models.CASCADE)
    tokenno=models.BigIntegerField()
    consultationtime=models.TimeField()