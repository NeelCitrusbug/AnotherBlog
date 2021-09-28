from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models

# ----------------------------------------------------------------------
# Event Catgory Model
# ----------------------------------------------------------------------


class TimeZone(models.Model):
    """This model stores the data into Class table in db"""

    name = CharField(_("Name"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Time Zone"
        verbose_name_plural = "Time Zone"

    def __str__(self):
        return "{0}".format(self.name)
