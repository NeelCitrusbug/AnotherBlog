from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

# ------------------------------------------------------------------------
# User Model
# ------------------------------------------------------------------------


class User(AbstractUser):

    """This model stores the data into User table in db"""

    name = CharField(_("Name"), max_length=255, blank=True, null=True)
    email = models.EmailField(
        max_length=255, unique=True, blank=True, null=True, verbose_name="Email"
    )
    is_influencer = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Influencer"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )
    customer_id = CharField(
        _("Customer Id"),
        max_length=255,
        blank=True,
        null=True,
    )
    firebase_token = models.TextField(
        _("Firebase Token"),
        blank=True,
        null=True,
    )
    user_uuid = models.UUIDField(blank=True, null=True)
    influencer_stripe_account_id = models.CharField(max_length=222, null=True, blank=True, verbose_name='Influencer stripe id')
    earned_money = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse("core:user-detail", kwargs={"name": self.name})

    def __str__(self):
        return "{0}".format(self.name)
