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

import pandas as pd
import random

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
        'year':range(1980,2017) })




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






def movie_recommendation(request):
    if request.method == 'POST':

        rand_item_list = request.session['rand_item_list']

        user = User.objects.get(username='thecoders97@gmail.com')
        print (user.id)

        i = 1
        for r in rand_item_list:
            
            r = request.POST.get(i)
            print (i)
            print (r)

            i += 1

        # df = open('movie_data/u.data','a')
        # feed =  1000 + user.id +'\t' + rand_item.split()[0] + '\t' + rating + '\t' + '881250949'
        # df.write(feed+'\n')
        # df.close()
        

        print (rand_item_list)

        print ("rand_list")

        r_cols = ['user_id', 'movie_id', 'rating']
        ratings = pd.read_csv('slamapp/movie_data/u.data', sep='\t', names=r_cols, 
            encoding='latin-1', usecols=range(3))

        m_cols = ['movie_id', 'title']
        movies = pd.read_csv('slamapp/movie_data/u.item', sep='|', names=m_cols, 
            encoding='latin-1', usecols=range(2))

        ratings = pd.merge(movies, ratings)

        userRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values=['rating'])

        corrMatrix = userRatings.corr(method='pearson', min_periods=60)

        myRatings = userRatings.loc[0].dropna()

        # print (myRatings.index)

        # print(myRatings)

        simCandidates = pd.Series()

        for i in range(0, len(myRatings.index)):
            sims = corrMatrix[myRatings.index[i]].dropna()

            sims = sims.map(lambda x: x * myRatings[i])

            simCandidates = simCandidates.append(sims)


        simCandidates = simCandidates.groupby( simCandidates.index ).sum()

        simCandidates.sort_values(inplace= True, ascending= False)

        final_list = list(simCandidates.head(10).index)

        final_rating = list(simCandidates.head(10))


        print (final_list)
        print (final_rating)

        return render(request,'pages/movie-recommendation.html',{ 'fl':final_list, 'fr':final_rating })


    else:

        movies_list = []
        rand_item_list = []

        df = open('slamapp/movie_data/choices','r')
        for line in df:
            movies_list.append(line)

        df.close()

        i = 8
        
        context = []

        while i > 0:

            rand_item = movies_list[random.randrange(len(movies_list))]

            if rand_item not in rand_item_list:

                rand_item_list.append(rand_item)

                context.append(rand_item.split('\t',1)[1])

                i = i - 1

        print (rand_item_list)

        request.session['rand_item_list'] = rand_item_list

        return render(request,'pages/movie-reviews.html',{ 'context':context, 'r_list':rand_item_list })
