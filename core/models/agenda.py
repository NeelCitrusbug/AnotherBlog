from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models

# ----------------------------------------------------------------------
# Agenda Model
# ----------------------------------------------------------------------


class Agenda(models.Model):

    """This model stores the data into Agenda table in db"""

    event = models.ForeignKey(
        "core.event",
        on_delete=models.CASCADE,
        related_name="evnt_agenda",
        null=True,
        blank=True,
    )
    title = CharField(_("Title"), max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agenda"

    def __str__(self):
        return "{0}".format(self.title)
