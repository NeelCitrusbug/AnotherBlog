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

from core.models import Credit
from ..forms import CreditForm

# -----------------------------------------------------------------------------
# Credit module
# -----------------------------------------------------------------------------


class CreditListView(MyListView):

    """
    View for Credit listing
    """

    model = Credit
    queryset = model.objects.order_by("price")
    template_name = "core/credit/list.html"
    permission_required = ("core.view_credit",)


class CreditCreateView(MyNewFormsetCreateView):

    """
    View to create Credit
    """

    model = Credit
    form_class = CreditForm
    template_name = "core/credit/form.html"
    permission_required = ("core.add_credit",)


class CreditUpdateView(MyNewFormsetUpdateView):

    """View to update Credit """

    model = Credit
    form_class = CreditForm
    template_name = "core/credit/form.html"
    permission_required = ("core.change_Credit",)


class CreditDeleteView(MyDeleteView):

    """
    View to delete Credit
    """

    model = Credit
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_credit",)


class CreditAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):

    """
    Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view.
    """

    model = Credit
    queryset = Credit.objects.all().order_by("id")

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
                Q(username__icontains=self.search)
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
                    "username": o.username,
                    "first_name": o.first_name,
                    "last_name": o.last_name,
                    "is_superuser": self._get_is_superuser(o),
                    # "modified": o.modified.strftime("%b. %d, %Y, %I:%M %p"),
                    "actions": self._get_actions(o),
                }
            )
        return data