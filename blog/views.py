from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post,Category
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy






def post_list(request):
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
    """Returns the post object which has been clicked by the user"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


    
def create_post(request):
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
    query = request.GET.get('query')

    if query:
        posts = Post.objects.filter(published_date__isnull=True).filter(Q(title__icontains=query) | Q(text__icontains=query))
    else:
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
    
    query = request.GET['query']
    
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
    
    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            object_list = Category.objects.filter(name__icontains=query)

        else:
            object_list = Category.objects.all()   
        return object_list 

   

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
    success_url = reverse_lazy("category_list")

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = "blog/category_edit.html"
    success_url = reverse_lazy("category_list")

def category_remove(request, category):
    cats = get_object_or_404(Category, name=category)
    cats.delete()
    return redirect('category_list')




