from datetime import datetime, timedelta
import time
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
import stripe

from core.api.apiviews import MyAPIView
from core.utils.daily_earning_money import (
    daily_earning,
    monthly_earning,
    yearly_earning,
)

from core.models import EventOrder

current_datetime = datetime.now()
current_datetime += timedelta(days=1)
today = datetime.now()


# .................................................................................
# InfluencerEarnMoneyListAPIView Plan API
# .................................................................................


class InfluencerEarnMoneyListAPIView(MyAPIView):

    """
    API View for banner  listing
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        try:

            data = {}
            result = []
            day = 0

            if request.user.influencer_stripe_account_id:
                new_result = stripe.Account.retrieve(
                    str(request.user.influencer_stripe_account_id)
                )
                new_result["settings"]["payouts"]['schedule']['delay_days'] = time.strptime(new_result["settings"]["payouts"]['schedule']['weekly_anchor'], '%A').tm_wday 
                data["next_payout"] = new_result["settings"]["payouts"]

            search = request.GET["q"]

            if search == "month":

                event = EventOrder.objects.filter(
                    event__user__id=request.user.id, created_at__year=today.year
                )

                event_credit_earning = EventOrder.objects.filter(
                    event__user__id=request.user.id,
                    transaction_type="credit",
                    created_at__year=today.year,
                )
                event_direct_earning = EventOrder.objects.filter(
                    event__user__id=request.user.id,
                    transaction_type="direct_purchase",
                    created_at__year=today.year,
                )

                direct_earning = event_direct_earning.aggregate(Sum("event__price"))
                credit_earning = event_credit_earning.aggregate(
                    Sum("event__credit_required")
                )

                if credit_earning["event__credit_required__sum"] is None:
                    credit_earning["event__credit_required__sum"] = 0

                if direct_earning["event__price__sum"] is None:
                    direct_earning["event__price__sum"] = 0

                total = round(
                    float(credit_earning["event__credit_required__sum"]) * 0.36, 2
                ) + float(direct_earning["event__price__sum"])
                data["total_earning"] = total
                res = monthly_earning(event)
                data["total_enroll_student"] = event.count()
                data["earning"] = res[0]
                result.append(data)

                return Response(
                    {
                        "status": "OK",
                        "message": "Successfully fetched data",
                        "data": result,
                    }
                )

            elif search == "year":

                event = EventOrder.objects.filter(event__user__id=request.user.id)
                event_credit_earning = EventOrder.objects.filter(
                    event__user__id=request.user.id, transaction_type="credit"
                )
                event_direct_earning = EventOrder.objects.filter(
                    event__user__id=request.user.id, transaction_type="direct_purchase"
                )

                direct_earning = event_direct_earning.aggregate(Sum("event__price"))
                credit_earning = event_credit_earning.aggregate(
                    Sum("event__credit_required")
                )

                if credit_earning["event__credit_required__sum"] is None:
                    credit_earning["event__credit_required__sum"] = 0

                if direct_earning["event__price__sum"] is None:
                    direct_earning["event__price__sum"] = 0

                total = round(
                    float(credit_earning["event__credit_required__sum"]) * 0.36, 2
                ) + float(direct_earning["event__price__sum"])
                data["total_earning"] = total

                res = yearly_earning(event)
                data["total_enroll_student"] = event.count()
                data["earning"] = res
                result.append(data)

                return Response(
                    {
                        "status": "OK",
                        "message": "Successfully fetched data",
                        "data": result,
                    }
                )

            elif search == "week":
                day = 7
                start_date = datetime.now() - timedelta(days=day)
                event = EventOrder.objects.filter(
                    created_at__range=[start_date, current_datetime],
                    event__user__id=request.user.id,
                )

                event_credit_earning = EventOrder.objects.filter(
                    created_at__range=[start_date, current_datetime],
                    event__user__id=request.user.id,
                    transaction_type="credit",
                )
                event_direct_earning = EventOrder.objects.filter(
                    created_at__range=[start_date, current_datetime],
                    event__user__id=request.user.id,
                    transaction_type="direct_purchase",
                )

                direct_earning = event_direct_earning.aggregate(Sum("event__price"))
                credit_earning = event_credit_earning.aggregate(
                    Sum("event__credit_required")
                )

                if credit_earning["event__credit_required__sum"] is None:
                    credit_earning["event__credit_required__sum"] = 0

                if direct_earning["event__price__sum"] is None:
                    direct_earning["event__price__sum"] = 0

                total = round(
                    float(credit_earning["event__credit_required__sum"]) * 0.36, 2
                ) + float(direct_earning["event__price__sum"])

                data["total_earning"] = total
                data["total_enroll_student"] = event.count()
                res = daily_earning(request.user.id, start_date, day)
                data["earning"] = res
                result.append(data)

                return Response(
                    {
                        "status": "OK",
                        "message": "Successfully fetched data",
                        "data": result,
                    }
                )

        except:
            return Response(
                {
                    "status": "FAIL",
                    "message": "Bad request",
                    "data": [],
                }
            )
