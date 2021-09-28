from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import (
    User,
    Category,
    Banner,
    ContactUs,
    UserProfile,
    SubscriptionOrder,
    SubscriptionPlan,
    Card,
    CreditOrder,
    Transactionlog,
    Event,
    EventClass,
    EventOrder,
    InfluencerTransferredMoney,
)



admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(SubscriptionOrder)
admin.site.register(Transactionlog)
admin.site.register(Card)
admin.site.register(Event)
admin.site.register(EventClass)
admin.site.register(EventOrder)
admin.site.register(CreditOrder)
admin.site.register(SubscriptionPlan)
admin.site.register(ContactUs)
admin.site.register(Category)
admin.site.register(Banner)
admin.site.register(InfluencerTransferredMoney)

