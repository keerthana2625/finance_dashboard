import csv
import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse

from .models import Income, Expense, Budget, Savings
from .forms import RegistrationForm, IncomeForm, ExpenseForm, BudgetForm, SavingsForm

# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to your Finance Dashboard, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user
    
    # Financial metrics
    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0.00
    total_expense = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0.00
    net_balance = total_income - total_expense
    
    # Recent logs (limit to 5)
    recent_incomes = Income.objects.filter(user=user)[:5]
    recent_expenses = Expense.objects.filter(user=user)[:5]
    
    # Savings Goals
    savings_goals = Savings.objects.filter(user=user)
    for goal in savings_goals:
        goal.progress = min(int((goal.current_amount / goal.target_amount) * 100), 100) if goal.target_amount > 0 else 0
    
    # Budgets & Warning Alerts
    budgets = Budget.objects.filter(user=user)
    over_budget_alerts = []
    for budget in budgets:
        # Calculate spending in that budget's range and category
        spent = Expense.objects.filter(
            user=user, 
            category=budget.category, 
            date__range=[budget.start_date, budget.end_date]
        ).aggregate(Sum('amount'))['amount__sum'] or 0.00
        budget.spent = spent
        budget.progress = min(int((spent / budget.amount) * 100), 100) if budget.amount > 0 else 0
        budget.is_over = spent > budget.amount
        
        if budget.is_over:
            over_budget_alerts.append({
                'category': budget.category,
                'budget': budget.amount,
                'spent': spent,
                'excess': spent - budget.amount
            })
            
    # Chart 1: Expenses by category (Doughnut)
    expense_by_cat = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount'))
    chart_categories = [item['category'] for item in expense_by_cat]
    chart_amounts = [float(item['total']) for item in expense_by_cat]
    
    # Chart 2: Cash flow (last 6 months bar chart)
    today = timezone.localdate()
    months_labels = []
    income_by_month = []
    expense_by_month = []
    
    # Generate last 6 months data dynamically
    for i in range(5, -1, -1):
        # Calculate starting and ending day of target month relative to current local date
        # Subtracting roughly i*30 days, then adjusting to the 1st of that target month
        target_date = today - timedelta(days=i*30)
        first_day = target_date.replace(day=1)
        
        # Determine last day of the month
        if first_day.month == 12:
            next_first = first_day.replace(year=first_day.year+1, month=1)
        else:
            next_first = first_day.replace(month=first_day.month+1)
        last_day = next_first - timedelta(days=1)
        
        month_label = first_day.strftime('%b %Y')
        months_labels.append(month_label)
        
        m_income = Income.objects.filter(user=user, date__range=[first_day, last_day]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        m_expense = Expense.objects.filter(user=user, date__range=[first_day, last_day]).aggregate(Sum('amount'))['amount__sum'] or 0.00
        
        income_by_month.append(float(m_income))
        expense_by_month.append(float(m_expense))
        
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'recent_incomes': recent_incomes,
        'recent_expenses': recent_expenses,
        'savings_goals': savings_goals,
        'budgets': budgets,
        'over_budget_alerts': over_budget_alerts,
        'chart_categories': json.dumps(chart_categories),
        'chart_amounts': json.dumps(chart_amounts),
        'months_labels': json.dumps(months_labels),
        'income_by_month': json.dumps(income_by_month),
        'expense_by_month': json.dumps(expense_by_month),
    }
    return render(request, 'dashboard.html', context)


@login_required
def income_view(request):
    incomes = Income.objects.filter(user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, "Income entry logged successfully!")
            return redirect('income')
    else:
        form = IncomeForm(initial={'date': timezone.localdate()})
        
    return render(request, 'income.html', {'incomes': incomes, 'form': form})


@login_required
def income_delete_view(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, "Income entry deleted successfully.")
    return redirect('income')


@login_required
def expense_view(request):
    expenses = Expense.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            # Check budgets for warning after logging expense
            budgets = Budget.objects.filter(user=request.user, category=expense.category)
            for budget in budgets:
                if expense.date >= budget.start_date and expense.date <= budget.end_date:
                    spent = Expense.objects.filter(
                        user=request.user, 
                        category=budget.category, 
                        date__range=[budget.start_date, budget.end_date]
                    ).aggregate(Sum('amount'))['amount__sum'] or 0.00
                    if spent > budget.amount:
                        messages.warning(request, f"ALERT: You have exceeded your budget limit of {budget.amount} for '{budget.category}'!")
                        
            messages.success(request, "Expense entry logged successfully!")
            return redirect('expense')
    else:
        form = ExpenseForm(initial={'date': timezone.localdate()})
        
    return render(request, 'expense.html', {'expenses': expenses, 'form': form})


@login_required
def expense_delete_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense entry deleted successfully.")
    return redirect('expense')


@login_required
def budget_view(request):
    budgets = Budget.objects.filter(user=request.user)
    for budget in budgets:
        spent = Expense.objects.filter(
            user=request.user, 
            category=budget.category, 
            date__range=[budget.start_date, budget.end_date]
        ).aggregate(Sum('amount'))['amount__sum'] or 0.00
        budget.spent = spent
        budget.progress = min(int((spent / budget.amount) * 100), 100) if budget.amount > 0 else 0
        budget.is_over = spent > budget.amount
        budget.excess = spent - budget.amount
        
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, f"Budget for '{budget.category}' created successfully!")
            return redirect('budget')
    else:
        form = BudgetForm(initial={'start_date': timezone.localdate().replace(day=1), 'end_date': timezone.localdate() + timedelta(days=30)})
        
    return render(request, 'budget.html', {'budgets': budgets, 'form': form})


@login_required
def budget_delete_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget limit removed successfully.")
    return redirect('budget')


@login_required
def savings_view(request):
    savings_goals = Savings.objects.filter(user=request.user)
    for goal in savings_goals:
        goal.progress = min(int((goal.current_amount / goal.target_amount) * 100), 100) if goal.target_amount > 0 else 0
        
    if request.method == 'POST':
        form = SavingsForm(request.POST)
        if form.is_valid():
            savings = form.save(commit=False)
            savings.user = request.user
            savings.save()
            messages.success(request, f"Savings goal '{savings.goal_name}' created successfully!")
            return redirect('savings')
    else:
        form = SavingsForm()
        
    return render(request, 'savings.html', {'savings_goals': savings_goals, 'form': form})


@login_required
def savings_delete_view(request, pk):
    savings = get_object_or_404(Savings, pk=pk, user=request.user)
    if request.method == 'POST':
        savings.delete()
        messages.success(request, "Savings goal deleted successfully.")
    return redirect('savings')


@login_required
def report_view(request):
    user = request.user
    
    # Filter states
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    # Default to current month range
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = timezone.localdate().replace(day=1)
        
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.localdate()
        
    # Query within dates
    incomes = Income.objects.filter(user=user, date__range=[start_date, end_date])
    expenses = Expense.objects.filter(user=user, date__range=[start_date, end_date])
    
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0.00
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0.00
    net_savings = total_income - total_expense
    
    # Group expenses by category
    expense_by_cat = expenses.values('category').annotate(total=Sum('amount'))
    chart_categories = [item['category'] for item in expense_by_cat]
    chart_amounts = [float(item['total']) for item in expense_by_cat]
    
    # Export CSV feature
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="finance_report_{start_date}_{end_date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Report Period', f'{start_date} to {end_date}'])
        writer.writerow([])
        writer.writerow(['SUMMARY'])
        writer.writerow(['Total Income', total_income])
        writer.writerow(['Total Expense', total_expense])
        writer.writerow(['Net Cashflow', net_savings])
        writer.writerow([])
        
        writer.writerow(['INCOME LOGS'])
        writer.writerow(['Date', 'Source', 'Amount', 'Description'])
        for inc in incomes:
            writer.writerow([inc.date, inc.source, inc.amount, inc.description or ''])
            
        writer.writerow([])
        writer.writerow(['EXPENSE LOGS'])
        writer.writerow(['Date', 'Category', 'Amount', 'Description'])
        for exp in expenses:
            writer.writerow([exp.date, exp.category, exp.amount, exp.description or ''])
            
        return response
        
    context = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_savings': net_savings,
        'chart_categories': json.dumps(chart_categories),
        'chart_amounts': json.dumps(chart_amounts),
    }
    return render(request, 'report.html', context)
