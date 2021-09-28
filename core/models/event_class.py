from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models

# ----------------------------------------------------------------------
# Event Class Model
# ----------------------------------------------------------------------


class EventClass(models.Model):

    """This model stores the data into Event Class table in db"""

    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="event_class_user",
        null=True,
        blank=True,
    )
    name = CharField(_("Name"), max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Event Class"
        verbose_name_plural = "Event Class"

    def __str__(self):
        return "{0}".format(self.name)
