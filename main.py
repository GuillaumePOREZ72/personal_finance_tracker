import pandas as pd  # Importation de la bibliothèque pandas pour les opérations de données
import csv  # Importation de la bibliothèque csv pour lire et écrire des fichiers csv
from datetime import datetime  # Importation de la classe datetime pour travailler avec les dates
from data_entry import get_description, get_amount, get_category, get_date # Importation des fonctions de saisie de données
import matplotlib.pyplot as plt  # Importation de la bibliothèque matplotlib pour les graphiques


class CSV:
    CSV_FILE = "finance_data.csv"  # Nom du fichier csv où sont stockées les données
    COLUMNS = ["date", "amount", "category", "description"]  # Noms des colonnes du fichier csv
    FORMAT = "%d-%m-%Y"  # Format de date utilisé pour l'entrée et la sortie des dates

    @classmethod
    def initialize_csv(cls):  # Méthode pour initialiser le fichier csv si il n'existe pas
        try:
            pd.read_csv(cls.CSV_FILE)  # Essaye de lire le fichier csv
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)  # Crée un dataframe vide avec les colonnes attendues
            df.to_csv(cls.CSV_FILE, index=False)  # Écrit le dataframe dans le fichier csv

    @classmethod
    def add_entry(cls, date, amount, category, description):  # Méthode pour ajouter une nouvelle entrée au fichier csv
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:  # Ouvre le fichier csv en mode ajout
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)  # Écrit la nouvelle entrée dans le fichier csv
        print("Entry added successfully")  # Affiche un message de succès

    @classmethod
    def get_transactions(cls, start_date, end_date):  # Méthode pour récupérer les transactions dans une plage de dates
        df = pd.read_csv(cls.CSV_FILE)  # Lit le fichier csv
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)  # Convertit les dates en format datetime
        start_date = datetime.strptime(start_date, CSV.FORMAT)  # Convertit la date de début en format datetime
        end_date = datetime.strptime(end_date, CSV.FORMAT)  # Convertit la date de fin en format datetime

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)  # Crée un masque pour filtrer les transactions
        filtered_df = df.loc[mask]  # Filtre les transactions avec le masque

        if filtered_df.empty:
            print("No transactions found in the given date range.") # Affiche un message si aucune transaction n'est trouvée
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )  # Affiche les transactions trouvées
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()  # Calcule le total des revenus
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()  # Calcule le total des dépenses
            print("\nSummary:")  # Affiche un résumé
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():  # Fonction pour ajouter une nouvelle transaction
    CSV.initialize_csv()  # Initialise le fichier csv
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )  # Demande la date de la transaction
    amount = get_amount()  # Demande le montant
    category = get_category()  # Demande la catégorie
    description = get_description()  # Demande la description
    CSV.add_entry(date, amount, category, description)  # Ajoute la nouvelle entrée au fichier csv


def plot_transactions(df):  #Fonction pour afficher un graphique des transactions
    df.set_index("date", inplace=True)  # Définit la date comme index

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )  # Calcule le total des revenus par jour
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )  # Calcule le total des dépenses par jour

    plt.figure(figsize=(10, 5))  # Crée une nouvelle fenêtre de graphique
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")  # Affiche les revenus
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")  # Affiche les dépenses
    plt.xlabel("Date")  # Met un label sur l'axe des x
    plt.ylabel("Amount")  # Met un label sur l'axe des y
    plt.title("Income and Expenses Over Time")  # Met un titre au graphique
    plt.legend()  # Affiche la légende
    plt.grid(True)  # Affiche la grille
    plt.show()  # Affiche le graphique


def main():  # Fonction principale
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")  # Demande la date de début
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")  # Demande la date de fin
            df = CSV.get_transactions(start_date, end_date)  # Récupère les transactions dans la plage de dates
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)  # Affiche un graphique des transactions
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
