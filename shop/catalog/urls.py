"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemListView.as_view(template_name='catalog/main_page.html'), name='index'),
    path('create-item/', views.ItemCreationView.as_view(), name ='create-item'),
    path('item/<str:slug>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/<str:slug>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('tag/<str:tag>/', views.ItemListView.as_view(template_name='catalog/main_page.html'), name='tag'),
    path('tag/<str:tag>/delete/', views.delete_tag, name='delete-tag'),
    path('delete-tag-list/', views.TagsListView.as_view(template_name='catalog/tags_delete_list.html'), name='delete-tag-list'),
    path('tag/', views.TagsListView.as_view(template_name='catalog/tags_list.html'), name='tag-list'),
    path('create-global-tag/', views.GlobalTagCreationView.as_view(), name='create-global-tag'),
    path('create-local-tag/', views.LocalTagCreationView.as_view(), name='create-local-tag'),
    path('items-confirm-list/', views.ItemConfirmList.as_view(template_name='catalog/main_page.html'), name='confirm-items'),
    path('item/<str:slug>/activate/', views.activate_item, name='activate-item'),
    path('item/<str:slug>/disactivate/', views.disactivate_item, name='disactivate-item'),
    path('item/<str:slug>/delete/', views.delete_item, name='delete-item'),
    path('admin-panel/', views.admin_panel, name='admin-panel'),
]
