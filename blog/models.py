from django.db import models
from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name", unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="author")
    title = models.CharField(max_length=200, verbose_name="title")
    category = models.ManyToManyField(Category,verbose_name="categories")
    text = models.TextField(verbose_name="description")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="date when post created")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="date when post published")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):  
        return self.title


#CUSTOM ADMIN

# ------------------------------------------------------------------------
# User Model
# --

# class User(AbstractUser):

#     """This model stores the data into User table in db"""

#     name = CharField(_("Name"), max_length=255, blank=True, null=True)
#     email = models.EmailField(
#         max_length=255, unique=True, blank=True, null=True, verbose_name="Email"
#     )
#     is_influencer = models.BooleanField(
#         default=False, blank=True, null=True, verbose_name="Influencer"
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         blank=True,
#         null=True,
#     )
#     updated_at = models.DateTimeField(
#         auto_now=True,
#         blank=True,
#         null=True,
#     )
#     customer_id = CharField(
#         _("Customer Id"),
#         max_length=255,
#         blank=True,
#         null=True,
#     )
#     firebase_token = models.TextField(
#         _("Firebase Token"),
#         blank=True,
#         null=True,
#     )
#     user_uuid = models.UUIDField(blank=True, null=True)
#     influencer_stripe_account_id = models.CharField(max_length=222, null=True, blank=True, verbose_name='Influencer stripe id')
#     earned_money = models.PositiveIntegerField(default=0, blank=True, null=True)

#     class Meta:
#         verbose_name = "User"
#         verbose_name_plural = "Users"

#     def get_absolute_url(self):
#         return reverse("core:user-detail", kwargs={"name": self.name})

#     def __str__(self):
#         return "{0}".format(self.name)





# # ----------------------------------------------------------------------
# # User Profile Model
# # ----------------------------------------------------------------------


# class UserProfile(models.Model):

#     """This model stores the data into User Profile table in db"""

#     user = models.ForeignKey(
#         "core.user",
#         on_delete=models.CASCADE,
#         related_name="user_profile",
#         null=True,
#         blank=True,
#     )
#     influencer = models.ForeignKey(
#         "core.category",
#         on_delete=models.CASCADE,
#         related_name="user_catgeory",
#         null=True,
#         blank=True,
#     )
#     subscription = models.ForeignKey(
#         "core.SubscriptionPlan",
#         on_delete=models.CASCADE,
#         related_name="user_subscription_plan",
#         null=True,
#         blank=True,
#     )
#     photo = models.FileField(
#         upload_to="photo", blank=True, null=True, verbose_name="Photo"
#     )
#     video = models.FileField(
#         upload_to="video", blank=True, null=True, verbose_name="Video"
#     )
#     about = models.TextField(blank=True, null=True, verbose_name="About")
#     credit = models.PositiveIntegerField(
#         default=0, blank=True, null=True, verbose_name="Credit"
#     )
#     follower = models.CharField(
#         default=0, blank=True, null=True, verbose_name="Followers", max_length=222
#     )
#     is_popular = models.BooleanField(
#         default=False, blank=True, null=True, verbose_name="Popular"
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True, blank=True, null=True, verbose_name="Created at"
#     )
#     stripe_subscription_id = models.CharField(max_length=222, blank=True, null=True)

#     class Meta:
#         verbose_name = "User Profile"
#         verbose_name_plural = "User Profile"


#     def __str__(self):
#             return "{0}".format(self.user)




# # ----------------------------------------------------------------------
# # Subscription Order Model
# # ----------------------------------------------------------------------


# class SubscriptionOrder(models.Model):

#     """This model stores the data into Subscription Order table in db"""

#     ORDER_STATUS = [("success", "Success"), ("pending", "Pending")]
#     Plan_STATUS = [("active", "Active"), ("cancel", "Cancel")]
#     user = models.ForeignKey(
#         "core.user",
#         on_delete=models.CASCADE,
#         related_name="subscriptionorder_user",
#         null=True,
#         blank=True,
#     )
#     subscription = models.ForeignKey(
#         "core.SubscriptionPlan",
#         on_delete=models.CASCADE,
#         related_name="subscriptionorder_plan",
#         null=True,
#         blank=True,
#     )
#     amount = models.PositiveIntegerField(default=0, blank=True, null=True)
#     charge_id = models.CharField(max_length=222, blank=True, null=True)
#     ordre_status = models.CharField(
#         max_length=222, blank=True, null=True, choices=ORDER_STATUS, default="pending"
#     )
#     plan_status = models.CharField(
#         max_length=222, blank=True, null=True, choices=Plan_STATUS
#     )
#     stripe_subscription_id = models.CharField(max_length=222, blank=True, null=True)
#     expire_date = models.DateTimeField(
#         blank=True,
#         null=True,
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         verbose_name = "User Subscriptions"
#         verbose_name_plural = "User Subscriptions"

#     def __str__(self):
#         return "{0}".format(self.amount)




# # ----------------------------------------------------------------------
# # Event Model
# # ----------------------------------------------------------------------


# class EventOrder(models.Model):
  
#     """This model stores the data into Event Order table in db"""

#     ORDER_STATUS = [("success", "Success"), ("pending", "Pending")]

#     TRANSACTION_TYPES = [
#         ("credit", "Credit"),
#         ("direct_purchase", "Direct_purchase"),
#     ]

#     user = models.ForeignKey(
#         "core.user",
#         on_delete=models.CASCADE,
#         related_name="eventorder_user",
#         null=True,
#         blank=True,
#     )
#     event = models.ForeignKey(
#         "core.event",
#         on_delete=models.CASCADE,
#         related_name="evntorder_order",
#         null=True,
#         blank=True,
#     )
#     used_credit = models.PositiveIntegerField(
#         default=0, blank=True, null=True, verbose_name="Used credit"
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         blank=True,
#         null=True,
#     )
#     charge_id = models.CharField(max_length=222, blank=True, null=True)
#     order_status = models.CharField(
#         max_length=222, blank=True, null=True, choices=ORDER_STATUS, default="pending"
#     )
#     transaction_type = models.CharField(
#         max_length=222,
#         blank=True,
#         null=True,
#         choices=TRANSACTION_TYPES,
#         default="credit",
#     )

#     class Meta:
#         verbose_name = "Event Order"
#         verbose_name_plural = "Event Order"

#     def __str__(self):
#         return "{0}".format(self.event.event_class.name)
