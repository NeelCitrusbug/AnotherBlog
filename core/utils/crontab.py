from core.models import SubscriptionOrder, UserProfile
from .stripe import MyStripe


def my_scheduled_job():

    check_active_plan = SubscriptionOrder.objects.filter(plan_status="active")

    try:
        for obj in check_active_plan:
            if obj.plan_status=="active":
                get_user_profile = UserProfile.objects.filter(user__id=obj.user.id).first()
                if get_user_profile.subscription:
                    stripe = MyStripe()
                    check_stripe_status = stripe.RetrieveSubscription(get_user_profile.stripe_subscription_id)
                    if check_stripe_status.status=="active":
                        get_user_profile.credit = int(get_user_profile.credit) + int(get_user_profile.subscription.number_of_credit)
                        get_user_profile.save()

                    return 'Updated successfully'

    except:
        return 'Error'
   
  