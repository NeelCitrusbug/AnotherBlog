from django.db import models


# ----------------------------------------------------------------------
# Event Model
# ----------------------------------------------------------------------


class EventOrder(models.Model):
  
    """This model stores the data into Event Order table in db"""

    ORDER_STATUS = [("success", "Success"), ("pending", "Pending")]

    TRANSACTION_TYPES = [
        ("credit", "Credit"),
        ("direct_purchase", "Direct_purchase"),
    ]

    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="eventorder_user",
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        "core.event",
        on_delete=models.CASCADE,
        related_name="evntorder_order",
        null=True,
        blank=True,
    )
    used_credit = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name="Used credit"
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
    transaction_type = models.CharField(
        max_length=222,
        blank=True,
        null=True,
        choices=TRANSACTION_TYPES,
        default="credit",
    )

    class Meta:
        verbose_name = "Event Order"
        verbose_name_plural = "Event Order"

    def __str__(self):
        return "{0}".format(self.event.event_class.name)
