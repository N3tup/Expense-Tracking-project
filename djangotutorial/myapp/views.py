from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Expense
from .models import Income

from .charts.pie_chart import generate_pie_chart
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

        if not photo:
            return render(request, "expenses/add_expense.html", {"error": "Photo is required for automatic extraction."})

        # Read the image in memory without saving it
        try:
            # Process the image directly from the uploaded file
            img = Image.open(photo)  # Open the image from the in-memory file
            img.save(r"C:\Users\romai\Documents\.1_ Romain\2_Esiea\PROJET\TODO\expense_project\djangotutorial\media\expense_photos/temp_image.jpg")  # Temporarily save it to a memory location if needed, optional

            # Process the photo with OCR
            try:
                # Pass the image directly to the OCR function
                extracted_data = extract_ticket_info(img)
                print(f"Extracted Data: {extracted_data}")

                if extracted_data is None:
                    return render(request, "expenses/add_expense.html", {"error": "Could not extract any data from the ticket."})

                # Mapping extracted data to variables
                name = extracted_data.get("location", "Unknown Location")  # Use 'location' as the name by default
                category = extracted_data.get("category", "Other")  # Default category
                amount = extracted_data.get("amount")
                date = extracted_data.get("date")

                # Validate critical fields before saving
                if not amount or not date:
                    error_message = (
                        f"Could not extract all required information from the ticket. "
                        f"Extracted data: {extracted_data}"
                    )
                    return render(request, "expenses/add_expense.html", {"error": error_message})

                # Save the extracted data to the database
                expense = Expense.objects.create(
                    name=name,
                    category=category,
                    amount=amount,
                    date=date,
                    photo=None  # Don't store the image in the database
                )

                # Redirect to the expense list page
                return redirect("view_expenses")
            except Exception as e:
                return render(request, "expenses/add_expense.html", {"error": f"Error processing the ticket: {str(e)}"})
            finally:
                os.remove(r"C:\Users\romai\Documents\.1_ Romain\2_Esiea\PROJET\TODO\expense_project\djangotutorial\media\expense_photos/temp_image.jpg")

        except Exception as e:
            return render(request, "expenses/add_expense.html", {"error": f"An error occurred while processing the photo: {str(e)}"})

    # Render the form initially if the method is GET
    return render(request, "expenses/add_expense.html", {"expense_categories": expense_categories})



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