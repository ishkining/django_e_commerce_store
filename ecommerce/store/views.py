from django.shortcuts import render

from .models import Category


def store(request):

    return render(request, 'store/store.html')


def categories(request):
    all_categories = Category.objects.all()

    return {'all_categories': all_categories}
