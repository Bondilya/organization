from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import *


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    description = forms.CharField(label='Расскажите о себе', widget=forms.Textarea,
                                  help_text='Ваши качества, навыки и ссылки на соц. сети')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        try:
            password_validation.validate_password(password1)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        if commit:
            user.save()
        user_registrated.send(RegistrationForm, instance=user)
        return user

    class Meta:
        model = Volunteer
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'image', 'description')
        labels = {'username': 'Логин'}


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    description = forms.CharField(label='О себе', widget=forms.Textarea)

    class Meta:
        model = Volunteer
        fields = ('username', 'email', 'first_name', 'last_name', 'image', 'description')
