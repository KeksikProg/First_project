from django import forms
from .models import Post
from django.forms import inlineformset_factory
from .models import AdditionalImage
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Comment

class ChangeUserInfoForm(forms.ModelForm):
	email = forms.EmailField(required = True, label = 'Адрес электронной почты')

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
		widgets = {'created_at' : forms.HiddenInput, 'author' : forms.HiddenInput}

AIFormSet = inlineformset_factory(Post, AdditionalImage, fields = '__all__')

class UserRegForm(forms.ModelForm):
	email = forms.EmailField(
		required = True,
		label = 'Электронная почта')
	pass1 = forms.CharField(
		label = 'Пароль',
		widget = forms.PasswordInput,
		help_text = password_validation.password_validators_help_text_html())
	pass2 = forms.CharField(
		label = 'Введите пароль повторно',
		widget = forms.PasswordInput,
		help_text = password_validation.password_validators_help_text_html())

	def clean(self):
		passw1 = self.cleaned_data['pass1']
		if passw1:
			password_validation.validate_password(passw1)
		super().clean()
		passw2 = self.cleaned_data['pass2']
		if passw1 and passw2 and passw1 != passw2:
			errors = {'pass2' : ValidationError(
				'Введенные пароли не совпадают',
				code = 'password_missmatch')}
			raise ValidationError(errors)

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data['pass1'])
		if commit:
			user.save()
		return user

	class Meta:
		model = User
		fields = ('username', 'email', 'pass1', 'pass2', 'first_name', 'last_name')

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = '__all__'
		widgets = {'post':forms.HiddenInput, 'author':forms.HiddenInput}

