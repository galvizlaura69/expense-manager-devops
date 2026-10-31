from django.urls import path
from . import views

urlpatterns = [
path('', views.dashboard, name='dashboard'),
    path(
        'categories/',
        views.category_list,
        name='category_list'
    ),

    path(
        'categories/create/',
        views.category_create,
        name='category_create'
    ),

    path(
        'categories/<int:pk>/edit/',
        views.category_update,
        name='category_update'
    ),

    path(
        'categories/<int:pk>/delete/',
        views.category_delete,
        name='category_delete'
    ),
    path(
    'transactions/',
    views.transaction_list,
    name='transaction_list'
),

path(
    'transactions/create/',
    views.transaction_create,
    name='transaction_create'
),

path(
    'transactions/<int:pk>/edit/',
    views.transaction_update,
    name='transaction_update'
),

path(
    'transactions/<int:pk>/delete/',
    views.transaction_delete,
    name='transaction_delete'
),
]