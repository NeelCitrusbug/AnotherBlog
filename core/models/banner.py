from django.db.models import CharField
from django.db import models
from django.utils.translation import ugettext_lazy as _


# ----------------------------------------------------------------------
# Banner Model
# ----------------------------------------------------------------------


class Banner(models.Model):

    """This model stores the data into Banner table in db"""

    title = CharField(_("Title"), max_length=255,null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.FileField(upload_to='image', blank=True, null=True, verbose_name="image")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True,)


    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return "{0}".format(self.title)
