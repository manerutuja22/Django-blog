from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Blog
from .models import Category
from django.shortcuts import get_object_or_404 
from django.shortcuts import redirect
from django.db.models import Q
from .models import Comment
from .forms import CommentForm

# Create your views here.
def posts_by_category(request, category_id):
  # print(category_id)
  #fetch post that belong to category with id
  posts = Blog.objects.filter(status='Published', category=category_id)
  # return HttpResponse(posts)

  #use when we want to do some custome action if the category does not exist 
  # try:
  #     category = Category.objects.get(pk=category_id)
  # except:
  #    return redirect(request,'home.html')
  
#use get_object_or-404 page when you want to show 404 error page if the category does not exist 
  # category = get_object_or_404(Category, pk=category_id)

#how to add custom error page add 404.html
  category = get_object_or_404(Category, pk=category_id)

  categories = Category.objects.all()
  context = {
    'posts' : posts,
    # 'category_id' : category_id,
    'category' : category,
    'categories': categories,
  }
  return render(request,'posts_by_category.html', context)

# def blogs(request, slug):
#   single_blog = get_object_or_404(Blog, slug=slug, status='Published')
#   context = {
#     'single_blog':single_blog,
#   }
#   return render(request, 'blogs.html', context)

def blogs(request, slug):

    single_blog = get_object_or_404(
        Blog,
        slug=slug,
        status='Published'
    )

    # Save comment
    if request.method == 'POST':

        if request.user.is_authenticated:

            comment_text = request.POST.get('comment')

            if comment_text:
                Comment.objects.create(
                    user=request.user,
                    blog=single_blog,
                    comment=comment_text
                )

            return redirect('blogs', slug=single_blog.slug)

        else:
            return redirect('login')

    # Get comments
    comments = Comment.objects.filter(
        blog=single_blog
    ).order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comments.count(),
        'categories': categories,
    }

    return render(request, 'blogs.html', context)

def about(request):

    return render(request, 'about.html')


def follow_us(request):

    return render(request, 'follow_us.html')


def search(request):

    keyword = request.GET.get('keyword')

    if keyword:

        posts = Blog.objects.filter(
            Q(title__icontains=keyword) |
            Q(short_description__icontains=keyword) |
            Q(blog_body__icontains=keyword),
            status='Published'
        )

    else:

        posts = Blog.objects.none()
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'keyword': keyword,
        'categories':categories,
    }

    return render(request, 'search.html', context)

