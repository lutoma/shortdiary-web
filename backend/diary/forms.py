import django.forms as forms
from diary.models import Post, DiaryUser
from hcaptcha.fields import hCaptchaField


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('text', 'mood', 'date', 'image', 'location_lat',
			'location_lon', 'location_verbose', 'public', 'part_of')


class SignUpForm(forms.ModelForm):
	hcaptcha = hCaptchaField()

	class Meta:
		model = DiaryUser
		fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
	username = forms.CharField(max_length=200)
	password = forms.CharField(max_length=200)


class AccountSettingsForm(forms.Form):
	email = forms.EmailField(max_length=100)
	geolocation_enabled = forms.BooleanField(required=False)
