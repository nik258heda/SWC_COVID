from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from auths.models import Profile


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=100, required=True)
	last_name = forms.CharField(max_length=100, required=True)

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email already exists")
		return email

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProfileCollectionForm(forms.Form):
	phone = forms.CharField(max_length=10, required=True)

	def clean_phone(self):
		print("Cleaning phone")
		phone = self.cleaned_data['phone']
		if Profile.objects.filter(phone=phone).exists():
			raise ValidationError("Phone Number already exists")
		return phone

	def save(self, user):
		phone = self.cleaned_data['phone']
		if Profile.objects.filter(user=user).exists():
			profile = Profile.objects.get(user=user)
			profile.phone = phone
			print("phone !!!!!!!!!!!!!!!!11", phone)
			profile.save()
		else:
			Profile.objects.create(user=user, phone=phone)
