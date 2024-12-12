from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", views.home, name="home"),
    path("expenses/", views.view_expenses, name="view_expenses"),
    path("expenses/add/", views.add_expense, name="add_expense"),
    path("expenses/<int:expense_id>/delete/", views.delete_expense, name="delete_expense"),
    path("about/", views.about, name="about"),
    path("fav_chart/", views.favorite_chart, name="fav_chart")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
