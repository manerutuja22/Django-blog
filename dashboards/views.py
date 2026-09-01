from django.shortcuts import render,redirect
from blogs.models import Category
from blogs.models import Blog
from django.contrib.auth.decorators import login_required
from django.contrib import auth 
from .forms import CategoryForm 
from django.shortcuts import get_object_or_404
from .forms import BlogPostForm 
from django.template.defaultfilters import slugify

# Create your views here.

@login_required(login_url='login')

def dashboard(request):
  category_count = Category.objects.all().count()
  # print(category_count)
  blogs_count = Blog.objects.all().count()
  # print(blogs_count)
  context = {
    'category_count': category_count,
    'blogs_count': blogs_count,
  }
  return render(request, 'dashboard/dashboard.html',context)

def logout(request):
    auth.logout(request)
    return redirect('login')


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'dashboard/categories.html', context)

def add_category(request):

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('categories')

    else:
        form = CategoryForm()

    context = {
        'form': form,
    }

    return render(request, 'dashboard/add_category.html', context)


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category':category,
    }
    return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'dashboard/posts.html',context)


def add_post(request):

    if request.method == 'POST':

        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            title = form.cleaned_data['title']

            post.slug = slugify(title)

            post.save()

            return redirect('posts')

        else:
            print('Form is invalid')
            print(form.errors)

    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }

    return render(request, 'dashboard/add_post.html', context)

def edit_post(request, pk):

    # Get the existing post
    post = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':

        # POST = user clicked Update Post
        form = BlogPostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            # Update existing post
            post = form.save(commit=False)

            # Generate/update slug
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)

            # Save updated post
            post.save()

            return redirect('posts')

    else:

        # GET = user clicked Edit button
        # Show existing post data in form
        form = BlogPostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'dashboard/edit_post.html', context)

def delete_post(request, pk):

    post = get_object_or_404(Blog, pk=pk)

    post.delete()

    return redirect('posts')