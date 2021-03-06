from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    category_name = models.CharField(max_length=128)

    def __str__(self):
        return self.category_name


class Request(models.Model):
    # requestor details
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    location = models.PointField(srid=4326, geography=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    # request details
    requirement = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='requests')
    urgency_rating = models.ManyToManyField(User, blank=True, related_name="post_urgency")
    created = models.DateTimeField(auto_now_add=True)
    address_allowed = models.BooleanField(default=True)

    timestamp_for_id = models.BigIntegerField(default=0)

    # remarks
    user_remarks = models.TextField(max_length=1024, blank=True)
    admin_remarks = models.TextField(max_length=1024, blank=True)

    # status
    status_completed = models.BooleanField(default=False)

    #constant offset by volunteer
    v_const = models.IntegerField(default=0);

    def __str__(self):
        return self.requestor.username + str(self.timestamp_for_id);

class Comment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    timestamp_for_id = models.BigIntegerField(default=0)

    def __str__(self):
        return self.user.username + str(self.timestamp_for_id)
