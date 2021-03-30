import uuid
import json
import requests
import threading
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

# -------------------------------------------------
# ---------------------- TokenURI --------------------
# -------------------------------------------------
class TokenURIManager(models.Manager):
    """ Represents a basic TokenURI Model Manager."""
    
    def create_TokenURI(self, **validated_data):
        tokenURI = TokenURI.objects.get_or_create(
            address=validated_data["address"],
        )[0]
        tokenURI.save(using=self._db)
        return tokenURI


class TokenURI(models.Model):
    """ Represents a basic TokenURI Model."""

    id      = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, verbose_name=_('Unique ID'))
    address = models.CharField(default=None, max_length=255, verbose_name=_('Wallet Address'))

    objects = TokenURIManager()

    def __str__(self):
        return str(id)
