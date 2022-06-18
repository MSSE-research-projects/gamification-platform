from rest_framework import generics
from rest_framework import permissions

from app.gamification.models import CustomUser
from app.gamification.serializers import UserSerializer


class IsAdminOrSelfOrReadOnly(permissions.BasePermission):
    '''
    Custom permission to only allow users to edit information of itself.
    Admin users are allowed to edit information of all users.
    '''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we will always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the user itself or admin users
        return bool(request.user.is_staff or request.user == obj)


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'andrew_id'
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelfOrReadOnly]
