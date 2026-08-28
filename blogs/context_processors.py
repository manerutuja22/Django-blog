from .models import Category,SocialLink

def get_categories(request):
  categories = Category.objects.all()
  return dict(categories=categories)
from .models import SocialLink


def social_links(request):

    return {
        'social_links': SocialLink.objects.filter(is_active=True)
    }