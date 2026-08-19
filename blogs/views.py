from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Blog

# Create your views here.
def posts_by_category(request, category_id):
  # print(category_id)
  #fetch post that belong to category with id
  posts = Blog.objects.filter(status='Published', category=category_id)
  # return HttpResponse(posts)
  context = {
    'posts' : posts,
  }
  return render(request,'posts_by_category.html', context)

