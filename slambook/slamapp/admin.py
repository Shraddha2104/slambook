# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import UserProfile, Set, FriendList

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Set)

from .models import Post

admin.site.register(FriendList)
admin.site.register(Post)