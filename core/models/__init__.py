from django.contrib.auth.models import Group
from django.conf import settings
from rest_framework.authtoken.models import Token as DefaultTokenModel
from core.utils import import_callable

# Register your models here.

from .users import User
from .card_details import Card
from .influencer_category import Category
from .userprofile import UserProfile
from .subscription_plan import SubscriptionPlan
from .subscriptin_order import SubscriptionOrder
from .event_class import EventClass
from .event_order import EventOrder
from .event_practice_audience_qa import EventPracticeAudienceQA
from .event import Event
from .offer import Offer
from .influencer_offer import InfluencerOffer
from .faq import Faq
from .agenda import Agenda
from .banner import Banner
from .contact_us import ContactUs
from .credit import Credit
from .credit_order import CreditOrder
from .transaction_log import Transactionlog
from .influncer_transferred_money import InfluencerTransferredMoney
from .evnt_script import EventScript

TokenModel = import_callable(
    getattr(settings, "REST_AUTH_TOKEN_MODEL", DefaultTokenModel)
)
