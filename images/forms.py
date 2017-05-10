from django import forms
from .models import Image
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title','image','description')
		widgets = {

		}