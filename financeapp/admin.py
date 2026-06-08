from django.contrib import admin
from .models import Income, Expense, Budget, Savings

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'date', 'user')
    list_filter = ('date', 'user')
    search_fields = ('source', 'description')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'user')
    list_filter = ('category', 'date', 'user')
    search_fields = ('category', 'description')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'start_date', 'end_date', 'user')
    list_filter = ('category', 'user')
    search_fields = ('category',)

@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = ('goal_name', 'target_amount', 'current_amount', 'target_date', 'user')
    list_filter = ('user',)
    search_fields = ('goal_name',)
