from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.gamification.decorators import admin_required
from app.gamification.views.pages.artifact_views import *
from app.gamification.views.pages.assignment_views import *
from app.gamification.views.pages.course_views import *
from app.gamification.views.pages.dashboard_views import *
from app.gamification.views.pages.member_views import *
from app.gamification.views.pages.profile_views import *
from app.gamification.views.pages.report_views import *
from app.gamification.views.pages.signin_views import *
from app.gamification.views.pages.survey_views import *
from app.gamification.views.pages.test_views import *


@login_required
@admin_required(redirect_field_name=None, login_url='dashboard')
def instructor_admin(request):
    return render(request, 'instructor_admin.html')
