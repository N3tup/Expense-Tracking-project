import pandas as pd
import matplotlib.pyplot as plt

def pie_chart(expenses, start_date, end_date, output_path):
    """
    Generates a pie chart from expenses data and saves it as an image.
    
    :param expenses: QuerySet of Expense objects.
    :param start_date: Start date for the chart title (string format: 'YYYY-MM-DD').
    :param end_date: End date for the chart title (string format: 'YYYY-MM-DD').
    :param output_path: Path to save the generated pie chart image.
    """
    try:
        # Convert the queryset to a DataFrame
        data = list(expenses.values('category', 'amount'))
        df = pd.DataFrame(data)
        
        if df.empty:
            raise ValueError("No data available for the specified date range.")
        
        # Calculate total amount per category
        category_totals = df.groupby('category')['amount'].sum()
        
        # Create the pie chart
        plt.figure(figsize=(8, 8))
        category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title(f"Expenses by Category ({start_date} to {end_date})")
        plt.ylabel('')  # Remove the y-label
        
        # Save the pie chart as an image
        plt.savefig(output_path)
        plt.close()
        
    except Exception as e:
        raise e  # Let the view handle the exception