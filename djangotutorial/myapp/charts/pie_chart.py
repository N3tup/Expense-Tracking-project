# charts/pie_chart.py
from matplotlib import pyplot as plt
import pandas as pd

def generate_pie_chart(expenses, start_date, end_date, buffer):
    # Prepare data
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]
    
    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, 
            colors=plt.cm.Paired.colors, explode=[0.1] * len(categories))  # Highlight slices
    plt.title(f"Expenses from {start_date} to {end_date} - Pie Chart", fontsize=14)
    _, texts, autotexts = plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    for text in autotexts + texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()