from datetime import date, timedelta,datetime
from django.db.models import Sum
import stripe

from django.core.management.base import BaseCommand
from django.conf import settings

from core.utils import send_sendgrid_email
from core.models import InfluencerTransferredMoney, EventOrder, User, Event
import pytz



# Date Format

today = date.today()
yesterday = today - timedelta(days=1)

yesterday_date = today - timedelta(days=7)
start_date_week = f"{yesterday_date} 00:00:00"
end_date = f"{yesterday} 23:59:00"

timez_zone= pytz.timezone('America/New_York')
start_date_week = datetime.strptime(start_date_week, '%Y-%m-%d %H:%M:%S')
start_date_week = timez_zone.localize(start_date_week)


class Command(BaseCommand):

    help = "Transfer Fund"

    def handle(self, *args, **options):



        try:

            user = User.objects.filter(is_influencer=True)

            for user_obj in user:

                """ Check influencer stripe """

                if user_obj.influencer_stripe_account_id:
                    connected_stripe_status = stripe.Account.retrieve(
                        str(user_obj.influencer_stripe_account_id)
                    )

                    """ Check influencer stripe card  details"""

                    if connected_stripe_status.details_submitted:

                        """ Check influencer account to any  transaction this week"""

                        transfer = InfluencerTransferredMoney.objects.filter(
                            user__id=user_obj.id,
                            created_at__range=[start_date_week, end_date],
                        )

                        if not transfer:
                            event = EventOrder.objects.filter(
                                event__user_id=user_obj.id,
                                
                                event__is_transfer=False,
                            )

                            for k in event:            

                                if k.event.event_date_time  < start_date_week:

                                    direct_purchase = event.filter(transaction_type="direct_purchase").aggregate(Sum("event__price"))
                                    credit_purchase = event.filter(transaction_type="credit").aggregate(Sum("event__credit_required"))


                                    if direct_purchase["event__price__sum"] is None:
                                        direct_purchase["event__price__sum"]=0

                                    if  credit_purchase['event__credit_required__sum'] is None:
                                        credit_purchase['event__credit_required__sum']=0


                                    credit_amount = credit_purchase['event__credit_required__sum']
                                    total_credit_price  = float(credit_amount) * 0.36

                                    total_amount = direct_purchase["event__price__sum"] + total_credit_price
                                    kuzo_amount = float(float(total_amount) * 10)/100
                                    transfer_amount = total_amount - kuzo_amount

                                    final_transfer = round(transfer_amount,2) 
                                    final_transfer_price =  round(transfer_amount,2) * 100
                                    
                                    try:
                                        transaction = stripe.Transfer.create(
                                            amount=int(final_transfer_price),
                                            currency="usd",
                                            destination=str(user_obj.influencer_stripe_account_id),
                                        )

                                        for k in event:
                                            ob = Event.objects.filter(id=k.event.id).first()
                                            ob.is_transfer = True
                                            ob.save()

                                        InfluencerTransferredMoney.objects.create(user=user_obj, transfer_amount=final_transfer, status="success", transaction_id=transaction.id, kuzo_amount=kuzo_amount, total_amount=total_amount)
                                        print(
                                            ".........................................success"
                                        )

                                    except Exception as e: 
                                        print("....................................................Error", e)

            print(".........................................success")
            self.stdout.write(self.style.SUCCESS("Successfully transfer amount"))

        except:
            print(".........................................Error")
            self.stdout.write(self.style.ERROR("Error in transfer amount"))
