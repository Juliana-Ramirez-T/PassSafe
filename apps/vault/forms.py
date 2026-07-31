from django import forms
from .models import Credential


class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ['service_name', 'category', 'url', 'username', 'password', 'notes']
        widgets = {
            'service_name': forms.TextInput(attrs={'placeholder': 'Ej: GitHub, Netflix'}),
            'category': forms.Select(),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'usuario@ejemplo.com'}),
            'password': forms.PasswordInput(render_value=True, attrs={'placeholder': 'Contraseña segura'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Información adicional, preguntas de seguridad...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_name'].label = 'Servicio'
        self.fields['service_name'].required = True
        self.fields['category'].label = 'Categoría'
        self.fields['url'].label = 'Sitio'
        self.fields['username'].label = 'Usuario'
        self.fields['username'].required = True
        self.fields['password'].label = 'Contraseña'
        self.fields['password'].required = True
        self.fields['notes'].label = 'Notas'

    def clean(self):
        cleaned_data = super().clean()
        service_name = cleaned_data.get('service_name')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not service_name:
            self.add_error('service_name', 'El servicio es obligatorio.')
        if not username:
            self.add_error('username', 'El usuario es obligatorio.')
        if not password:
            self.add_error('password', 'La contraseña es obligatoria.')

        return cleaned_data
