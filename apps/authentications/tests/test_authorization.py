from apps.authentications.factories import UserFactory, USER_PASSWORD
from tests import BaseTestCase


class TokenAuthenticationTestCase(BaseTestCase):
    BASE_URL = '/api-token-auth/'

    def test_user_can_obtain_their_token(self):
        # ARRANGE
        user = UserFactory()
        payload = {
            'username': user.username,
            'password': USER_PASSWORD,
        }

        # ACT
        response = self.client.post(self.BASE_URL, payload, format='json')

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get('token'))
