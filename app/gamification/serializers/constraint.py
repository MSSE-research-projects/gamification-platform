from rest_framework import serializers

from app.gamification.models import Constraint

class ConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constraint
        fields = ['pk', 'url', 'threshold']