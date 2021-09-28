from django.db import models

# ----------------------------------------------------------------------
# User Profile Model
# ----------------------------------------------------------------------


class UserProfile(models.Model):

    """This model stores the data into User Profile table in db"""

    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="user_profile",
        null=True,
        blank=True,
    )
    influencer = models.ForeignKey(
        "core.category",
        on_delete=models.CASCADE,
        related_name="user_catgeory",
        null=True,
        blank=True,
    )
    subscription = models.ForeignKey(
        "core.SubscriptionPlan",
        on_delete=models.CASCADE,
        related_name="user_subscription_plan",
        null=True,
        blank=True,
    )
    photo = models.FileField(
        upload_to="photo", blank=True, null=True, verbose_name="Photo"
    )
    video = models.FileField(
        upload_to="video", blank=True, null=True, verbose_name="Video"
    )
    about = models.TextField(blank=True, null=True, verbose_name="About")
    credit = models.PositiveIntegerField(
        default=0, blank=True, null=True, verbose_name="Credit"
    )
    follower = models.CharField(
        default=0, blank=True, null=True, verbose_name="Followers", max_length=222
    )
    is_popular = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Popular"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, verbose_name="Created at"
    )
    stripe_subscription_id = models.CharField(max_length=222, blank=True, null=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profile"


    def __str__(self):
            return "{0}".format(self.user)


