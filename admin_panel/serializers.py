from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'first_name']


class RequestSerializer(serializers.ModelSerializer):
    # requestor = serializers.RelatedField(source='User')

    class Meta:
        model = models.Request
        fields = ['requestor', 'category', 'location', 'user_remarks', 'created', 'urgency_rating', 'status_completed']
