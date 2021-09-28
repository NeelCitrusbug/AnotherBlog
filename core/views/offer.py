# -*- coding: utf-8 -*-
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from core.mixins import HasPermissionsMixin

from core.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyNewFormsetUpdateView,
    MyNewFormsetCreateView,
)

from core.models import Offer
from ..forms import OfferForm

# -----------------------------------------------------------------------------
# Offer module
# -----------------------------------------------------------------------------


class OfferListView(MyListView):

    """
    View for Offer listing
    """

    paginate_by = 10
    ordering = ["-created_at"]
    model = Offer
    queryset = model.objects.all().order_by("-created_at")
    template_name = "core/offer/list.html"
    permission_required = ("core.view_offer",)


class OfferCreateView(MyNewFormsetCreateView):

    """
    View to create Offer
    """

    model = Offer
    form_class = OfferForm
    template_name = "core/offer/form.html"
    permission_required = ("core.add_offer",)


class OfferUpdateView(MyNewFormsetUpdateView):

    """View to update Offer """

    model = Offer
    form_class = OfferForm
    template_name = "core/offer/form.html"
    permission_required = ("core.change_offer",)


class OfferDeleteView(MyDeleteView):

    """
    View to delete Offer Plan
    """

    model = Offer
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_offer",)


class OfferAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):

    """
    Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view.
    """

    model = Offer
    queryset = Offer.objects.all().order_by("id")

    def _get_is_superuser(self, obj):
        """
        Get boolean column markup.
        """
        t = get_template("core/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def _get_actions(self, obj, **kwargs):
        """
        Get actions column markup.
        """
        # ctx = super().get_context_data(**kwargs)
        t = get_template("core/partials/list_basic_actions.html")
        # ctx.update({"obj": obj})
        # print(ctx)
        return t.render({"o": obj})

    def filter_queryset(self, qs):
        """
        Return the list of items for this view.
        """
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(title__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "created_at": o.created_at,
                    "actions": self._get_actions(o),
                }
            )
        return data