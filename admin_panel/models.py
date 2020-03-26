from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    category_name = models.CharField(max_length=128)
    urgency_level = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(1)])

    def __str__(self):
        return self.category_name


class Request(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='requests')
    requested_on = models.DateTimeField(auto_now=True)
    user_remarks = models.TextField(max_length=1024, blank=True)
    admin_remarks = models.TextField(max_length=1024, blank=True)
    urgency_rating = models.FloatField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    status_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.requested_by.first_name + ' - ' + self.category.category_name
