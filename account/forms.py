from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)




class UserRegistrationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password',
								widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat password',
								widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username','first_name','email')
	def clean_password2(self):
		cd = self.cleaned_data
		if (cd['password1'] == cd['password2']):
			return cd['password2']
		else:
			raise forms.ValidationError('Passwords don\'t match.')
		

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name','email')

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('date_of_birth','photo')