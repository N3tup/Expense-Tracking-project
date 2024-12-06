import panda
import os
from error_management import file_error, input_error, date_error
from expence import Expense
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from datetime import datetime



expense_categories = [
        "Food",
        "Home", 
        "Work", 
        "Travel", 
        "Other"
    ]

def main():
    print(f'🪄 running expense tracker of Romain')
    expense_file_path = "expenses.csv"

    # Chose what the user want to do
    try:
        user_choice = int(input("What do you want to do?\n1. Add an expense\n2. View expenses\n3. Generate chart\n"))
        if user_choice == 1:
            print("Adding an expense...")
        elif user_choice == 2:
            print("Viewing expenses...")
            read_expenses_from_file()
        elif user_choice == 3:
            print("Generating chart...")
            # TODO: Faire plus de chart utiles
            selected_chart = panda.chart_choser()
            print(f"chosed chart: {selected_chart}")
            panda.execute_chart(selected_chart)
            # get the png and show it

        else:
            print("Invalid choice. Please select 1, 2, or 3.")
    except ValueError:
        input_error("Invalid input. Please enter a number.")
    pass


def get_user_expense():
    print (f'getting user expenses')

    # Name
    try:
        expense_name = input("Enter your expense name: ")
        if not expense_name:
            raise ValueError("Expense name cannot be empty")
    except ValueError as e:
        input_error(str(e))



    # Category
    # TODO: if category doesnt exist, ask to create it 
    print("Choose an expense category:")
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")
    
    value_range = f"[1 - {len(expense_categories)}]"
    try:
            selected_index_str = input(f"Enter a number between {value_range}: ")
            if not selected_index_str:  # Check for empty input
                raise ValueError("Input cannot be empty") # Raise error to fit within the Try Except block

            selected_index = int(selected_index_str) - 1
            if selected_index not in range(len(expense_categories)):
                raise ValueError("Invalid category index")  # Raise ValueError for out-of-range index

            selected_category = expense_categories[selected_index]

    except ValueError as e:
            input_error(str(e))  # Handle ValueError (empty or invalid index)
            
    # Amount
    try:
        expense_amount = float(input("Enter your expense amount: "))
    except ValueError:
        input_error("Invalid amount. Please enter a valid number.")
    
    # Date
    expense_date = input("Enter your expense date (YYYY-MM-DD): ")
    
    if expense_date == "today":
        expense_date = datetime.now().strftime("%Y-%m-%d")       
    try:
        expense_date = datetime.strptime(expense_date, "%Y-%m-%d")
    except:
        date_error("Invalid date format. Please use YYYY-MM-DD.")
            
    new_expense = Expense(
        name=expense_name,category=selected_category, amount=expense_amount, date=expense_date
    )
    return new_expense



def save_user_expense_to_file(expense: Expense,expense_file_path):
    
    if os.path.exists(expense_file_path):
        try:
            # Charger les données existantes
            expenses_df = pd.read_csv(expense_file_path)
            # si le colomn n'existe pas, il faut les créer
            if expenses_df.empty or not all(
            column in expenses_df.columns for column in ["name", "category", "amount", "date"]
            ):
                expenses_df = pd.DataFrame(columns=["name", "category", "amount", "date"])
                expenses_df.to_csv(expense_file_path, index=False)
        except pd.errors.EmptyDataError:
            # Handle case where the file exists but is empty
            print("File exists but is empty. Recreating with correct structure.")
            expenses_df = pd.DataFrame(columns=["name", "category", "amount", "date"])
            expenses_df.to_csv(expense_file_path, index=False)
    else:
        # Create a new DataFrame if the file doesn't exist
        expenses_df = pd.DataFrame(columns=["name", "category", "amount", "date"])
    new_expense_data = {
        "name": [expense.name],
        "category": [expense.category],
        "amount": [expense.amount],
        "date": [expense.date.strftime("%Y-%m-%d")],
    }
    new_expense_df = pd.DataFrame(new_expense_data)
    expenses_df = pd.concat([expenses_df, new_expense_df], ignore_index=True)
    expenses_df.to_csv(expense_file_path, index=False)

    

def read_expenses_from_file():
    expense_file_path = "expenses.csv"
    df = pd.read_csv(expense_file_path)
    print(df)


if __name__ == "__main__":
    main()
