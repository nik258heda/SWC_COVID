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
from admin_panel.models import Request, Category, Comment
from .forms import AddRequestForm, CommentForm
import time
from django.db.models import Count





class PostToPass():
	request = Request()
	liked = False

	def __init__(self, a, b):
		self.request = a
		self.liked = b

def home(request, latitude, longitude):



	if request.user.is_authenticated:
		if request.POST:
			print(request.POST)

			if('coordinatesSubmitted' in request.POST):


				newlatitude = float(request.POST['latitude'])

				newlongitude = float(request.POST['longitude'])

				print('LATITUDE: {}, LONGITUDE: {}'.format(newlatitude, newlongitude))

				user_location = Point(newlongitude, newlatitude, srid=4326)

				print(user_location)

				return HttpResponseRedirect(reverse('home:home', args=[newlatitude, newlongitude]))
			elif 'refreshLocation' in request.POST:

				return HttpResponseRedirect(reverse('home:home', args=[0, 0]))

			elif 'deletePost' in request.POST:
				postToDelete = request.POST['postToDelete'].split()
				print('POST TO BE DELETED: ', postToDelete)
				Request.objects.filter(requestor__username=postToDelete[0], timestamp_for_id=int(postToDelete[1])).delete()
				return HttpResponseRedirect(reverse('home:home', args=[latitude, longitide]))

			elif 'postToLike' in request.POST:
				postToLike = request.POST['postToLike'].split()
				print("POST TO LIKE", postToLike)
				req = Request.objects.get(requestor__username=postToLike[0], timestamp_for_id=int(postToLike[1]))
				if req.urgency_rating.filter(id=request.user.id).exists():
					Request.objects.get(requestor__username=postToLike[0], timestamp_for_id=int(postToLike[1])).urgency_rating.remove(request.user)
				else:
					Request.objects.get(requestor__username=postToLike[0], timestamp_for_id=int(postToLike[1])).urgency_rating.add(request.user)



				return HttpResponseRedirect(reverse('home:home', args=[latitude, longitude]))

		queryse = Request.objects.filter(requestor=request.user).order_by('-id');
		queryset = []
		for query in queryse:
			print("QUERY", type(query))
			if query.urgency_rating.filter(id=request.user.id).exists():
				queryset.append(PostToPass(query, True))
			else:
				queryset.append(PostToPass(query, False))

		print("Queries: ", queryset)

		latitudeToPass = float(latitude);
		longitudeToPass = float(longitude);


		return render(request, "home/index.html", {'queryset': queryset, 'latitude':latitudeToPass, 'longitude':longitudeToPass})

	return render(request, "home/index.html")

def postForm(request):
	if request.user.is_authenticated:
		if request.POST:
			request_form = AddRequestForm(data=request.POST)
			if request_form.is_valid():
				print("VALID REQUEST")
				requestt = request_form.save(commit=False)
				requestt.requestor = request.user
				global user_location
				if user_location:
					requestt.location = user_location
				requestt.timestamp_for_id = int(round(time.time() * 1000))
				print("RECK: ", requestt)
				requestt.save()


				return HttpResponseRedirect(reverse('home:home'))
		else:
			print("USAAR", user_location);
			add_request_form=AddRequestForm();
			return render(request, 'home/post_form.html', {'add_request_form':add_request_form})
	else:
		return HttpResponseRedirect(reverse('home:home'))

def mainPage(request):
	if request.user.is_authenticated:
		if request.POST:



			if 'coordinatesSubmitted' in request.POST:
				global latitude
				latitude = float(request.POST['latitude'])
				global longitude
				longitude = float(request.POST['longitude'])
				print('LATITUDE: {}, LONGITUDE: {}'.format(latitude, longitude))
				global user_location
				user_location = Point(longitude, latitude, srid=4326)
				print(user_location)
				return HttpResponseRedirect(reverse('home:main_page'))
			elif 'refreshLocation' in request.POST:

				longitude = 0

				latitude = 0
				return HttpResponseRedirect(reverse('home:main_page'))

			elif 'postToLike' in request.POST:
				postToLike = request.POST['postToLike'].split()
				print("POST TO LIKE", postToLike)
				req = Request.objects.get(requestor__username=postToLike[0], timestamp_for_id=int(postToLike[1]))
				if req.urgency_rating.filter(id=request.user.id).exists():
					Request.objects.get(requestor__username=postToLike[0], timestamp_for_id=int(postToLike[1])).urgency_rating.remove(request.user)
				else:
					Request.objects.get(requestor__username=postToLike[0], timestamp_for_id=int(postToLike[1])).urgency_rating.add(request.user)

				return HttpResponseRedirect(reverse('home:main_page'))

		queryse = Request.objects.filter(location__distance_lte=(user_location, D(km=3))).annotate(distance=Distance('location',user_location), q_count=Count('urgency_rating')).filter(address_allowed=True).order_by('distance', '-q_count', '-id')

		queryset=[]

		for query in queryse:
			if query.urgency_rating.filter(id=request.user.id).exists():
				queryset.append(PostToPass(query,True))
			else:
				queryset.append(PostToPass(query, False))

		return render(request, "home/main_page.html", {'queryset':queryset, 'latitude': latitude, 'longitude': longitude})
	else:
		return HttpResponseRedirect(reverse('home:home'))


def openPost(request, post_requestor_name, post_timestamp):
	if request.user.is_authenticated:

		comment_form = CommentForm()

		if request.POST:

			if 'commentMade' in request.POST:
				comment_form = CommentForm(request.POST or None)
				if comment_form.is_valid():
					print("VALID COMMENT")
					comment = comment_form.save(commit=False)
					comment.user = request.user
					comment.request = Request.objects.get(requestor__username=post_requestor_name, timestamp_for_id=post_timestamp)
					comment.timestamp_for_id = int(round(time.time() * 1000))
					comment.save()

					return HttpResponseRedirect(reverse('home:open_post', args=[post_requestor_name, post_timestamp]))
				else:
					return HttpResponseRedirect(reverse('home:open_post', args=[post_requestor_name, post_timestamp]))



			if "Like" in request.POST:
				print("LIKE: ", request.POST)
				postToLike = Request.objects.get(requestor__username=post_requestor_name, timestamp_for_id=post_timestamp)
				if postToLike.urgency_rating.filter(id=request.user.id).exists():
					Request.objects.get(requestor__username=post_requestor_name, timestamp_for_id=post_timestamp).urgency_rating.remove(request.user)
				else:
					Request.objects.get(requestor__username=post_requestor_name, timestamp_for_id=post_timestamp).urgency_rating.add(request.user)

				url=reverse('home:open_post', args=[post_requestor_name, post_timestamp])
				return HttpResponseRedirect(url)


		postToShow = Request.objects.get(requestor__username=post_requestor_name, timestamp_for_id=post_timestamp)

		if postToShow.urgency_rating.filter(id=request.user.id).exists():
			postToShow = PostToPass(postToShow, True)
		else:
			postToShow = PostToPass(postToShow, False)


		comments = Comment.objects.filter(request=postToShow.request).order_by('-id')

		print("POST TO SHOW: ", postToShow)

		return render(request, "home/post_page.html", {'postToShow': postToShow, 'comments': comments, 'comment_form': comment_form})

	else:
		return HttpResponseRedirect(reverse('home:home'))
