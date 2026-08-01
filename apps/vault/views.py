from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Credential, Category
from .forms import CredentialForm


@login_required
def dashboard_view(request):
    query = request.GET.get('q', '').strip()
    credentials = request.user.credentials.all()
    if query:
        credentials = credentials.filter(
            Q(service_name__icontains=query) |
            Q(username__icontains=query) |
            Q(url__icontains=query) |
            Q(category__icontains=query)
        )
    return render(request, 'vault/dashboard.html', {
        'credentials': credentials,
        'query': query,
    })


@login_required
def credential_create_view(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            credential = form.save(commit=False)
            credential.owner = request.user
            credential.save()
            messages.success(request, 'Credencial guardada correctamente.')
            return redirect('vault:dashboard')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = CredentialForm()
    return render(request, 'vault/credential_form.html', {
        'form': form,
        'page_title': 'Agregar Nueva Credencial',
        'subtitle': 'Registra tus accesos con seguridad en tu bóveda.',
        'submit_label': 'Guardar Credencial',
    })


@login_required
def credential_edit_view(request, pk):
    credential = get_object_or_404(Credential, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=credential)
        if form.is_valid():
            form.save()
            messages.success(request, 'Credencial actualizada.')
            return redirect('vault:dashboard')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = CredentialForm(instance=credential)
    return render(request, 'vault/credential_form.html', {
        'form': form,
        'credential': credential,
        'page_title': 'Editar Credencial',
        'subtitle': 'Actualiza los datos de acceso de forma segura.',
        'submit_label': 'Guardar Cambios',
    })


@login_required
def credential_delete_view(request, pk):
    credential = get_object_or_404(Credential, pk=pk, owner=request.user)
    if request.method == 'POST':
        credential.delete()
        messages.success(request, 'Credencial eliminada.')
        return redirect('vault:dashboard')
    return render(request, 'vault/credential_confirm_delete.html', {'credential': credential})
