# charts/pie_chart.py
import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
import time
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments

# Custom cleanup function
def clean_up_old_files():
    chart_dir = os.path.join(settings.BASE_DIR, 'static/images')
    for filename in os.listdir(chart_dir):
        file_path = os.path.join(chart_dir, filename)
        if os.path.getmtime(file_path) < time.time() - 3600:  # 1 hour old
            os.remove(file_path)


def generate_pie_chart(expenses, start_date, end_date, output_path):
    """Generates a Pie Chart showing expenses by category."""
    try:
        data = list(expenses.values('category', 'amount'))
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No data available for the specified date range.")

        category_totals = df.groupby('category')['amount'].sum()
        total = category_totals.sum()

        plt.figure(figsize=(8, 8))
        category_totals.plot(
            kind='pie',
            autopct=lambda pct: f'${pct/100.*total:.2f}',
            startangle=90,
            colors=plt.cm.Paired.colors
        )
        plt.title(f"Expenses by Category ({start_date} to {end_date})")
        plt.ylabel('')
        plt.savefig(output_path,bbox_inches='tight')
        plt.close()

    except Exception as e:
        raise e

def generate_bar_chart(expenses, start_date, end_date, output_path):
    """Generates a Bar Chart showing expenses by category."""
    try:
        data = list(expenses.values('category', 'amount'))
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No data available for the specified date range.")

        category_totals = df.groupby('category')['amount'].sum()

        plt.figure(figsize=(8, 6))
        category_totals.sort_values().plot(kind='bar', color='skyblue')
        plt.title(f"Expenses by Category ({start_date} to {end_date})")
        plt.xlabel("Category")
        plt.ylabel("Amount ($)")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    except Exception as e:
        raise e

def generate_line_chart(expenses, start_date, end_date, output_path):
    """Generates a Line Chart showing expenses over time."""
    try:
        data = list(expenses.values('date', 'amount'))
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No data available for the specified date range.")

        daily_totals = df.groupby('date')['amount'].sum().sort_index()

        plt.figure(figsize=(12, 6))
        daily_totals.plot(kind='line', marker='o', linestyle='-')
        plt.title(f"Daily Expenses ({start_date} to {end_date})")
        plt.xlabel("Date")
        plt.ylabel("Amount ($)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    except Exception as e:
        raise e

def generate_donut_chart(expenses, start_date, end_date, output_path):
    """Generates a Donut Chart showing expenses by category."""
    try:
        data = list(expenses.values('category', 'amount'))
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("No data available for the specified date range.")

        category_totals = df.groupby('category')['amount'].sum()
        total = category_totals.sum()

        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(
            category_totals,
            autopct=lambda pct: f'${pct/100.*total:.2f}',
            startangle=90,
            colors=plt.cm.Paired.colors
        )
        plt.title(f"Expenses by Category ({start_date} to {end_date})")
        # Draw circle for donut shape
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    except Exception as e:
        raise e