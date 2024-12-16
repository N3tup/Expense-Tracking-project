from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("expenses/", views.view_expenses, name="view_expenses"),
    path("expenses/add/", views.add_expense, name="add_expense"),
    path("expenses/<int:expense_id>/delete/", views.delete_expense, name="delete_expense"),
    path("about/", views.about, name="about"),
    path("fav_chart/", views.favorite_chart, name="fav_chart"),
    path("view_incomes/", views.view_incomes, name="view_incomes"),
    path("incomes/add/", views.add_income, name="add_income"),
    path("incomes/<int:income_id>/delete/", views.delete_income, name="delete_income"),
    path('set_budget/', views.set_budget, name='set_budget'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)