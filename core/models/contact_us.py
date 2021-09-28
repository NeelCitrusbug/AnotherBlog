from django.db import models

# ----------------------------------------------------------------------
# Contact Us Model
# ----------------------------------------------------------------------


class ContactUs(models.Model):

    """This model stores the data into Event table in db"""

    email = models.CharField(
        max_length=222, blank=True, null=True, verbose_name="Email"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Mailing list"
        verbose_name_plural = "Mailing list"

    def __str__(self):
        return "{0}".format(self.email)
