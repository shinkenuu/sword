from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(IntEnum):
    MANAGER = 1
    TECHNICIAN = 2


class User(AbstractUser):
    role = models.SmallIntegerField()

    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]

    def __str__(self):
        return f"{self.id} - {self.username}"

    @property
    def is_manager(self):
        return self.role == Role.MANAGER.value

    @property
    def is_technician(self):
        return self.role == Role.TECHNICIAN.value
