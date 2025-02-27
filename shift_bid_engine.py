import csv

def import_user_selections(filename):
    """
    Imports user selections from a CSV file.
    
    :param filename: Name of the CSV file to read the user selections
    :return: Dictionary with user as the key and list of selections as the value
    """
    user_selections = {}
    
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        # Skip header
        next(reader)
        for row in reader:
            user = int(row[0])
            selections = row[1:]
            user_selections[user] = selections
    
    return user_selections

def import_user_rankings(filename):
    """
    Imports user rankings from a CSV file.
    
    :param filename: Name of the CSV file to read the user rankings
    :return: List of tuples with (user, rank)
    """
    user_rankings = []
    
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        # Skip header
        next(reader)
        for row in reader:
            user = int(row[0])
            rank = int(row[1])
            user_rankings.append((user, rank))
    
    return user_rankings

def assign_items_based_on_ranking(user_selections, user_rankings):
    """
    Assigns one item from the user's selection list based on their ranking and tracks the selection index.
    
    :param user_selections: Dictionary with user as the key and list of selections as the value
    :param user_rankings: List of tuples with (user, rank)
    :return: Dictionary with user as the key and a tuple (assigned item, selection index) as the value
    """
    # Sort user rankings by rank
    user_rankings_sorted = sorted(user_rankings, key=lambda x: x[1])
    
    assigned_items = set()
    assignments = {}

    # Debugging: print user selections and rankings
    print("User Selections:", user_selections)
    print("User Rankings (sorted):", user_rankings_sorted)
    
    for user, _ in user_rankings_sorted:
        if user not in user_selections:
            # Handle missing users with a warning message and skip them
            print(f"Warning: User {user} not found in selections. Skipping.")
            continue  # Skip this user and move to the next

        for index, item in enumerate(user_selections[user]):
            if item not in assigned_items:
                # Assign the item and store the selection index (starting from 1 for 1st, 2nd, etc.)
                assignments[user] = (item, index + 1)
                assigned_items.add(item)
                break
    
    return assignments

def export_to_csv(assignments, user_rankings, user_selections, filename):
    """
    Exports the assignments to a CSV file, including ranking, user selections, and assigned item index.
    
    :param assignments: Dictionary with user as the key and tuple (assigned item, index) as the value
    :param user_rankings: List of tuples with (user, rank)
    :param user_selections: Dictionary with user as the key and list of selections as the value
    :param filename: Name of the CSV file to save the assignments
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["User", "Assigned Item", "Assigned Item Index", "Rank", "Selections"])
        # Write user assignments with rank, selection list, and assigned item index
        for user, (assigned_item, assigned_index) in assignments.items():
            # Find the user's rank
            user_rank = next((rank for u, rank in user_rankings if u == user), None)
            # Get user's full selection list
            user_selection_list = ', '.join(user_selections[user])
            writer.writerow([user, assigned_item, f"{assigned_index} ({ordinal(assigned_index)})", user_rank, user_selection_list])

def ordinal(n):
    """
    Returns the ordinal string representation of an integer (e.g., 1 -> 1st, 2 -> 2nd).
    """
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

# Prompt the user for input file paths, queue group, and timezone
user_selections_csv = input("Enter the path to the user selections CSV file: ")
user_rankings_csv = input("Enter the path to the user rankings CSV file: ")
queue_group = input("Enter the queue group: ")
timezone = input("Enter the timezone: ")

# Import user selections and rankings from CSV
user_selections = import_user_selections(user_selections_csv)
user_rankings = import_user_rankings(user_rankings_csv)

# Assign items to users based on ranking
assignments = assign_items_based_on_ranking(user_selections, user_rankings)

# Define the output CSV file name
output_csv = f"user_item_assignments_{queue_group}_{timezone}.csv"

# Export to CSV with ranking, full user selections, and assigned item index
export_to_csv(assignments, user_rankings, user_selections, output_csv)

# Display the assignments
for user, (item, index) in assignments.items():
    print(f"{user} is assigned {item} (their {ordinal(index)} choice)")
