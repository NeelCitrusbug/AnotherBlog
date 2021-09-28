from django.db import models

# ----------------------------------------------------------------------
# InfluencerTransferredMoney Model
# ----------------------------------------------------------------------


class InfluencerTransferredMoney(models.Model):

    """This model stores the data into InfluencerTransferredMoney table in db"""

    STATUS = [("success", "Success"), ("fail", "Fail")]
    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="user_influncer",
        null=True,
        blank=True,
    )
    transfer_amount = models.CharField(default=0, blank=True, null=True, max_length=222)
    total_amount = models.CharField(default=0, blank=True, null=True, max_length=222)
    kuzo_amount = models.CharField(default=0, blank=True, null=True, max_length=222)

    status = models.CharField(
        max_length=222, blank=True, null=True, choices=STATUS, default="fail"
    )
    transaction_id = models.CharField(
        max_length=222,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Influencer Transferred Money"
        verbose_name_plural = "Influencer Transferred Money"

    def __str__(self):
        return "{0}".format(self.transfer_amount)
