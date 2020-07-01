from django.shortcuts import render, redirect

from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from .forms import ItemCreationForm, ItemImagesForm, GlobalTagCreationForm, LocalTagCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from . import models
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import mixins


class TagCreationMixin(UserPassesTestMixin, View):

    tag_form = None

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        form = self.tag_form()
        return render(request, 'catalog/tag_create.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        form = self.tag_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have create new tag')
            return redirect('tag-list')
        return render(request, 'catalog/tag_create.html', {'form': form})
