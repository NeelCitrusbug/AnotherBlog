# -*- coding: utf-8 -*-
from django.urls import include, path
from django.conf.urls import url

from core.api.views import (
    MyRegisterView,
    LoginView,
    LogoutView,
    ProfileDetailsView,
    ProfileUpdateView,
    ChangeCurrentPassword,
    PasswordResetView,
    PasswordResetConfirmView,
    VerifyEmailView
)

from core.api.views import (
    BookEventAPI,
    CancelSubscriptionAPI,
    ChangeCurrentSubscriptionAPI,
    BannerListAPIView,
    InfluencerListAPIView,
    InfluencerDetailsListAPIView,
    CheckEventBooking,
    BookEventWithCreditAPI,
)


from . import billing_details
from . import subscribe_plan
from . import offer
from . import credit
from . import faq
from . import event
from . import event_class
from . import event_agenda
from . import event_qa
from . import contact_us
from . import user_registred_event
from . import timezone
from . import influencer_category
from . import influencer_earn_money
from . import influencer_payout
from . import influencer_profile
from . import script


urlpatterns = [

    # Authentication

    path("create-account/", MyRegisterView.as_view(), name="create-account"),
    path("login/", LoginView.as_view(), name="core-auth-login"),
    path("logout/", LogoutView.as_view(), name="core-auth-logout"),
    path("profile-details/", ProfileDetailsView.as_view(), name="profile-details"),
    path("profile-update/", ProfileUpdateView.as_view(), name="user-update"),
    path(
        "change-current-password/",
        ChangeCurrentPassword.as_view(),
        name="change-current-password",
    ),
    path("forget-password/", PasswordResetView.as_view(), name="forget-password"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),

    path(
        "set-new-password/", PasswordResetConfirmView.as_view(), name="set-new-password"
    ),

    # User subscription & card

    path("billing-details/", include(billing_details)),
    path("subscribe-plan/", include(subscribe_plan)),
    path("credit/", include(credit)),
    path(
        "cancel-subscription/",
        CancelSubscriptionAPI.as_view(),
        name="cancel-subscription",
    ),
    path(
        "change-subscription/",
        ChangeCurrentSubscriptionAPI.as_view(),
        name="change-subscription",
    ),
    path("book-event/", BookEventAPI.as_view(), name="book-event"),
    path("user-registered-event/", include(user_registred_event)),
    path("check-event/", CheckEventBooking.as_view(), name="check-event"),


    # Influencer side

    path("event/", include(event)),
    path("event-class/", include(event_class)),
    path("event-agenda/", include(event_agenda)),
    path("event-qa/", include(event_qa)),
    path("faq/", include(faq)),
    path("influencer-offer/", include(offer)),
    path("influencer-eran-money-list/", include(influencer_earn_money)),
    path("timezone-list/", include(timezone)),
    path("influencer-payout/", include(influencer_payout)),
    path("influencer-profile/", include(influencer_profile)),
    path("script/", include(script)),


    path("book-event-credit/", BookEventWithCreditAPI.as_view(), name="book-event-credit"),
    # Home page

    path("banner-list/", BannerListAPIView.as_view(), name="banner-list"),
    path(
        "popular-influencer-list/",
        InfluencerListAPIView.as_view(),
        name="popular-influencer-list",
    ),
    path("contact-us/", include(contact_us)),
    path("influencer-category-list/", include(influencer_category)),
    path(
        "influencer-details/<int:pk>",
        InfluencerDetailsListAPIView.as_view(),
        name="influencer-details",
    ),
]
