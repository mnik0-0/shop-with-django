from django.shortcuts import render, redirect

from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404
from . import forms
from django.contrib import messages
from django.db import transaction

from . import models
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from catalog.models import Item


@login_required(login_url='login')
def chat_list(request):
    chats = models.Chat.objects.filter(users__in=[request.user]).order_by('-last_update')
    return render(request, 'chat/chat_list.html', {'chats': chats})


class ChatView(View):

    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        form = forms.MessageForm()

        try:
            chat = models.Chat.objects.filter(users__in=[request.user]).filter(item=item)[0]

        except IndexError:
            if item.user == request.user:
                raise Http404
            chat = models.Chat.objects.create(item=item)
            chat.users.add(request.user)
            chat.users.add(item.user)
            chat.save()

        for message in chat.messages.filter(is_read=False):
            if message.sender != request.user:
                message.is_read = True
                message.save()
        return render(request, 'chat/chat_view.html', {'chat': chat, 'form': form})

    def post(self, request, slug):
        form = forms.MessageForm(request.POST)
        item = get_object_or_404(Item, slug=slug)
        chat = get_object_or_404(models.Chat, item=item, users__in=[request.user])
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            chat.last_update = message.date
            chat.save()
            message.save()
            return redirect('chat', slug=slug)
        return render(request, 'chat/chat_view.html', {'chat': chat, 'form': form})
