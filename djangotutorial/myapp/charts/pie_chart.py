from matplotlib import pyplot as plt

def generate_pie_chart(expenses, start_date, end_date, buffer):
    # Prepare data
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]
    
    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, 
            colors=plt.cm.Paired.colors, explode=[0.1] * len(categories))  # Highlight slices
    plt.title(f"Expenses from {start_date} to {end_date} - Pie Chart", fontsize=14)
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

def generate_bar_chart(expenses, start_date, end_date, buffer):
    # Prepare data
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]
    
    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(categories, amounts, color=plt.cm.Paired.colors)
    plt.xlabel('Categories')
    plt.ylabel('Amounts')
    plt.title(f"Expenses from {start_date} to {end_date} - Bar Chart", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()