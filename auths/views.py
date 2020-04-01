from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from auths.forms import SignUpForm, PhoneVerificationForm, TokenForm
from authy.api import AuthyApiClient
from django.conf import settings
from auths.models import Profile
from django.core.exceptions import ValidationError

authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)
	


def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			if user.is_authenticated:     
				login(request, user)
			# return redirect('home:home')
			return redirect('auths:phoneVerification')
	else:
		form = SignUpForm()
	return render(request, 'auths/signup.html', {'form': form})


def phoneVerificationView(request):
	if request.user.is_authenticated:
		# if not Profile.objects.filter(user=request.user).exists():
		if request.method == 'POST':
			form = PhoneVerificationForm(request.POST)
			if form.is_valid():
				request.session['phone_number'] = form.cleaned_data['phone_number']
				request.session['country_code'] = form.cleaned_data['country_code']
				if Profile.objects.filter(phone=form.cleaned_data['phone_number'], country_code=form.cleaned_data['country_code']).exists():
					print("FC@@@@@@@@@@@@@@@@@@@@@@@@@@")
					raise ValidationError("Phone Number already exists")
				authy_api.phones.verification_start(
					form.cleaned_data['phone_number'],
					form.cleaned_data['country_code'],
					via=form.cleaned_data['via']
				)
				return redirect('auths:tokenValidation')

		else :
			form = PhoneVerificationForm()
			return render(request, 'auths/phoneVerification.html', {'form': form})

	return redirect('home:home')


def tokenValidation(request):
	if request.method == 'POST':
		form = TokenForm(request.POST)
		if form.is_valid():
			verification = authy_api.phones.verification_check(
				request.session['phone_number'],
				request.session['country_code'],
				form.cleaned_data['token']
			)
			if verification.ok():
				request.session['is_verified'] = True
				if not Profile.objects.filter(user=request.user).exists():
					Profile.objects.create(user=request.user, phone=request.session['phone_number'], country_code=request.session['country_code'])
				else:
					request.user.profile.phone = request.session['phone_number']
					request.user.profile.country_code = request.session['country_code']
					request.user.profile.save()
				return redirect('auths:phoneVerified')
			else:
				for error_msg in verification.errors().values():
					form.add_error(None, error_msg)
	else:
		form = TokenForm()
	return render(request, 'auths/tokenverify.html', {'form': form})


def phoneVerified(request):
	if not request.session.get('is_verified'):
		return redirect('auths:phoneVerification')
	return render(request, 'auths/phoneverified.html', {'phoneNumber':request.session['phone_number']})

