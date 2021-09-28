from django.db import models

# ----------------------------------------------------------------------
# Subscription Order Model
# ----------------------------------------------------------------------


class SubscriptionOrder(models.Model):

    """This model stores the data into Subscription Order table in db"""

    ORDER_STATUS = [("success", "Success"), ("pending", "Pending")]
    Plan_STATUS = [("active", "Active"), ("cancel", "Cancel")]
    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="subscriptionorder_user",
        null=True,
        blank=True,
    )
    subscription = models.ForeignKey(
        "core.SubscriptionPlan",
        on_delete=models.CASCADE,
        related_name="subscriptionorder_plan",
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    charge_id = models.CharField(max_length=222, blank=True, null=True)
    ordre_status = models.CharField(
        max_length=222, blank=True, null=True, choices=ORDER_STATUS, default="pending"
    )
    plan_status = models.CharField(
        max_length=222, blank=True, null=True, choices=Plan_STATUS
    )
    stripe_subscription_id = models.CharField(max_length=222, blank=True, null=True)
    expire_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "User Subscriptions"
        verbose_name_plural = "User Subscriptions"

    def __str__(self):
        return "{0}".format(self.amount)
