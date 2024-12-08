from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from datetime import datetime
from .chart1 import pie_chart
from .models import Expense

import os


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


# chart page where there will be all tha favorite chart
# views.py

# views.py

# views.py



def favorite_chart(request):
    # Get the start and end dates from the GET parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    chart_image = None
    error_message = None

    if start_date and end_date:
        try:
            # Convert date strings to datetime objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Query the Expense model for the specified date range
            expenses = Expense.objects.filter(date__gte=start_date_obj, date__lte=end_date_obj)
            
            # Define the output path for the chart image relative to the static directory
            output_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
            output_path = os.path.join(output_dir, 'pie_chart.png')
            
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Call the pie_chart function
            pie_chart(expenses, start_date, end_date, output_path)
            
            # Relative path for the template (relative to the 'static' directory)
            chart_image = 'images/pie_chart.png'
        
        except Exception as e:
            error_message = str(e)

    context = {
        "chart_image": chart_image,
        "error_message": error_message
    }

    return render(request, "favorite_chart.html", context)


# views.py

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    
    if request.method == "POST":
        expense.delete()
        return redirect("view_expenses")
    
    return render(request, "delete_expense_confirm.html", {"expense": expense})