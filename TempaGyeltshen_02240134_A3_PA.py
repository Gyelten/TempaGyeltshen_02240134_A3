"""
Enhanced Bank Application with Modern GUI

This version improves the visual design and user experience of the banking application
while maintaining all original functionality. Features include:
- Modern color scheme and styling
- Better widget organization
- Improved input validation
- Responsive layout
- Enhanced visual feedback
"""
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox

# --- Custom Exceptions ---
class InputError(Exception):      #Exception raised for invalid user inputs.
    pass

class FundTransferError(Exception):    
    pass

# --- Account Classes ---
class Account:                         #Base class for all account types.
    def __init__(self, number, pin, acc_type, amount=0.0):
        self.num = number
        self.pin = pin
        self.type = acc_type
        self.balance = amount

    def deposit(self, amount):      #Adds the specified amount to the account balance.
        if amount <= 0:
            raise InputError("Amount must be more than zero.")
        self.balance += amount

    def withdraw(self, amount):        #Deducts the specified amount from the balance if sufficient funds exist.
        if amount > self.balance:
            raise InputError("Not enough balance.")
        self.balance -= amount

    def transfer(self, amount, receiver): #Transfers funds to another account.
        if amount > self.balance:
            raise FundTransferError("Not enough funds to send.")
        self.withdraw(amount)
        receiver.deposit(amount)

    def recharge(self, number, amount):         #Simulates a mobile recharge by deducting the amount.
        if not number.isdigit() or len(number) != 10:
            raise InputError("Phone number must be 10 digits.")
        if amount > self.balance:
            raise InputError("Not enough balance for top-up.")
        self.balance -= amount

class Personal(Account):                    #Represents a personal account.
    def __init__(self, number, pin, balance=0.0):
        super().__init__(number, pin, "personal", balance)

class Business(Account):                   #Represents a business account.
    def __init__(self, number, pin, balance=0.0):
        super().__init__(number, pin, "business", balance)

# --- Core Banking System Logic ---
class BankCore:              #Manages all user accounts and data persistence.
    def __init__(self):
        self.users = {}
        self._load_data()

    def _load_data(self):       #Loads account data from the local text file.
        if not os.path.isfile("data.txt"):
            return
        with open("data.txt", "r") as file:
            for line in file:
                acc, pwd, typ, bal = line.strip().split(",")
                cls = Personal if typ == "personal" else Business
                self.users[acc] = cls(acc, pwd, float(bal))

    def _save_data(self):               #Writes all current account data to the local text file.
        with open("data.txt", "w") as file:
            for acc in self.users.values():
                file.write(f"{acc.num},{acc.pin},{acc.type},{acc.balance}\n")

    def new_account(self, kind):        #Creates and registers a new account.
        acc_num = str(random.randint(10000, 99999))
        pin = str(random.randint(1000, 9999))
        user = Personal(acc_num, pin) if kind == "personal" else Business(acc_num, pin)
        self.users[acc_num] = user
        self._save_data()
        return acc_num, pin

    def authenticate(self, acc_num, pin):                      
#Authenticates a user based on account number and PIN.
        acc = self.users.get(acc_num)
        if acc and acc.pin == pin:
            return acc
        raise InputError("Incorrect login details.")

    def remove_account(self, acc_num):                            #Deletes an existing account from the system.
        if acc_num in self.users:
            del self.users[acc_num]
            self._save_data()
        else:
            raise InputError("Account not found.")

# --- Enhanced Graphical User Interface ---
class BankApp:                   #Modernized GUI for the banking application.
    def __init__(self, system):
        self.bank = system
        self.user = None
        self.app = tk.Tk()
        self.app.title("AchoDaka Bank")
        self.app.geometry("400x500")
        self.app.resizable(False, False)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Times New Roman', 10))
        self.style.configure('Header.TLabel', font=('Times New Roman', 14, 'bold'))
        self.style.configure('TButton', font=('Times New Roman', 10), padding=5)
        self.style.configure('Primary.TButton', foreground='black', background='#0078d7')
        self.style.configure('Success.TButton', foreground='black', background='#4CAF50')
        self.style.configure('Danger.TButton', foreground='black', background='#f44336')
        
        # Main container
        self.main_frame = ttk.Frame(self.app)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._show_login()
        self.app.mainloop()

    def _clear(self):                  #Clears the current window content.
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def _show_login(self):    #Displays the login screen with modern styling.
        self._clear()
        
        # Header
        ttk.Label(self.main_frame, text="AchoDaka Bank", style='Header.TLabel').pack(pady=(0, 20))
        
        # Login container
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=10)
        
        # Account number field
        ttk.Label(form_frame, text="Account Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_acc = ttk.Entry(form_frame, font=('Times New Roman', 10))
        self.entry_acc.grid(row=0, column=1, pady=5, padx=5)
        
        # PIN field
        ttk.Label(form_frame, text="PIN:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_pin = ttk.Entry(form_frame, show="•", font=('Times New Roman', 10))
        self.entry_pin.grid(row=1, column=1, pady=5, padx=5)
        
        # Buttons container
        b_layout = ttk.Frame(self.main_frame)
        b_layout.pack(pady=20)
        
        # Login
        ttk.Button(b_layout, text="Login", command=self._login, style='Primary.TButton').pack(fill=tk.X, pady=5)
        
        # Registration buttons
        ttk.Label(b_layout, text="Don't have an account?").pack(pady=(10, 5))
        ttk.Button(b_layout, text="Open Personal Account", 
                  command=lambda: self._register("personal"), style='Success.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(b_layout, text="Open Business Account", 
                  command=lambda: self._register("business"), style='Success.TButton').pack(fill=tk.X, pady=5)
        
        # Focus on account number field
        self.entry_acc.focus_set()

    def _register(self, acc_type):          #Handles new account registration with visual feedback.
        acc_num, pin = self.bank.new_account(acc_type)
        messagebox.showinfo("Account Created", 
                          f"Your new {acc_type} account has been created!\n\n"
                          f"Account Number: {acc_num}\n"
                          f"PIN: {pin}\n\n"
                          "Please keep this information secure.")

    def _login(self):           #Attempts to log the user into the system.
        num = self.entry_acc.get()
        pin = self.entry_pin.get()
        try:
            self.user = self.bank.authenticate(num, pin)
            self.dashboard()
        except InputError as er:
            messagebox.showerror("Login Fails", str(er))
            self.entry_pin.delete(0, tk.END)
            self.entry_pin.focus_set()

    def dashboard(self):             #Displays the main dashboard with account controls.
        self._clear()
        
        # Header with user info
        ttk.Label(self.main_frame, 
                 text=f"Welcome, {self.user.type.capitalize()} User\nAccount: {self.user.num}",
                 style='Header.TLabel').pack(pady=(0, 20))
        
        # Balance display
        amount_layout = ttk.Frame(self.main_frame)
        amount_layout.pack(fill=tk.X, pady=10)
        ttk.Label(amount_layout, text="Balance:").pack(side=tk.LEFT)
        ttk.Label(amount_layout, text=f"Nu. {self.user.balance:.1f}", 
                 font=('Times New Roman', 12, 'bold')).pack(side=tk.RIGHT)
        
        # Action buttons
        b_layout = ttk.Frame(self.main_frame)
        b_layout.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(b_layout, text="Deposit", command=self._deposit, 
                  style='Primary.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(b_layout, text="Withdraw", command=self._withdraw, 
                  style='Primary.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(b_layout, text="Transfer Money", command=self._transfer, 
                  style='Primary.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(b_layout, text="Mobile Recharge", command=self._recharge, 
                  style='Primary.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(b_layout, text="View Balance", command=self._balance, 
                  style='Success.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(b_layout, text="Delete Account", command=self._delete_account, 
                  style='Danger.TButton').pack(fill=tk.X, pady=5)
        ttk.Button(b_layout, text="Logout", command=self._logout).pack(fill=tk.X, pady=(20, 5))

    def _balance(self):              #Shows the current account balance in a styled dialog.
        messagebox.showinfo("Account Balance", 
                          f"Your current balance is:\n\nNu. {self.user.balance:.2f}")

    def _deposit(self):           #Handles deposit transactions with input validation.
        amt = self._prompt_amount("Enter deposit amount:")
        if amt:
            try:
                self.user.deposit(amt)
                self.bank._save_data()
                messagebox.showinfo("Success", f"Deposit of Nu. {amt:.2f} was successful.\nNew balance: Nu. {self.user.balance:.2f}")
            except InputError as e:
                messagebox.showerror("Deposit Failed", str(e))

    def _withdraw(self):         #Handles withdrawals with confirmation.
        amt = self._prompt_amount("Enter withdrawal amount:")
        if amt:
            try:
                self.user.withdraw(amt)
                self.bank._save_data()
                messagebox.showinfo("Success", f"Withdrawal of Nu. {amt:.2f} was successful.\nNew balance: Nu. {self.user.balance:.2f}")
            except InputError as e:
                messagebox.showerror("Withdrawal Failed", str(e))

    def _transfer(self):        #Handles money transfers between accounts.
        receiver = self._prompt("Enter receiver's account number:")
        if not receiver:
            return
            
        if receiver == self.user.num:
            messagebox.showerror("Error", "Cannot transfer to your own account")
            return
            
        amt = self._prompt_amount("Enter amount to transfer:")
        if amt:
            try:
                target = self.bank.users.get(receiver)
                if not target:
                    raise FundTransferError("Receiver account not found.")
                
                if messagebox.askyesno("Confirm Transfer", 
                                     f"Transfer Nu. {amt:.2f} to account {receiver}?"):
                    self.user.send_money(amt, target)
                    self.bank._save_data()
                    messagebox.showinfo("Success", 
                                      f"Transfer of Nu. {amt:.2f} to account {receiver} was successful.\n"
                                      f"New balance: Nu. {self.user.balance:.2f}")
            except (InputError, FundTransferError) as e:
                messagebox.showerror("Transfer Failed", str(e))

    def _recharge(self):           #Handles mobile recharge with validation.
        number = self._prompt("Enter 10-digit mobile number:")
        if not number:
            return
            
        amt = self._prompt_amount("Enter recharge amount:")
        if amt:
            try:
                if messagebox.askyesno("Confirm Recharge", 
                                     f"Recharge Nu. {amt:.2f} to number {number}?"):
                    self.user.recharge(number, amt)
                    self.bank._save_data()
                    messagebox.showinfo("Success", 
                                      f"Recharge of Nu. {amt:.2f} to {number} was successful.\n"
                                      f"New balance: Nu. {self.user.balance:.2f}")
            except InputError as e:
                messagebox.showerror("Recharge Failed", str(e))

    def _delete_account(self):   #Handles account deletion with confirmation.
        if messagebox.askyesno("Confirm delete action", 
                             "Are you sure?\n"
                             "This action is permanent."):
            try:
                self.bank.remove_account(self.user.num)
                messagebox.showinfo("Account successfully deleted.")
                self._show_login()
            except InputError as e:
                messagebox.showerror("Account deletion Fails", str(e))

    def _logout(self):          #returns to login screen.
        self.user = None
        self._show_login()

    def _prompt(self, message):
        """Creates a custom styled input dialog."""
        dialog = tk.Toplevel(self.app)
        dialog.title("Input Required")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text=message).pack(pady=10, padx=20)
        entry = ttk.Entry(dialog, font=('Helvetica', 10))
        entry.pack(pady=5, padx=20)
        result = []
        
        def submit():
            result.append(entry.get())
            dialog.destroy()
        
        b_layout = ttk.Frame(dialog)
        b_layout.pack(pady=10)
        
        ttk.Button(b_layout, text="OK", command=submit, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(b_layout, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        entry.focus_set()
        dialog.grab_set()
        dialog.wait_window()
        
        return result[0] if result else None

    def _prompt_amount(self, message):  #Prompts for a numeric value with validation.
        try:
            value = self._prompt(message)
            if not value:
                return None
            amount = float(value)
            if amount <= 0:
                raise ValueError("Invalid Amount")
            return amount
        except ValueError:
            messagebox.showerror("Please enter a valid amount.")
            return None

# --- Application Launch ---
if __name__ == "__main__":
    system = BankCore()
    BankApp(system)
