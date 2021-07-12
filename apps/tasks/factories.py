from django.db.models import signals
import factory

from apps.authentications.factories import UserFactory
from apps.tasks.models import Task


@factory.django.mute_signals(signals.pre_save, signals.post_save)
class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
        # django_get_or_create = ("id",)

    summary = factory.Faker('text')
    user = factory.SubFactory(UserFactory)
