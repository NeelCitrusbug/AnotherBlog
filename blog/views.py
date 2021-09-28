from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm,CategoryForm
from .models import Post,Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

#FOR CUSTOM ADMIN
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.template.loader import get_template
from django.views.generic import TemplateView
from django_datatables_too.mixins import DataTableMixin
from extra_views import InlineFormSetFactory
# from blog.mixins import HasPermissionsMixin
# from blog.models import User, UserProfile, SubscriptionOrder, EventOrder

# from blog.generic import (
#     MyDeleteView,
#     MyListView,
#     MyLoginRequiredView,
#     MyUpdateView,
#     MyNewFormsetCreateView,
#     MyNewFormsetUpdateView,
# )



def post_list(request):
    """
        it passes list of posts objects that are published to post_list template
        :return : post objects that are published
    """
    query = request.GET.get('query')

    if query:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(Q(title__icontains=query) | Q(text__icontains=query))
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "-published_date"
    )

    p = Paginator(posts, 3)
    page_number = request.GET.get("page")  # 1
    page_obj = p.get_page(page_number)  # <Page 1 of 2>
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "query":query})

def post_detail(request, pk):
    """
    Returns the detail of perticular post which has been clicked by the user
    :param pk:
    :return : post object value with primary key value of pk
    """
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})

def create_post(request):
    """
    Creates the new post
    :return : form object values
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        
        if form.is_valid():
            cats = request.POST.getlist('category')    #o/p ['9', '10']
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            cats = Category.objects.filter(id__in=cats)   #o/p  <QuerySet [<Category: sports>, <Category: coding>]>
            for cat in cats:
                post.category.add(cat)
            return redirect("post_detail", pk=post.pk)
            
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})

def post_edit(request, pk):
    """
    Used to edit the detail of particular post 
    :param pk:
    :return : form object of that post
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            cats = request.POST.getlist('category')
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            post.category.clear()
            cats = Category.objects.filter(id__in=cats)
            
            for cat in cats:
                post.category.add(cat)
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})

def post_draft_list(request):
    """
    Returns the list of posts which are not published
    :return : post objects which are not published
    """
    query = request.GET.get('query')

    if query:
        posts = Post.objects.filter(published_date__isnull=True).filter(Q(title__icontains=query) | Q(text__icontains=query))
    else:
        posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")

    p = Paginator(posts, 3)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    return render(request, "blog/post_draft_list.html", {"page_obj": page_obj, "query":query})

def post_publish(request, pk):
    """
    it's method to publish any post
    :param pk:
    
    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect("post_detail", pk=pk)

def post_remove(request, pk):
    """
    It used to delete the particular post
    :param pk:
    
    """
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("post_list")


class CategoryList(ListView):
    """
    Used to give the list of categories
    :return : all the category objects
    """
    model = Category()
    template_name = "blog/category_list.html"
    context_object_name= "category"
    
    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            object_list = Category.objects.filter(name__icontains=query)
        else:
            object_list = Category.objects.all()   
        return object_list 


class CategoryPostList(ListView):
    """
    Gives the list of post belonging to the particular category.
    :param category-name:
    :return : post objects which belongs to particular category
    """
    template_name = "blog/category_post_list.html"
    context_object_name = "category"
    
    def get_queryset(self):
        context={
            'cat': self.kwargs['category'],
            'posts':Post.objects.filter(category__name= self.kwargs['category']).filter(published_date__lte=timezone.now())
        }
        return context 


class CategoryNew(CreateView):
    """
    Creates new category
    :return : category-name that's been filled in the form by user
    """
    model = Category
    context_object_name = "category"
    template_name = "blog/category_edit.html"
    form_class = CategoryForm
    success_url = reverse_lazy("category_list")


class CategoryUpdateView(UpdateView):
    """
    Updates the name of the particular category
    :return: returns updated category name
    """
    model = Category
    form_class = CategoryForm
    template_name = "blog/category_edit.html"
    success_url = reverse_lazy("category_list")

def category_remove(request, category):
    """
    To remove the particular Category
    :param category-name:
    """
    cats = get_object_or_404(Category, name=category)
    cats.delete()
    return redirect('category_list')



# #CUSTOM ADMIN VIEWS STARTS HERE


# # -----------------------------------------------------------------------------
# # Users
# # -----------------------------------------------------------------------------


# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = "core/index.html"

#     def get(self, request):

#         get_total_user = User.objects.all().count()
#         recent_users = User.objects.order_by("-created_at")[:5]
#         influencer_users = User.objects.filter(is_influencer=True).count()
#         get_active_plan = SubscriptionOrder.objects.filter(plan_status="active").count()
#         get_event = EventOrder.objects.filter(order_status="success").count()

#         self.context = {
#             "user_count": get_total_user,
#             "recent_users": recent_users,
#             "influencer_users": influencer_users,
#             "get_active_plan": get_active_plan,
#             "get_event": get_event,
#         }

#         return render(request, self.template_name, self.context)


# class UserListView(MyListView):
#     """
#     View for User listing
#     """

#     ordering = ["-created_at"]
#     model = User
#     queryset = model.objects.exclude(username="admin")
#     template_name = "core/adminuser/user_list.html"
#     permission_required = ("core.view_user",)

#     def get_queryset(self):

#         return self.model.objects.exclude(username="admin").exclude(
#             username=self.request.user
#         ).order_by("-created_at")


# class UserProfileInline(InlineFormSetFactory):

#     """Inline view to show UserProfileUpdateInline within the Parent View"""

#     model = UserProfile
#     form_class = UserProfileForm
#     factory_kwargs = {
#         "extra": 1,
#         "max_num": None,
#         "can_order": False,
#         "can_delete": True,
#     }


# class UserProfileUpdateInline(InlineFormSetFactory):

#     """Inline view to show UserProfileUpdateInline within the Parent View"""

#     model = UserProfile
#     form_class = UserProfileForm
#     factory_kwargs = {"extra": 1, "max_num": 1, "can_order": False, "can_delete": True}


# class UserCreateView(MyNewFormsetCreateView):
#     """
#     View to create User
#     """

#     model = User
#     inlines = [
#         UserProfileInline,
#     ]

#     form_class = MyUserCreationForm
#     template_name = "core/adminuser/user_form.html"
#     permission_required = ("core.add_user",)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["user"] = self.request.user
#         return kwargs


# class UserUpdateView(MyNewFormsetUpdateView):
#     """
#     View to update User
#     """

#     model = User
#     inlines = [
#         UserProfileUpdateInline,
#     ]
#     form_class = MyUserChangeForm
#     template_name = "core/adminuser/user_form.html"
#     permission_required = ("core.change_user",)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["user"] = self.request.user
#         return kwargs


# class UserDeleteView(MyDeleteView):
#     """
#     View to delete User
#     """

#     model = User
#     template_name = "core/confirm_delete.html"
#     permission_required = ("core.delete_user",)


# class UserPasswordView(MyUpdateView):
#     """
#     View to change User Password
#     """

#     model = User
#     form_class = AdminPasswordChangeForm
#     template_name = "core/adminuser/password_change_form.html"
#     permission_required = ("core.change_user",)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         # kwargs['user'] = self.request.user
#         kwargs["user"] = kwargs.pop("instance")
#         return kwargs


# class UserAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
#     """
#     Built this before realizing there is
#     https://bitbucket.org/pigletto/django-datatables-view.
#     """

#     model = User
#     queryset = User.objects.all().order_by("-created_at")

#     def _get_is_superuser(self, obj):
#         """
#         Get boolean column markup.
#         """
#         t = get_template("core/partials/list_boolean.html")
#         return t.render({"bool_val": obj.is_superuser})

#     def _get_actions(self, obj, **kwargs):
#         """
#         Get actions column markup.
#         """
#         # ctx = super().get_context_data(**kwargs)
#         t = get_template("core/partials/list_basic_actions.html")
#         # ctx.update({"obj": obj})
#         # print(ctx)
#         return t.render({"o": obj})

#     def filter_queryset(self, qs):
#         """
#         Return the list of items for this view.
#         """
#         # If a search term, filter the query
#         if self.search:
#             return qs.filter(Q(name__icontains=self.search))
#         return qs

#     def prepare_results(self, qs):
#         # Create row data for datatables
#         data = []
#         for o in qs:
#             data.append(
#                 {
#                     "name": o.name,
#                     "created_at": o.created_at,
#                     "actions": self._get_actions(o),
#                 }
#             )
#         return data