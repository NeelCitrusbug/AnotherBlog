from django.db import models

# ----------------------------------------------------------------------
# Credit Model
# ----------------------------------------------------------------------


class CreditOrder(models.Model):

    """This model stores the data into Credit Order table in db"""

    ORDER_STATUS = [("success", "Success"), ("pending", "Pending")]

    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="creditorder_user",
        null=True,
        blank=True,
    )
    credit = models.ForeignKey(
        "core.credit",
        on_delete=models.CASCADE,
        related_name="credit_order",
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name="amount"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    charge_id = models.CharField(max_length=222, blank=True, null=True)
    order_status = models.CharField(
        max_length=222, blank=True, null=True, choices=ORDER_STATUS, default="pending"
    )

    class Meta:
        verbose_name = "Credit Order"
        verbose_name_plural = "Credit Order"

    def __str__(self):
        return "{0}".format(self.amount)
