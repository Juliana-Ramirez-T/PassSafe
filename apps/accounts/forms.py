from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True)
    password1 = forms.CharField(
        label='Contraseña maestra',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Usa una contraseña fuerte y única.',
    )
    password2 = forms.CharField(
        label='Confirmar contraseña maestra',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@ejemplo.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Ya existe una cuenta con ese correo.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        if password:
            validate_password(password, self.instance)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario o correo',
        widget=forms.TextInput(attrs={'placeholder': 'usuario@ejemplo.com'}),
    )
    password = forms.CharField(
        label='Contraseña maestra',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
