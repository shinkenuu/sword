from django.db import models
from apps.tasks.validations import validate_past_or_present


class Task(models.Model):
    summary = models.CharField(max_length=2500, null=False)

    user = models.ForeignKey("authentications.User", null=False, on_delete=models.DO_NOTHING)
    performed_at = models.DateField(null=True, validators=[validate_past_or_present])

    def __str__(self):
        return f"{self.id} - {self.user.username} - {self.summary[:10]}"
