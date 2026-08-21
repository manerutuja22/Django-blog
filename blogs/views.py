from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Blog
from .models import Category
from django.shortcuts import get_object_or_404 
from django.shortcuts import redirect

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

