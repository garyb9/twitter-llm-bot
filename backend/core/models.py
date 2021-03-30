import uuid
import json
import requests
import threading
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres import fields

# -------------------------------------------------
# ---------------------- TokenURI --------------------
# -------------------------------------------------
class TokenURIManager(models.Manager):
    """ Represents a basic TokenURI Model Manager."""
    
    def create_TokenURI(self, **validated_data):
        tokenURI = TokenURI.objects.get_or_create(
            address=validated_data["address"],
            name=validated_data["name"],
            description=validated_data["description"],
            imageURL=validated_data["imageURL"],
            traits=validated_data["traits"],
        )[0]
        tokenURI.save(using=self._db)
        return tokenURI


class TokenURI(models.Model):
    """ Represents a basic TokenURI Model."""

    id          = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, verbose_name=_('Unique ID'))
    address     = models.CharField(default=None, max_length=255, verbose_name=_('Wallet Address'))

    name        = models.CharField(default=None, max_length=255, blank=True, null=True, verbose_name=_('Name'))
    description = models.CharField(default=None, max_length=255, blank=True, null=True, verbose_name=_('Description'))
    imageURL    = models.URLField(default=None, null=True, blank=True, verbose_name=_('Image URL'))
    traits      = fields.ArrayField(default=list, base_field=models.JSONField(default=dict), verbose_name=_('Traits'))

    objects     = TokenURIManager()

    def __str__(self):
        return str(id)
