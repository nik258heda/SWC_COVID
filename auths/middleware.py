from django.utils.deprecation import MiddlewareMixin
from social_django.models import UserSocialAuth
from auths.models import Profile
from django.http import HttpResponseRedirect
from django.urls import reverse


class PhoneVerificationMiddleware(MiddlewareMixin):
	def __init__(self, get_response=None):
		self.get_response = get_response

	def process_view(self, request, view_func, view_args, view_kwargs):
		if request.user.is_authenticated and not UserSocialAuth.objects.filter(user_id=request.user.id).exists() and not Profile.objects.filter(user=request.user).exists():
		# if not request.backends.associated and not request.user.profile:
			return HttpResponseRedirect(reverse('auths:phoneVerification'))
		return None