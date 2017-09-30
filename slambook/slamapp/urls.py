from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^(?P<p>[\w\-\_]+)/registration/$',views.registration),
    url(r'^login/', views.login_site),
    url(r'^logout/', views.logout_site),
    url(r'^fillslam/',views.questions),
    url(r'^register/', views.register, name='register'),
    url(r'^profile/', views.profile),
    url(r'^edit-profile/', views.edit_profile),
    url(r'^create-profile/', views.create_profile.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
