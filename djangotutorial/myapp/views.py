from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from datetime import datetime,timedelta
from .charts.pie_chart import (
    generate_pie_chart,
    generate_bar_chart,
    generate_line_chart,
    generate_donut_chart
)
from .models import Expense

import os
import uuid



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
    # Get the start and end dates from the GET parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    chart_images = {}
    error_message = None

    # Set default date range to the current month if not provided
    if not start_date or not end_date:
        today = datetime.today()
        start_date_obj = today.replace(day=1)
        end_date_obj = today
        start_date = start_date_obj.strftime("%Y-%m-%d")
        end_date = end_date_obj.strftime("%Y-%m-%d")
    else:
        try:
            # Convert date strings to datetime objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            error_message = f"Invalid date format: {e}"
            start_date = end_date = None

    if start_date and end_date:
        try:
            # Query the Expense model for the specified date range
            expenses = Expense.objects.filter(date__gte=start_date_obj, date__lte=end_date_obj)

            # Define the output directory
            output_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
            os.makedirs(output_dir, exist_ok=True)

            # Generate unique filenames for each chart to prevent caching issues
            unique_id = uuid.uuid4().hex  # Generates a unique hexadecimal string

            # Generate Pie Chart
            pie_output = os.path.join(output_dir, f'pie_chart_{unique_id}.png')
            generate_pie_chart(expenses, start_date, end_date, pie_output)
            chart_images['pie'] = f'images/pie_chart_{unique_id}.png'

            # Generate Bar Chart
            bar_output = os.path.join(output_dir, f'bar_chart_{unique_id}.png')
            generate_bar_chart(expenses, start_date, end_date, bar_output)
            chart_images['bar'] = f'images/bar_chart_{unique_id}.png'

            # Generate Line Chart
            line_output = os.path.join(output_dir, f'line_chart_{unique_id}.png')
            generate_line_chart(expenses, start_date, end_date, line_output)
            chart_images['line'] = f'images/line_chart_{unique_id}.png'

            # Generate Donut Chart
            donut_output = os.path.join(output_dir, f'donut_chart_{unique_id}.png')
            generate_donut_chart(expenses, start_date, end_date, donut_output)
            chart_images['donut'] = f'images/donut_chart_{unique_id}.png'

        except Exception as e:
            error_message = f"An error occurred while generating the charts: {e}"

    context = {
        "chart_images": chart_images,
        "error_message": error_message,
        "start_date": start_date,
        "end_date": end_date
    }

    return render(request, "favorite_chart.html", context)

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('view_expenses')