from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from core.utils import MyStripe
from .subscriptin_order import SubscriptionOrder

# ----------------------------------------------------------------------
# SubscriptionPlan Model
# ----------------------------------------------------------------------

class SubscriptionPlan(models.Model):

    """This model stores the data into Class table in db"""

    title = CharField(_("Title"), max_length=255, null=True, blank=True, unique=True)
    price = models.FloatField(default=0, blank=True, null=True)
    number_of_credit = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stripe_plan_id = models.CharField(blank=True, null=True, max_length=222)
    stripe_product_id = models.CharField(blank=True, null=True, max_length=222)
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-price"]
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plan"

    def __str__(self):
        return "{0}".format(self.title)

    def save(self, *args, **kwargs):
        return super(SubscriptionPlan, self).save(*args, **kwargs)


@receiver(pre_delete, sender=SubscriptionPlan)
def delete_img_pre_delete_post(sender, instance, *args, **kwargs):
    exist = SubscriptionOrder.objects.filter(subscription__id=instance.id).exists()
    if not exist:
        stripe = MyStripe()
        if instance.stripe_plan_id:
            stripe.deletePlan(instance.stripe_plan_id)
            stripe.deleteProduct(instance.stripe_product_id)
            return


@receiver(post_save, sender=SubscriptionPlan)
def create_plan(sender, instance, created, **kwargs):
    stripe = MyStripe()
    if created:
        product_obj = stripe.createProduct(instance.title)
        plan_id = stripe.createPlan(
            int(instance.price) * 100, "month", product_obj["id"]
        )
        instance.stripe_plan_id = plan_id["id"]
        instance.stripe_product_id = product_obj["id"]
        instance.save()
        return


@receiver(post_save, sender=SubscriptionPlan)
def update_plan(sender, instance, created, **kwargs):
    stripe = MyStripe()
    if not created and instance.stripe_product_id:
        stripe.modifyProduct(instance.stripe_product_id, instance.title)
        return