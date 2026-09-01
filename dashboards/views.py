from django.shortcuts import render,redirect
from blogs.models import Category
from blogs.models import Blog
from django.contrib.auth.decorators import login_required
from django.contrib import auth 
from .forms import CategoryForm, AddUserForm, BlogPostForm, EditUserForm
from django.shortcuts import get_object_or_404

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 



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

# users
def users(request):
    users = User.objects.all()
    context = {
        'users':users,
    }
    return render(request, 'dashboard/users.html',context)

def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    form = AddUserForm(request.POST)
    
    context = {
        'form':form,
    }
    return render(request, 'dashboard/add_user.html', context)

# edit user
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = EditUserForm(instance=user)
    context = {
        'form': form 
    }
    return render(request, 'dashboard/edit_user.html', context) 

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')