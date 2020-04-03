import random
from django.contrib.gis.geos import Point
from factory.fuzzy import BaseFuzzyAttribute
from django.contrib.auth.models import User
import factory
import factory.django
from .models import Request, Category


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(random.uniform(76.0, 77.0),
                     random.uniform(28.0, 29.0))


class FuzzyTimestamp(BaseFuzzyAttribute):
    def fuzz(self):
        return random.uniform(10000000, 10000000000000)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category_name = factory.Faker('word')


class RequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Request

    # requestor details
    requestor = factory.Iterator(User.objects.all())
    location = FuzzyPoint()
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')

    # request details
    requirement = factory.Faker('sentence')
    category = factory.Iterator(Category.objects.all())
    created = factory.Faker('date_time')
    address_allowed = factory.LazyAttribute(lambda x: True)

    timestamp_for_id = FuzzyTimestamp()

    # remarks
    user_remarks = factory.Faker('paragraph')
    admin_remarks = factory.Faker('paragraph')

    # status
    status_completed = factory.LazyAttribute(lambda x: False)

