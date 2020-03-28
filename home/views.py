from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from django.shortcuts import redirect
from six.moves import urllib
from rest_framework import serializers
from django.core import serializers
import json
from django.http import HttpResponse, JsonResponse
from admin_panel.models import Request, Category

def index(request):
	queryset={}
	if request.POST:
		print(request.POST)

		if('coordinatesSubmitted' in request.POST):
		    messages.success(request, "Your coordinate has been saved!")
		    latitude = float(request.POST['latitude'])
		    longitude = float(request.POST['longitude'])
		    print('LATITUDE: {}, LONGITUDE: {}'.format(latitude, longitude))

		    user_location = Point(longitude, latitude, srid=4326)
		# #
		#     queryset = Request.objects.filter(location__distance_lte=(user_location, D(km=115)))
		#     # queryset = Request.objects.all()
		#
		#     print(user_location)
		#     print(len(queryset))
		# #
		#     coin_amount = [key.requestor for key in queryset]

		    # request.session['requests'] = coin_amount

		    return HttpResponseRedirect(reverse('home:home'))
		    # return JsonResponse({'requests':coin_amount})
		else:
		    return HttpResponseRedirect(reverse('home:home'))
	else:
		storage = messages.get_messages(request)
		storage.used = True
		return render(request, "home/index.html")
