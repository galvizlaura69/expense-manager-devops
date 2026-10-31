from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.deletion import ProtectedError

from .models import Category
from .forms import CategoryForm


from decimal import Decimal
from django.db.models import Sum


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

from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm


@login_required
def transaction_list(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('category')

    return render(
        request,
        'expenses/transaction_list.html',
        {'transactions': transactions}
    )


@login_required
def transaction_create(request):

    form = TransactionForm(
        request.POST or None,
        user=request.user
    )

    if request.method == 'POST' and form.is_valid():

        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()

        messages.success(request, 'Movimiento registrado.')

        return redirect('transaction_list')

    return render(
        request,
        'expenses/transaction_form.html',
        {'form': form}
    )


@login_required
def transaction_update(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    form = TransactionForm(
        request.POST or None,
        instance=transaction,
        user=request.user
    )

    if request.method == 'POST' and form.is_valid():

        form.save()

        messages.success(request, 'Movimiento actualizado.')

        return redirect('transaction_list')

    return render(
        request,
        'expenses/transaction_form.html',
        {'form': form}
    )


@login_required
def transaction_delete(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        transaction.delete()

        messages.success(request, 'Movimiento eliminado.')

        return redirect('transaction_list')

    return render(
        request,
        'expenses/transaction_confirm_delete.html',
        {'transaction': transaction}
    )



@login_required
def dashboard(request):

    transactions = Transaction.objects.filter(
        user=request.user
    )

    income = transactions.filter(
        category__type='INCOME'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    expenses = transactions.filter(
        category__type='EXPENSE'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    balance = income - expenses

    return render(
        request,
        'expenses/dashboard.html',
        {
            'income': income,
            'expenses': expenses,
            'balance': balance
        }
    )