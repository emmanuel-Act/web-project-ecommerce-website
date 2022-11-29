"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), #for the default route, include all urls of the core app. this makes django
    path('accounts/', include('accounts.urls'))                    #to acknowledge all the urls of the core app.
    #a url for the accounts app. all other urls in this app will follow accounts/...
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)# to map my media files to the urls 
#from settings access the media url and the document root will be the media root and we've seen that the media root is appended to the base_dir
#so the url for the media file will be configured as base_dir/media/pic.jpg 