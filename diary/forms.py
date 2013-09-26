import django.forms as forms
from diary.models import Post
from django.contrib.auth.models import User
import datetime
from django.utils.translation import ugettext as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'mood', 'date', 'image', 'location_lat', 'location_lon', 'location_verbose', 'public')

    def clean_date(self):
        date = self.cleaned_data["date"]
        today = datetime.date.today()
        delta = today - date
        
        if delta.days > 1:
            raise forms.ValidationError(_("Invalid date. You can't go that far back."))

        return date

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 200)
    password = forms.CharField(max_length = 200)


class AccountSettingsForm(forms.Form):
    email = forms.EmailField(max_length = 100)
    geolocation_enabled = forms.BooleanField(required = False)
    password = forms.CharField(max_length = 200, required = False)
