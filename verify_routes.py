import urllib.request
from urllib.error import HTTPError, URLError

urls = [
    'http://127.0.0.1:8001/',
    'http://127.0.0.1:8001/accounts/login/',
    'http://127.0.0.1:8001/accounts/register/',
    'http://127.0.0.1:8001/vault/',
]

for url in urls:
    try:
        with urllib.request.urlopen(url) as r:
            data = r.read(8192).decode('utf-8', errors='replace')
            print('URL:', url)
            print('Status:', r.status)
            print('Contains base:', 'PassSafe' in data)
            print('Contains sidebar:', 'class="sidebar"' in data or 'class="menu-item"' in data)
            print('CSS loaded:', 'css/base.css' in data)
            print('TemplateDoesNotExist:', 'TemplateDoesNotExist' in data)
            print('NoReverseMatch:', 'NoReverseMatch' in data)
            print('---')
    except HTTPError as e:
        print('URL ERROR', url, e.code, e.reason)
        content = e.read().decode('utf-8', errors='replace')
        print(content)
    except URLError as e:
        print('URL ERROR', url, e)
