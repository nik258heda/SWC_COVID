from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'first_name']


class RequestSerializer(serializers.ModelSerializer):
    requestor = serializers.SerializerMethodField(read_only=True)
    urgency_rating = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    status_completed = serializers.SerializerMethodField(read_only=True)

    def get_requestor(self, request):
        return request.requestor.first_name + ' ' + request.requestor.last_name

    def get_urgency_rating(self, request):
        return request.urgency_rating.count() + request.v_const;

    def get_category(self, request):
        return request.category.category_name

    def get_status_completed(self, request):
        if request.status_completed:
            return 'Completed'
        else:
            return 'Pending'

    class Meta:
        model = models.Request
        fields = ['id', 'requestor', 'category', 'location', 'user_remarks', 'created', 'urgency_rating', 'status_completed']
