from datetime import datetime

from django.test import TestCase

from apps.tasks.factories import TaskFactory
from apps.tasks.models import Task


class TaskTestCase(TestCase):
    def test_performed_at_cannot_be_in_the_future(self):
        task = TaskFactory(performed_at=datetime(9999, 12, 31))
