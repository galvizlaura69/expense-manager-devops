from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Transaction


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = ['name', 'type']

        labels = {
            'name': 'Nombre',
            'type': 'Tipo',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'type': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction

        fields = ['description', 'amount', 'date', 'category']

        labels = {
            'description': 'Descripción',
            'amount': 'Monto',
            'date': 'Fecha',
            'category': 'Categoría',
        }

        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0.01',
                    'placeholder': '0.00'
                }
            ),
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
            'category': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = (
            Category.objects.filter(user=self.user)
        )

        # Si estamos editando, asegurar que el monto se muestre como número limpio
        if self.instance and self.instance.pk:
            self.fields['amount'].initial = self.instance.amount


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        help_text='Requerido. Ingresa una dirección de correo válida.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user