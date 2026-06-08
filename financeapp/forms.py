from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Income, Expense, Budget, Savings

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'source': forms.TextInput(attrs={'placeholder': 'e.g., Salary, Freelance', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional details...', 'rows': 3, 'class': 'form-control'}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional details...', 'rows': 3, 'class': 'form-control'}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'start_date', 'end_date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['goal_name', 'target_amount', 'current_amount', 'target_date']
        widgets = {
            'goal_name': forms.TextInput(attrs={'placeholder': 'e.g., Emergency Fund, New Laptop', 'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'}),
            'current_amount': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
