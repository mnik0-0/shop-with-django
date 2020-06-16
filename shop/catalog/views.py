from django.shortcuts import render, redirect

from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from .forms import ItemCreationForm, ItemImagesForm
from .models import Item, ItemPhoto, GlobalTag
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from . import models
from django.utils.timezone import now


# Create your views here.


class ItemCreationView(LoginRequiredMixin, View):
    def get(self, request):
        form = ItemCreationForm()
        form_images = ItemImagesForm()
        return render(request, 'catalog/item_create.html', {'form': form, 'form_images': form_images})

    @transaction.atomic
    def post(self, request):
        form = ItemCreationForm(request.POST)
        form_images = ItemImagesForm(request.POST, request.FILES, request=request)
        if form.is_valid() and form_images.is_valid():
            item = models.Item.objects.create(title=form.cleaned_data['title'], description=form.cleaned_data['description'], tag=form.cleaned_data['tag'], user=request.user)
            form_images.save_for(item)
            messages.success(request, 'You have uploaded your item')
            return redirect('index')
        return render(request, 'catalog/item_create.html', {'form': form, 'form_images': form_images})


class ItemListView(ListView):
    model = Item

    def get(self, request, tag=None):
        self.tag = None
        if tag != None:
            self.tag = tag
        return super().get(request)

    def get_queryset(self):
        if self.tag == None:
            return super().get_queryset()
        return get_object_or_404(models.LocalTag, title__iexact=self.tag).items.all()


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


class ItemUpdateView(LoginRequiredMixin, View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug__iexact=slug)
        if request.user != item.user:
            return redirect('index')
        form = ItemCreationForm({'title': item.title, 'description': item.description, })
        return render(request, 'catalog/item_update.html', {'form': form, })

    @transaction.atomic
    def post(self, request, slug):
        item = get_object_or_404(Item, slug__iexact=slug)
        item.date_upd = now()
        form = ItemCreationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have update your item')
            return redirect('index')
        return render(request, 'catalog/item_update.html', {'form': form, })


class TagsListView(ListView):
    model = GlobalTag
