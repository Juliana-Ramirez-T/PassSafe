from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.audit.services import SecurityAuditService
from apps.vault.models import Credential


class SecurityAuditServiceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='audit_user',
            email='audit@example.com',
            password='StrongPass!123'
        )

    def test_analyze_no_credentials_returns_perfect_score(self):
        result = SecurityAuditService.analyze(self.user.credentials.all())

        self.assertEqual(result['total'], 0)
        self.assertEqual(result['weak_count'], 0)
        self.assertEqual(result['reused_count'], 0)
        self.assertEqual(result['score'], 100)
        self.assertIn('Agrega tus primeras credenciales para iniciar la auditoría.', result['recommendations'])

    def test_analyze_weak_password_is_detected(self):
        Credential.objects.create(
            owner=self.user,
            service_name='Test Service',
            category='other',
            username='user@example.com',
            password='12345',
        )

        result = SecurityAuditService.analyze(self.user.credentials.all())

        self.assertEqual(result['total'], 1)
        self.assertEqual(result['weak_count'], 1)
        self.assertEqual(result['reused_count'], 0)
        self.assertEqual(result['score'], 90)
        self.assertEqual(len(result['weak_list']), 1)
        self.assertEqual(result['weak_list'][0].password, '12345')

    def test_analyze_reused_passwords_are_detected(self):
        Credential.objects.create(
            owner=self.user,
            service_name='Service One',
            category='other',
            username='user1@example.com',
            password='Password123!'
        )
        Credential.objects.create(
            owner=self.user,
            service_name='Service Two',
            category='other',
            username='user2@example.com',
            password='Password123!'
        )

        result = SecurityAuditService.analyze(self.user.credentials.all())

        self.assertEqual(result['total'], 2)
        self.assertEqual(result['weak_count'], 0)
        self.assertEqual(result['reused_count'], 1)
        self.assertEqual(result['score'], 95)
        self.assertEqual(len(result['reused_list']), 2)
        self.assertEqual({cred.password for cred in result['reused_list']}, {'Password123!'})

    def test_score_decreases_with_weak_and_reused_passwords(self):
        Credential.objects.create(
            owner=self.user,
            service_name='Service A',
            category='other',
            username='usera@example.com',
            password='weak'
        )
        Credential.objects.create(
            owner=self.user,
            service_name='Service B',
            category='other',
            username='userb@example.com',
            password='CommonPass123!'
        )
        Credential.objects.create(
            owner=self.user,
            service_name='Service C',
            category='other',
            username='userc@example.com',
            password='CommonPass123!'
        )

        result = SecurityAuditService.analyze(self.user.credentials.all())

        self.assertEqual(result['total'], 3)
        self.assertEqual(result['weak_count'], 1)
        self.assertEqual(result['reused_count'], 1)
        self.assertEqual(result['score'], 85)
