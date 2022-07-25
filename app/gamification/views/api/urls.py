from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .user import UserList, UserDetail
from .course import CourseList, CourseDetail


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'courses': reverse('course-list', request=request, format=format),
    })


urlpatterns = [
    path('', api_root),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<str:andrew_id>/', UserDetail.as_view(), name='user-detail'),
    path('courses/', CourseList.as_view(), name='course-list'),
    path('courses/<str:id>/', CourseDetail.as_view(), name='course-detail'),
]
