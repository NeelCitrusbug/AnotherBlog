# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template.loader import get_template
from django.views.generic import TemplateView
from django_datatables_too.mixins import DataTableMixin
from django.shortcuts import render
from extra_views import InlineFormSetFactory
from core.mixins import HasPermissionsMixin

from core.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView,
)

from core.models import User, UserProfile, SubscriptionOrder, EventOrder
from ..forms import MyUserChangeForm, MyUserCreationForm, UserProfileForm
from blog.models import Post,Category
from django.utils import timezone
# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

    def get(self, request):

        get_total_user = User.objects.all().count()
        recent_users = User.objects.order_by("-created_at")[:5]
        influencer_users = User.objects.filter(is_influencer=True).count()
        get_active_plan = SubscriptionOrder.objects.filter(plan_status="active").count()
        get_event = EventOrder.objects.filter(order_status="success").count()
        get_post = Post.objects.all().count()
        get_category = Category.objects.all().count()
        self.context = {
            "user_count": get_total_user,
            "recent_users": recent_users,
            "influencer_users": influencer_users,
            "get_active_plan": get_active_plan,
            "get_event": get_event,
            "get_post": get_post,
            "get_category": get_category,
        }

        return render(request, self.template_name, self.context)


class UserListView(MyListView):
    """
    View for User listing
    """

    ordering = ["-created_at"]
    model = User
    queryset = model.objects.exclude(username="admin")
    template_name = "core/adminuser/user_list.html"
    permission_required = ("core.view_user",)

    def get_queryset(self):

        return self.model.objects.exclude(username="admin").exclude(
            username=self.request.user
        ).order_by("-created_at")


class UserProfileInline(InlineFormSetFactory):

    """Inline view to show UserProfileUpdateInline within the Parent View"""

    model = UserProfile
    form_class = UserProfileForm
    factory_kwargs = {
        "extra": 1,
        "max_num": None,
        "can_order": False,
        "can_delete": True,
    }


class UserProfileUpdateInline(InlineFormSetFactory):

    """Inline view to show UserProfileUpdateInline within the Parent View"""

    model = UserProfile
    form_class = UserProfileForm
    factory_kwargs = {"extra": 1, "max_num": 1, "can_order": False, "can_delete": True}


class UserCreateView(MyNewFormsetCreateView):
    """
    View to create User
    """

    model = User
    inlines = [
        UserProfileInline,
    ]

    form_class = MyUserCreationForm
    template_name = "core/adminuser/user_form.html"
    permission_required = ("core.add_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UserUpdateView(MyNewFormsetUpdateView):
    """
    View to update User
    """

    model = User
    inlines = [
        UserProfileUpdateInline,
    ]
    form_class = MyUserChangeForm
    template_name = "core/adminuser/user_form.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UserDeleteView(MyDeleteView):
    """
    View to delete User
    """

    model = User
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_user",)


class UserPasswordView(MyUpdateView):
    """
    View to change User Password
    """

    model = User
    form_class = AdminPasswordChangeForm
    template_name = "core/adminuser/password_change_form.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        kwargs["user"] = kwargs.pop("instance")
        return kwargs


class UserAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view.
    """

    model = User
    queryset = User.objects.all().order_by("-created_at")

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
            return qs.filter(Q(name__icontains=self.search))
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "name": o.name,
                    "created_at": o.created_at,
                    "actions": self._get_actions(o),
                }
            )
        return data