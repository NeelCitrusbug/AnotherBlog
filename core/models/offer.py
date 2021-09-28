from django.db.models import CharField
from django.db import models
from django.utils.translation import ugettext_lazy as _

# ----------------------------------------------------------------------
# Offer Model
# ----------------------------------------------------------------------


class Offer(models.Model):

    """This model stores the data into Offer table in db"""

    title = CharField(_("Title"), max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    icon = models.FileField(
        upload_to="icon", blank=True, null=True, verbose_name="Icon"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def __str__(self):
        return "{0}".format(self.title)
