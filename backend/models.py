from uuid import uuid4
from django.db import models


class BaseModel(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    id = models.AutoField(primary_key=True, unique=True)

    class Meta:
        abstract = True


class NameAbstractModel(models.Model):

    name = models.CharField(max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CreatedAbstractModel(models.Model):

    created_by = models.ForeignKey(
        'users.User',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        editable=False,
    )

    created_at = models.DateTimeField(
        "Created_at",
        blank=True,
        null=True,
        auto_now_add=True,
        db_index=True,
        editable=False,
    )

    class Meta:
        abstract = True


class ModifiedAbstractModel(models.Model):

    modified_by = models.ForeignKey(
        'users.User',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_modified",
        editable=False,
    )

    modified_at = models.DateTimeField(
        "Modified_at",
        blank=True,
        null=True,
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True


class TrackingAbstractModel(CreatedAbstractModel, ModifiedAbstractModel, BaseModel):

    class Meta:
        abstract = True

    def update_fields(self, **kwargs):
        self._set_fields(**kwargs)
        self.save()

    def _set_fields(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)

    def save_without_signals(self, *args, **kwargs):
        self._disable_signals = True
        self.save()
        self._disable_signals = False
