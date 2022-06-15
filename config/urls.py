"""gamification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import app.gamification.views.pages as page_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', page_views.signin, name = 'signin'),
    path('signup/', page_views.signup, name='signup'),
    path('dashboard/', page_views.dashboard, name='dashboard'),
    path('profile/', page_views.profile, name='profile'),
    path('test/', page_views.test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
