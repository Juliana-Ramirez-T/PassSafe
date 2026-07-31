import secrets
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .forms import PasswordGeneratorForm
from .services import PasswordGeneratorService


@login_required
def generate_password_view(request):
    generated = ''
    strength = 0
    if request.method == 'POST':
        form = PasswordGeneratorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            generated = PasswordGeneratorService.generate(
                length=data['length'],
                use_uppercase=data['use_uppercase'],
                use_lowercase=data['use_lowercase'],
                use_numbers=data['use_numbers'],
                use_symbols=data['use_symbols'],
                use_diceware=data['use_diceware'],
            )
            strength = PasswordGeneratorService.calculate_strength(generated, data['use_diceware'])
    else:
        form = PasswordGeneratorForm()
    return render(request, 'generator/index.html', {
        'form': form,
        'generated': generated,
        'strength': strength,
    })


@login_required
def generator_api_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

    form = PasswordGeneratorForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    data = form.cleaned_data
    generated = PasswordGeneratorService.generate(
        length=data['length'],
        use_uppercase=data['use_uppercase'],
        use_lowercase=data['use_lowercase'],
        use_numbers=data['use_numbers'],
        use_symbols=data['use_symbols'],
        use_diceware=data['use_diceware'],
    )
    strength = PasswordGeneratorService.calculate_strength(generated, data['use_diceware'])
    return JsonResponse({'password': generated, 'strength': strength})
