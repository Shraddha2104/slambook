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

from .models import UserProfile, Set, Set_Content

from django.http import HttpResponse

#import pandas as pd
import random

# Create your views here.



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
        body = "Please Click On The Link To Complete Registration: {0}://{1}/{2}/registration".format(scheme, domain, tp)
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

        if request.method=='POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')

            print (fname)

            try:
                profile_pic = request.FILES['profile_pic']
                up.update(profile_pic=profile_pic)
            except:
                pass

            day = request.POST.get('day')
            month = request.POST.get('month')
            year = request.POST.get('year')

            city = request.POST.get('city')

            about = request.POST.get('information')

            up = UserProfile.objects.filter(user=request.user)

            up.update(first_name=fname,last_name=lname,
                day=day,month=month,year=year,
                city=city,
                about=about)

            return redirect('/profile/')


        else:
            up = UserProfile.objects.get(user=request.user)
            print (up.about)
            month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

            return render(request,'pages/edit-profile.html',{ 'up':up, 'day':range(31),
            'month':month,'year':range(1980,2017) })

    else:
        return redirect('/login/')



def change_password(request):
    if request.user.is_authenticated:
        up = UserProfile.objects.get(user=request.user)

        if request.method == 'POST':


            upass = request.POST.get('upass')
            upass1 = request.POST.get('upass1')


            if upass == upass1:
                usr = request.user
                usr.set_password(upass1)
                usr.save()


            user = authenticate(username=usr.username, password=upass1)

            if user.is_active:
                auth_login(request, user)

                return redirect('/profile/')

            else:
                return HttpResponse("ERROR PLEASE RETRY")

        else:
            return render(request, 'pages/change_password.html',{ 'up':up })


    else:
        return redirect('/login/') 




def create_questions(request):
    if request.user.is_authenticated:
        up = UserProfile.objects.get(user=request.user)

        questions = []
        if request.method == 'POST':
            filler = request.POST.get('filler')
            questions = request.POST.getlist('qs[]')

            print (filler)
            print (questions)


            hash = hashlib.sha1()
            now = datetime.datetime.now()
            hash.update(str(now).encode('utf-8') + filler.encode('utf-8') + 'kuttu'.encode('utf-8'))
            fillerkey = hash.hexdigest()


            set_main = Set.objects.create(sender=request.user,filler=filler,filler_key=fillerkey)

            for qs in questions:
                set_content = Set_Content.objects.create(set_main=set_main,question=qs)



            fromaddr = mymail
            toaddr = filler
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            

            domain = request.get_host()
            scheme = request.is_secure() and "https" or "http"

            msg['Subject'] = "Your Friend {0} Requests You To Fill In His SlamBook".format(up.first_name)

            domain = request.get_host()
            scheme = request.is_secure() and "https" or "http"

            body = "Use The Button Below"
            part1 = MIMEText(body, 'plain')
            msg.attach(part1)

            
            filling_link = "{0}://{1}/fill-slambook/{2}".format(scheme,domain,fillerkey)
            part3 = MIMEText(u'<center>Please click <a href="'+filling_link+'" style="font-size:16px;">here to complete your subscription</a> to our newsletter</center>','html')
            msg.attach(part3)


            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(mymail, mypassword)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()


            return redirect('/profile/')


        else:
            return render(request, 'pages/questionnaire.html',{ 'up':up })


    else:
        return redirect('/login/')





def fill_slambook(request,p):
    if request.method=='POST':
        pass


    else:
        s = Set.objects.get(filler_key=p)
        print (s)
        return render(request,'pages/fill-slambook.html')





def movie_recommendation(request):
    if request.user.is_authenticated:
        up = UserProfile.objects.get(user=request.user)

        if request.method == 'POST':

            rand_item_list = request.session['rand_item_list']

            user = UserProfile.objects.get(user=request.user)

            df = open('slamapp/movie_data/u.data','a')

            i = 1
            for r in rand_item_list:

                r = request.POST.get("in" + str(i))
                print (rand_item_list[i-1])
                print (r)

                feed =  '1000' + str(user.id) +'\t' + rand_item_list[i-1].split()[0] + '\t' + r + '\t' + '881250949'
                df.write(feed+'\n')

                i += 1

            df.close()


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

            myRatings = userRatings.loc[int('1000' + str(user.id))].dropna()

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

            return render(request,'pages/movie-recommendation.html',{ 'fl':final_list, 'fr':final_rating,
            'up':up })


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

            return render(request,'pages/movie-reviews.html',{ 'context':context, 'up':up })
        

    else:
        return redirect('/login/')