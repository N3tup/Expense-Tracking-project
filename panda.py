from error_management import input_error

from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt


chart_type = ["pie_chart","category_pie"]

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



def chart_choser():
    print(f"Chose your chart: ")

    for i, category in enumerate(chart_type, 1):
        print(f"{i}. {category}")
    value_range = f"[1 - {len(chart_type)}]"
    try:
            selected_index_str = input(f"Enter a number between {value_range}: ")
            if not selected_index_str:  # Check for empty input
                raise ValueError("Input cannot be empty") # Raise error to fit within the Try Except block

            selected_index = int(selected_index_str) - 1
            if selected_index not in range(len(chart_type)):
                raise ValueError("Invalid category index")  # Raise ValueError for out-of-range index

            selected_chart = chart_type[selected_index]
    except ValueError as e:
            input_error(str(e))  # Handle ValueError (empty or invalid index)
    return selected_chart

def execute_chart(selected_chart):
    try:     
        # Select date range
        start_date, end_date = date_choser()
        if not start_date or not end_date:
            raise ValueError("Invalid date range selected.")

        # Execute the corresponding chart function
        if selected_chart == "pie_chart":
            show_chart(pie_chart(filepath, start_date, end_date))
        elif selected_chart == "":
            show_chart()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def show_chart(selected_chart):
    plt.plot(selected_chart)
    plt.show()


def pie_chart(filepath, start_date, end_date):
    """
    Génère un graphique en secteurs (pie chart) à partir d'un fichier CSV.
    
    :param filepath: Chemin du fichier CSV contenant les données.
    :param start_date: Date de début pour filtrer les données (format: 'YYYY-MM-DD').
    :param end_date: Date de fin pour filtrer les données (format: 'YYYY-MM-DD').
    """
    try:
        # Charger les données du CSV
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")
        
        df = pd.read_csv(filepath)

        # Vérifier les colonnes nécessaires
        if 'date' not in df.columns or 'category' not in df.columns or 'amount' not in df.columns:
            raise ValueError("Le fichier CSV doit contenir les colonnes 'date', 'category', et 'amount'.")
        
        # Convertir la colonne 'date' en format datetime
        df['date'] = pd.to_datetime(df['date'])

        # Filtrer les données par plage de dates
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        if filtered_df.empty:
            raise ValueError("Aucune donnée disponible pour la plage de dates spécifiée.")

        # Calculer les totaux par catégorie
        category_totals = filtered_df.groupby('category')['amount'].sum()

        # Créer le graphique en secteurs
        plt.figure(figsize=(8, 8))
        category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title(f"Répartition des dépenses par catégorie ({start_date.date()} à {end_date.date()})")
        plt.ylabel('')  # Supprimer l'étiquette de l'axe Y
        plt.show()

    except Exception as e:
        print(f"Une erreur est survenue : {e}")


if __name__ == "__main__":
    filepath = "expenses.csv"
    chart_type = chart_choser()
    try:
        print(chart_type)
        execute_chart(chart_type)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

