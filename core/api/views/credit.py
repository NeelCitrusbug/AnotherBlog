from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card, User,CreditOrder, UserProfile, Transactionlog, Credit
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_card_object
import stripe as stripeErr
from core.api.serializers import CreditSerializer, CreditOrderListSerializer, TransactionlogSerializer, CreditOrderSerializer, UserDetailsSerializer
from core.utils import Emails
from core.utils import Emails, send_sendgrid_email
from django.conf import settings


# .................................................................................
# Credit Plan API
# .................................................................................


class CreditListAPIView(MyAPIView):

    """
    API View for Credit  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = CreditSerializer

    def get(self, request, format=None):    

        try:
            credit = Credit.objects.all().order_by('price')
            serializer = self.serializer_class(credit, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched credit list", "data": serializer.data})

        except:
            return Response({"status": "FAIL", "message": "Credit plan not found", "data": []})


class CreditPurchaseAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            try:

                stripe = MyStripe()
                user_obj = User.objects.filter(id=request.user.id).first()
                user_plan = UserProfile.objects.filter(user__id=request.user.id).first()
                credit_obj = Credit.objects.filter(id=request.data['credit']).first()

                data = {
                    'source':request.data['stripe_token']
                }

                if not request.user.customer_id:
                    new_stripe_customer = stripe.createCustomer(request.user)
                    user_obj.customer_id = new_stripe_customer['id']
                    user_obj.save()

                new_card = stripe.createCard(user_obj.customer_id, data)
                transaction = stripe.createCharge(credit_obj.price, new_card, user_obj.customer_id)

                credit_order_data = {

                    "user": request.user,
                    "credit" : credit_obj,
                    "amount" : credit_obj.price,
                    "charge_id": transaction['id'] ,
                    "order_status": "success",
                }

                new_credit = CreditOrder.objects.create(**credit_order_data)

                transaction_data = {

                        "user": request.user,
                        "transaction_type" : 'credit',
                        "amount" : credit_obj.price,
                        "credit": credit_obj.number_of_credit,
                        "types": "credit",
                        "transaction_status": "success" ,   
                        "transaction_id": new_credit.id ,       

                    }

                ob=Transactionlog.objects.create(**transaction_data)

                user_plan.credit = int(user_plan.credit) + int(credit_obj.number_of_credit)
                user_plan.save()
                serilizer = CreditOrderListSerializer(new_credit)

                user_serializer = UserDetailsSerializer(user_obj)
                context={"user":user_serializer.data, 'credit_order':serilizer.data}

                send_sendgrid_email(context,"Purchased credit Transaction Receipt",request.user.email, settings.CREDIT_ORDER_TEMPLATE_ID)
                
                return Response({"status": "OK", "message": "Successfully purchased credit", "data": serilizer.data})
                    
            except stripeErr.error.CardError as e:
                body = e.json_body
                err  = body.get('error', {})

                return Response({"status": "FAIL", "message": err['message'], "data": []})

            except stripeErr.error.AuthenticationError as e:

                body = e.json_body
                err  = body.get('error', {})
                return Response({"status": "FAIL", "message": err['message'], "data": []})

    
            except stripeErr.error.InvalidRequestError  as e:
                body = e.json_body
                err  = body.get('error', {})
                return Response({"status": "FAIL", "message": err['message'], "data": []})

            except Exception as e:

                return Response({"status": "FAIL", "message": str(e), "data": []})
