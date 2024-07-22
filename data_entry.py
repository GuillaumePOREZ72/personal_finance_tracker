from datetime import datetime  # Importation de la classe datetime pour travailler avec les dates

date_format ="%d-%m-%Y"  # Format de date utilisé pour l'entrée et la sortie des dates
CATEGORIES = {"I": "Income", "E": "Expense"}  # Dictionnaire des catégories de transactions


def get_date(prompt, allow_default=False):  # Fonction pour demander une date à l'utilisateur
    date_str = input(prompt)  # Demande une date à l'utilisateur
    if allow_default and not date_str:  # Si la date est vide et que le défaut est autorisé
        return datetime.today().strftime(date_format)  # Retourne la date du jour

    try:
        valid_date = datetime.strptime(date_str, date_format)  # Essaye de parser la date entrée
        return valid_date.strftime(date_format)  # Retourne la date au format attendu
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")  # Affiche un message d'erreur si le format est incorrect
        return get_date(prompt, allow_default)  # Réessaie de demander une date


def get_amount():  # Fonction pour demander un montant à l'utilisateur
    try:
        amount = float(input("Enter the amount: "))  # Demande un montant à l'utilisateur
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")  # Lève une erreur si le montant est négatif ou nul
        return amount
    except ValueError as e:
        print(e)  # Affiche le message d'erreur
        return get_amount()  # Réessaie de demander un montant


def get_category():  # Fonction pour demander une catégorie à l'utilisateur
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()  # Demande une catégorie à l'utilisateur
    if category in CATEGORIES:
        return CATEGORIES[category]  # Retourne la catégorie correspondante

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")  # Affiche un message d'erreur si la catégorie est incorrecte
    return get_category()  # Réessaie de demander une catégorie


def get_description():  # Fonction pour demander une description à l'utilisateur
    return input("Enter a description (optional)")  # Demande une description à l'utilisateur