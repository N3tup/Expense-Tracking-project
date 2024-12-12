from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from datetime import datetime
from .charts.pie_chart import generate_pie_chart
import base64
import io
import os
from django.conf import settings
import time



def home(request):
    return render(request, "home.html")

def view_expenses(request):
    expenses = Expense.objects.all()
    return render(request, "expenses/view_expenses.html", {"expenses": expenses})

def add_expense(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        if date.lower() == "today":
            date = datetime.now().strftime("%Y-%m-%d")

        Expense.objects.create(
            name=name,
            category=category,
            amount=float(amount),
            date=datetime.strptime(date, "%Y-%m-%d")
        )
        return redirect("view_expenses")
    return render(request, "expenses/add_expense.html")

def about(request):
    return render(request, "about.html")

def favorite_chart(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    chart_images = {}
    error_message = None

    if not start_date or not end_date:
        today = datetime.today()
        start_date_obj = today.replace(day=1)
        end_date_obj = today
        start_date = start_date_obj.strftime("%Y-%m-%d")
        end_date = end_date_obj.strftime("%Y-%m-%d")
    else:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            error_message = f"Invalid date format: {e}"
            start_date = end_date = None

    if start_date and end_date:
        try:
            expenses = Expense.objects.filter(date__gte=start_date_obj, date__lte=end_date_obj)

            chart_images['pie'] = generate_chart_image(generate_pie_chart, expenses, start_date, end_date)
            #chart_images['bar'] = generate_chart_image(generate_bar_chart, expenses, start_date, end_date)
            #chart_images['line'] = generate_chart_image(generate_line_chart, expenses, start_date, end_date)
            #chart_images['donut'] = generate_chart_image(generate_donut_chart, expenses, start_date, end_date)

        except Exception as e:
            error_message = f"An error occurred while generating the charts: {e}"

    context = {
        "chart_images": chart_images,
        "error_message": error_message,
        "start_date": start_date,
        "end_date": end_date
    }

    return render(request, "favorite_chart.html", context)

def generate_chart_image(chart_function, expenses, start_date, end_date):
    img_buffer = io.BytesIO()
    chart_function(expenses, start_date, end_date, img_buffer)
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('view_expenses')

def clean_up_old_files():
    chart_dir = os.path.join(settings.BASE_DIR, 'static/images')
    for filename in os.listdir(chart_dir):
        file_path = os.path.join(chart_dir, filename)
        if os.path.getmtime(file_path) < time.time() - 600:  # 10 minutes old
            os.remove(file_path)