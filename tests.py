from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.authentications.factories import UserFactory, Role


class BaseTestCase(TestCase):
    def setUp(self):
        # super().setUp()
        self.client = APIClient()
        self.manager = UserFactory(role=Role.MANAGER)
        self.technician = UserFactory(role=Role.TECHNICIAN)

    def login_as_manager(self):
        token, *_ = Token.objects.get_or_create(user=self.manager)
        return self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}',
        )

    def login_as_technician(self):
        token, *_ = Token.objects.get_or_create(user=self.technician)
        return self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.key}',
        )
