from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("expenses/", views.view_expenses, name="view_expenses"),
    path("expenses/add/", views.add_expense, name="add_expense"),
    path("expenses/<int:expense_id>/delete/", views.delete_expense, name="delete_expense"),
    path("about/", views.about, name="about"),
    path("fav_chart/", views.favorite_chart, name="fav_chart")
]
