from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm,CategoryForm
from .models import Post,Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

#requirments for the rest-framework
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from blog.models import Post
from blog.serializers import PostSerializer

#requirements for classbased api
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
            return redirect("blog:post_detail", pk=post.pk)
            
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
            return redirect("blog:post_detail", pk=post.pk)
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
    return redirect("blog:post_detail", pk=pk)

def post_remove(request, pk):
    """
    It used to delete the particular post
    :param pk:
    
    """
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("blog:post_list")


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
    return redirect('blog:category_list')


#------------------API CALL USING FUNCTION BASED VIEWS-----------------------#

# @csrf_exempt
# def blogpost_list(request):
#     """
#     List all blog posts, or create a new post.
#     """
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)



# @csrf_exempt
# def blogpost_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         post.delete()
#         return HttpResponse(status=204)



#------------------API CALL USING CLASS BASED VIEWS-----------------------#

class BlogpostList(APIView):
    """
    List all posts, or create a new post.
    """

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BlogpostDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)