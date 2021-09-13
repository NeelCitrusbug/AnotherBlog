from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post,Category
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages

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

# class PostNew(CreateView):
#     model = Post
#     context_object_name = "post"
#     template_name = "blog/post_edit.html"
    
def post_new(request):
    if request.method == "POST":
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",'asdbaskdbasbjk')

        form = PostForm(request.POST)
        form.category = request.POST.getlist('category')
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",request.POST.getlist('new-select'))

        if form.is_valid():
            print(form)
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            
            return redirect("post_detail", pk=post.pk)
            # return redirect("/")
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

def search(request):
    # query = request.GET.get('query')
    query = request.GET['query']
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
    #     "-published_date"
    # ).filter(title__icontains=query)
    postsTitle = Post.objects.filter(published_date__lte=timezone.now()).filter(title__icontains=query)
    postsText  =  Post.objects.filter(published_date__lte=timezone.now()).filter(text__icontains=query)

    posts = postsTitle.union(postsText)
    
    if posts.count() == 0:
        messages.warning(request,"No search results found")

    return render(request, "blog/search.html", {"posts": posts , "query":query})

class CategoryList(ListView):
    model = Category()
    template_name = "blog/category_list.html"
    context_object_name= "category"
    queryset = Category.objects.all()
    

class CategoryPostList(ListView):
    template_name = "blog/category_post_list.html"
    context_object_name = "category"
    
    def get_queryset(self):
        content={
            'cat': self.kwargs['category'],
            'posts':Post.objects.filter(category__name= self.kwargs['category']).filter(published_date__lte=timezone.now())
        }
        return content 

class CategoryNew(CreateView):
    model = Category
    context_object_name = "category"
    template_name = "blog/category_edit.html"
    fields = "__all__"
    success_url = reverse_lazy("post_list")



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
