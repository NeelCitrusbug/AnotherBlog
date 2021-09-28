from django.db import models

# ----------------------------------------------------------------------
# Transaction log Model
# ----------------------------------------------------------------------


class Transactionlog(models.Model):

    """This model stores the data into Transactionlog table in db"""

    TRANSACION_STATUS = [("success", "Success"), ("pending", "Pending")]
    TRANSACTION_TYPES = [
        ("credit", "Credit"),
        ("direct_purchase", "Direct_purchase"),
        ("subscription", "Subscription"),
    ]
   
    CREDIT_TYPES = [("credit", "Credit"), ("debit", "Debit")]
   
    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="transaction_user",
        null=True,
        blank=True,
    )
    transaction_type = models.CharField(
        max_length=222, blank=True, null=True, choices=TRANSACTION_TYPES
    )
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    credit = models.PositiveIntegerField(default=0, blank=True, null=True)
    types = models.CharField(
        max_length=222, blank=True, null=True, choices=CREDIT_TYPES
    )
    transaction_status = models.CharField(
        max_length=222,
        blank=True,
        null=True,
        choices=TRANSACION_STATUS,
        default="pending",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    transaction_id = models.CharField(max_length=222, blank=True, null=True)

    class Meta:
        verbose_name = "Transaction log"
        verbose_name_plural = "Transaction log"

    def __str__(self):
        return "{0}".format(self.credit)
