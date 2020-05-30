from django.shortcuts import render, redirect

from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from .forms import RegistrationForm, LoginForm, ChangeSlugForm
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from catalog.models import Item


# Create your views here.


class RegistrationView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'user/registration.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'success')
            return redirect('login')
        return render(request, 'user/registration.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are in')
                return redirect('index')
        return render(request, 'user/login.html', {'form': form})


def profile(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    items = Item.objects.filter(user=profile.user)
    return render(request, 'user/profile.html', {'profile': profile, 'items': items, })


class ChangeSlugView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        profile = UserProfile.objects.get(slug__iexact=request.user.profile.slug)
        form = ChangeSlugForm(instance=profile)
        return render(request, 'user/login.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        profile = UserProfile.objects.get(slug__iexact=request.user.profile.slug)
        form = ChangeSlugForm(request.POST, instance=profile)
        if form.is_valid():
            form.clean_slug()
            form.save()
            messages.success(request, 'You have changed your slug')
            return redirect('index')
        return render(request, 'user/login.html', {'form': form})
