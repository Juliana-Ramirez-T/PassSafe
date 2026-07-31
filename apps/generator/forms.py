from django import forms


class PasswordGeneratorForm(forms.Form):
    length = forms.IntegerField(
        label='Longitud',
        min_value=4,
        max_value=64,
        initial=16,
        widget=forms.NumberInput(attrs={'class': 'short-input', 'min': 4, 'max': 64}),
    )
    use_uppercase = forms.BooleanField(label='Mayúsculas', required=False, initial=True)
    use_lowercase = forms.BooleanField(label='Minúsculas', required=False, initial=True)
    use_numbers = forms.BooleanField(label='Números', required=False, initial=True)
    use_symbols = forms.BooleanField(label='Símbolos', required=False, initial=True)
    use_diceware = forms.BooleanField(label='Frase Diceware', required=False)

    def clean(self):
        cleaned_data = super().clean()
        use_diceware = cleaned_data.get('use_diceware')
        length = cleaned_data.get('length')
        use_uppercase = cleaned_data.get('use_uppercase')
        use_lowercase = cleaned_data.get('use_lowercase')
        use_numbers = cleaned_data.get('use_numbers')
        use_symbols = cleaned_data.get('use_symbols')

        if use_diceware:
            if length is not None and (length < 4 or length > 12):
                self.add_error('length', 'El número de palabras debe estar entre 4 y 12 para Diceware.')
        else:
            if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
                raise forms.ValidationError('Selecciona al menos un tipo de carácter para la contraseña.')