from django.shortcuts import render, redirect

from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from .forms import ItemCreationForm, ItemImagesForm
from .models import Item, ItemPhoto
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile


# Create your views here.


class ItemCreation(LoginRequiredMixin, View):
    def get(self, request):
        form = ItemCreationForm()
        form_images = ItemImagesForm()
        return render(request, 'catalog/item_create.html', {'form': form, 'form_images': form_images})

    @transaction.atomic
    def post(self, request):
        form = ItemCreationForm(request.POST)
        form_images = ItemImagesForm(request.POST, request.FILES, request=request)
        if form.is_valid() and form_images.is_valid():
            item = form.save(user=request.user)
            print(item)
            form_images.save_for(item)
            messages.success(request, 'You have uploaded your item')
            return redirect('index')
        return render(request, 'catalog/item_create.html', {'form': form, 'form_images': form_images})


class ItemList(ListView):
    model = Item

class ItemDetailView(DetailView):
    model = Item
