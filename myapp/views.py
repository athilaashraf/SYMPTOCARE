import json

import datetime

import pymysql
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render

# Create your views here.


from myapp.models import *
from myapp.myknn import prep


def login(request):
    return render(request,'index.html')

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    try:
        ob=login_table.objects.get(username=username,password=password)
        request.session['lid']=ob.id
        request.session['type']=ob.type
        if ob.type == 'admin':
            return HttpResponse('''<script>alert('admin logined successfully');window.location='/adminhome'</script>''')
        elif ob.type == 'hospital':
            return HttpResponse('''<script>alert('hospital login successfully');window.location='/hospitalhome'</script>''')
        elif ob.type == 'doctor':
            return HttpResponse('''<script>alert('doctor login successfully');window.location='/doctorhome'</script>''')
        elif ob.type == 'user':
            return HttpResponse('''<script>alert('user login successfully');window.location='/userhome'</script>''')
        else:
            return HttpResponse('''<script>alert(invalid);window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert(invalid);window.location='/'</script>''')


def adddiseaseinformation(request):
    # Check if doctor is logged in
    if 'lid' not in request.session or request.session.get('type') != 'doctor':
        return HttpResponse('''<script>alert("Please login as doctor");window.location='/'</script>''')
    
    ob = department.objects.all()
    return render(request, 'doctor/addinfo.html', {"val": ob})


def adddiseaseinformationpost(request):
    # Check if doctor is logged in
    if 'lid' not in request.session or request.session.get('type') != 'doctor':
        return HttpResponse('''<script>alert("Please login as doctor");window.location='/'</script>''')
    
    disease = request.POST["textfield"]
    causes = request.POST["textfield2"]
    dep = request.POST["dep"]
    hwtprvnt = request.POST["textfield3"]
    ob = disease_table()
    ob.DEPARTMENT = department.objects.get(id=dep)
    ob.diseasename = disease
    ob.causes = causes
    ob.howtoprevent = hwtprvnt
    ob.save()
    return HttpResponse('''<script>alert("added");window.location='/managediseaseinfo'</script>''')


def adminhome(request):
    return render(request,'admin/index.html')


def managediseaseinfo(request):
    # Check if doctor is logged in
    if 'lid' not in request.session or request.session.get('type') != 'doctor':
        return HttpResponse('''<script>alert("Please login as doctor");window.location='/'</script>''')
    
    a = disease_table.objects.all()
    return render(request, 'doctor/mngdiseaseinfo.html', {'data': a})


def searchdisease(request):
    # Check if doctor is logged in
    if 'lid' not in request.session or request.session.get('type') != 'doctor':
        return HttpResponse('''<script>alert("Please login as doctor");window.location='/'</script>''')
    
    diseasename = request.POST['textfield']
    ob = disease_table.objects.filter(diseasename__contains=diseasename)
    return render(request, 'doctor/mngdiseaseinfo.html', {'data': ob, 'diseasename': diseasename})


def editinfo(request, id):
    # Check if doctor is logged in
    if 'lid' not in request.session or request.session.get('type') != 'doctor':
        return HttpResponse('''<script>alert("Please login as doctor");window.location='/'</script>''')
    
    request.session["id"] = id
    ob = disease_table.objects.get(id=id)
    ob2 = department.objects.all()
    return render(request, 'doctor/editinfo.html', {'data': ob, 'val': ob2})


def editinfopost(request):
    # Check if doctor is logged in
    if 'lid' not in request.session or request.session.get('type') != 'doctor':
        return HttpResponse('''<script>alert("Please login as doctor");window.location='/'</script>''')
    
    ob = disease_table.objects.get(id=request.session["id"])
    ob.diseasename = request.POST["textfield"]
    ob.causes = request.POST["textfield2"]
    ob.howtoprevent = request.POST["textfield3"]
    if "dep" in request.POST:
        ob.DEPARTMENT = department.objects.get(id=request.POST["dep"])
    ob.save()
    return HttpResponse('''<script>alert("edited successfully");window.location='/managediseaseinfo'</script>''')

def deletedisease(request, id):
    # Check if doctor is logged in
    if 'lid' not in request.session or request.session.get('type') != 'doctor':
        return HttpResponse('''<script>alert("Please login as doctor");window.location='/'</script>''')
    
    request.session['did'] = id
    ob = disease_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("deleted");window.location='/managediseaseinfo'</script>''')


def editdisease(request,id):
    request.session["id"]=id
    ob=disease_table.objects.get(id=id)
    return render(request,'admin/editinfo.html',{'data':ob})


def accepthospital(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="hospital"
    ob.save()
    return HttpResponse('''<script>alert("accepted");window.location='/verifyhospital'</script>''')




def rejecthospital(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="hospital"
    ob.delete()
    return HttpResponse('''<script>alert("rejected");window.location='/verifyhospital'</script>''')



def unblockuser(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="user"
    ob.save()
    return HttpResponse('''<script>alert("unblocked");window.location='/viewusers'</script>''')

def blockuser(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="blocked"
    ob.save()
    return HttpResponse('''<script>alert("blocked");window.location='/viewusers'</script>''')




def verifyhospital(request):
    a=hospital_table.objects.all()
    return render(request,'admin/verifyhospital.html',{'data':a})

def searchhospital(request):
    hospitalname=request.POST['textfield']
    ob=hospital_table.objects.filter(hospitalname__contains=hospitalname)
    return render(request,'admin/verifyhospital.html',{'data':ob,'hospitalname':hospitalname})


def viewdoctors(request,id):
    request.session['aid']=id
    a=doctor_table.objects.filter(HOSPITAL_id=request.session['aid'])
    return render(request,'admin/viewdoctors.html',{'data':a})

def searchdoctor(request):
    doctorname=request.POST['textfield']
    ob=doctor_table.objects.filter(HOSPITAL_id=request.session['aid'],doctorname__icontains=doctorname)
    return render(request,'admin/viewdoctors.html',{'data':ob,'doctorname':doctorname})




def viewusers(request):
    a = user_table.objects.all()
    return render(request,'admin/viewusers.html',{'data':a})


def searchuser(request):
    username=request.POST['textfield']
    ob=user_table.objects.filter(username__contains=username)
    return render(request,'admin/viewusers.html',{'data':ob,'username':username})


def viewverifiedhospitals(request):
    a = hospital_table.objects.all()
    return render(request,'admin/viewverifiedhsptls.html',{"data":a})


def searchverifiedhospital(request):
    hospitalname=request.POST['textfield']
    ob=hospital_table.objects.filter(hospitalname__contains=hospitalname)
    return render(request,'admin/viewverifiedhsptls.html',{'data':ob,'hospitalname':hospitalname})




def and_editprofile(request):
    lid = request.POST['lid']
    fname = request.POST['fname']
    phonenumber = request.POST['phonenumber']
    email = request.POST['email']

    try:
        profile = user_table.objects.get(LOGIN_id=lid)
    except user_table.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})

    profile.name = fname
    profile.phone = phonenumber
    profile.Email = email

    if 'image' in request.FILES:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        profile.image = filename

    profile.save()
    return JsonResponse({'status': 'ok'})











# secondmodule

def register(request):
    return render(request,'hospital/register.html')


def registerpost(request):
    username=request.POST['textfield7']
    password=request.POST['textfield8']
    hospitalname=request.POST['textfield']
    place=request.POST['textfield2']
    pin = request.POST['textfield4']
    post = request.POST['textfield3']
    latitude = request.POST['textfield10']
    longitude = request.POST['textfield11']
    logo = request.FILES['file']
    fs=FileSystemStorage()
    fp=fs.save(logo.name,logo)
    contact = request.POST['textfield5']
    email = request.POST['textfield6']


    ob1=login_table()
    ob1.username=username
    ob1.password=password
    ob1.type='hospital'
    ob1.save()

    ob=hospital_table()
    ob.LOGIN=ob1
    ob.username=username
    ob.password=password
    ob.hospitalname=hospitalname
    ob.place=place
    ob.pin=pin
    ob.post=post
    ob.latitude=latitude
    ob.longitude = longitude
    ob.logo = fp
    ob.contact = contact
    ob.email=email
    ob.save()
    return HttpResponse('''<script>alert("register successfully");window.location='/'</script>''')













def hospitalhome(request):
    return render(request,'hospital/index.html')




def viewbooking(request):
    a=booking_table.objects.filter(SCHEDULE__DOCTOR__HOSPITAL__LOGIN_id=request.session['lid'])
    return render(request,'hospital/viewbooking.html',{'data':a})





def managedoctors(request):
    a=doctor_table.objects.filter(HOSPITAL__LOGIN_id=request.session['lid'])
    return render(request,'hospital/managedoctors.html',{'data':a})


# Department Management Functions
def managedepartments(request):
    """View all departments"""
    departments = department.objects.all()
    return render(request, 'hospital/managedepartments.html', {'data': departments})

def adddepartment(request):
    """Display add department form"""
    return render(request, 'hospital/adddepartment.html')

def adddepartmentpost(request):
    """Add new department"""
    dept_name = request.POST['department_name']
    dept_details = request.POST['department_details']
    
    # Check if department already exists
    if department.objects.filter(department_name=dept_name).exists():
        return HttpResponse('''<script>alert("Department already exists");history.back();</script>''')
    
    # Create new department
    dept = department()
    dept.department_name = dept_name
    dept.department_details = dept_details
    dept.save()
    
    return HttpResponse('''<script>alert("Department added successfully");window.location='/managedepartments'</script>''')

def editdepartment(request, id):
    """Edit department form"""
    request.session["dept_id"] = id
    dept = department.objects.get(id=id)
    return render(request, 'hospital/editdepartment.html', {'data': dept})

def editdepartmentpost(request):
    """Update department"""
    dept = department.objects.get(id=request.session["dept_id"])
    dept.department_name = request.POST["department_name"]
    dept.department_details = request.POST["department_details"]
    dept.save()
    return HttpResponse('''<script>alert("Department updated successfully");window.location='/managedepartments'</script>''')

def deletedepartment(request, id):
    """Delete department"""
    dept = department.objects.get(id=id)
    dept.delete()
    return HttpResponse('''<script>alert("Department deleted successfully");window.location='/managedepartments'</script>''')

def populate_departments(request):
    """Populate common medical departments - call this once to setup"""
    common_departments = [
        {"name": "Cardiology", "details": "Heart and cardiovascular diseases"},
        {"name": "Neurology", "details": "Brain and nervous system disorders"},
        {"name": "Orthopedics", "details": "Bone, joint, and muscle conditions"},
        {"name": "Pediatrics", "details": "Medical care for children"},
        {"name": "Dermatology", "details": "Skin, hair, and nail disorders"},
        {"name": "Psychiatry", "details": "Mental health and behavioral disorders"},
        {"name": "General Medicine", "details": "General medical conditions and primary care"},
        {"name": "Surgery", "details": "Surgical procedures and operations"},
        {"name": "Gynecology", "details": "Women's reproductive health"},
        {"name": "Ophthalmology", "details": "Eye and vision care"},
        {"name": "ENT", "details": "Ear, Nose, and Throat conditions"},
        {"name": "Radiology", "details": "Medical imaging and diagnostics"},
        {"name": "Emergency Medicine", "details": "Emergency and critical care"},
        {"name": "Anesthesiology", "details": "Anesthesia and pain management"},
        {"name": "Pathology", "details": "Disease diagnosis through lab tests"}
    ]
    
    created_count = 0
    for dept_data in common_departments:
        if not department.objects.filter(department_name=dept_data["name"]).exists():
            dept = department()
            dept.department_name = dept_data["name"]
            dept.department_details = dept_data["details"]
            dept.save()
            created_count += 1
    
    return HttpResponse(f'''<script>alert("{created_count} departments created successfully");window.location='/managedepartments'</script>''')

# Updated adddoctor function
def adddoctor(request):
    """Display add doctor form with departments"""
    doctors = doctor_table.objects.filter(HOSPITAL__LOGIN_id=request.session['lid'])
    departments = department.objects.all()
    
    # If no departments exist, create them automatically
    if not departments.exists():
        common_departments = [
            {"name": "Cardiology", "details": "Heart and cardiovascular diseases"},
            {"name": "Neurology", "details": "Brain and nervous system disorders"},
            {"name": "Orthopedics", "details": "Bone, joint, and muscle conditions"},
            {"name": "Pediatrics", "details": "Medical care for children"},
            {"name": "Dermatology", "details": "Skin, hair, and nail disorders"},
            {"name": "General Medicine", "details": "General medical conditions"},
            {"name": "Surgery", "details": "Surgical procedures"},
            {"name": "Gynecology", "details": "Women's reproductive health"},
            {"name": "ENT", "details": "Ear, Nose, and Throat conditions"}
        ]
        
        for dept_data in common_departments:
            dept = department()
            dept.department_name = dept_data["name"]
            dept.department_details = dept_data["details"]
            dept.save()
        
        # Refresh departments after creation
        departments = department.objects.all()
    
    return render(request, 'hospital/adddoctor.html', {'data': doctors, 'departments': departments})


def adddoctorpost(request):
    Username=request.POST["textfield"]
    Password=request.POST["textfield2"]
    registration_number=request.POST["textfield_reg"]
    doctorname=request.POST["textfield3"]
    department_id=request.POST["textfield4"]  # This is now department ID
    qualification=request.POST["textfield5"]
    image=request.FILES["file"]
    place = request.POST["textfield7"]
    pin = request.POST["textfield8"]
    post = request.POST["textfield9"]

    # Get department name from ID
    dept = department.objects.get(id=department_id)
    department_name = dept.department_name

    ob1=login_table()
    ob1.username=Username
    ob1.password=Password
    ob1.type='doctor'
    ob1.save()

    ob=doctor_table()
    ob.LOGIN=ob1
    ob.HOSPITAL=hospital_table.objects.get(LOGIN=request.session["lid"])
    ob.registration_number=registration_number
    ob.doctorname=doctorname
    ob.department=department_name  # Store department name
    ob.qualification=qualification
    ob.image=image
    ob.place=place
    ob.pin=pin
    ob.post=post
    ob.save()
    return HttpResponse('''<script>alert("added");window.location='/managedoctors'</script>''')






def deletedoctor(request,id):
    request.session['id']=id
    ob=login_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("deleted");window.location='/managedoctors'</script>''')



def editdoctor(request,id):
    request.session["id"]=id
    ob=doctor_table.objects.get(id=id)
    return render(request,'hospital/editdoctor.html.',{'data':ob})



def editdoctorpost(request):
    ob = doctor_table.objects.get(id=request.session["id"])

    if 'textfield6' in request.FILES:
        img=request.FILES["textfield6"]
        fs=FileSystemStorage()
        fsave=fs.save(img.name,img)
        ob.image = fsave

    ob.doctorname=request.POST["textfield3"]
    ob.department=request.POST["textfield4"]
    ob.qualification=request.POST["textfield5"]

    ob.place=request.POST["textfield7"]
    ob.pin=request.POST["textfield8"]
    ob.post=request.POST["textfield9"]
    ob.save()
    return HttpResponse('''<script>alert("edited successfully");window.location='/managedoctors'</script>''')





def manageschedule(request,id):
    request.session["docid"]=id
    a=schedule_table.objects.filter(DOCTOR=id)
    return render(request,'hospital/manageschedule.html',{'data':a})



def addschedule(request):
    return render(request,'hospital/addschedule.html')




def addschedulepost(request):

    date=request.POST["textfield3"]
    fromtime=request.POST["textfield4"]
    totime=request.POST["textfield5"]
    ob = schedule_table()
    ob.DOCTOR_id= request.session["docid"]

    ob.date=date
    ob.fromtime=fromtime
    ob.totime=totime
    ob.save()
    return HttpResponse('''<script>alert("added");window.location='/managedoctors'</script>''')

def addleave(request):
    return render(request,'doctor/leave.html.')



def addleavepost(request):
    from datetime import datetime
    date=request.POST["textfield"]
    reason=request.POST["textfield1"]
    ob = leave_table()
    ob.date=date
    ob.reason=reason
    ob.time=datetime.now().time()
    ob.DOCTOR=doctor_table.objects.get(LOGIN__id=request.session["lid"])
    ob.save()
    return HttpResponse('''<script>alert("added");window.location='/viewleave'</script>''')



def viewleave(request):
    res=leave_table.objects.filter(DOCTOR__LOGIN_id=request.session['lid'])
    return render(request,'doctor/viewleave.html',{'data':res})


def hospitalviewleave(request):
    res=leave_table.objects.filter(DOCTOR__HOSPITAL__LOGIN_id=request.session['lid'])
    return render(request,'hospital/viewleave.html',{'data':res})





def deleteschedule(request,id):
    request.session['id']=id
    ob=schedule_table.objects.get(id=id)
    ob.delete()
    return HttpResponse(f'''<script>alert("deleted");window.location='/manageschedule/{request.session["docid"]}'</script>''')


def deleteleave(request,id):
    request.session['id']=id
    ob=leave_table.objects.get(id=id)
    ob.delete()
    return HttpResponse(f'''<script>alert("deleted");window.location='/viewleave'</script>''')





def editschedule(request,id):
    request.session["id"]=id
    ob=schedule_table.objects.get(id=id)
    return render(request,'hospital/editschedule.html',{'data':ob})



def editschedulepost(request):
    ob=schedule_table.objects.get(id=request.session["id"])
    ob.date=request.POST["textfield3"]
    ob.fromtime=request.POST["textfield4"]
    ob.totime=request.POST["textfield5"]
    ob.save()
    return HttpResponse(f'''<script>alert("Edited");window.location='/manageschedule/{request.session["docid"]}'</script>''')



def searchdoctors(request):
    doctorname=request.POST['textfield']
    ob=doctor_table.objects.filter(HOSPITAL__LOGIN_id=request.session['lid'],doctorname__contains=doctorname)
    return render(request,'hospital/managedoctors.html',{'data':ob,'doctorname':doctorname})


















# thirdmodule




def doctorhome(request):
    return render(request,'doctor/index.html')





def viewprofile(request):
    ob=doctor_table.objects.get(LOGIN=request.session["lid"])
    return render(request,'doctor/viewprofile.html',{'data':ob})


def viewrating(request):
    session_lid = request.session.get("lid")
    ob = rating_table.objects.filter(DOCTOR__LOGIN_id=session_lid)
    return render(request, 'doctor/app review & rating.html', {'data': ob})



def editprofile(request):
    ob=doctor_table.objects.get(LOGIN_id=request.session["lid"])
    return render(request,'doctor/editprofile.html',{'data':ob})


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import doctor_table


def editprofilepost(request):
    try:
        ob = doctor_table.objects.get(LOGIN_id=request.session["lid"])

        # Update fields
        ob.doctorname = request.POST["textfield"]
        ob.place = request.POST["textfield3"]
        ob.pin = request.POST["textfield2"]
        ob.post = request.POST["textfield4"]

        # Check if an image file is uploaded
        if "file" in request.FILES:
            image = request.FILES["file"]
            fs = FileSystemStorage()
            fp = fs.save(image.name, image)
            ob.image = fp  # Save the file path to the model field

        ob.save()
        return HttpResponse('''<script>alert("edited successfully");window.location='/viewprofile'</script>''')

    except Exception as e:
        return HttpResponse(f'''<script>alert("Error: {str(e)}");window.location='/editprofile'</script>''')


# def editprofilepost(request):
#     try:
#
#         ob=doctor_table.objects.get(LOGIN_id=request.session["lid"])
#         ob.doctorname=request.POST["textfield"]
#         ob.place=request.POST["textfield3"]
#         ob.pin=request.POST["textfield2"]
#         ob.post= request.POST["textfield4"]
#         ob.save()
#         return HttpResponse('''<script>alert("edited successfully");window.location='/viewprofile'</script>''')
#     except:
#         image = request.FILES["file"]
#         ob = doctor_table.objects.get(LOGIN_id=request.session["lid"])
#         ob.doctorname = request.POST["textfield"]
#         fs = FileSystemStorage()
#         fp = fs.save(image.name, image)
#         ob.image = fp
#         ob.place = request.POST["textfield3"]
#         ob.pin = request.POST["textfield2"]
#         ob.post = request.POST["textfield4"]
#         ob.save()
#         return HttpResponse('''<script>alert("edited successfully");window.location='/viewprofile'</script>''')






def viewschedule(request):
    a = schedule_table.objects.filter(DOCTOR__LOGIN_id=request.session['lid'])
    return render(request,'doctor/viewschedule.html',{'data':a})



def docviewbooking(request):
    a = booking_table.objects.filter(SCHEDULE__DOCTOR__LOGIN_id=request.session['lid'])
    return render(request,'doctor/docviewbooking.html',{'data':a})




def addprescription(request,id):
    request.session['pid']=id
    a=prescription_table.objects.filter(BOOKING__id=id)
    return render(request,'doctor/addprescription.html',{'data':a})



def addprescriptionpost(request):
    prescription=request.POST['textfield']
    medicine=request.POST['textfield2']
    instruction=request.POST['textfield3']
    duration=request.POST['textfield4']
    ob=prescription_table()
    ob.prescription=prescription
    ob.medicine=medicine
    ob.instruction=instruction
    ob.duration=duration
    ob.BOOKING=booking_table.objects.get(id=request.session['pid'])
    ob.save()
    return HttpResponse('''<script>alert("added");window.location='/docviewbooking'</script>''')






def deleteprescription(request,id):
    request.session['id']=id
    ob=prescription_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("deleted");window.location='/docviewbooking'</script>''')



def editprescription(request,id):
    request.session["id"]=id
    ob=prescription_table.objects.get(id=id)
    return render(request,'doctor/editprescription.html',{'data':ob})


def editprescriptionpost(request):
    ob=prescription_table.objects.get(id=request.session["id"])
    ob.prescription=request.POST["textfield"]
    ob.medicine=request.POST["textfield2"]
    ob.instruction=request.POST["textfield3"]
    ob.duration=request.POST["textfield4"]
    ob.save()
    return HttpResponse('''<script>alert("edited successfully");window.location='/docviewbooking'</script>''')






####################android##########################




def user_registration(request):
        name=request.POST['name']
        image=request.FILES['image']
        place = request.POST['place']
        pin = request.POST['pin']
        post = request.POST['post']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email=request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        fs=FileSystemStorage()
        fp=fs.save(image.name,image)


        a=login_table()
        a.username=username
        a.password=password
        a.type='user'
        a.save()


        b=user_table()
        b.username=name
        b.place=place
        b.pin=pin
        b.post=post
        b.age=age
        b.gender=gender
        b.phone=phone
        b.image=fp
        b.email=email
        b.LOGIN=a
        b.type = 'user'
        b.save()
        print("uuuuuuuuuu",b)
        return JsonResponse({'task':'valid'})



def logincode(request):
    print(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    print(username,password)
    try:
        ob = login_table.objects.get(username=username, password=password)

        if ob is None:
            data = {"task": "invalid"}
        else:
            print("in user function")
            data = {"task": "valid", "lid": ob.id,"type":ob.type}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    except:
        data = {"task": "invalid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)


def viewhospitaluser(request):
    ob=hospital_table.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'hospitalname':i.hospitalname,'place':i.place,'pin':str(i.pin),'post':i.post,'latitude':str(i.latitude),'longitude':str(i.longitude),'logo':str(i.logo.url),'contact':str(i.contact),'email':i.email,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def viewdoctoruser(request):
    hid=request.POST['hosid']
    ob=doctor_table.objects.filter(HOSPITAL__id=hid)
    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'doctorname': i.doctorname, 'department': i.department, 'image': i.image.url, 'qualification': str(i.qualification),
                'place': str(i.place), 'pin': str(i.pin),
                'post': str(i.post), 'id': i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok", "data": mdata})

#
# def viewscheduleuser(request):
#     did = request.POST['docid']
#     ob=schedule_table.objects.filter(DOCTOR__id=did)
#     print(ob,"HHHHHHHHHHHHHHH")
#     mdata=[]
#     for i in ob:
#         data={'date':str(i.date),'fromtime':str(i.fromtime),'totime':str(i.totime),'id':i.id}
#         mdata.append(data)
#         print(mdata)
#     return JsonResponse({"status":"ok","data":mdata})


from datetime import datetime, timedelta
from django.http import JsonResponse


def viewscheduleuser(request):
    try:
        # Fetch doctor ID from POST data
        did = request.POST['docid']

        # Get the current date and calculate the "day before" threshold
        today = datetime.today().date()
        threshold_date = today + timedelta(days=1)

        # Query schedules for the doctor where the date is at least one day away
        ob = schedule_table.objects.filter(DOCTOR__id=did, date__gte=threshold_date)

        # Prepare data for response
        mdata = []
        for i in ob:
            data = {
                'date': str(i.date),
                'fromtime': str(i.fromtime),
                'totime': str(i.totime),
                'id': i.id
            }
            mdata.append(data)

        # Debugging print statement (optional)
        print(mdata, "Filtered Schedule Data")

        # Return the filtered schedule as JSON response
        return JsonResponse({"status": "ok", "data": mdata})

    except Exception as e:
        # Handle exceptions gracefully and return an error response
        print(f"Error: {e}")
        return JsonResponse({"status": "error", "message": str(e)})


#
# def user_booking(request):
#     lid=request.POST['lid']
#     sid=request.POST['sid']
#     date=request.POST['date']
#     time=request.POST['time']
#     cc=booking_table.objects.filter(SCHEDULE_id=sid,USER__LOGIN_id=lid,date=date)
#     if cc.exists():
#         return JsonResponse({"status": "not ok"})
#
#     a=booking_table()
#     a.SCHEDULE=schedule_table.objects.get(id=sid)
#     a.USER=user_table.objects.get(LOGIN_id=lid)
#     a.status='booked'
#     a.date=date
#     a.time = time  # Set time properly
#     a.save()
#     return JsonResponse({"status": "ok"})


# def user_booking(request):
#     lid = request.POST['lid']
#     sid = request.POST['sid']
#     date = request.POST['date']
#     time = request.POST['time']
#
#     daily_booking_check = booking_table.objects.filter(USER__LOGIN_id=lid, date=date)
#     if daily_booking_check.exists():
#         return JsonResponse({"status": "limit reached", "message": "You can only book one appointment per day"})
#
#     schedule_check = booking_table.objects.filter(SCHEDULE_id=sid, date=date)
#     if schedule_check.exists():
#         return JsonResponse({"status": "not ok", "message": "This slot is already booked"})
#
#     a = booking_table()
#     a.SCHEDULE = schedule_table.objects.get(id=sid)
#     a.USER = user_table.objects.get(LOGIN_id=lid)
#     a.status = 'booked'
#     a.date = date
#     a.time = time
#     a.save()
#     return JsonResponse({"status": "ok"})



# def user_booking(request):
#     lid = request.POST['lid']
#     sid = request.POST['sid']
#     pname = request.POST['name']
#     age = request.POST['age']
#     place = request.POST['place']
#     token = request.POST['token']
#     from datetime import datetime
#     date = datetime.now().today()
#     # date = request.POST['date']
#     # time = request.POST['time']
#     time = datetime.now().time()
#
#     # Check if the user has already booked with the same doctor for the given date
#     daily_booking_check = booking_table.objects.filter(USER__LOGIN_id=lid, SCHEDULE_id=sid, date=date)
#     if daily_booking_check.exists():
#         return JsonResponse(
#             {"status": "limit reached", "message": "You can only book one appointment per doctor per day"})
#
#     # Check if the slot is already booked for the given doctor and date
#     schedule_check = booking_table.objects.filter(SCHEDULE_id=sid, date=date)
#     if schedule_check.exists():
#         return JsonResponse({"status": "not ok", "message": "This slot is already booked"})
#
#     if booking_table.objects.filter(token=token, date=datetime.now().today()).exists():
#         return JsonResponse({"status": "token", "message": "Alreday Booked"})
#
#     # Create a new booking
#     a = booking_table()
#     a.SCHEDULE = schedule_table.objects.get(id=sid)
#     a.USER = user_table.objects.get(LOGIN_id=lid)
#     a.status = 'booked'
#     a.date = date
#     a.time = time
#     a.patientname=pname
#     a.age=age
#     a.place=place
#     a.token=token
#     a.save()
#
#     return JsonResponse({"status": "ok"})


def user_booking(request):
    lid = request.POST['lid']
    sid = request.POST['sid']
    pname = request.POST['name']
    age = request.POST['age']
    place = request.POST['place']
    token = request.POST['token']

    from datetime import datetime
    date = datetime.now().date()
    time = datetime.now().time()

    # One booking per user per schedule per day
    daily_booking_check = booking_table.objects.filter(USER__LOGIN_id=lid, SCHEDULE_id=sid, date=date)
    if daily_booking_check.exists():
        return JsonResponse({
            "status": "limit reached",
            "message": "You can only book one appointment per doctor per day"
        })

    # Check if the same token is already taken for the same schedule and date
    if booking_table.objects.filter(token=token, date=date, SCHEDULE_id=sid).exists():
        return JsonResponse({
            "status": "token",
            "message": "This token is already taken for this schedule"
        })

    # Create the booking
    a = booking_table()
    a.SCHEDULE = schedule_table.objects.get(id=sid)
    a.USER = user_table.objects.get(LOGIN_id=lid)
    a.status = 'booked'
    a.date = date
    a.time = time
    a.patientname = pname
    a.age = age
    a.place = place
    a.token = token
    a.save()

    return JsonResponse({"status": "ok"})


def sendbookinguser(request):
    lid=request.POST['lid']
    schedule_id=request.POST['sid']
    ob=booking_table()
    ob.USER=user_table.objects.get(LOGIN_id=lid)
    ob.SCHEDULE=schedule_table.objects.get(id=schedule_id)
    ob.date=datetime.datetime.now()
    ob.time=datetime.datetime.today.now()
    ob.save()
    return JsonResponse({"status": "ok"})


def viewbookinguser(request):
    ob=booking_table.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'doctor':i.SCHEDULE.DOCTOR.doctorname,'date':i.date,'time':i.time,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})




def viewprescriptionuser(request):
    lid=request.POST['lid']
    ob=prescription_table.objects.filter(BOOKING__USER__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={"dname":i.BOOKING.SCHEDULE.DOCTOR.doctorname,"pname":i.BOOKING.patientname,"date":str(i.BOOKING.date),'prescription':i.prescription,'medicine':i.medicine,'instruction':i.instruction,'duration':i.duration,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})





def androchangepwd(request):
    lid=request.POST["lid"]
    old=request.POST["old"]
    newpwd=request.POST["newpwd"]
    cnfirmpwd=request.POST["cnpwd"]
    if newpwd == cnfirmpwd:
        ob=login_table.objects.get(id=lid,password=old)
        ob.password=newpwd
        ob.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'notok'})




# def userviewprofile(request):
#
#             lid = request.POST.get('lid')
#             user = user_table.objects.get(LOGIN__id=lid)
#
#             data = {
#                 'name': user.username,
#                 'email': user.email,
#                 'phone': user.phone,
#                 'image': str(user.image.url),
#                 'place': user.place,
#                 'pin': user.pin,
#                 'post': user.post,
#                 # 'gender': user.gender,
#                 # 'age': user.age,
#             }
#             return JsonResponse(data)




def and_profile(request):
    lid = request.POST.get('lid')
    student = user_table.objects.get(LOGIN_id=lid)
    print(student)
    return JsonResponse(
        {'status': 'ok',
         'name': student.username,
         'place': student.place,
         'post': student.post,
         'phone': str(student.phone),
         'pin': str(student.pin),
         'Image': student.image.url[1:]})


def updateprofile(request):
    lid = request.POST['lid']
    user = user_table.objects.get(LOGIN__id=lid)
    if 'image' in request.FILES:
        image=request.FILES['image']
        fs=FileSystemStorage()
        fn=fs.save(image.name,image)
        user.image = fn
    user.username = request.POST['name']
    user.phone = request.POST['phone']
    user.place = request.POST['place']
    user.pin = request.POST['pin']
    user.post = request.POST['post']
    user.save()
    return JsonResponse({'status': 'ok'})



def cancel_booking(request):
    booking_id = request.POST.get('bid')

    if not booking_id:
        return JsonResponse({"status": "error", "message": "Booking ID not provided"}, status=400)

    try:
        booking = booking_table.objects.get(id=booking_id)
        booking.status = 'cancel'
        booking.delete()
        return JsonResponse({"status": "ok"})
    except booking_table.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Booking not found"}, status=404)


def view_bookingg(request):
    lid = request.POST['lid']
    a=booking_table.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in a:
        l.append({'id':i.id,'DoctorID':i.SCHEDULE.DOCTOR.doctorname,
                  'hospital':i.SCHEDULE.DOCTOR.HOSPITAL.hospitalname,
                  'date':str(i.SCHEDULE.date),
                  'fromtime':str(i.SCHEDULE.fromtime),
                  'totime':str(i.SCHEDULE.totime),
                  'patientname':i.patientname,
                  'age':i.age,
                  'place':i.place,
                  'tokenno':i.token,
                  'statuss':i.status,
                  # 'from_time':str(i.SCHEDULE.fromtime),
                  # 'totime':str(i.SCHEDULE.totime),

                  })
    print(l)
    return JsonResponse({"status": "ok",'data':l})





def send_rating(request):
    did = request.POST['did']
    rating = request.POST['rating']
    feedback = request.POST['feedback']
    lid = request.POST['lid']
    lob = rating_table()
    lob.USER = user_table.objects.get(LOGIN_id=lid)
    lob.DOCTOR = doctor_table.objects.get(id=did)
    lob.rating = rating
    lob.review = feedback
    lob.date = datetime.today().now()
    lob.time = datetime.today().time()
    lob.save()
    return JsonResponse({'status': 'ok'})



def predict_symptoms(requsest):
    sym=requsest.POST['symptoms'].split("#")
    syms = sym
    print("---", sym)
    symrow = []
    for i in syms:

        if i != "":
            symrow.append(i)

    print(symrow)
    symrow = ",".join(symrow)
    print(symrow)
    symrow = "'" + symrow + "'"
    symrow = symrow.replace(",", "','")

    con = pymysql.connect(host='localhost', user='root', password='123456789', port=3306, db='symptocare')
    cmd = con.cursor()
    # qry = "SELECT DISTINCT `disease_id_id` FROM `doctor_app_symptoms` WHERE `symptom` IN(" + symrow + ")"
    qry = "SELECT DISTINCT `DISEASE_id` FROM `myapp_symptom_table` WHERE `symptom` IN(" + symrow + ")"
    cmd.execute(qry)
    resss = cmd.fetchall()

    distdi = []
    for i in resss:
        print(i)
        distdi.append(str(i[0]))

    distdi = ','.join(distdi)

    try:
        cmd.execute(
            "select distinct symptom from myapp_symptom_table WHERE `DISEASE_id` IN(" + distdi + ") order by symptom")
    except Exception as e:
        print(e)
        return JsonResponse({"status": "failed"})
    s = cmd.fetchall()
    print(s)
    dsym = []
    for i in s:
        dsym.append(i[0])
    row = []
    for w in dsym:
        if w in syms:
            row.append(1)
        else:
            row.append(0)

    ress = prep([row], distdi)
    qry = "select diseasename,causes,howtoprevent from myapp_disease_table where id=" + str(ress)
    cmd.execute(qry)
    res = cmd.fetchone()
    print(res[0], "aaaaaaaaaaaaaa")
    print(res[0], "aaaaaaaaaaaaaa")
    print(res[1], "aaaaaaaaaaaaaa")
    print(res[2], "aaaaaaaaaaaaaa")
    ob = disease_table.objects.get(id=ress)
    print(res[1],"kkkkkkkkkkkkkk")
    print(res[2],"prewww")
    print({"status":"ok","did":res[0],"result":res[0],"trt":res[1],"pm":res[2]})
    return JsonResponse({"status":"ok","did":res[0],"result":res[0],"trt":res[2],"pm":res[1]})



from django.http import JsonResponse
from .models import disease_table, doctor_table


def recommendatedviewdoctoruser(request):
    diseasename = request.POST['disease']
    try:
        # Get the disease object
        disease = disease_table.objects.get(diseasename=diseasename)

        # Get department name from the related department object
        dept_name = disease.DEPARTMENT.department_name

        # Find doctors with matching department name
        doctors = doctor_table.objects.filter(department=dept_name)

        mdata = []
        for i in doctors:
            data = {
                'doctorname': i.doctorname,
                'department': i.department,
                'image': i.image.url,
                'qualification': str(i.qualification),
                'place': str(i.place),
                'pin': str(i.pin),
                'post': str(i.post),
                'id': i.id
            }
            mdata.append(data)

        return JsonResponse({"status": "ok", "data": mdata})

    except disease_table.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Disease not found"})




def viewdoctorleavu(request):
    lid = request.POST['lid']
    bookings = booking_table.objects.filter(USER__LOGIN_id=lid)
    mdata = []

    for booking in bookings:
        doctor = booking.SCHEDULE.DOCTOR
        booking_date=booking.SCHEDULE.date


        leave_entries = leave_table.objects.filter(DOCTOR=doctor, date=booking_date)

        print(leave_entries,'eeeeeeeeeeeeeee')

        if leave_entries.exists():
            for leave in leave_entries:
                data = {
                    'hospitalname': leave.DOCTOR.HOSPITAL.hospitalname,
                    'doctorname': leave.DOCTOR.doctorname,
                    'deptname': leave.DOCTOR.department,
                    'date': str(leave.date),
                    'contact': str(leave.DOCTOR.HOSPITAL.contact),
                    'id': leave.id
                }
                mdata.append(data)


    return JsonResponse({"status": "ok", "data": mdata})




def userhome(request):
    if 'lid' not in request.session or request.session.get('type') != 'user':
        return HttpResponse('''<script>alert("Please login as user");window.location='/'</script>''')
    return render(request, 'user/userhome.html')


def symptom_checker(request):
    return render(request, 'user/symptomchecker.html')




def viewhospitals(request):
    if 'lid' not in request.session or request.session.get('type') != 'user':
        return HttpResponse('''<script>alert("Please login as user");window.location='/'</script>''')
    hospitals = hospital_table.objects.all()
    return render(request, 'user/viewhospitals.html', {'hospitals': hospitals})



def viewdoctorsbyh(request, id):
    if 'lid' not in request.session or request.session.get('type') != 'user':
        return HttpResponse('''<script>alert("Please login as user");window.location='/'</script>''')
    doctors = doctor_table.objects.filter(HOSPITAL__id=id)
    hospital = hospital_table.objects.get(id=id)
    return render(request, 'user/viewdoctors.html', {'doctors': doctors, 'hospital': hospital})


def bookappointment(request, id):
    if 'lid' not in request.session or request.session.get('type') != 'user':
        return HttpResponse('''<script>alert("Please login");window.location='/'</script>''')
    from datetime import datetime, timedelta
    doctor = doctor_table.objects.get(id=id)
    today = datetime.today().date()
    threshold = today + timedelta(days=1)
    schedules = schedule_table.objects.filter(DOCTOR__id=id, date__gte=threshold)
    return render(request, 'user/bookappointment.html', {'doctor': doctor, 'schedules': schedules})

def confirmbooking(request):
    if 'lid' not in request.session:
        return HttpResponse('''<script>alert("Please login");window.location='/'</script>''')
    
    sid = request.POST['schedule_id']
    pname = request.POST['patientname']
    age = request.POST['age']
    place = request.POST['place']
    token = request.POST['token']
    
    from datetime import datetime
    date = datetime.now().date()
    time = datetime.now().time()
    
    if booking_table.objects.filter(USER__LOGIN_id=request.session['lid'], SCHEDULE_id=sid, date=date).exists():
        return HttpResponse('''<script>alert("Already booked today");window.location='/mybookings'</script>''')
    
    if booking_table.objects.filter(token=token, date=date, SCHEDULE_id=sid).exists():
        return HttpResponse('''<script>alert("Token taken");history.back()</script>''')
    
    b = booking_table()
    b.SCHEDULE = schedule_table.objects.get(id=sid)
    b.USER = user_table.objects.get(LOGIN_id=request.session['lid'])
    b.status = 'booked'
    b.date = date
    b.time = time
    b.patientname = pname
    b.age = age
    b.place = place
    b.token = token
    b.save()
    
    return HttpResponse('''<script>alert("Booking successful");window.location='/mybookings'</script>''')



def mybookings(request):
    if 'lid' not in request.session or request.session.get('type') != 'user':
        return HttpResponse('''<script>alert("Please login");window.location='/'</script>''')
    bookings = booking_table.objects.filter(USER__LOGIN_id=request.session['lid']).order_by('-date')
    return render(request, 'user/mybookings.html', {'bookings': bookings})

def cancelbooking(request):
    if 'lid' not in request.session:
        return HttpResponse('''<script>alert("Please login");window.location='/'</script>''')
    
    bid = request.POST['booking_id']
    booking = booking_table.objects.get(id=bid)
    booking.status = 'cancelled'
    booking.save()
    
    return HttpResponse('''<script>alert("Booking cancelled");window.location='/mybookings'</script>''')



def myprescriptions(request):
    if 'lid' not in request.session or request.session.get('type') != 'user':
        return HttpResponse('''<script>alert("Please login");window.location='/'</script>''')
    prescriptions = prescription_table.objects.filter(BOOKING__USER__LOGIN_id=request.session['lid']).order_by('-id')
    return render(request, 'user/myprescriptions.html', {'prescriptions': prescriptions})



def userregister(request):
    return render(request, 'user/userregister.html')

def userregisterpost(request):
    name = request.POST['name']
    age = request.POST['age']
    gender = request.POST['gender']
    phone = request.POST['phone']
    email = request.POST['email']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    image = request.FILES['image']
    username = request.POST['username']
    password = request.POST['password']
    
    # Check if username exists
    if login_table.objects.filter(username=username).exists():
        return HttpResponse('''<script>alert("Username already exists");history.back()</script>''')
    
    from django.core.files.storage import FileSystemStorage
    fs = FileSystemStorage()
    fp = fs.save(image.name, image)
    
    # Create login
    a = login_table()
    a.username = username
    a.password = password
    a.type = 'user'
    a.save()
    
    # Create user
    b = user_table()
    b.username = name
    b.place = place
    b.pin = pin
    b.post = post
    b.age = age
    b.gender = gender
    b.phone = phone
    b.image = fp
    b.email = email
    b.LOGIN = a
    b.save()
    
    return HttpResponse('''<script>alert("Registration successful! Please login");window.location='/'</script>''')