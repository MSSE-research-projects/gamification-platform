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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

import app.gamification.views.pages as page_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', page_views.dashboard, name='home'),
    path('signin/', page_views.signin, name='signin'),
    path('signup/', page_views.signup, name='signup'),
    path('signout/', page_views.signout, name='signout'),

    path('email_user/<str:andrew_id>/', page_views.email_user, name='email_user'),

    path('dashboard/', page_views.dashboard, name='dashboard'),
    path('profile/', page_views.profile, name='profile'),
    path('instructor_admin/', page_views.instructor_admin, name='instructor_admin'),

    path('test/', page_views.test, name='test'),
    path('test_survey_template/', page_views.test_survey_template,
         name='test_survey_template'),
    path('test_add_survey/', page_views.test_add_survey, name='test_add_survey'),
    path('test_preview_survey/', page_views.test_preview_survey,
         name='test_preview_survey'),
    path('test_fill_survey/', page_views.test_fill_survey, name='test_fill_survey'),

    path('course/', include([
        path('', page_views.course_list, name='course'),

        path('<int:course_id>/', include([
            path('delete/', page_views.delete_course, name='delete_course'),
            path('edit/', page_views.edit_course, name='edit_course'),
            path('view/', page_views.view_course, name='view_course'),

            path('assignment/', include([
                path('', page_views.assignment, name='assignment'),
                path('<int:assignment_id>/', include([
                    path('delete/', page_views.delete_assignment,
                         name='delete_assignment'),
                    path('edit/', page_views.edit_assignment,
                         name='edit_assignment'),
                    path('view/', page_views.view_assignment,
                         name='view_assignment'),
                    path('add/', page_views.add_survey, name='add_survey'),
                    path('survey/', include([
                        path('', page_views.survey_list, name='survey_list'),
                        path('addsection/', page_views.add_section,
                             name='add_section'),
                        path('<int:section_id>/', include([
                            path('delete/', page_views.delete_section,
                                 name='delete_section'),
                            path('edit/', page_views.edit_section,
                                 name='edit_section'),
                            path('add/', page_views.add_question,
                                 name='add_question'),
                            path('<int:question_id>/', include([
                                path('delete/', page_views.delete_question,
                                     name='delete_question'),
                                path('edit/', page_views.edit_question,
                                     name='edit_question')
                            ])),
                        ])),
                    ])),

                    path('artifact/', include([
                        path('', page_views.artifact, name='artifact'),
                        path('admin/', page_views.artifact_admin,
                             name='artifact_admin'),
                        path('<int:artifact_id>/', include([
                            path('delete/', page_views.delete_artifact,
                                 name='delete_artifact'),
                            path('edit/', page_views.edit_artifact,
                                 name='edit_artifact'),
                            path('view/', page_views.view_artifact,
                                 name='view_artifact'),
                            path('download/', page_views.download_artifact,
                                 name='download_artifact'),
                        ])),
                    ])),
                ]))
            ])),


            path('member_list/', include([
                path('', page_views.member_list, name='member_list'),
                path('<str:andrew_id>/', include([
                    path('delete/', page_views.delete_member,
                         name='delete_member'),
                ])),
                path('<str:andrew_id>/', include([
                    path('report/', page_views.report,
                         name='report'),
                ]))
            ])),
        ])),
    ])),

    path('api/', include('app.gamification.views.api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('reset_password/', page_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
