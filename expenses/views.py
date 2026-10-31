from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.deletion import ProtectedError

from .models import Category
from .forms import CategoryForm


@login_required
def category_list(request):

    categories = Category.objects.filter(
        user=request.user
    )

    return render(
        request,
        'expenses/category_list.html',
        {'categories': categories}
    )


@login_required
def category_create(request):

    form = CategoryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        category = form.save(commit=False)
        category.user = request.user
        category.save()

        messages.success(request, 'Categoría creada.')

        return redirect('category_list')

    return render(
        request,
        'expenses/category_form.html',
        {'form': form}
    )


@login_required
def category_update(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
        user=request.user
    )

    form = CategoryForm(
        request.POST or None,
        instance=category
    )

    if request.method == 'POST' and form.is_valid():

        form.save()

        messages.success(request, 'Categoría actualizada.')

        return redirect('category_list')

    return render(
        request,
        'expenses/category_form.html',
        {'form': form}
    )


@login_required
def category_delete(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        try:
            category.delete()
            messages.success(request, 'Categoría eliminada.')

        except ProtectedError:
            messages.error(
                request,
                'No puedes eliminar una categoría con transacciones.'
            )

        return redirect('category_list')

    return render(
        request,
        'expenses/category_confirm_delete.html',
        {'category': category}
    )