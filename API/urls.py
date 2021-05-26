"""SaveLifeAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url

from API import views

urlpatterns = [
    url('login/', views.loginUser),
    url('signup/', views.signupUser),
    url('findBlood/', views.get_BloodAndDonor_byArea),
    url('bloodInfo/', views.getBlood_info),
    url('addbank/', views.add_bloodbank),
    url('getbank/', views.get_bloodbank),
    url('addpatient/', views.add_patient),
    url('getpatients/', views.get_patients),
    url('verify/', views.verify_otp),
    url('send_sms/', views.SMS),
    url('make_request/', views.Make_request)
]
