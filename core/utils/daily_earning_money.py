from datetime import timedelta
from django.db.models import Sum
from itertools import groupby

from core.models.event_order import EventOrder


def daily_earning(user, start_date, total_days):

    new_date = start_date
    earning_by_days = {}

    for i in range(0, total_days):
        new_date += timedelta(days=1)
        event_direct_earning  = EventOrder.objects.filter(
            created_at__range=[start_date, new_date], event__user__id=user, transaction_type="direct_purchase"
        )

        event_credit_earning = EventOrder.objects.filter(
            created_at__range=[start_date, new_date], event__user__id=user, transaction_type="credit"
        )

        direct_earning = event_direct_earning.aggregate(Sum("event__price"))
        credit_earning = event_credit_earning.aggregate(Sum("event__credit_required"))
        if credit_earning['event__credit_required__sum'] is None:
            credit_earning['event__credit_required__sum']=0

        if direct_earning['event__price__sum'] is None:
            direct_earning['event__price__sum']=0

        total = round(float(credit_earning['event__credit_required__sum']) * 0.36, 2) + float(direct_earning['event__price__sum'])

        start_date += timedelta(days=1)
        earning_by_days[str(start_date.strftime("%d-%m-%Y"))] = total

    return earning_by_days



def monthly_earning(event_object):

    month_totals = {
        k: sum(round(x.event.credit_required * 0.36, 2) if x.transaction_type=="credit" else x.event.price for x in g)
        for k, g in groupby(event_object, key=lambda i: i.created_at.month)
    }

    data = {}
    res = []
    month_name = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    for k in range(1, 13):
        data[month_name[k - 1]] = 0
        if k in month_totals.keys():
            data[month_name[k - 1]] = month_totals[k]

    res.append(data)
    return res



def yearly_earning(event_object):
   
    year_totals = {
        k: sum( round(x.event.credit_required * 0.36, 2) if x.transaction_type=="credit" else x.event.price for x in g)
        for k, g in groupby(event_object, key=lambda i: i.created_at.year)
    }
    return year_totals
