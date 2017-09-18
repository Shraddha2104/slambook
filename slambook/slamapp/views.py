# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

import smtplib
import re
import hashlib
import ast
import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from slamapp.safe import mymail,mypassword
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .models import UserProfile

from django.http import HttpResponse

# Create your views here.


month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


def register(request):
    if request.method == 'POST':
        usermail = request.POST.get('usermail')
        username = request.POST.get('username')

        hash = hashlib.sha1()
        now = datetime.datetime.now()
        hash.update(str(now).encode('utf-8') + usermail.encode('utf-8') + 'kuttu'.encode('utf-8'))
        tp = hash.hexdigest()

        fromaddr = mymail
        toaddr = usermail
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Confirmational Email'
        domain = request.get_host()
        scheme = request.is_secure() and "https" or "http"
        body = "Please Click On The Link To complete registration: {0}://{1}/{2}/registration".format(scheme, domain, tp)
        part1 = MIMEText(body, 'plain')
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, mypassword)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

        user = User.objects.create(username=usermail,password=tp)
        user.save()

        return render(request,'pages/sentack.html')

    else:
        return render(request,'pages/register.html')



def registration(request,p):
    if request.method=='POST':
        print (p)
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        profile_pic = request.FILES['profile_pic']

        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')

        gender = request.POST.get('gender')

        city = request.POST.get('city')
        country = request.POST.get('country')

        upass = request.POST.get('upass')
        upass1 = request.POST.get('upass1')

        print (fname)
        print(lname)
        print(day)
        print(month)
        print(year)
        print(gender)
        print(city)
        print(country)

        if upass == upass1:
            up = User.objects.get(password=p)
            print (up)

            userprofile = UserProfile.objects.create(user=up,first_name=fname,last_name=lname,
                profile_pic=profile_pic,day=day,month=month,year=year,gender=gender,
                city=city,country=country)
            userprofile.save()   

            up.set_password(upass)
            up.save()

            user = authenticate(username=up.username, password=upass)

            if user.is_active:
                auth_login(request, user)

                return redirect('/profile/')


            else:
                return HttpResponse("Unexpected Error! Please Try Again.")

        else:
            return HttpResponse('Enter password correctly')

    else:
        up=User.objects.get(password=p)
        print (up)
        return render(request,'pages/details.html',{ 'p':p, 'day':range(31),
        'month':month,'year':range(1980,2017) })




def login_site(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/profile/')

            else:
                context['error'] = 'Non active user'
        else:
            context['error'] = 'Wrong username or password'
    else:
        context['error'] = ''

    populateContext(request, context)

    return render(request, 'pages/login.html', context)



def logout_site(request):
    context = {}
    if request.user.is_authenticated():
        auth_logout(request)
    else:
        context['error'] = 'Some error occured.'

    populateContext(request, context)
    return render(request, 'pages/login.html', context)



def populateContext(request, context):
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username






def profile(request):
    if request.user.is_authenticated:
        up = UserProfile.objects.get(user=request.user)
        return render(request,'pages/profile.html',{ 'up':up })

    else:
        return redirect('/login/')



def edit_profile(request):
    if request.user.is_authenticated:
        up = UserProfile.objects.get(user=request.user)
        return render(request,'pages/edit-profile.html',{ 'up':up, 'day':range(31),
        'month':month,'year':range(1980,2017) })

    else:
        return redirect('/login/')
