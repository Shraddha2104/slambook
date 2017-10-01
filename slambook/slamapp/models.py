# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,blank=False,verbose_name = "First Name")
    last_name = models.CharField(max_length=200, blank=False,verbose_name = "Last Name")

    profile_pic = models.ImageField(upload_to='profile_pics',verbose_name="Profile Picture")

    day = models.CharField(max_length=5,blank=True)
    month = models.CharField(max_length=5,blank=True)
    year = models.CharField(max_length=5,blank=True)

    gender = models.CharField(max_length=10,blank=True)

    city = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)

    class Meta:
        verbose_name = "User Profile"

    def __str__(self):
        return self.user.username


class Set(models.Model):
	sender = models.ForeignKey(User, on_delete = models.CASCADE)
	filler = models.EmailField(max_length=70, blank=False, null=False, unique=False)
	filler_key = models.CharField(max_length=30,blank=False,verbose_name='Filler Key')
	date = models.DateField(auto_now=True)
	status = models.IntegerField(default=0)

	class Meta:
		app_label = 'slamapp'

	def __str__(self):
		return '%s %s %s %s' % (self.sender.username, self.filler, self.status, self.date)


class Set_Content(models.Model):
	set_main = models.ForeignKey(Set, on_delete = models.CASCADE)
	question = models.CharField(max_length=2000,blank=True,verbose_name = "Question")
	answer = models.CharField(max_length=4000,blank=True,verbose_name = "Answer")

	class Meta:
		app_label = 'slamapp'





	# question_1 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 1")
	# answer_1 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 1")
	# question_2 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 2")
	# answer_2 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 2")
	# question_3 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 3")
	# answer_3 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 3")
	# question_4 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 4")
	# answer_4 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 4")
	# question_5 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 5")
	# answer_5 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 5")
	# question_6 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 6")
	# answer_6 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 6")
	# question_7 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 7")
	# answer_7 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 7")
	# question_8 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 8")
	# answer_8 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 8")
	# question_9 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 9")
	# answer_9 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 9")
	# question_10 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 10")
	# answer_10 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 10")
	# question_11 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 11")
	# answer_11 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 11")
	# question_12 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 12")
	# answer_12 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 12")
	# question_13 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 13")
	# answer_13 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 13")
	# question_14 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 14")
	# answer_14 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 14")
	# question_15 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 15")
	# answer_15 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 15")
	# question_16 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 16")
	# answer_16 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 16")
	# question_17 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 17")
	# answer_17 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 17")
	# question_18 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 18")
	# answer_18 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 18")
	# question_19 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 19")
	# answer_19 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 19")
	# question_20 = models.CharField(max_length=2000,blank=True,verbose_name = "Question 20")
	# answer_20 = models.CharField(max_length=4000,blank=True,verbose_name = "Answer 20")

