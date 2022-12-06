from app.gamification.models.constraint import Constraint
from app.gamification.serializers.constraint import ConstraintSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

class ConstraintList(generics.ListCreateAPIView):
    queryset = Constraint.objects.all()
    serializer_class = ConstraintSerializer
    # permission_classes = [IsAdminOrReadOnly]

class ConstraintDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constraint.objects.all()
    serializer_class = ConstraintSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, url, *args, **kwargs):
        constraint = get_object_or_404(Constraint, url=url)
        serializer = self.get_serializer(constraint)
        return Response(serializer.data)

    def put(self, request, url, *args, **kwargs):
        constraint = get_object_or_404(Constraint, url=url)
        threshold = request.data.get('threshold')
        
        constraint.threshold = threshold
        constraint.save()
        serializer = self.get_serializer(constraint)
        return Response(serializer.data)

    def delete(self, request, url, *args, **kwargs):
        constraint = get_object_or_404(Constraint, url=url)
        constraint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ConstraintProgressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constraint.objects.all()
    serializer_class = ConstraintSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, url, *args, **kwargs):
        constraint = get_object_or_404(Constraint, url=url)
        serializer = self.get_serializer(constraint)
        return Response(serializer.data)

    def put(self, request, url, *args, **kwargs):
        constraint = get_object_or_404(Constraint, url)
        threshold = request.data.get('threshold')
        
        constraint.threshold = threshold
        constraint.save()
        serializer = self.get_serializer(constraint)
        return Response(serializer.data)

    def delete(self, request, url, *args, **kwargs):
        constraint = get_object_or_404(Constraint, url=url)
        constraint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    