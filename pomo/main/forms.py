from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    
	email = forms.EmailField(required=True)


	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class MainForm(forms.Form):
	title = forms.CharField(label='title',max_length=50,required=True)
	year = forms.CharField(label='year',max_length=20,required=False)
	watched = forms.BooleanField(label='have you watched it')


class SearchForm(forms.Form):
	tit = forms.CharField(label='title',max_length=50,required=True)
