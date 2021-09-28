from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import stripe as stripeErr
from django.conf import settings

from core.models import Card, User, SubscriptionOrder, UserProfile
from core.api.serializers import CardSerializer, UserDetailsSerializer, CardListSerializer

from core.api.apiviews import MyAPIView
from core.utils import MyStripe
from core.utils import send_sendgrid_email

# .................................................................................
# Credit/Debit Card API
# .................................................................................


class CardAPIView(MyAPIView):
    """
    API View for Card listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CardListSerializer

    def get(self, request):

        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use user id """

            try:
                cards = Card.objects.filter(user_id=request.user.id)

                serializer = CardListSerializer(
                    cards, many=True, context={"request": request}
                )
                return Response(
                    {
                        "status": "OK",
                        "message": "Successfully fetched cards",
                        "data": serializer.data,
                    }
                )

            except Card.DoesNotExist:
                return Response(
                    {"status": "FAIL", "message": "Cards not found", "data": []}
                )

        else:
            return Response(
                {"status": "FAIL", "message": "Unauthorised User", "data": []}
            )


class CardCreateAPI(MyAPIView):
    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request):

        """POST method to create the data"""

        if request.user.is_authenticated:

            try:

                stripe = MyStripe()

                """ Create Customer """

                user_obj = User.objects.get(id=request.user.id)
                user_plan = UserProfile.objects.filter(user__id=user_obj.id).first()
                user_serilizer = UserDetailsSerializer(user_obj)

                if not request.user.customer_id:

                    new_stripe_customer = stripe.createCustomer(request.user)

                    user_obj.customer_id = new_stripe_customer["id"]
                    user_obj.save()

                """ Add Card in stripe """

                payment_method = stripe.CreatePaymentMethod(request.data["source"])
                stripe.PaymentMethodAttach(payment_method.id, user_obj.customer_id)

                if user_plan.subscription:

                    current_subscription = SubscriptionOrder.objects.filter(
                        user__id=user_obj.id,
                        subscription__id=user_plan.subscription.id,
                        plan_status="active",
                    ).exists()

                    check_card = Card.objects.filter(user__id=request.user.id).first()

                    if check_card:

                        stripeErr.PaymentMethod.detach(
                            check_card.stripe_card_id,
                        )
                        if current_subscription:

                            subscription_obj = SubscriptionOrder.objects.filter(
                                user__id=user_obj.id,
                                subscription__id=user_plan.subscription.id,
                                plan_status="active",
                            ).first()
                            stripeErr.Subscription.modify(
                                subscription_obj.stripe_subscription_id,
                                default_payment_method=payment_method.id,
                            )

                        card_order = Card.objects.filter(user__id=user_obj.id).update(
                            stripe_card_id=payment_method.id,
                            last4=payment_method["card"]["last4"],
                            card_expiration_date="{0}/{1}".format(
                                payment_method["card"]["exp_month"],
                                payment_method["card"]["exp_year"],
                            ),
                        )
                        check_card = Card.objects.filter(
                            user__id=request.user.id
                        ).first()

                        srializer = CardSerializer(check_card)
                        context = {
                            "user": user_serilizer.data,
                            "card_order": srializer.data,
                        }
                        send_sendgrid_email(
                            context,
                            "Purchased credit Transaction Receipt",
                            request.user.email,
                            settings.BILLING_DETAILS_TEMPLATE_ID,
                        )

                        return Response(
                            {
                                "status": "OK",
                                "message": "Successfully Updated billing details",
                                "data": srializer.data,
                            }
                        )

                    else:
                        card_order = Card.objects.create(
                            user=user_obj,
                            stripe_card_id=payment_method.id,
                            last4=payment_method["card"]["last4"],
                            card_expiration_date="{0}/{1}".format(
                                payment_method["card"]["exp_month"],
                                payment_method["card"]["exp_year"],
                            ),
                        )

                        srializer = CardSerializer(card_order)
                        context = {
                            "user": user_serilizer.data,
                            "card_order": srializer.data,
                        }
                        send_sendgrid_email(
                            context,
                            "Purchased credit Transaction Receipt",
                            request.user.email,
                            settings.BILLING_DETAILS_TEMPLATE_ID,
                        )

                        return Response(
                            {
                                "status": "OK",
                                "message": "Successfully Updated billing details",
                                "data": [],
                            }
                        )

                else:
                    check_card = Card.objects.filter(user__id=request.user.id).first()

                    if check_card:
                        card_order = Card.objects.filter(user__id=user_obj.id).update(
                            stripe_card_id=payment_method.id,
                            last4=payment_method["card"]["last4"],
                            card_expiration_date="{0}/{1}".format(
                                payment_method["card"]["exp_month"],
                                payment_method["card"]["exp_year"],
                            ),
                        )

                        check_card = Card.objects.filter(
                            user__id=request.user.id
                        ).first()
                        srializer = CardSerializer(check_card)
                        context = {
                            "user": user_serilizer.data,
                            "card_order": srializer.data,
                        }
                        send_sendgrid_email(
                            context,
                            "Purchased credit Transaction Receipt",
                            request.user.email,
                            settings.BILLING_DETAILS_TEMPLATE_ID,
                        )

                        return Response(
                            {
                                "status": "OK",
                                "message": "Successfully Updated billing details",
                                "data": srializer.data,
                            }
                        )

                    else:
                        card_order = Card.objects.create(
                            user=user_obj,
                            stripe_card_id=payment_method.id,
                            last4=payment_method["card"]["last4"],
                            card_expiration_date="{0}/{1}".format(
                                payment_method["card"]["exp_month"],
                                payment_method["card"]["exp_year"],
                            ),
                        )
                        srializer = CardSerializer(card_order)
                        context = {
                            "user": user_serilizer.data,
                            "card_order": srializer.data,
                        }
                        send_sendgrid_email(
                            context,
                            "Purchased credit Transaction Receipt",
                            request.user.email,
                            settings.BILLING_DETAILS_TEMPLATE_ID,
                        )

                        return Response(
                            {
                                "status": "OK",
                                "message": "Successfully Updated billing details",
                                "data": srializer.data,
                            }
                        )

            except stripeErr.error.CardError as e:
                body = e.json_body
                err = body.get("error", {})

                return Response(
                    {"status": "FAIL", "message": err["message"], "data": []}
                )

            except stripeErr.error.AuthenticationError as e:

                body = e.json_body
                err = body.get("error", {})
                return Response(
                    {"status": "FAIL", "message": err["message"], "data": []}
                )

            except stripeErr.error.InvalidRequestError as e:
                body = e.json_body
                err = body.get("error", {})
                return Response(
                    {"status": "FAIL", "message": err["message"], "data": []}
                )

            except Exception as e:

                return Response({"status": "FAIL", "message": str(e), "data": []})
        else:
            return Response(
                {"status": "FAIL", "message": "Unauthorised User", "data": []}
            )
