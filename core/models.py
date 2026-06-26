"""Core app models — intentionally no concrete models; shared abstractions only."""

from django.db import models


class ValidatedModel(models.Model):
    """Base model that enforces field validation on every save."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
