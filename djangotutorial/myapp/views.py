from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from datetime import date
from django.db.models import Sum

from .models import Expense, Budget
from .models import Income

from .charts.pie_chart import generate_pie_chart, generate_bar_chart
import base64
import io
import os
import time
from datetime import datetime

from .OCR.OCR import extract_ticket_info
from PIL import Image




def home(request):
    return render(request, "home.html")

def add_expense(request):
    expense_categories = ["Food", "Housing", "Transportation", "Utilities", "Entertainment", "Travel", "Shopping", "Other"]
    if request.method == "POST":
        photo = request.FILES.get("photo")
        name = request.POST.get("name")
        category = request.POST.get("expense_category")
        amount = request.POST.get("amount")
        expense_date = request.POST.get("date")

        if photo:
            try:
                # Process the image directly from the uploaded file
                img = Image.open(photo)
                img.save(r"C:\Users\romai\Documents\.1_ Romain\2_Esiea\PROJET\TODO\expense_project\djangotutorial\media\expense_photos/temp_image.jpg")

                # Process the photo with OCR
                try:
                    extracted_data = extract_ticket_info(img)
                    if extracted_data is None:
                        return render(request, "expenses/add_expense.html", {"error": "Could not extract any data from the ticket."})

                    # Mapping extracted data to variables
                    name = extracted_data.get("location", name)  # Use 'location' as the name by default
                    category = extracted_data.get("category", category)  # Default category
                    amount = extracted_data.get("amount", amount)
                    expense_date = extracted_data.get("date", expense_date)

                    # Validate critical fields before saving
                    if not amount or not expense_date:
                        error_message = (
                            f"Could not extract all required information from the ticket. "
                            f"Extracted data: {extracted_data}"
                        )
                        return render(request, "expenses/add_expense.html", {"error": error_message})

                except Exception as e:
                    return render(request, "expenses/add_expense.html", {"error": f"Error processing the ticket: {str(e)}"})
                finally:
                    os.remove(r"C:\Users\romai\Documents\.1_ Romain\2_Esiea\PROJET\TODO\expense_project\djangotutorial\media\expense_photos/temp_image.jpg")

            except Exception as e:
                return render(request, "expenses/add_expense.html", {"error": f"An error occurred while processing the photo: {str(e)}"})

        # Save the expense
        expense = Expense.objects.create(
            name=name,
            category=category,
            amount=amount,
            date=expense_date,
            photo=photo if photo else None  # Save photo if provided
        )

        # Redirect to the expense list page
        return redirect("view_expenses")

    # Render the form initially if the method is GET
    return render(request, "expenses/add_expense.html", {"expense_categories": expense_categories})



def about(request):
    return render(request, "about.html")

from matplotlib import pyplot as plt
import pandas as pd

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
            chart_images['bar'] = generate_chart_image(generate_bar_chart, expenses, start_date, end_date)

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


def view_expenses(request):
    expenses = Expense.objects.all()  # Fetch all expenses or customize as needed
    return render(request, 'expenses/view_expenses.html', {'expenses': expenses})

def view_incomes(request):
    incomes = Income.objects.all()  # Fetch all income records
    return render(request, "incomes/view_incomes.html", {"incomes": incomes})

def add_income(request):
    expense_categories = ["Salary", "Business", "Investment", "Gift", "Other"]  # Replace with your actual categories

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        category = request.POST.get("income_categories", "other").capitalize()
        amount = request.POST.get("amount", "").strip()
        date = request.POST.get("date", "").strip()

        error = None

        # Validate amount
        try:
            amount = float(amount)
        except ValueError:
            error = "Amount must be a valid number."

        # Validate date or 'today'
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            error = error or "Date must be in YYYY-MM-DD format."

        # If no errors, save income to the database
        if not error:
            Income.objects.create(name=name, category=category, amount=amount, date=date)
            return redirect("view_incomes")  # Redirect to incomes list after success

        # Return the form with the error message if validation fails
        return render(
            request, 
            "incomes/add_income.html", 
            {"error": error, "name": name, "amount": amount, "date": date, "expense_categories": expense_categories}
        )

    # Render the form initially with categories
    return render(request, "incomes/add_income.html", {"expense_categories": expense_categories})

def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    income.delete()
    return redirect('view_incomes')



from django.utils import timezone

from django.utils import timezone

from django.utils import timezone
from django.contrib import messages
from .models import Budget
from datetime import datetime

def set_budget(request):
    expense_categories = ["Food", "Housing", "Transportation", "Utilities", "Entertainment", "Travel", "Shopping", "Other"]
    
    if request.method == 'POST':
        expense_category = request.POST.get('expense_category')
        amount = request.POST.get('amount', None)
        date_str = request.POST.get('date', None)
        
        # Validate inputs
        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, 'set_budget.html', {
                'expense_categories': expense_categories,
                'amount': amount,
                'date': date_str,
            })

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, "Invalid amount format. Please enter a valid number.")
            return render(request, 'set_budget.html', {
                'expense_categories': expense_categories,
                'amount': amount,
                'date': date_str,
            })

        # Validate and parse date
        if not date_str:
            date = timezone.now()
        else:
            try:
                date = datetime.strptime(date_str, '%Y-%m')
            except ValueError:
                messages.error(request, "Invalid date format. Please enter a date in YYYY-MM format.")
                return render(request, 'set_budget.html', {
                    'expense_categories': expense_categories,
                    'amount': amount,
                    'date': date_str,
                })

        # Extract month and year
        month = date.month
        year = date.year

        # Check if a budget already exists for the given category, month, and year
        budget, created = Budget.objects.update_or_create(
            category=expense_category,
            month=month,
            year=year,
            defaults={'amount': amount, 'date': date}
        )

        if created:
            messages.success(request, "Budget set successfully!")
        else:
            messages.success(request, "Budget updated successfully!")

        return redirect('dashboard')  # Redirect to the dashboard or another page

    # Render the form
    return render(request, 'set_budget.html', {
        'expense_categories': expense_categories,
    })



def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    budget.delete()
    messages.success(request, "Budget deleted successfully!")
    return redirect('dashboard')


from datetime import date
from django.db.models import Sum

def dashboard(request):
    current_year = date.today().year
    current_month_num = date.today().month
    current_month_name = date.today().strftime("%B")

    # List of all possible categories
    all_categories = ["Food", "Housing", "Transportation", "Utilities", "Entertainment", "Travel", "Shopping", "Other"]

    # Fetch budgets for the current month and year
    budgets = Budget.objects.filter(year=current_year, month=current_month_num).order_by('category')

    expenses = (
        Expense.objects.filter(date__year=current_year, date__month=current_month_num)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
    )

    # Prepare alerts and budget usage data
    alerts = []
    budget_usage = []

    for budget in budgets:
        # Get total spent for this category, default to 0 if not found
        spent = next((e['total'] for e in expenses if e['category'] == budget.category), 0)
        percentage_used = (spent / budget.amount) * 100 if budget.amount > 0 else 0

        budget_usage.append({
            'id': budget.id,  # Include the id attribute
            'category': budget.category,
            'limit': budget.amount,
            'spent': spent,
            'percentage_used': round(percentage_used, 2),
        })

        # 80% threshold alert
        if spent >= budget.amount * 0.8:  
            alerts.append(
                f"⚠️ You have spent {spent} ({percentage_used:.1f}%) in {budget.category}, nearing your limit of {budget.amount}!"
            )

    # Determine categories without budgets
    categories_with_budgets = [budget.category.lower().strip() for budget in budgets]
    categories_without_budgets = [category for category in all_categories if category.lower().strip() not in categories_with_budgets]

    # Pass the budget data and alerts to the template
    return render(
        request,
        'dashboard.html',
        {
            'budgets': budget_usage,
            'alerts': alerts,
            'expenses': expenses,
            'current_year': current_year,
            'current_month': current_month_name,
            'categories_without_budgets': categories_without_budgets,
        },
    )