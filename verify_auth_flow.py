import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'passsafe.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()
username = f'testuser_{uuid.uuid4().hex[:8]}'
email = f'{username}@example.com'
password = 'StrongPass123!'

print('Registering user:', username, email)
register_response = client.post(
    '/accounts/register/',
    {
        'username': username,
        'email': email,
        'password1': password,
        'password2': password,
    },
    follow=True,
)
print('Register status:', register_response.status_code)
print('Register redirects:', register_response.redirect_chain)
print('Register final path:', register_response.request['PATH_INFO'])
print('Register contains login form:', 'Iniciar Sesión' in register_response.content.decode('utf-8', errors='replace'))

user_exists = User.objects.filter(username=username, email=email).exists()
print('User created in DB:', user_exists)

if not user_exists:
    raise SystemExit('User was not created.')

print('Logging in...')
login_response = client.post(
    '/accounts/login/',
    {'username': username, 'password': password},
    follow=True,
)
print('Login status:', login_response.status_code)
print('Login redirects:', login_response.redirect_chain)
print('Login final path:', login_response.request['PATH_INFO'])
print('Login page contains dashboard:', '/vault/' in login_response.request['PATH_INFO'])
print('Login response contains CSS:', 'css/base.css' in login_response.content.decode('utf-8', errors='replace'))
print('Login response contains sidebar:', 'class="sidebar"' in login_response.content.decode('utf-8', errors='replace'))
print('Login response contains username:', username in login_response.content.decode('utf-8', errors='replace'))

print('Accessing /vault/ after login...')
vault_response = client.get('/vault/', follow=True)
print('Vault status:', vault_response.status_code)
print('Vault final path:', vault_response.request['PATH_INFO'])
print('Vault contains sidebar:', 'class="sidebar"' in vault_response.content.decode('utf-8', errors='replace'))
print('Vault contains username:', username in vault_response.content.decode('utf-8', errors='replace'))
print('Vault contains CSS:', 'css/base.css' in vault_response.content.decode('utf-8', errors='replace'))

print('Logging out...')
logout_response = client.get('/accounts/logout/', follow=True)
print('Logout status:', logout_response.status_code)
print('Logout redirects:', logout_response.redirect_chain)
print('Logout final path:', logout_response.request['PATH_INFO'])
print('Logout page contains home:', '/' == logout_response.request['PATH_INFO'])
print('Post-logout vault access...')
post_logout_vault = client.get('/vault/', follow=False)
print('Post-logout vault status:', post_logout_vault.status_code)
print('Post-logout vault redirect:', post_logout_vault['Location'] if post_logout_vault.status_code in (301,302) else 'N/A')
print('Post-logout vault is redirect to login:', '/accounts/login/' in (post_logout_vault.get('Location') or ''))
