from django.db import models

# ----------------------------------------------------------------------
# Credit Model
# ----------------------------------------------------------------------


class Credit(models.Model):
    """This model stores the data into Class table in db"""

    price = models.PositiveIntegerField(default=0, blank=True, null=True)
    number_of_credit = models.PositiveIntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Credit"
        verbose_name_plural = "Credits"

    def __str__(self):
        return "{0}".format(self.price)
