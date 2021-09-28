from django.core.management.base import BaseCommand
from datetime import datetime
from dateutil import relativedelta
from core.utils import MyStripe

from core.models import SubscriptionOrder, UserProfile

today = datetime.now().date()
nextmonth = datetime.today() + relativedelta.relativedelta(months=1)


class Command(BaseCommand):

    help = "Update credit"

    def handle(self, *args, **options):
        check_active_plan = SubscriptionOrder.objects.filter(plan_status="active", expire_date__date=today)
        try:
            for obj in check_active_plan:
                if obj.plan_status=="active":
                    get_user_profile = UserProfile.objects.filter(user__id=obj.user.id).first()
                    if get_user_profile.subscription:
                        stripe = MyStripe()
                        check_stripe_status = stripe.RetrieveSubscription(get_user_profile.stripe_subscription_id)
                        check_invoice = stripe.InvoiceStatus(check_stripe_status['latest_invoice'])
                        if check_stripe_status.status=="active" and check_invoice['status']=='paid':
                            get_user_profile.credit = int(get_user_profile.credit) + int(get_user_profile.subscription.number_of_credit)
                            get_user_profile.save()
                            obj.expire_date=nextmonth
                            obj.save()
                       
                        print(".........................................success")
            print(".........................................success")
            self.stdout.write(self.style.SUCCESS("Successfully updated credit"))
        except:
            self.stdout.write(self.style.ERROR("Error in credit update"))
