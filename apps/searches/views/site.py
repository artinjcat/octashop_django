from django.shortcuts import render

from apps.catalogs.infrastructure.models import Category, Product


def sub_category_list():
    return Category.objects.filter(depth=1, is_public=True).order_by("title")

class Search():
    def page(request):
        context = {}
        context["sub_categories"] = sub_category_list()
        context["last20"] = Product.objects.filter(is_public=True).order_by("-id")[:20]
        return render(request, "searches/search.html", context)
    
    
    def search_box(request):
        pass