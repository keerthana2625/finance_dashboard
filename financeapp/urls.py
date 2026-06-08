from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('income/', views.income_view, name='income'),
    path('income/delete/<int:pk>/', views.income_delete_view, name='income_delete'),
    path('expense/', views.expense_view, name='expense'),
    path('expense/delete/<int:pk>/', views.expense_delete_view, name='expense_delete'),
    path('budget/', views.budget_view, name='budget'),
    path('budget/delete/<int:pk>/', views.budget_delete_view, name='budget_delete'),
    path('savings/', views.savings_view, name='savings'),
    path('savings/delete/<int:pk>/', views.savings_delete_view, name='savings_delete'),
    path('report/', views.report_view, name='report'),
]
