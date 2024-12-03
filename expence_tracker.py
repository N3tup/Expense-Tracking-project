from datetime import datetime
from error_management import file_error, input_error, date_error
from expence import Expense


expense_categories = [
        "🍔 Food",
        "🏠 Home", 
        "💼 Work", 
        "✈️ Travel", 
        "✨ Other"
    ]

def main():
    print(f'🪄 running expense tracker of Romain')


    # TODO: Get user input for expense 
    expense = get_user_expense()
    print(expense)

    # TODO: put it in to a file
    #save_user_expense_to_file(expense_name, expense_category, expense_amount, expense_date)
    
    # TODO: Read file and summarize expences
    #read_expenses_from_file()


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



def save_user_expense_to_file(expense_name, expense_category, expense_amount, expense_date):
    print (f'Saving user expense to file')
    f = open("expense.csv","a")
    try:
        f.write(f"{expense_name},{expense_category},{expense_amount},{expense_date}\n")
    except:
        
        handle_file_error("Error writing to file")
    f.close()    

    

def read_expenses_from_file():
    print (f'Here are your expenses !')
    

if __name__ == "__main__":
    main()
