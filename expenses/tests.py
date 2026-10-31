from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Category, Transaction


class ExpenseManagerTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='Test12345'
        )

        self.category_income = Category.objects.create(
            name='Salary',
            type='INCOME',
            user=self.user
        )

        self.category_expense = Category.objects.create(
            name='Food',
            type='EXPENSE',
            user=self.user
        )

        self.client = Client()

        self.client.login(
            username='testuser',
            password='Test12345'
        )

    def test_create_income(self):

        transaction = Transaction.objects.create(
            description='Monthly salary',
            amount=Decimal('3000000'),
            date='2026-10-01',
            category=self.category_income,
            user=self.user
        )

        self.assertEqual(
            transaction.category.type,
            'INCOME'
        )

    def test_create_expense(self):

        transaction = Transaction.objects.create(
            description='Lunch',
            amount=Decimal('50000'),
            date='2026-10-01',
            category=self.category_expense,
            user=self.user
        )

        self.assertEqual(
            transaction.category.type,
            'EXPENSE'
        )

    def test_dashboard_balance(self):

        Transaction.objects.create(
            description='Salary',
            amount=Decimal('3000000'),
            date='2026-10-01',
            category=self.category_income,
            user=self.user
        )

        Transaction.objects.create(
            description='Food',
            amount=Decimal('150000'),
            date='2026-10-01',
            category=self.category_expense,
            user=self.user
        )

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context['balance'],
            Decimal('2850000')
        )

    def test_user_cannot_see_other_user_transactions(self):

        other_user = User.objects.create_user(
            username='otheruser',
            password='Test12345'
        )

        other_category = Category.objects.create(
            name='Other food',
            type='EXPENSE',
            user=other_user
        )

        transaction = Transaction.objects.create(
            description='Private expense',
            amount=Decimal('10000'),
            date='2026-10-01',
            category=other_category,
            user=other_user
        )

        response = self.client.get(
            reverse('transaction_update', args=[transaction.pk])
        )

        self.assertEqual(response.status_code, 404)