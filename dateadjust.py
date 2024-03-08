from datetime import datetime, timedelta

def calculate_priority(creation_date, selection):
    # Convert creation_date string to datetime object
    creation_date = datetime.strptime(creation_date, "%Y-%m-%d")

    # Get current date
    current_date = datetime.now()

    # Adjust selection based on days passed
    if selection == "within a week" and (current_date - creation_date).days >= 6:
        selection = "today"
    elif selection == "within a month" and (current_date - creation_date).days >= 21:
        selection = "within a week"

    # Assign priority based on selection
    if selection == "today":
        return "high"
    elif selection == "within a week":
        return "medium"
    elif selection == "within a month":
        return "low"
    else:
        return "Invalid selection"

# Example usage
creation_date = input("Enter the date of creation (YYYY-MM-DD): ")
selection = input("Enter your selection ('today', 'within a week', or 'within a month'): ")

priority = calculate_priority(creation_date, selection)
print("Priority:", priority)
