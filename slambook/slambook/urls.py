"""slambook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from slamapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^register/', views.register),
    url(r'^(?P<p>[\w\-\_]+)/registration/$',views.registration),
    url(r'^login/', views.login_site),
    url(r'^logout/', views.logout_site),


    url(r'^profile/', views.profile),
    url(r'^edit-profile/', views.edit_profile),

    url(r'^movie-recommendation/', views.movie_recommendation),


    url(r'^create-questions/', views.create_questions),
    url(r'^fill-slambook/(?P<p>[\w\-\_]+)/$',views.fill_slambook),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
