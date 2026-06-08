from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.source} - {self.amount} ({self.user.username})"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Housing', 'Housing'),
        ('Utilities', 'Utilities'),
        ('Food & Dining', 'Food & Dining'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Shopping', 'Shopping'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Others', 'Others'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Others')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.user.username})"


class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('Housing', 'Housing'),
        ('Utilities', 'Utilities'),
        ('Food & Dining', 'Food & Dining'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Shopping', 'Shopping'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Others', 'Others'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"Budget: {self.category} - {self.amount} ({self.user.username})"


class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    goal_name = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    target_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['target_date', 'created_at']

    def __str__(self):
        return f"Savings Goal: {self.goal_name} - {self.current_amount}/{self.target_amount} ({self.user.username})"
