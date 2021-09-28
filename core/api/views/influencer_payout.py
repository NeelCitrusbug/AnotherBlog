import stripe
import time
from django.conf import settings
from core.api.apiviews import MyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import InfluencerTransferredMoney, EventOrder, User, Event
from core.api.serializers import InfluencerTransferredMoneySerializer
from django.db.models import Sum
from datetime import datetime, timedelta

current_datetime =  datetime.now()
start_date = datetime.now() - timedelta(days = 7)



stripe.api_key = settings.API_KEY


class StripeAccountCreateAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:
            request.data._mutable = True


            front_file = request.data['front']
            back_file = request.data['back']


            front=stripe.File.create(purpose="identity_document",file=front_file)
            back=stripe.File.create(purpose="identity_document",file=back_file)


            email=request.user.email       
            create_acc=stripe.Account.create(
            type="custom",
            country=request.data['country'],
            business_type="individual",

            business_profile = {"url": request.data['website_url'], "mcc":"1520"},

            individual={
                "dob":{"day":"01","month":"12","year":"1997",},
                "first_name":request.data['first_name'],
                "last_name":request.data['last_name'],
                "phone":request.data['phone'],
                "email":email,
                "id_number":"012345789",
                "verification": {"document": {"front": front['id'], "back":back['id']}},
                "address":{"line1":request.data['address1'],"line2":request.data['address1'], "city":request.data['city'], "state": request.data['state'], "postal_code":request.data['postal_code'],"country":request.data['country']}
            },
            email=email,
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },

            external_account={
                "object":"bank_account",
                "country": request.data['country'],
                "currency":request.data['currency'],
                "account_holder_name": "{0} {1}".format(request.data['first_name'],request.data['last_name'] ),
                "account_holder_type":"individual",
                "account_number":request.data['account_number'],
                "routing_number":request.data['routing_number'],
            },
            settings = {
                "payouts":{"schedule":{"interval":"weekly", "weekly_anchor":"sunday"}}
            },
            tos_acceptance={
                'date': int(time.time()),
                'ip': '8.8.8.8', 
            }
            )
            ob=User.objects.filter(id=request.user.id).first()
            ob.influencer_stripe_account_id = create_acc.id
            ob.save()

            return Response({"status": "OK", "message": "Successfully created event", "data": create_acc.id})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



class StripeAccountConnectAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:

            try:
                if not request.user.influencer_stripe_account_id:
                    today = datetime.today().strftime('%A')
                    account = stripe.Account.create(
                            type='express',
                            settings = {
                                "payouts":{"schedule":{"interval":"weekly", "weekly_anchor":str(today).lower()}}
                                },
                        )   

                    ob=User.objects.filter(id=request.user.id).first()
                    ob.influencer_stripe_account_id = account.id
                    ob.save()

                    account_links = stripe.AccountLink.create(
                        account=account.id,
                        refresh_url=settings.FRONTEND_STRIPE_RETURN_URL,
                        return_url=settings.FRONTEND_STRIPE_RETURN_URL,
                        type='account_onboarding',
                    )

                    return Response({"status": "OK", "message": "Successfully connected stripe account", "data": account_links})
                else:

                    return Response({"status": "FAIL", "message": "You have already coonected with stripe", "data": []})

           
            except Exception as e:
                return Response({"status": "FAIL", "message": str(e), "data": []})   
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})




class StripeAccountLoginAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:

            try:
                check_status=stripe.Account.retrieve(str(request.user.influencer_stripe_account_id))
                if check_status.details_submitted:
                    link=stripe.Account.create_login_link(str(request.user.influencer_stripe_account_id))
                    return Response({"status": "OK", "message": "Successfully created stripe login url", "data": link})
           
                else:
                    account_links = stripe.AccountLink.create(
                        account=request.user.influencer_stripe_account_id,
                        refresh_url='http://44.225.113.133/influencer-transfer-funds',
                        return_url='http://44.225.113.133/influencer-transfer-funds',
                        type='account_onboarding',
                    )

                    return Response({"status": "OK", "message": "Successfully created stripe registration link", "data": account_links})
           
            except Exception as e:
                return Response({"status": "FAIL", "message": str(e), "data": []})   
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



class StripeAccountDiscoonectAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:

            try:
                if request.user.influencer_stripe_account_id:
                    stripe.Account.delete(request.user.influencer_stripe_account_id)
                    ob=User.objects.filter(id=request.user.id).first()
                    ob.influencer_stripe_account_id = ""
                    ob.save()    
                    return Response({"status": "OK", "message": "Successfully removed stripe accpunt", "data": account_links})
           
            except Exception as e:
                return Response({"status": "FAIL", "message": str(e), "data": []})   
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



class StripeTransferMoneyCreateAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:
            
            if request.user.influencer_stripe_account_id:

                event = EventOrder.objects.filter(event__user_id=request.user.id, event__event_date_time__range=[start_date, current_datetime], event__is_transfer=False)

                if event:
                
                
                    total=event.aggregate(Sum('event__price'))
                    final_transfer = total['event__price__sum']
                
                    transaction=stripe.Transfer.create(
                    amount=int(final_transfer)*100,
                    currency="usd",
                    destination= str(request.user.influencer_stripe_account_id),
                    )

                    transfer = {
                        "user": request.user.id,
                        "amount": int(final_transfer),
                        "status":"success",
                        "transaction_id":transaction.id,
                    }
                    for k in event:
                        ob=Event.objects.filter(id=k.event.id).first()
                        ob.is_transfer=True
                        ob.save()

                    serializer = InfluencerTransferredMoneySerializer(data=transfer)
                    if serializer.is_valid():
                        serializer.save()
            
                        return Response({"status": "OK", "message": "Successfully transfered money", "data": serializer.data})
                    else:
                        return Response({"status": "OK", "message": "Serializer errors", "data": serializer.errors})

                else:

                    return Response({"status": "OK", "message": "Not enough money", "data": []})

            else:
                return Response({"status": "OK", "message": "Please create stripe account & update into kuzo account", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})




class PayoutHistoryAPIView(MyAPIView):

    """
    API View for transaction history
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = InfluencerTransferredMoneySerializer

    def get(self, request):

        if request.user.is_authenticated:

            transaction_history = InfluencerTransferredMoney.objects.filter(user__id=request.user.id).order_by("-created_at")
            serializer = self.serializer_class(
                transaction_history, many=True, context={"request": request}
            )
            return Response(
                {
                    "status": "OK",
                    "message": "Successfully fetched transaction history",
                    "data": serializer.data,
                }
            )
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})




class StripeAccountCheckAPI(MyAPIView):

    """API View to Stripe Account Check API """

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:

            if not request.user.influencer_stripe_account_id:
                return Response({"status": "FAIL", "message": "Please connect account with stripe", "data": []})

            try:
                check_status= stripe.Account.retrieve(str(request.user.influencer_stripe_account_id))
                if check_status.details_submitted:
                    return Response({"status": "OK", "message": "Stripe account is verified", "data": []})
                else:
                    return Response({"status": "FAIL", "message": "Not verified stripe account", "data": []})

            except Exception as e:
                return Response({"status": "FAIL", "message": str(e), "data": []})   
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})