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
from app.gamification.models import assignment

import app.gamification.views.pages as page_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', page_views.signin, name='signin'),
    path('signup/', page_views.signup, name='signup'),
    path('dashboard/', page_views.dashboard, name='dashboard'),
    path('profile/', page_views.profile, name='profile'),
    path('test/', page_views.test, name='test'),
    path('course/', page_views.course, name='course'),
    path('delete_course/<str:course_id>', page_views.delete_course, name = 'delete_course'),
    path('course/edit_course/<str:course_id>',
         page_views.edit_course, name='edit_course'),
    path('assignment/', page_views.assignment, name='assignment'),
    path('delete_assignment/<str:assignment_id>', page_views.delete_assignment, name = 'delete_assignment'),
    path('assignment/edit_assignment/<str:assignment_id>',
         page_views.edit_assignment, name='edit_assignment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
