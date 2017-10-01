# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import UserProfile, Set, Set_Content
# Register your models here.



class Set_ContentInline(admin.StackedInline):
    model = Set_Content


class SetAdmin(admin.ModelAdmin):
	list_display = ('sender','filler','date','status')
	list_filter = ('status',)
	inlines = [Set_ContentInline]


admin.site.register(UserProfile)
admin.site.register(Set, SetAdmin)