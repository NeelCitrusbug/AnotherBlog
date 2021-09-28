from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card, User, SubscriptionPlan, UserProfile, SubscriptionOrder, Transactionlog, Event, EventOrder
from core.api.serializers import CardSerializer, UserDetailsSerializer,UserProfileSerializer,  EventOrderListSerializer, EventOrderSerializer, SubscriptionPlanSerializer, TransactionlogSerializer, SubscriptionOrderSerializer
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_card_object
import stripe as stripeErr
import datetime
from dateutil import relativedelta
from core.utils import Emails
from core.utils import Emails, send_sendgrid_email
from django.conf import settings


# .................................
# .................................................................................
# Subscription Plan API
# .................................................................................


class SubscriptionPlanListAPIView(MyAPIView):

    """
    API View for Subscription Plan listing
    """

    permission_classes = (AllowAny,)
    serializer_class = SubscriptionPlanSerializer

    def get(self, request, format=None):    

        try:
            plan = SubscriptionPlan.objects.all().order_by('price')
            serializer = self.serializer_class(plan, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched subscription plan list", "data": serializer.data})

        except Card.DoesNotExist:
            return Response({"status": "FAIL", "message": "Subscription plan not found", "data": []})



class CheckEventBooking(MyAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:
            event = Event.objects.filter(id=request.data['event']).first()
            check_participant = EventOrder.objects.filter(user__id=request.user.id, event__id=event.id).exists()

            if check_participant:
                return Response({"status": "OK", "message": "You have already participated in this event", "data": []})

            else:

                return Response({"status": "FAIL", "message": "You have not participated in this event", "data": []})




class BookEventWithCreditAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            user_obj = User.objects.filter(id=request.user.id).first()
            user_plan = UserProfile.objects.filter(user__id=request.user.id).first()
            event = Event.objects.filter(id=request.data['event']).first()
            user_serilizer=UserDetailsSerializer(user_obj)
            check_participant = EventOrder.objects.filter(user__id=request.user.id, event__id=event.id).exists()

            if check_participant:

                return Response({"status": "OK", "message": "You have already participated in this event", "data": []})

            if event.number_of_participants == event.remianing_spots:
                return Response({"status": "OK", "message": "Event is full now", "data": []})
                
            # event registration


            if int(user_plan.credit) < int(event.credit_required):

                return Response({"status": "OK", "message": "Please Change your current subscriptin plan or buy more credit.", "data": []})

            try:
                
                event_order_data = {

                    "user": request.user,
                    "event" : event,
                    "used_credit" : event.credit_required,
                    "order_status": "success",
                    "charge_id": "credit used",

                }

                event.remianing_spots = int(event.remianing_spots) + 1
                event.save()
                event_new = EventOrder.objects.create(**event_order_data)

                transaction_data = {

                        "user": request.user,
                        "transaction_type" : 'credit',
                        "amount" : event.price,
                        "credit": event.credit_required,
                        "types": "debit",
                        "transaction_status": "success" ,   
                        "transaction_id": event_new.id,       

                }

                Transactionlog.objects.create(**transaction_data)
                user_plan.credit =  int(user_plan.credit)  - int(event.credit_required)
                user_plan.save()

                serilzer = EventOrderListSerializer(event_new)

                context={"user":user_serilizer.data, 'event_order':serilzer.data}
                send_sendgrid_email(context,"Event booking Transaction Receipt",request.user.email, settings.EVENT_ORDER_TEMPLATE_ID)
                
                obj = User.objects.filter(id=event.user.id).first()
                if obj:
                    obj.earned_money = float(obj.earned_money) + float(event.price)
                    obj.save()

                return Response({"status": "OK", "message": "Event registration  process completed successfully", "data": serilzer.data})

            except:
                return Response({"status": "FAIL", "message": "Bad request", "data": []})






class BookEventAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            nextmonth = datetime.datetime.today() + relativedelta.relativedelta(months=1)

            stripe = MyStripe()

            user_obj = User.objects.filter(id=request.user.id).first()
            user_plan = UserProfile.objects.filter(user__id=request.user.id).first()
            event = Event.objects.filter(id=request.data['event']).first()
            user_serilizer=UserDetailsSerializer(user_obj)

            check_participant = EventOrder.objects.filter(user__id=request.user.id, event__id=event.id).exists()

            if check_participant:
                return Response({"status": "OK", "message": "You have already participated in this event", "data": []})

            if event.number_of_participants == event.remianing_spots:
                return Response({"status": "OK", "message": "Event is full now", "data": []})

            
            # Check stripe customer id 

            if not request.user.customer_id:
                new_stripe_customer = stripe.createCustomer(request.user)
                user_obj.customer_id = new_stripe_customer['id']
                user_obj.save()

            # New Subscription & event registration

            if request.data['is_subscription_access']=='true':


                if user_plan.subscription :

                    if int(user_plan.credit) < int(event.credit_required):

                        return Response({"status": "OK", "message": "Please Change your current subscriptin plan or buy more credit.", "data": []})

                    else:

                        event_order_data = {

                            "user": request.user,
                            "event" : event,
                            "used_credit" : event.credit_required,
                            "order_status": "success",
                            "charge_id": "credit used",

                        }

                        event.remianing_spots = int(event.remianing_spots) + 1
                        event.save()
                        event_new = EventOrder.objects.create(**event_order_data)

                        transaction_data = {

                                "user": request.user,
                                "transaction_type" : 'credit',
                                "amount" : event.price,
                                "credit": event.credit_required,
                                "types": "debit",
                                "transaction_status": "success" ,   
                                "transaction_id": event_new.id,       

                        }

                        Transactionlog.objects.create(**transaction_data)
                        user_plan.credit =  int(user_plan.credit)  - int(event.credit_required)
                        user_plan.save()

                        serilzer = EventOrderListSerializer(event_new)

                        context={"user":user_serilizer.data, 'event_order':serilzer.data}
                        send_sendgrid_email(context,"Event booking Transaction Receipt",request.user.email, settings.EVENT_ORDER_TEMPLATE_ID)
                        
                        obj = User.objects.filter(id=event.user.id).first()
                        if obj:
                            obj.earned_money = float(obj.earned_money) + float(event.price)
                            obj.save()

                        return Response({"status": "OK", "message": "Event registration  process completed successfully", "data": serilzer.data})


                try:
                    subscription = SubscriptionPlan.objects.filter(id=request.data['subscription']).first()

                    if event.credit_required  > subscription.number_of_credit:

                        return Response({"status": "OK", "message": "This Plan is not enought for this event.Please choose another plan.", "data": []})


                    payment_method = stripe.CreatePaymentMethod(request.data['stripe_token'])

                    Card.objects.create(user=user_obj, stripe_card_id=payment_method.id, last4=payment_method['card']['last4'], card_expiration_date='{0}/{1}'.format(payment_method['card']['exp_month'], payment_method['card']['exp_year']))

                    stripe.PaymentMethodAttach(payment_method.id, user_obj.customer_id)
                
                    subscribe_new_plan = stripe.subscribePlan(user_obj.customer_id, subscription.stripe_plan_id, payment_method.id)
                    
            
                    if subscribe_new_plan['status']=='active':

                        subscripton_data = {
                                "user":request.user,
                                "subscription": subscription,
                                "amount": subscription.price,
                                "charge_id": subscribe_new_plan['id'],
                                "ordre_status":"success",
                                "plan_status":"active",
                                "stripe_subscription_id":subscribe_new_plan['id'],
                                "expire_date": nextmonth,   
                        }

                        event_order_data = {

                            "user": request.user,
                            "event" : event,
                            "used_credit" : event.credit_required,
                            "order_status": "success",
                            "charge_id": "credit used",

                        }

                        user_plan.credit =  int(user_plan.credit) + int(subscription.number_of_credit) - int(event.credit_required)
                        user_plan.subscription = subscription
                        user_plan.stripe_subscription_id = subscribe_new_plan['id']
                        user_plan.save()

                        event.remianing_spots = int(event.remianing_spots) + 1
                        event.save()

                        subscription_new = SubscriptionOrder.objects.create(**subscripton_data)


                        transaction_data = {

                            "user": request.user,
                            "transaction_type" : 'subscription',
                            "amount" : subscription.price,
                            "credit": subscription.number_of_credit,
                            "types": "credit",
                            "transaction_status": "success" ,   
                            "transaction_id": subscription_new.id ,       

                        }
                        Transactionlog.objects.create(**transaction_data)
                        event_new = EventOrder.objects.create(**event_order_data)

                        event_transaction_data = {

                            "user": request.user,
                            "transaction_type" : 'credit',
                            "amount" : event.price,
                            "credit": event.credit_required,
                            "types": "debit",
                            "transaction_status": "success" ,   
                            "transaction_id": event_new.id,       
                        }

                        Transactionlog.objects.create(**event_transaction_data)
                        serilzer = EventOrderListSerializer(event_new)

                        # Email for event 
                        context={"user":user_serilizer.data, 'event_order':serilzer.data}
                        send_sendgrid_email(context,"Event booking Transaction Receipt",request.user.email, settings.EVENT_ORDER_TEMPLATE_ID)

                     
                        # Email for subscription 

                        subscriptin_serializer = SubscriptionOrderSerializer(subscription_new)
                        context={"user":user_serilizer.data, 'subscription_order':subscriptin_serializer.data}
                        send_sendgrid_email(context,"Event booking Transaction Receipt",request.user.email, settings.SUBSCRIPTION_ORDER_TEMPLATE_ID)
                        
                        obj = User.objects.filter(id=event.user.id).first()
                        if obj:
                            obj.earned_money = float(obj.earned_money) + float(event.price)
                            obj.save()

                        return Response({"status": "OK", "message": "Subscription & event registration process completed successfully", "data": serilzer.data})

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

            else:

                try:

                    data={
                        'source':request.data['stripe_token']
                    }

                    new_card = stripe.createCard(user_obj.customer_id, data)

                    transaction = stripe.createCharge(event.price, new_card, user_obj.customer_id)

                    event_order_data = {

                        "user": request.user,
                        "event" : event,
                        "used_credit" : 0,
                        "charge_id":transaction['id'],
                        "order_status": "success",
                        "transaction_type": "direct_purchase",

                    }

                    event_new = EventOrder.objects.create(**event_order_data)


                    transaction_data = {

                            "user": request.user,
                            "transaction_type" : 'direct_purchase',
                            "amount" : event.price,
                            "credit": event.credit_required,
                            "types": "debit",
                            "transaction_status": "success" ,   
                            "transaction_id": event_new.id,       

                        }

                    event.remianing_spots = int(event.remianing_spots) + 1
                    event.save()
                    Transactionlog.objects.create(**transaction_data)

                    serializer = EventOrderListSerializer(event_new)

                    context={"user":user_serilizer.data, 'event_order':serializer.data}
                    send_sendgrid_email(context,"Event booking Transaction Receipt",request.user.email, settings.DIRECT_EVENT_BOOKING)

                    # Update

                    obj = User.objects.filter(id=event.user.id).first()
                    if obj:
                        obj.earned_money = float(obj.earned_money) + float(event.price)
                        obj.save()

                     
                    return Response({"status": "OK", "message": "Event registration process completed successfully", "data": serializer.data})
                
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



class CancelSubscriptionAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            try:
                stripe = MyStripe()
                user_obj = User.objects.filter(id=request.user.id).first()
                user_plan = UserProfile.objects.filter(user__id=request.user.id).first()
                user_serilizer=UserDetailsSerializer(user_obj)
                user_plan_serializer=UserProfileSerializer(user_plan)

                if not user_plan.subscription:
                    return Response({"status": "OK", "message": "No subscription plan active now.", "data":[]})
                
                subscription_order = SubscriptionOrder.objects.filter(user__id=user_obj.id, stripe_subscription_id=user_plan.stripe_subscription_id, plan_status='active')
                
                for cancel in subscription_order:
                    sub_object = subscription_cancel_order = SubscriptionOrder.objects.filter(id=cancel.id).first()
                    sub_object.plan_status='cancel'
                    sub_object.save()

                context={"user":user_serilizer.data, 'user_plan':user_plan_serializer.data}
                send_sendgrid_email(context,"Cancel subscription plan details",request.user.email, settings.CANCEL_SUBSCRIPTION_ORDER_TEMPLATE_ID)
                        
                
                stripe = MyStripe() 
                subscription_stripe = stripe.CancelSubscriptionPlan(user_plan.stripe_subscription_id)  
                user_plan.subscription = None
                user_plan.stripe_subscription_id=''
                user_plan.save()
                return Response({"status": "OK", "message": "Subscription cancelled ", "data":[]})

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


class ChangeCurrentSubscriptionAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            try:
                stripe = MyStripe()
                nextmonth = datetime.datetime.today() + relativedelta.relativedelta(months=1)
                user_obj = User.objects.filter(id=request.user.id).first()
                user_plan = UserProfile.objects.filter(user__id=request.user.id).first()
                subscription = SubscriptionPlan.objects.filter(id=request.data['subscription']).first()
                card = Card.objects.filter(user__id=request.user.id).first()
                user_serilizer=UserDetailsSerializer(user_obj)
                user_plan_serializer=UserProfileSerializer(user_plan)

                # if not user_plan.subscription:
                #     return Response({"status": "OK", "message": "No subscription plan active now.", "data":[]})
              

                if not request.user.customer_id:
                    new_stripe_customer = stripe.createCustomer(request.user)
                    user_obj.customer_id = new_stripe_customer['id']
                    user_obj.save()

                if not card:
                    return Response({"status": "FAIL", "message": "Please update billing details", "data":[]})
                    
                subscribe_new_plan = stripe.subscribePlan(user_obj.customer_id, subscription.stripe_plan_id, card.stripe_card_id)
                
                if subscribe_new_plan['status']=='active':
                    

                    if user_plan.subscription:
                        subscription_order = SubscriptionOrder.objects.filter(user__id=user_obj.id, stripe_subscription_id=user_plan.stripe_subscription_id, plan_status='active')
                        subscription_stripe = stripe.CancelSubscriptionPlan(user_plan.stripe_subscription_id)  
                        for cancel in subscription_order:
                            sub_object = subscription_cancel_order = SubscriptionOrder.objects.filter(id=cancel.id).first()
                            sub_object.plan_status='cancel'
                            sub_object.save()

                        context={"user":user_serilizer.data, 'user_plan':user_plan_serializer.data}
                        send_sendgrid_email(context,"cancel subscription plan details",request.user.email, settings.CANCEL_SUBSCRIPTION_ORDER_TEMPLATE_ID)
                        


                    subscripton_data = {
                            "user":request.user,
                            "subscription": subscription,
                            "amount": subscription.price,
                            "charge_id": subscribe_new_plan['id'],
                            "ordre_status":"success",
                            "plan_status":"active",
                            "stripe_subscription_id":subscribe_new_plan['id'],
                            "expire_date": nextmonth,   
                    }

                    user_plan.credit =  int(user_plan.credit) + int(subscription.number_of_credit)
                    user_plan.subscription = subscription
                    user_plan.stripe_subscription_id = subscribe_new_plan['id']
                    user_plan.save()

                    subscription_new = SubscriptionOrder.objects.create(**subscripton_data)

                    transaction_data = {

                        "user": request.user,
                        "transaction_type" : 'subscription',
                        "amount" : subscription.price,
                        "credit": subscription.number_of_credit,
                        "types": "credit",
                        "transaction_status": "success" ,   
                        "transaction_id": subscription_new.id ,       

                    }
                    Transactionlog.objects.create(**transaction_data)

                    serializer = SubscriptionOrderSerializer(subscription_new)

                    subscriptin_serializer = SubscriptionOrderSerializer(subscription_new)
                    context={"user":user_serilizer.data, 'subscription_order':subscriptin_serializer.data}
                    send_sendgrid_email(context,"New Subscription Transaction Receipt",request.user.email, settings.SUBSCRIPTION_ORDER_TEMPLATE_ID)
                        
                
                    return Response({"status": "OK", "message": "Your plan successfully started now.", "data":serializer.data})

                else:
                    return Response({"status": "FAIL", "message": "Please Update billing details.", "data":[]})



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