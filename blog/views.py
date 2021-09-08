from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post
from django.core.paginator import Paginator

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

# Create your views here.

# Create your views here.


# def post_list(request):
#     posts = Post.objects.filter(published_date__lte = timezone.now())

#     return render(request, 'blog/post_list.html', {'posts':posts})


def post_list(request):
    """Returns the all the post objects that are published"""
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "-published_date"
    )
    p = Paginator(posts, 3)

    page_number = request.GET.get("page")  # 1
    page_obj = p.get_page(page_number)  # <Page 1 of 2>

    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def post_detail(request, pk):
    """Returns the post object which has been clicked by the user"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")
    p = Paginator(posts, 3)

    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(request, "blog/post_draft_list.html", {"page_obj": page_obj})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect("post_detail", pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("post_list")


# class CategoryNew(CreateView):
#     model = Category
#     context_object_name = "category"
#     template_name = "blog/category_edit.html"
#     fields = "__all__"


# class CategoryList(ListView):
#     model = Category
#     context_object_name = "category"
#     queryset = Category.objects.all()
#     template_name = "blog/category_list.html"


# def category_detail(request, cats):
#     category_posts = Post.objects.filter(category=cats)
#     print(category_posts, cats)
#     return render(
#         request,
#         "blog/category_detail.html",
#         {"cats": cats, "category_posts": category_posts},
#     )


# def post_draft_list(request):
#     posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
#     return render(request , 'blog/post_draft_list.html',{'posts':posts})


# class PostList(ListView):
#     model = Post
#     context_object_name = "post"
#     queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by(
#         "-published_date"
#     )
#     template_name = "blog/post_list.html"
#     paginate_by = 3


# class PostNew(CreateView):
#     model = Post
#     context_object_name = "post"
#     template_name = "blog/post_edit.html"
#     form_class = PostForm
#     success_url = reverse_lazy("post_detail")

#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.author = user
#         post.published_date = timezone.now()
#         post.save()
#         return super().form_valid(form)


# class PostEdit(UpdateView):
#     model = Post
#     context_object_name = "post"
#     fields = ["title", "text"]
#     success_url = reverse_lazy("post_detail")

# class PostDetail(DetailView):
#     model = Post
#     context_object_name = "post"
#     template_name = "blog/post_detail.html."
