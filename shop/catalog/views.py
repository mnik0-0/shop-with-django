from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404
from .forms import ItemCreationForm, ItemImagesForm, GlobalTagCreationForm, LocalTagCreationForm
from django.contrib import messages
from django.db import transaction
from . import models
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import mixins
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.db.models import Max
from . import utils
from django.views.decorators.http import require_http_methods


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
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            form_images.save_for(item)
            messages.success(request, 'You have uploaded your item')
            return redirect('index')
        return render(request, 'catalog/item_create.html', {'form': form, 'form_images': form_images})


class ItemListView(ListView):
    model = models.Item
    paginate_by = 12

    def get(self, request, tag=None):
        self.search = request.GET.get('search', '')
        self.min = request.GET.get('min')
        self.max = request.GET.get('max')
        self.tag = None

        if not utils.is_digit(str(self.max)):
            self.max = models.Item.objects.aggregate(Max('price'))['price__max']

        if not utils.is_digit(str(self.min)):
            self.min = 0

        if tag is not None:
            self.tag = tag
        return super().get(request)

    def get_queryset(self):
        if self.tag is None:
            return models.Item.objects.filter(is_active=True, price__range=[self.min, self.max]).filter(
                Q(title__contains=self.search) | Q(description__contains=self.search)).order_by('-date_pub')
        return models.Item.objects.filter(tag=get_object_or_404(models.LocalTag, title__iexact=self.tag)).filter(
            is_active=True, price__range=[self.min, self.max]).filter(
            Q(title__contains=self.search) | Q(description__contains=self.search)).order_by('-date_pub')


class ItemConfirmList(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = models.Item
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        self.search = request.GET.get('search', '')
        self.min = request.GET.get('min')
        self.max = request.GET.get('max')

        if not utils.is_digit(str(self.max)):
            self.max = models.Item.objects.aggregate(Max('price'))['price__max']

        if not utils.is_digit(str(self.min)):
            self.min = 0

        return super().get(request)

    def get_queryset(self):
        return models.Item.objects.filter(is_active=False, price__range=[self.min, self.max]).filter(
            Q(title__contains=self.search) | Q(description__contains=self.search)).order_by('-date_pub')


@require_http_methods(["GET"])
@staff_member_required(login_url='login')
@transaction.atomic
def activate_item(request, slug):
    item = get_object_or_404(models.Item, slug=slug)
    item.is_active = True
    item.save()
    messages.success(request, f'Item {item.title} has been activated')
    return redirect('confirm-items')


@require_http_methods(["GET"])
@staff_member_required(login_url='login')
@transaction.atomic
def disactivate_item(request, slug):
    item = get_object_or_404(models.Item, slug=slug)
    item.is_active = False
    item.save()
    messages.success(request, f'Item {item.title} has been disactivated')
    return redirect('confirm-items')


@require_http_methods(["GET"])
@transaction.atomic
def delete_item(request, slug):
    item = get_object_or_404(models.Item, slug=slug)
    if request.user.is_staff or request.user == item.user:
        item.delete()
        messages.success(request, f'Item {item.title} has been deleted')
        return redirect('index')
    return redirect('login')


@require_http_methods(["GET"])
@staff_member_required(login_url='login')
@transaction.atomic
def delete_tag(request, tag):
    tag = get_object_or_404(models.LocalTag, title=tag)
    tag.delete()
    messages.success(request, f'Tag {tag.title} has been deleted')
    return redirect('tag-list')


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = models.Item

    def get(self, request, slug):
        item = get_object_or_404(models.Item, slug=slug)
        if not item.is_active and not request.user.is_staff and not request.user == item.user:
            raise Http404
        return super(ItemDetailView, self).get(request, slug)


class ItemUpdateView(LoginRequiredMixin, View):

    def get(self, request, slug):
        item = get_object_or_404(models.Item, slug=slug)
        if request.user != item.user:
            return redirect('index')
        form = ItemCreationForm(instance=item)
        return render(request, 'catalog/item_update.html', {'form': form, })

    @transaction.atomic
    def post(self, request, slug):
        item = get_object_or_404(models.Item, slug=slug)
        item.date_upd = now()
        item.is_active = False
        form = ItemCreationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have update your item')
            return redirect('index')
        return render(request, 'catalog/item_update.html', {'form': form, })


class TagsListView(ListView):
    model = models.GlobalTag


class GlobalTagCreationView(mixins.TagCreationMixin):
    tag_form = GlobalTagCreationForm


class LocalTagCreationView(mixins.TagCreationMixin):
    tag_form = LocalTagCreationForm


@require_http_methods(["GET"])
@staff_member_required(login_url='login')
def admin_panel(request):
    return render(request, 'user/admin_panel.html')
