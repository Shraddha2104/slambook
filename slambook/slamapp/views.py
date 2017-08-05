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

from django.http import HttpResponse

# Create your views here.


def signup(request):
    if request.method == 'POST':
        usermail = request.POST.get('usermail')

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

        return HttpResponse('User Has Been Sent Mail')

    else:
        return render(request,'signup.html')



def registration(request,p):
    if request.method=='POST':
        print (p)
        upass=request.POST.get('upass')
        upass1=request.POST.get('upass1')
        # pic = request.FILES['pic']
        print ("TRUE")
        if upass==upass1:
            up=User.objects.get(password=p)
            print (up)

            up.set_password(upass)
            up.save()

            return HttpResponse("DONE")

        else:
            return HttpResponse('Enter password correctly')

    else:
        up=User.objects.get(password=p)
        print (up)
        return render(request,'changepass.html',{ 'p':p })




def login_site(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print (user)

        if user is not None:
            if user.is_active:
                auth_login(request, user)

            else:
                context['error'] = 'Non active user'
        else:
            context['error'] = 'Wrong username or password'
    else:
        context['error'] = ''

    populateContext(request, context)

    return render(request, 'login.html', context)


def logout_site(request):
    context = {}
    if request.user.is_authenticated():
        auth_logout(request)
    else:
        context['error'] = 'Some error occured.'

    populateContext(request, context)
    return render(request, 'login.html', context)


def populateContext(request, context):
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username
