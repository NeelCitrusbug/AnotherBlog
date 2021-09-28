from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models

# ----------------------------------------------------------------------
# Credit/Debit Card Model
# ----------------------------------------------------------------------


class Card(models.Model):

    """This model stores the data into Card table in db"""

    user = models.ForeignKey("core.user", on_delete=models.CASCADE)
    stripe_card_id = CharField(_("Stripe cusotmer Id"), max_length=255, blank=True)
    last4 = CharField(_("Last 4 digits"), max_length=255, blank=True)
    card_expiration_date = models.CharField(max_length=222, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def __str__(self):
        return "{0}".format(self.user)
