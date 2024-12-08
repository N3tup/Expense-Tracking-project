from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

def date_choser():

    #chose the filter option
    filter_option = input("Choose a filter option:\n1. This month\n2. Last month\n3. Last 3 months\n4. This year\n5. Custom\n")
    from datetime import timedelta

    today = datetime.today()
    try:
        if filter_option == "1":  # This Month
            start_date = today.replace(day=1)
            end_date = today
        elif filter_option == "2":  # Last Month
            start_date = today.replace(day=1) - timedelta(days=1)
            start_date = start_date.replace(day=1)
            end_date = today.replace(day=1) - timedelta(days=1)
        elif filter_option == "3":  # Last 3 Months
            start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1) - timedelta(days=90)
            end_date = today.replace(day=1) - timedelta(days=1)
        elif filter_option == "4":  # This Year
            start_date = today.replace(month=1, day=1)
            end_date = today
        elif filter_option == "5":  # Custom Dates
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            raise ValueError("Input Error: Invalid filter option.")
    except ValueError as e:
        print(f"An error occurred: {str(e)}")
        return None, None
    return start_date, end_date