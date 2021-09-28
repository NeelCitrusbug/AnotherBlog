from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models

# ----------------------------------------------------------------------
# Category Model
# ----------------------------------------------------------------------


class Category(models.Model):
    """This model stores the data into Class table in db"""

    name = CharField(_("Name"), max_length=255, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"

    def __str__(self):
        return "{0}".format(self.name)
