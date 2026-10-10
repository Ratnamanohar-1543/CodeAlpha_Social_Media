from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from social import views as v
urlpatterns = [path("admin/", admin.site.urls), path("accounts/register/", v.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")), path("", include("social.urls"))] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
