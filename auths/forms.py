from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from auths.models import Profile
import phonenumbers

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


# class ProfileCollectionForm(forms.Form):
# 	phone = forms.CharField(max_length=10, required=True)

# 	def clean_phone(self):
# 		print("Cleaning phone")
# 		phone = self.cleaned_data['phone']
# 		if Profile.objects.filter(phone=phone).exists():
# 			raise ValidationError("Phone Number already exists")
# 		return phone

# 	def save(self, user):
# 		phone = self.cleaned_data['phone']
# 		if Profile.objects.filter(user=user).exists():
# 			profile = Profile.objects.get(user=user)
# 			profile.phone = phone
# 			profile.save()
# 		else:
# 			Profile.objects.create(user=user, phone=phone)


class BootstrapInput(forms.TextInput):
	def __init__(self, placeholder, size=12, *args, **kwargs):
		self.size = size
		super(BootstrapInput, self).__init__(attrs={
			'class': 'form-control input-sm',
			'placeholder': placeholder
		})

	def bootwrap_input(self, input_tag):
		classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

		return '''<div class="{classes}">
					<div class="form-group">{input_tag}</div>
				  </div>
			   '''.format(classes=classes, input_tag=input_tag)

	def render(self, *args, **kwargs):
		input_tag = super(BootstrapInput, self).render(*args, **kwargs)
		return self.bootwrap_input(input_tag)



class PhoneVerificationForm(forms.Form):
	country_code = forms.CharField(
		widget=BootstrapInput('Country Code', size=3))
	phone_number = forms.CharField(
		widget=BootstrapInput('Phone Number', size=10))
	via = forms.ChoiceField(
		choices=[('sms', 'SMS'), ('call', 'Call')])

	def clean_country_code(self):
		country_code = self.cleaned_data['country_code']
		if not country_code.startswith('+'):
			country_code = '+' + country_code
		return country_code

	def clean(self):
		data = self.cleaned_data
		
		phone_number = self.cleaned_data['country_code'] + self.cleaned_data['phone_number']
		try:
			phone_number = phonenumbers.parse(phone_number, None)
			if not phonenumbers.is_valid_number(phone_number):
				self.add_error('phone_number', 'Invalid phone number')
			print(phone_number)
		except NumberParseException as e:
			self.add_error('phone_number', e)


class TokenForm(forms.Form):
	token = forms.CharField(
		widget=BootstrapInput('Verification Token', size=6))
