from random import choice

from django.contrib.auth.hashers import make_password
import factory

from apps.authentications.models import User, Role

USER_PASSWORD = "sword123"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        # django_get_or_create = ("id",)

    username = factory.SelfAttribute('email')
    password = make_password(USER_PASSWORD)
    email = factory.Faker("email")


    role = factory.LazyFunction(lambda: choice([role.value for role in Role]))
