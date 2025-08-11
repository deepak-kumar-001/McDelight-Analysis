import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
import os
import matplotlib.pyplot as plt
from time import strftime 

# File paths for CSV
MENU_CSV = 'menu.csv'
CUSTOMER_CSV = 'customer.csv'
BILL_CSV = 'bill.csv'

fields = ['Food ID', 'Menu Items', 'Per Serve Size', 'Energy (kCal)', 'Protein (g)',
          'Total fat (g)', 'Sat Fat (g)', 'Trans fat (g)', 'Cholesterols (mg)',
          'Total carbohydrate (g)', 'Total Sugars (g)', 'Added Sugars (g)', 
          'Sodium (mg)', 'PRICE', 'Produce CP', 'Order Count']

#function to clear the screen
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg='medium turquoise')

# Create the lock screen
def create_lock_screen():
    clear_screen()
    logo = Image.open("logo.png") 
    logo = logo.resize((150, 150)) 
    logo_image = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo_image, bg='medium turquoise')
    logo_label.image = logo_image
    logo_label.pack(pady=10)
    tk.Label(root, text="Mc Delight's Analysis", font=("arial", 24),
             bg='medium turquoise', fg='#002A5E').pack(pady=50)
    tk.Button(root, text="Admin Login", width=20, command=owner_login,
             bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Customer Login", width=20, command=customer_login,
              bg='orange', fg='black').pack(pady=10)

# Owner login
def owner_login():
    clear_screen()
    tk.Label(root, text="Admin Login", font=("arial", 20), bg='medium turquoise',
             fg='#002A5E').pack(pady=20)
    tk.Label(root, text="Username", bg='medium turquoise', fg='#002A5E').pack()
    username_entry = tk.Entry(root)
    username_entry.pack()
    tk.Label(root, text="Password", bg='medium turquoise', fg='#002A5E').pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()
    tk.Button(root, text="Login", command=lambda: verify_owner_login(username_entry,
              password_entry), bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="Back", command=create_lock_screen, bg='orange', 
              fg='black').pack(pady=20)

def verify_owner_login(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "admin123":
        owner_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

# Customer login
def customer_login():
    clear_screen()
    tk.Label(root, text="Customer Login", font=("arial", 20), bg='medium turquoise',
             fg='#002A5E').pack(pady=20)
    tk.Label(root, text="Customer ID", bg='medium turquoise', fg='#002A5E').pack()
    customer_id_entry = tk.Entry(root)
    customer_id_entry.pack()
    tk.Label(root, text="Password", bg='medium turquoise', fg='#002A5E').pack()
    customer_password_entry = tk.Entry(root, show="*")
    customer_password_entry.pack()
    tk.Button(root, text="Login", command=lambda:verify_customer_login(customer_id_entry, 
              customer_password_entry), bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="Back", command=create_lock_screen, bg='orange', 
              fg='black').pack(pady=20)

def verify_customer_login(customer_id_entry, customer_password_entry):
    global customer_id  
    customer_id = customer_id_entry.get()
    password = customer_password_entry.get()
    customer_df = pd.read_csv(CUSTOMER_CSV)
    if customer_id in customer_df['Customer ID'].astype(str).values:
        customer = customer_df[customer_df['Customer ID'].astype(str) == customer_id]
        if password == customer['Password'].values[0]:
            customer_dashboard() 
        else:
            messagebox.showerror("Login Failed", "Incorrect Password")
    else:
        messagebox.showerror("Login Failed", "Customer ID not found")

# Owner dashboard
def owner_dashboard():
    clear_screen()
    tk.Label(root, text="Admin Dashboard", font=("arial", 24), bg='medium turquoise',fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Manage Menu", width=20, command=menu_management,bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Manage Customers", width=20, command=customer_management,bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Manage Bills", width=20, command=bill_management,bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="View Graphs", width=20, command=owner_graphs,bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Logout", width=20, command=create_lock_screen,bg='orange', fg='black').pack(pady=20)

# Customer dashboard
def customer_dashboard():
    global customer_id
    clear_screen()
    tk.Label(root, text=f"Customer Dashboard ID: {customer_id}", font=("arial", 24),bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Display Menu Items", width=20, command=cust_menu,bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="View Bills", width=20, command=lambda: show_cust_bills(customer_id),bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="View Analysis", width=20, command=user_graphs,bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Logout", width=20, command=create_lock_screen,bg='orange', fg='black').pack(pady=20)

def cust_menu():
    clear_screen()
    try:
        if os.path.exists(MENU_CSV):
            # Load the menu data
            menu_df = pd.read_csv(MENU_CSV)
            display_table(menu_df[['Food ID','Menu Items','Per Serve Size','Energy (kCal)','Protein (g)','Total fat (g)','Sat Fat (g)',
                                   'Trans fat (g)','Cholesterols (mg)','Total carbohydrate (g)','Total Sugars (g)','Added Sugars (g)',
                                   'Sodium (mg)','PRICE','Produce CP' ,'Order Count']])
        else:
            tk.Label(root, text="Menu file not found.", font=("arial", 12), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    tk.Button(root, text="Back", width=20, command=customer_dashboard, bg='orange', fg='black').pack(pady=20)


def show_cust_bills(customer_id):
    clear_screen()
    tk.Label(root, text=f"Customer ID: {customer_id}", font=("arial", 24), bg='medium turquoise',fg='#002A5E').pack()
    bill_df = pd.read_csv(BILL_CSV)
    customer_bills = bill_df[bill_df['Customer ID'].astype(str) == customer_id]
    if not customer_bills.empty:  # Check if the customer has bills
        display_table(customer_bills)
    else:
        tk.Label(root, text="No bills found for this customer.", font=("Helvetica",12)).pack(pady=20)
    tk.Button(root, text="Home", width=20, command=customer_dashboard,bg='orange', fg='black').pack(pady=20)

def owner_graphs():
    clear_screen()
    tk.Label(root, text="Admin Graphs", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Cost Vs Selling Price", width=30, command=plot_cost_vs_selling_price, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Sales Vs Time Of Day", width=30, command=sales_vs_time_of_day, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Most Profitable Items", width=30, command=most_profitable_items, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Least Profitable Items", width=30, command=least_profitable_items, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Sales Trend", width=30, command=plot_sales_trend_over_time, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Home", width=20, command=owner_dashboard, bg='orange', fg='black').pack(pady=20)

def most_profitable_items():
    """Displays a bar chart showing the 10 most profitable menu items."""
    if os.path.exists(MENU_CSV):
        menu_df = pd.read_csv(MENU_CSV)
        menu_df['PRICE'] = pd.to_numeric(menu_df['PRICE'], errors='coerce')
        menu_df['Produce CP'] = pd.to_numeric(menu_df['Produce CP'], errors='coerce')
        if 'PRICE' not in menu_df.columns or 'Produce CP' not in menu_df.columns:
            messagebox.showerror("Error", "Required columns ('PRICE', 'Produce CP') not found in menu data.")
            return
        menu_df['Profit'] = menu_df['PRICE'] - menu_df['Produce CP']
        menu_df = menu_df.dropna(subset=['Profit'])
        sorted_menu_df = menu_df.sort_values(by='Profit', ascending=False)
        most_profitable = sorted_menu_df.head(10)
        plt.figure(figsize=(10, 6))
        plt.barh(most_profitable['Menu Items'], most_profitable['Profit'], color='lightgreen', edgecolor='black')
        plt.xlabel('Profit (₹)', fontsize=12)
        plt.ylabel('Menu Items', fontsize=12)
        plt.title('Top 10 Most Profitable Menu Items', fontsize=14)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", f"{MENU_CSV} file not found.")

def least_profitable_items():
    """Displays a bar chart showing the 10 least profitable menu items."""
    if os.path.exists(MENU_CSV):
        menu_df = pd.read_csv(MENU_CSV)
        menu_df['PRICE'] = pd.to_numeric(menu_df['PRICE'], errors='coerce')
        menu_df['Produce CP'] = pd.to_numeric(menu_df['Produce CP'], errors='coerce')
        if 'PRICE' not in menu_df.columns or 'Produce CP' not in menu_df.columns:
            messagebox.showerror("Error", "Required columns ('PRICE', 'Produce CP') not found in menu data.")
            return
        menu_df['Profit'] = menu_df['PRICE'] - menu_df['Produce CP']
        menu_df = menu_df.dropna(subset=['Profit'])
        sorted_menu_df = menu_df.sort_values(by='Profit', ascending=True)
        least_profitable = sorted_menu_df.head(10)
        plt.figure(figsize=(10, 6))
        plt.barh(least_profitable['Menu Items'], least_profitable['Profit'], color='salmon', edgecolor='black')
        plt.xlabel('Profit (₹)', fontsize=12)
        plt.ylabel('Menu Items', fontsize=12)
        plt.title('Top 10 Least Profitable Menu Items', fontsize=14)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", f"{MENU_CSV} file not found.")

def plot_sales_trend_over_time():
    """Plots the sales trend over time from the bill data."""
    if os.path.exists(BILL_CSV):
        bill_data = pd.read_csv(BILL_CSV)
        if 'Bill Date' not in bill_data.columns or 'Total Price' not in bill_data.columns:
            messagebox.showerror("Error", "Required columns ('Bill Date', 'Total Price') not found in bill data.")
            return
        bill_data['Bill Date'] = pd.to_datetime(bill_data['Bill Date'], errors='coerce')
        bill_data = bill_data.dropna(subset=['Bill Date'])
        sales_trend = bill_data.groupby(bill_data['Bill Date'].dt.to_period('M'))['Total Price'].sum()
        sales_trend.index = sales_trend.index.to_timestamp()
        plt.figure(figsize=(10, 6))
        plt.plot(sales_trend.index, sales_trend.values, marker='o', color='teal', label='Sales')
        plt.title("Sales Trend Over Time", fontsize=16)
        plt.xlabel("Month", fontsize=14)
        plt.ylabel("Total Sales (₹)", fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", f"{BILL_CSV} file not found.")

def plot_cost_vs_selling_price():
    menu_df = pd.read_csv(MENU_CSV)

    def generate_plot():
        food_ids_input = food_ids_entry.get().split(',')
        try:
            food_ids = [fid.strip() for fid in food_ids_input]
        except ValueError:
            messagebox.showerror("Error", "Invalid Food IDs. Please enter values separated by commas.")
            return
        filtered_df = menu_df[menu_df['Food ID'].isin(food_ids)]
        if filtered_df.empty:
            messagebox.showerror("Error", "No matching food items found for the given Food IDs.")
            return

        food_items = filtered_df['Menu Items']
        cost_of_prep = filtered_df['Produce CP']
        selling_price = filtered_df['PRICE']
        x = range(len(food_items))
        plt.bar(x, cost_of_prep, width=0.4, label='Cost of Preparation', align='center')
        plt.bar(x, selling_price, width=0.3, label='Selling Price', align='edge')
        plt.xlabel('Food Items')
        plt.ylabel('Price (₹)')
        plt.title('Cost of Preparation vs Selling Price')
        plt.xticks(x, food_items, fontsize=8)
        plt.yticks(fontsize=8)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Create a small interface for input
    clear_screen()
    tk.Label(root, text="Plot Cost vs Selling Price", font=("arial", 20), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Label(root, text="Enter Food IDs (comma-separated):", bg='medium turquoise', fg='#002A5E').pack()
    food_ids_entry = tk.Entry(root, width=50)
    food_ids_entry.pack(pady=10)
    tk.Button(root, text="Generate Plot", command=generate_plot, bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="Back", command=owner_graphs, bg='orange', fg='black').pack(pady=20)

def sales_vs_time_of_day():
    if os.path.exists(BILL_CSV):
        bill_df = pd.read_csv(BILL_CSV)
        if 'Bill Time' in bill_df.columns and 'Total Price' in bill_df.columns:
            bill_df['Bill Time'] = pd.to_datetime(bill_df['Bill Time'], errors='coerce')
            bill_df['Hour'] = bill_df['Bill Time'].dt.hour
            total_sales_by_hour = bill_df.groupby('Hour')['Total Price'].sum()
            plt.bar(total_sales_by_hour.index, total_sales_by_hour.values, width=0.4, label='Total Sales', align='center')
            plt.xlabel('Hour of Day')
            plt.ylabel('Total Sales (₹)')
            plt.title('Total Sales vs Time of Day')
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showerror("Error", "The required columns ('Bill Time' and 'Total Price') are missing from the CSV.")
    else:
        messagebox.showerror("Error", "Bill CSV file not found.")
        
def menu_item_purchases_chart():
    """Displays a horizontal bar chart of menu item purchase counts."""
    if os.path.exists(BILL_CSV):
        bill_df = pd.read_csv(BILL_CSV)
        # Aggregate menu item purchase counts
        menu_item_counts = bill_df.groupby('Menu Items')['Quantity'].sum().sort_values(ascending=False)
        plt.figure(figsize=(20, 12))
        menu_item_counts.plot(kind='barh', color='skyblue', edgecolor='black')
        plt.title('Number of Times Each Menu Item Has Been Purchased', fontsize=16)
        plt.xlabel('Number of Times Purchased', fontsize=14)
        plt.ylabel('Menu Items', fontsize=14)
        plt.yticks(fontsize=4)
        plt.tight_layout()
        plt.gca().invert_yaxis()  # Invert y-axis to show the highest values at the top
        plt.show()
    else:
        messagebox.showerror("Error", "Bill CSV file not found.")
def user_graphs():
    clear_screen()
    tk.Label(root, text="User Analysis", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Customer nutrition", width=30, command=customer_nutrition, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Purchase Quantity", width=30, command=cust_history, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Top 10 Menu Items", width=30, command=top_10_menu_items_chart, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Protein Rich Items", width=30, command=plot_top_protein_foods, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Home", width=20, command=customer_dashboard, bg='orange', fg='black').pack(pady=20)


def plot_top_protein_foods(menu_csv='menu.csv'):
    """Plots a bar chart of the top 10 foods with the most protein content."""
    try:
        menu_df = pd.read_csv(menu_csv)
        if 'Menu Items' not in menu_df.columns or 'Protein (g)' not in menu_df.columns:
            print("Error: Required columns ('Menu Items', 'Protein (g)') are missing.")
            return
        top_protein_foods = menu_df[['Menu Items', 'Protein (g)']].sort_values(by='Protein (g)', ascending=False).head(10)
        plt.figure(figsize=(10, 6))
        plt.barh(top_protein_foods['Menu Items'],top_protein_foods['Protein (g)'],color='royalblue',edgecolor='black')
        plt.xlabel('Protein Content (g)', fontsize=12)
        plt.ylabel('Menu Items', fontsize=12)
        plt.title('Top 10 Foods with Most Proteins', fontsize=16)
        plt.yticks(fontsize=8)
        plt.gca().invert_yaxis()  
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{menu_csv}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def top_10_menu_items_chart():
    """Displays a horizontal bar chart for the top 10 most purchased menu items."""
    if os.path.exists(BILL_CSV):
        bill_df = pd.read_csv(BILL_CSV)
        menu_item_counts = bill_df.groupby('Menu Items')['Quantity'].sum().sort_values(ascending=False)
        top_10_menu_items = menu_item_counts.head(10)
        plt.figure(figsize=(10, 6))
        top_10_menu_items.plot(kind='barh', color='skyblue', edgecolor='black')
        plt.title('Top 10 Most Purchased Menu Items', fontsize=16)
        plt.xlabel('Number of Times Purchased', fontsize=14)
        plt.ylabel('Menu Items', fontsize=14)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror("Error", "Bill CSV file not found.")

def cust_history():
    clear_screen()
    tk.Label(root, text="Show Quantity", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Label(root, text="Enter Bill Number", bg='medium turquoise', fg='#002A5E').pack()

    bill_number_entry = tk.Entry(root)
    bill_number_entry.pack(pady=10)

    def show_history():
        bill_number = bill_number_entry.get()
        if not bill_number.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid numeric Bill Number.")
            return
        bill_number = int(bill_number)
        if os.path.exists(BILL_CSV):
            df_bill = pd.read_csv(BILL_CSV)
            if bill_number in df_bill['Bill Number'].values:
                data = df_bill[df_bill['Bill Number'] == bill_number]
                data.plot(kind='barh', x='Menu Items', y='Quantity', legend=True, color='lightsalmon', edgecolor='black')
                plt.xlabel('Menu Items')
                plt.ylabel('Quantity')
                plt.yticks(fontsize=7)
                plt.title(f'Order Quantity for Bill Number {bill_number}')
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showerror("Not Found", f"Bill Number {bill_number} not found.")
        else:
            messagebox.showerror("File Not Found", "Bill CSV file not found.")

    tk.Button(root, text="Show Quantity", command=show_history, bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="All Graphs", width=10, command=user_graphs, bg='orange', fg='black').pack(pady=10)
def customer_nutrition():
    global customer_id 
    try:
        bill_data = pd.read_csv(BILL_CSV)
        menu_data = pd.read_csv(MENU_CSV)

        # Merge the data on 'Menu Items'
        combined_data = pd.merge(bill_data, menu_data, on="Menu Items", how="inner")
        combined_data["Total Protein"] = combined_data["Protein (g)"] * combined_data["Quantity"]
        combined_data["Total Fat"] = combined_data["Total fat (g)"] * combined_data["Quantity"]
        combined_data["Total Energy"] = combined_data["Energy (kCal)"] * combined_data["Quantity"]
        combined_data["Total Sugar"] = combined_data["Total Sugars (g)"] * combined_data["Quantity"]
        customer_data = combined_data[combined_data["Customer ID"] == int(customer_id)]
        if customer_data.empty:
            messagebox.showerror("Error", f"No data found for Customer ID {customer_id}")
        nutrition_summary = customer_data.groupby("Bill Number")[
            ["Total Protein", "Total Fat", "Total Energy", "Total Sugar"]].sum()
        nutrition_summary.plot(kind="bar", figsize=(10, 6), color=['skyblue', 'orange', 'green', 'red'],edgecolor='black')
        plt.title(f"Nutrition Consumption per Visit (Customer ID: {customer_id})")
        plt.xlabel("Bill Number")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def menu_management():
    clear_screen()
    tk.Label(root, text="Manage Menu", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Add Menu Item", width=20, command=add_menu_item, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Modify Menu Item", width=20, command=modify_menu, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Delete Menu Item", width=20, command=delete_menu_tk, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Display Menu Items", width=20, command=display_menu_items, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Home", width=20, command=owner_dashboard, bg='orange', fg='black').pack(pady=20)

def add_menu_item():
    clear_screen()
    tk.Label(root, text="Add Menu Item", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    fields = [
        'Food ID', 'Menu Items', 'Per Serve Size', 'Energy (kCal)', 'Protein (g)', 'Total fat (g)',
        'Sat Fat (g)', 'Trans fat (g)', 'Cholesterols (mg)', 'Total carbohydrate (g)',
        'Total Sugars (g)', 'Added Sugars (g)', 'Sodium (mg)', 'PRICE', 'Produce CP', 'Order Count'
    ]
    entries = create_entry_fields(fields)

    tk.Button(root, text="Add", command=lambda: save_menu_item(entries), bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="Back", width=20, command=menu_management, bg='orange', fg='black').pack()

def save_menu_item(entries):
    data = {field: entry.get() for field, entry in entries.items()}
    if os.path.exists(MENU_CSV):
        menu_df = pd.read_csv(MENU_CSV)
    else:
        menu_df = pd.DataFrame(columns=data.keys())
    menu_df = pd.concat([menu_df, pd.DataFrame([data])], ignore_index=True)
    menu_df.to_csv(MENU_CSV, index=False)
    messagebox.showinfo("Success", "Menu item added successfully!")
    menu_management()

def modify_menu():
    """Function to modify a menu item."""
    clear_screen()
    tk.Label(root, text="Modify Menu Item", font=('arial', 24), bg='medium turquoise', fg='#002A5E').pack(pady=9)
    tk.Label(root, text='Enter Food ID', bg='medium turquoise', fg='#002A5E').pack()

    global food_id_entry
    food_id_entry = tk.Entry(root)
    food_id_entry.pack()

    display_button = tk.Button(root, text="Display", command=display_food_by_id, bg='orange', fg='black')
    display_button.pack(pady=10)

    global entry_fields
    entry_fields = {}
    fields = [
        'Menu Items', 'Per Serve Size', 'Energy (kCal)', 'Protein (g)', 'Total fat (g)',
        'Sat Fat (g)', 'Trans fat (g)', 'Cholesterols (mg)', 'Total carbohydrate (g)',
        'Total Sugars (g)', 'Added Sugars (g)', 'Sodium (mg)', 'PRICE', 'Produce CP', 'Order Count'
    ]
    for col in fields:
        tk.Label(root, text=col, bg='medium turquoise', fg='#002A5E').pack()
        entry = tk.Entry(root)
        entry.pack()
        entry_fields[col] = entry

    save_button = tk.Button(root, text="Save", command=save_menu, bg='orange', fg='black')
    save_button.pack(pady=2)

    back_button = tk.Button(root, text="Back", width=20, command=menu_management, bg='orange', fg='black')
    back_button.pack(pady=1)
def display_food_by_id():
    """Display menu item details by Food ID."""
    food_id = food_id_entry.get()

    menu_df = pd.read_csv(MENU_CSV)

    row = menu_df[menu_df['Food ID'] == food_id]
    if row.empty:
        messagebox.showerror("Error", "Food ID not found.")
        return
    for col in fields[1:]:
        entry_fields[col].delete(0, tk.END)
        entry_fields[col].insert(0, row.iloc[0][col])

def save_menu():
    """Save the modified menu item to the CSV file."""
    food_id = food_id_entry.get()
    menu_df = pd.read_csv(MENU_CSV)
    index = menu_df.index[menu_df['Food ID'] == food_id].tolist()
    if not index:
        messagebox.showerror("Error", "Food ID not found.")
        return
    idx = index[0]
    for col in fields[1:]:
        menu_df.at[idx, col] = entry_fields[col].get()
    menu_df.to_csv(MENU_CSV, index=False)
    messagebox.showinfo("Success", "Data updated successfully!")
    menu_management()

def delete_menu_tk():
    
    clear_screen()
    tk.Label(root, text="Delete Menu Item", font=('arial', 24), bg='medium turquoise', fg='#002A5E').pack(pady=9)
    tk.Label(root, text='Enter Food ID', bg='medium turquoise', fg='#002A5E').pack()

    global food_id_entry
    food_id_entry = tk.Entry(root)
    food_id_entry.pack()

    display_button = tk.Button(root, text="Display", command=display_food_by_id, bg='orange', fg='black')
    display_button.pack(pady=10)

    global entry_fields
    entry_fields = {}
    fields = [
        'Menu Items', 'Per Serve Size', 'Energy (kCal)', 'Protein (g)', 'Total fat (g)',
        'Sat Fat (g)', 'Trans fat (g)', 'Cholesterols (mg)', 'Total carbohydrate (g)',
        'Total Sugars (g)', 'Added Sugars (g)', 'Sodium (mg)', 'PRICE', 'Produce CP', 'Order Count'
    ]
    for col in fields:
        tk.Label(root, text=col, bg='medium turquoise', fg='#002A5E').pack()
        entry = tk.Entry(root)
        entry.pack()
        entry_fields[col] = entry

    tk.Button(root, text="Delete", command=lambda: delete_menu_item(food_id_entry), bg='orange', fg='black').pack(pady=1)
    
    back_button = tk.Button(root, text="Back", width=20, command=menu_management, bg='orange', fg='black')
    back_button.pack(pady=1)

def delete_menu_item(food_id_entry):
    food_id = food_id_entry.get()
    if os.path.exists(MENU_CSV):
        menu_df = pd.read_csv(MENU_CSV)
        if food_id in menu_df['Food ID'].astype(str).values:
            menu_df = menu_df[menu_df['Food ID'] != food_id]
            menu_df.to_csv(MENU_CSV, index=False)
            messagebox.showinfo("Success", f"Menu item with Food ID {food_id} deleted successfully!")
            menu_management()
        else:
            messagebox.showerror("Error", "Food ID not found.")
    else:
        messagebox.showerror("Error", "Menu database not found.")

def display_menu_items():
    clear_screen()
    if os.path.exists(MENU_CSV):
        menu_df = pd.read_csv(MENU_CSV)
        display_table(menu_df)
    else:
        tk.Label(root, text="No menu items found.", font=("arial", 12), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Back", width=20, command=menu_management, bg='orange', fg='black').pack(pady=20)


# Customer management
def customer_management():
    clear_screen()
    tk.Label(root, text="Manage Customers", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Add Customer", width=20, command=add_customer, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Modify Customer", width=20, command=modify_customer_tk, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Delete Customer", width=20, command=delete_customer_tk, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Display Customers", width=20, command=display_customers, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Home", width=20, command=owner_dashboard, bg='orange', fg='black').pack(pady=20)
def add_customer():
    clear_screen()
    tk.Label(root, text="Add Customer", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    fields = ['Customer ID', 'Tokens', 'Visits', 'Password']
    entries = create_entry_fields(fields)
    tk.Button(root, text="Add", command=lambda: save_customer(entries), bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="Back", width=20, command=customer_management, bg='orange', fg='black').pack(pady=20)
    
def save_customer(entries):
    data = {field: entry.get() for field, entry in entries.items()}
    if os.path.exists(CUSTOMER_CSV): customer_df =pd.read_csv(CUSTOMER_CSV)
    else:
        customer_df = pd.DataFrame(columns=data.keys())
    customer_df = pd.concat([customer_df, pd.DataFrame([data])], ignore_index=True)
    customer_df.to_csv(CUSTOMER_CSV, index=False)
    messagebox.showinfo("Success", "Customer added successfully!")
    customer_management()
    
def modify_customer_tk():  # No NaN values can be entered when modifying
    clear_screen()
    tk.Label(root, text="Modify Customer", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Label(root, text="Enter Customer ID", bg='medium turquoise', fg='#002A5E').pack()
    customer_id_entry = tk.Entry(root)
    customer_id_entry.pack()
    tk.Button(root, text="Search", command=lambda: display_customer_details(customer_id_entry), bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="Back", width=20, command=customer_management, bg='orange', fg='black').pack(pady=20)

def display_customer_details(customer_id_entry):
    customer_id = customer_id_entry.get()
    if os.path.exists(CUSTOMER_CSV):
        customer_df = pd.read_csv(CUSTOMER_CSV)
        row = customer_df[customer_df['Customer ID'].astype(str) == customer_id]
        if not row.empty:
            fields = row.columns.tolist()[1:]
            entries = create_entry_fields(fields, row.iloc[0])
            tk.Button(root, text="Save", command=lambda: save_modified_customer(customer_df, customer_id, entries), bg='orange', fg='black').pack(pady=20)
        else:
            messagebox.showerror("Error", "Customer ID not found.")
    else:
        messagebox.showerror("Error", "Customer database not found.")


def save_modified_customer(customer_df, customer_id, entries):
    for field, entry in entries.items():
        customer_df.loc[customer_df['Customer ID'].astype(str) == customer_id, field] = entry.get()
    customer_df.to_csv(CUSTOMER_CSV, index=False)
    messagebox.showinfo("Success", "Customer details updated successfully!")
    customer_management()
def delete_customer_tk():
    clear_screen()
    tk.Label(root, text="Delete Customer", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Label(root, text="Enter Customer ID", bg='medium turquoise', fg='#002A5E').pack()
    customer_id_entry = tk.Entry(root)
    customer_id_entry.pack()
    tk.Button(root, text="Delete", command=lambda: delete_customer(customer_id_entry), bg='orange', fg='black').pack(pady=20)
    back_button = tk.Button(root, text="Back", width=20, command=menu_management, bg='orange', fg='black')
    back_button.pack(pady=20)


def delete_customer(customer_id_entry):
    customer_id = customer_id_entry.get()
    if os.path.exists(CUSTOMER_CSV):
        customer_df = pd.read_csv(CUSTOMER_CSV)
        if customer_id in customer_df['Customer ID'].astype(str).values:
            customer_df = customer_df[customer_df['Customer ID'].astype(str) != customer_id]
            customer_df.to_csv(CUSTOMER_CSV, index=False)
            messagebox.showinfo("Success", f"Customer with ID {customer_id} deleted successfully!")
            customer_management()
        else:
            messagebox.showerror("Error", "Customer ID not found.")
    else:
        messagebox.showerror("Error", "Customer database not found.")


def display_customers():
    clear_screen()
    if os.path.exists(CUSTOMER_CSV):
        customer_df = pd.read_csv(CUSTOMER_CSV)
        display_table(customer_df)
    else:
        tk.Label(root, text="No customers found.", font=("arial", 12), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Back", width=20, command=customer_management, bg='orange', fg='black').pack(pady=20)


# Bill management
def bill_management():
    clear_screen()
    tk.Label(root, text="Manage Bills", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Add Bill", width=20, command=add_bill, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Display Bills", width=20, command=display_bills, bg='orange', fg='black').pack(pady=10)
    tk.Button(root, text="Home", width=20, command=owner_dashboard, bg='orange', fg='black').pack(pady=20)


def add_bill():
    clear_screen()
    tk.Label(root, text="Add Bill", font=("arial", 24), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    fields = ['Customer ID', 'Bill Number', 'Menu Items', 'Quantity', 'Unit Price', 'Total Price']
    entries = create_entry_fields(fields)
    tk.Button(root, text="Add", command=lambda: save_bill(entries), bg='orange', fg='black').pack(pady=20)
    tk.Button(root, text="Back", width=20, command=bill_management, bg='orange', fg='black').pack(pady=20)
def save_bill(entries):
    data = {field: entry.get() for field, entry in entries.items()}
    if os.path.exists(BILL_CSV):
        bill_df = pd.read_csv(BILL_CSV)
    else:
        bill_df = pd.DataFrame(columns=data.keys())
    bill_df = pd.concat([bill_df, pd.DataFrame([data])], ignore_index=True)
    bill_df.to_csv(BILL_CSV, index=False)
    messagebox.showinfo("Success", "Bill added successfully!")
    bill_management()

def display_bills():
    clear_screen()
    if os.path.exists(BILL_CSV):
        bill_df = pd.read_csv(BILL_CSV)
        display_table(bill_df)
    else:
        tk.Label(root, text="No bills found.", font=("arial", 12), bg='medium turquoise', fg='#002A5E').pack(pady=20)
    tk.Button(root, text="Back", width=20, command=bill_management, bg='orange', fg='black').pack(pady=20)

def create_entry_fields(fields, row=None):
    entries = {}
    for field in fields:
        tk.Label(root, text=field, bg='medium turquoise', fg='#002A5E').pack()
        entry = tk.Entry(root)
        if row is not None:
            entry.insert(0, row[field])
        entry.pack()
        entries[field] = entry
    return entries

def display_table(df):
    tree = ttk.Treeview(root)
    tree["columns"] = df.columns.tolist()
    for col in df.columns:
        tree.column(col, anchor=tk.W, width=100)
        tree.heading(col, text=col)
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
    tree.pack(pady=20)


# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    root.title("MC DELIGHT'S ANALYSIS")
    root.geometry("750x800")
    root.resizable(True,True)
    create_lock_screen()
    root.mainloop()

