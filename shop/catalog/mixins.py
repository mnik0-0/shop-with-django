from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class TagCreationMixin(UserPassesTestMixin, LoginRequiredMixin, View):

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
