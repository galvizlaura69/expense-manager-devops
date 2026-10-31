from django import forms
from .models import Category, Transaction


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = ['name', 'type']

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

        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0.01'
                }
            ),
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
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