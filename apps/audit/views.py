from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import SecurityAuditService


@login_required
def audit_dashboard_view(request):
    credentials = request.user.credentials.all()
    result = SecurityAuditService.analyze(credentials)
    return render(request, 'audit/dashboard.html', result)
