import csv
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import re

generated_ids = set()  # Store the generated IDs

def generate_unique_id():
    new_id = 0
    while True:
        new_id += 1  # Generate a random 4-digit ID
        if new_id not in generated_ids:
            with open(user_info_filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == str(new_id):  # Check if the ID exists in the user_info file
                        break
                else:
                    generated_ids.add(new_id)
                    return new_id
def get_user_info():
    global unique_ID
    global name
    global dob
    global occupation
    name = name_var.get()
    dob = dob_var.get()
    occupation = occupation_var.get()
    return [unique_ID, name, dob, occupation]

def get_favorite_things():
    global user_id
    user_id = user_id_var.get()
    sport = sport_var.get()
    activity = activity_var.get()
    return [user_id, sport, activity]

def write_to_csv(filename, data):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        is_existing_row = False

        for row in rows:
            if row and row[0] == data[0]:  # Check if the ID exists in the first column of the row
                writer.writerow(data)
                is_existing_row = True
            else:
                writer.writerow(row)

        if not is_existing_row:
            writer.writerow(data)


def merge_info(user_info, favorite_things):
    return user_info + favorite_things[1:]  # Exclude the user_id in the merge

def search_info(filename, search_value):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == search_value or row[1] == search_value:
                return row
    return None

def submit_user_info():
    global unique_ID
    global name
    global dob
    global occupation
    unique_ID = generate_unique_id()
    name = name_var.get()
    dob = dob_var.get()
    occupation = occupation_var.get()
    user_info = [unique_ID, name, dob, occupation]

    # Check if the name already exists in the user_info file
    user_info_exists = False
    with open(user_info_filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        for i, row in enumerate(rows):
            if row and row[1] == name:
                confirmation = messagebox.askquestion("Confirmation", f"The name '{name}' already exists. Are you sure you want to submit this info?", icon='warning')
                if confirmation == 'yes':
                    # Overwrite the existing row with the new user info
                    rows[i] = [unique_ID, name, dob, occupation]
                    user_info_exists = True
                    break
                else:
                    # Show a message in the tab
                    message_label.config(text=f"User info for '{name}' not submitted.")
                    return  # Do not submit

    # If the name exists, overwrite the existing row with the new user info
    if user_info_exists:
        with open(user_info_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
        # Clear input fields
        name_var.set('')
        dob_var.set('')
        occupation_var.set('')
        message_label.config(text = f"User info updated successfully. ID: {unique_ID}, Name: {name}, Date of Birth: {dob}, Occupation: {occupation}.", foreground= "green")
    else:
        # Write the new user info to the user_info file
        write_to_csv(user_info_filename, user_info)
        # Clear input fields
        name_var.set('')
        dob_var.set('')
        occupation_var.set('')
        message_label.config(text=f"User info for '{name}' submitted successfully. ID: {unique_ID}, Date of Birth: {dob}, Occupation: {occupation}.", foreground = "green")
def merge(user_id):
    # Get the user info and favorite things from the CSV files
    user_info = search_info(user_info_filename, user_id)
    favorite_things = search_info(favorite_things_filename, user_id)

    # Check if both user_info and favorite_things exist for the given user_id
    if user_info is not None and favorite_things is not None:
        # Merge the user_info and favorite_things data
        merge_data = merge_info(user_info, favorite_things)

        # Check if the ID already exists in the CSV file and update the row if it does
        with open(merge_filename, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        with open(merge_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            is_existing_row = False

            for row in rows:
                if row and row[0] == user_id:  # Check if the ID exists in the first column of the row
                    writer.writerow(merge_data)
                    is_existing_row = True
                else:
                    writer.writerow(row)

            if not is_existing_row:
                writer.writerow(merge_data)

        messagebox.showinfo("Information", "Data merged successfully.")


def submit_favorite_things():
    global user_id
    name = name_var.get()
    user_id = user_id_var.get()
    sport = sport_var.get()
    activity = activity_var.get()

    # Check if the user ID exists in the favorite_things file
    favorite_things_exists = False
    with open(favorite_things_filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == user_id or row and row[1] == name:
                favorite_things_exists = True
                break

    # If the user ID exists, overwrite the existing entry
    if favorite_things_exists:
        # Read all existing rows, updating the row for the user ID
        rows = []
        with open(favorite_things_filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == user_id or row and row[1] == name:
                    rows.append([user_id_var.get(),sport, activity])
                else:
                    rows.append(row)

        # Write the updated rows back to the file
        with open(favorite_things_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
    else:
        # User ID does not exist, add a new entry
        favorite_things = [user_id_var.get(), sport, activity]
        write_to_csv(favorite_things_filename, favorite_things)

    # Merge user info and favorite things data
    user_info = search_info(user_info_filename, user_id)
    if user_info:
        merge_data = merge_info(user_info, [user_id, sport, activity])

        # Check if the ID already exists in the merge file and update the row if it does
        with open(merge_filename, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        with open(merge_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            is_existing_row = False

            for row in rows:
                if row and row[0] == user_id or row and row [1] == name:  # Check if the ID exists in the first column of the row
                    writer.writerow(merge_data)
                    is_existing_row = True
                else:
                    writer.writerow(row)

            if not is_existing_row:
                writer.writerow(merge_data)

        # Clear the input fields
        user_id_var.set('')
        sport_var.set('')
        activity_var.set('')

        # Show success message in the message label
        message_label_3.config(text="Favorite things submitted successfully.", foreground="green")
    else:
        # User ID does not exist in user_info file, show error message in the message label
        message_label_3.config(text="User ID does not exist. Unable to submit favorite things.", foreground="red")


    
def search():
    search_value = simpledialog.askstring("Search", "Enter the ID or Name to search for:")
    result = search_info(merge_filename, search_value)
    if result:
        message_label_4.config(text =  f"Information found: {result}", foreground = "green")
    else:
        message_label_4.config(text = "Information not found.", foreground = "red")

def show_user_info_to_submit():
    # Get user info based on the provided ID or name
    search_value = user_id_var.get()
    user_info_by_id = search_info(user_info_filename, search_value)
    if user_info_by_id:
        # Show the user info to be submitted    
        user_id, name, dob, occupation = user_info_by_id[0], user_info_by_id[1], user_info_by_id[2], user_info_by_id[3]
        message = f"User Info to Submit: \nID: {user_id} \nName: {name}\nDate of Birth: {dob}\nOccupation: {occupation}"
        message_label_2.config(text=message, foreground="green")
    else:
        # If not found by ID, search by name
        user_info_by_name = None
        with open(user_info_filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[1] == search_value:
                    user_info_by_name = row
                    break
        if user_info_by_name:
            # Show the user info to be submitted
            user_id, name, dob, occupation = user_info_by_id[0], user_info_by_id[1], user_info_by_id[2], user_info_by_id[3]
            message = f"User Info to Submit: \nID: {user_id} \nName: {name}\nDate of Birth: {dob}\nOccupation: {occupation}"
            message_label_2.config(text=message, foreground="green")
        else:
            message_label_2.config(text=f"User info not found for ID/Name: {search_value}.", foreground="red")

def validate_dob_format(P):
    return re.match(r'^\d{4}-\d{2}-\d{2}$', P)

def validate_dob_input(P):
    if not re.match(r'^\d{0,4}(-\d{0,2}){0,2}$', P):
        return False

    parts = P.split('-')
    if len(parts) > 3:
        return False

    year = int(parts[0]) if parts[0] else 0
    month = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    day = int(parts[2]) if len(parts) > 2 and parts[2] else 0

    if year < 0 or month < 0 or day < 0:
        return False

    if month > 12 or day > 31:
        return False

    if month in [4, 6, 9, 11] and day > 30:
        return False

    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            if day > 29:
                return False
        elif day > 28:
            return False

    return True



if __name__ == "__main__":

    user_info_filename = 'user_info.csv'
    favorite_things_filename = 'favorite_things.csv'
    merge_filename = 'merge.csv'
    unique_ID = ""  # Initialize the unique_ID variable
    name = ""  # Initialize the name variable
    dob = ""  # Initialize the dob variable
    occupation = ""  # Initialize the occupation variable
    user_id = ""  # Initialize the user_id variable

    # Your existing code


    root = tk.Tk()
    root.title("Welcome File Operator")
    root.geometry("800x600")

    style = ttk.Style()
    style.theme_use("alt") 

    # Create a Notebook widget for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(padx=20, pady=20, fill='both', expand=True)

    # User Info Tab
    user_info_tab = ttk.Frame(notebook)
    notebook.add(user_info_tab, text='User Info')

    # User Info Input Fields
    name_var = tk.StringVar()
    dob_var = tk.StringVar()
    occupation_var = tk.StringVar()

    ttk.Label(user_info_tab, text="User Info", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=20)


    ttk.Label(user_info_tab, text="Name:").grid(row=1, column=0, padx=10, pady=10)
    ttk.Entry(user_info_tab, textvariable=name_var).grid(row=1, column=1, padx=10, pady=10)

    message_label = ttk.Label(user_info_tab, text="", foreground="green")
    message_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


    ttk.Label(user_info_tab, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
    dob_entry = ttk.Entry(user_info_tab, textvariable=dob_var, validate="key")
    dob_entry.grid(row=2, column=1, padx=10, pady=10)
    # Set the validation functions for DOB entry
  # Set the validation functions for DOB entry
    dob_entry['validatecommand'] = (root.register(validate_dob_input), '%P')
    dob_entry['validate'] = 'key'
    dob_entry.bind('<FocusOut>', lambda e: dob_var.set(dob_var.get()[:10]))  # Truncate input to 10 characters
    
    # Limit DOB input to 10 characters
    dob_var.trace("w", lambda *args: dob_var.set(dob_var.get()[:10]))

    # Validate date of birth format
   
    ttk.Label(user_info_tab, text="Occupation:").grid(row=3, column=0, padx=10, pady=10)
    ttk.Entry(user_info_tab, textvariable=occupation_var).grid(row=3, column=1, padx=10, pady=10)

    ttk.Button(user_info_tab, text="Submit User Info", command=submit_user_info).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Favorite Things Tab
    favorite_things_tab = ttk.Frame(notebook)
    notebook.add(favorite_things_tab, text='Favorite Things')

    # Favorite Things Input Fields
    user_id_var = tk.StringVar()


    ttk.Label(favorite_things_tab, text="Favorite Things", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    ttk.Label(favorite_things_tab, text="User ID or Name:").grid(row=1, column=0, padx=10, pady=10)
    ttk.Entry(favorite_things_tab, textvariable=user_id_var).grid(row=1, column=1, padx=10, pady=10)

    ttk.Button(favorite_things_tab, text="Show User Info to Submit", command=show_user_info_to_submit).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    message_label_2 = ttk.Label(favorite_things_tab, text="", foreground="green")
    message_label_2.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    # Your favorite_things input fields and button placement here
    sport_var = tk.StringVar()
    activity_var = tk.StringVar()

    ttk.Label(favorite_things_tab, text="Favorite Sport:").grid(row=4, column=0, padx=10, pady=10)
    ttk.Entry(favorite_things_tab, textvariable=sport_var).grid(row=4, column=1, padx=10, pady=10)

    ttk.Label(favorite_things_tab, text="Favorite Activity:").grid(row=5, column=0, padx=10, pady=10)
    ttk.Entry(favorite_things_tab, textvariable=activity_var).grid(row=5, column=1, padx=10, pady=10)

    ttk.Button(favorite_things_tab, text="Submit Favorite Things", command=submit_favorite_things).grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    
    message_label_3 = ttk.Label(favorite_things_tab, text="", foreground="green")
    message_label_3.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    # Search Data Tab
    search_data_tab = ttk.Frame(notebook)
    notebook.add(search_data_tab, text='Search Data')

    # Search Data Input Fields
    search_value_var = tk.StringVar()
    
    ttk.Label(search_data_tab, text="Search Info", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=20)


    ttk.Label(search_data_tab, text="Search only if have submitted all information.").grid(row=1, column=0, padx=10, pady=10)

    ttk.Button(search_data_tab, text="Search", command=search).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    message_label_4 = ttk.Label(search_data_tab, text="", foreground="green")
    message_label_4.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    root.mainloop()