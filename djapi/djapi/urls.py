"""djapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.auth.views import login, logout_then_login
from django.conf.urls import url, include
from django.contrib import admin
from tools.format_excel import api_upload
from app01 import urls
from usejks import urls
from dns_api import urls
from deploy import urls
from passport import urls
from cmdb import urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api_passport/', include('passport.urls')),
    url(r'^api/v1/', include('app01.urls')),
    url(r'^api_jks/', include('usejks.urls')),
    url(r'^api_dns/', include('dns_api.urls')),
    url(r'^api_deploy/', include('deploy.urls')),
    url(r'^api_cmdb/', include('cmdb.urls')),
    url(r'^api_upload/', api_upload, name='api_upload')
]
