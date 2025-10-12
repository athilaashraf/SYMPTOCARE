"""symptocare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('',views.login),
    path('adddiseaseinformation',views.adddiseaseinformation),
    path('adminhome',views.adminhome),
    path('managediseaseinfo',views.managediseaseinfo),
    path('verifyhospital',views.verifyhospital),
    path('viewdoctors/<id>',views.viewdoctors),
    path('viewusers',views.viewusers),
    path('viewverifiedhospitals',views.viewverifiedhospitals),
    path('login_post',views.login_post),
    path('accepthospital/<id>',views.accepthospital),
    path('rejecthospital/<id>',views.rejecthospital),
    path('unblockuser/<id>',views.unblockuser),
    path('blockuser/<id>',views.blockuser),
    path('adddiseaseinformationpost',views.adddiseaseinformationpost),
    path('deletedisease/<id>',views.deletedisease),
    path('editinfo/<id>',views.editinfo),
    path('editinfopost',views.editinfopost),
    path('searchhospital',views.searchhospital),
    path('searchuser',views.searchuser),
    path('searchverifiedhospital',views.searchverifiedhospital),
    path('searchdoctor',views.searchdoctor),
    path('searchdisease',views.searchdisease),
    path('updateprofile',views.updateprofile),
    path('predict_symptoms',views.predict_symptoms),
    path('userhome', views.userhome, name='userhome'),
    path('symptom_checker', views.symptom_checker, name='symptom_checker'),
    path('viewhospitals', views.viewhospitals, name='viewhospitals'),
    path('viewdoctorsbyh/<id>', views.viewdoctorsbyh, name='viewdoctorsbyh'),
    path('bookappointment/<id>', views.bookappointment, name='bookappointment'),
    path('confirmbooking', views.confirmbooking, name='confirmbooking'),
    path('mybookings', views.mybookings, name='mybookings'),
    path('cancelbooking', views.cancelbooking, name='cancelbooking'),
    path('myprescriptions', views.myprescriptions, name='myprescriptions'),
    path('userregister', views.userregister, name='userregister'),
    path('userregisterpost', views.userregisterpost, name='userregisterpost'),
    path('adminviewalldoctors', views.adminviewalldoctors, name='adminviewalldoctors'),
    path('recommendatedviewdoctoruser', views.recommendatedviewdoctoruser, name='recommendatedviewdoctoruser'),





    path('register',views.register),
    path('hospitalhome',views.hospitalhome),
    path('viewbooking',views.viewbooking),
    path('managedoctors',views.managedoctors),
    path('adddoctor',views.adddoctor),
    # Department Management URLs
    path('managedepartments',views.managedepartments),
    path('adddepartment',views.adddepartment),
    path('adddepartmentpost',views.adddepartmentpost),
    path('populate_departments',views.populate_departments),
    path('editdepartment/<id>',views.editdepartment),
    path('editdepartmentpost',views.editdepartmentpost),
    path('deletedepartment/<id>',views.deletedepartment),
    # End Department Management URLs
    path('manageschedule/<id>',views.manageschedule),
    path('addschedule',views.addschedule),
    path('adddoctorpost',views.adddoctorpost),
    path('deletedoctor/<id>',views.deletedoctor),
    path('addschedulepost',views.addschedulepost),
    path('deleteschedule/<id>',views.deleteschedule),
    path('editschedule/<id>',views.editschedule),
    path('editschedulepost',views.editschedulepost),
    path('editdoctor/<id>',views.editdoctor),
    path('editdoctorpost',views.editdoctorpost),
    path('searchdoctors',views.searchdoctors),
    path('registerpost',views.registerpost),
    path('logincode',views.logincode),
    path('/user_booking',views.user_booking),
    path('/view_bookingg',views.view_bookingg),
    path('/cancel_booking',views.cancel_booking),
    path('and_profile',views.and_profile),
    path('addleave',views.addleave),
    path('addleavepost',views.addleavepost),
    path('viewleave',views.viewleave),
    path('hospitalviewleave',views.hospitalviewleave),








    path('doctorhome',views.doctorhome),
    path('viewprofile',views.viewprofile),
    path('editprofile',views.editprofile),
    path('viewschedule',views.viewschedule),
    path('docviewbooking',views.docviewbooking),
    path('addprescription/<id>',views.addprescription),
    path('addprescriptionpost',views.addprescriptionpost),
    path('deleteprescription/<id>',views.deleteprescription),
    path('editprescription/<id>',views.editprescription),
    path('editprescriptionpost',views.editprescriptionpost),
    path('editprofile/<id>',views.editprofile),
    path('editprofilepost',views.editprofilepost),
    path('viewrating',views.viewrating),
    path('deleteleave/<id>',views.deleteleave),





    path('user_registration',views.user_registration),
    path('/logincode',views.logincode),
    path('viewhospitaluser',views.viewhospitaluser),
    path('viewdoctoruser',views.viewdoctoruser),
    path('viewscheduleuser',views.viewscheduleuser),
    path('viewbookinguser',views.viewbookinguser),
    path('viewprescriptionuser',views.viewprescriptionuser),
    path('androchangepwd',views.androchangepwd),
    # path('userviewprofile',views.userviewprofile),
    path('updateprofile',views.updateprofile),
    path('send_rating',views.send_rating),
    path('updateprofile',views.updateprofile),
    path('recommendatedviewdoctoruser',views.recommendatedviewdoctoruser),
    path('viewdoctorleavu',views.viewdoctorleavu),
    ]