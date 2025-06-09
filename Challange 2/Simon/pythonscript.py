import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

# --- Main Application Class ---
class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Persoonlijke Financiën Tracker")
        self.root.geometry("1200x700")

        self.transactions = []
        self.budget = {} # Format: {"YYYY-MM": amount}

        # --- UI Layout ---
        self.create_widgets()
        self.update_summary_and_list()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for input and summary
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # --- Transaction Input Form ---
        form_frame = ttk.LabelFrame(left_frame, text="Transactie Toevoegen")
        form_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Datum (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(form_frame, text="Beschrijving:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Categorie:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Entry(form_frame)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Bedrag:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Toevoegen", command=self.add_transaction)
        add_button.grid(row=4, columnspan=2, pady=10)

        # --- Summary Display ---
        summary_frame = ttk.LabelFrame(left_frame, text="Overzicht")
        summary_frame.pack(fill=tk.X, pady=10)

        self.summary_label = ttk.Label(summary_frame, text="", font=("Helvetica", 12))
        self.summary_label.pack(pady=5, padx=5)
        
        # --- Budget and Export ---
        action_frame = ttk.LabelFrame(left_frame, text="Acties")
        action_frame.pack(fill=tk.X, pady=10)

        budget_button = ttk.Button(action_frame, text="Maandbudget Instellen", command=self.set_monthly_budget)
        budget_button.pack(pady=5, fill=tk.X)

        export_button = ttk.Button(action_frame, text="Exporteer naar CSV", command=self.export_to_csv)
        export_button.pack(pady=5, fill=tk.X)


        # Right frame for list and graph
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # --- Filters ---
        filter_frame = ttk.Frame(right_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(filter_frame, text="Filter op Categorie:").pack(side=tk.LEFT, padx=(0, 5))
        self.filter_category_entry = ttk.Entry(filter_frame)
        self.filter_category_entry.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(filter_frame, text="Filter op Maand (YYYY-MM):").pack(side=tk.LEFT, padx=(0, 5))
        self.filter_month_entry = ttk.Entry(filter_frame)
        self.filter_month_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        filter_button = ttk.Button(filter_frame, text="Filter", command=self.apply_filters)
        filter_button.pack(side=tk.LEFT)

        reset_button = ttk.Button(filter_frame, text="Reset", command=self.reset_filters)
        reset_button.pack(side=tk.LEFT, padx=5)

        # --- Transaction List ---
        list_frame = ttk.LabelFrame(right_frame, text="Transacties")
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Datum", "Beschrijving", "Categorie", "Bedrag")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # --- Graph ---
        graph_frame = ttk.LabelFrame(right_frame, text="Uitgaven Grafiek")
        graph_frame.pack(fill=tk.X, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack()

    # --- Core Logic ---
    def add_transaction(self):
        date_str = self.date_entry.get()
        description = self.desc_entry.get()
        category = self.category_entry.get()
        amount_str = self.amount_entry.get()

        if not all([date_str, description, category, amount_str]):
            messagebox.showerror("Fout", "Alle velden zijn verplicht.")
            return

        try:
            amount = float(amount_str)
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Fout", "Ongeldige datum (gebruik YYYY-MM-DD) of bedrag.")
            return
            
        # Automatische categorisatie
        if not category:
            category = self.auto_categorize(description)

        transaction = {
            "date": date_str,
            "description": description,
            "category": category,
            "amount": amount
        }
        self.transactions.append(transaction)
        
        # Sorteer transacties op datum
        self.transactions.sort(key=lambda x: x['date'])

        self.check_budget(date_str)
        self.update_summary_and_list()
        self.clear_entries()

    def update_summary_and_list(self, filtered_transactions=None):
        transactions_to_show = filtered_transactions if filtered_transactions is not None else self.transactions

        income = sum(t['amount'] for t in transactions_to_show if t['amount'] > 0)
        expenses = sum(t['amount'] for t in transactions_to_show if t['amount'] < 0)
        balance = income + expenses

        summary_text = f"Inkomsten: €{income:.2f}\nUitgaven: €{abs(expenses):.2f}\n\nSaldo: €{balance:.2f}"
        self.summary_label.config(text=summary_text)

        self.tree.delete(*self.tree.get_children())
        for t in transactions_to_show:
            amount_formatted = f"€{t['amount']:.2f}"
            self.tree.insert("", "end", values=(t['date'], t['description'], t['category'], amount_formatted))

        self.update_graph(transactions_to_show)

    def update_graph(self, transactions):
        self.ax.clear()
        
        expense_categories = {}
        for t in transactions:
            if t['amount'] < 0:
                category = t['category']
                amount = abs(t['amount'])
                expense_categories[category] = expense_categories.get(category, 0) + amount

        if expense_categories:
            labels = expense_categories.keys()
            sizes = expense_categories.values()
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            self.ax.set_title("Uitgaven per Categorie")
        else:
            self.ax.text(0.5, 0.5, "Geen uitgaven om te tonen", ha='center', va='center')
        
        self.canvas.draw()

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.desc_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def apply_filters(self):
        category_filter = self.filter_category_entry.get().lower()
        month_filter = self.filter_month_entry.get()

        filtered = self.transactions
        
        if category_filter:
            filtered = [t for t in filtered if category_filter in t['category'].lower()]
        
        if month_filter:
            try:
                datetime.strptime(month_filter, "%Y-%m")
                filtered = [t for t in filtered if t['date'].startswith(month_filter)]
            except ValueError:
                messagebox.showerror("Fout", "Ongeldige maand-format (gebruik YYYY-MM).")
                return

        self.update_summary_and_list(filtered)

    def reset_filters(self):
        self.filter_category_entry.delete(0, tk.END)
        self.filter_month_entry.delete(0, tk.END)
        self.update_summary_and_list()

    # --- Bonus Features ---
    def set_monthly_budget(self):
        month = simpledialog.askstring("Budget", "Voer de maand in (YYYY-MM):")
        if not month: return
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            messagebox.showerror("Fout", "Ongeldige maand-format (gebruik YYYY-MM).")
            return

        amount = simpledialog.askfloat("Budget", f"Voer het budget in voor {month}:")
        if amount is not None:
            self.budget[month] = amount
            messagebox.showinfo("Succes", f"Budget voor {month} ingesteld op €{amount:.2f}")

    def check_budget(self, date_str):
        month = date_str[:7]
        if month in self.budget:
            monthly_expenses = sum(abs(t['amount']) for t in self.transactions if t['date'].startswith(month) and t['amount'] < 0)
            if monthly_expenses > self.budget[month]:
                messagebox.showwarning("Budget Waarschuwing", f"Je hebt het budget van €{self.budget[month]:.2f} voor {month} overschreden!\n"
                                                           f"Huidige uitgaven: €{monthly_expenses:.2f}")

    def auto_categorize(self, description):
        description = description.lower()
        if re.search(r'boodschappen|supermarkt|albert heijn|jumbo', description):
            return "Boodschappen"
        if re.search(r'huur|hypotheek', description):
            return "Huisvesting"
        if re.search(r'salaris|loon', description):
            return "Salaris"
        if re.search(r'restaurant|cafe|eten buiten de deur', description):
            return "Uit eten"
        return "Overig" # Default category

    def export_to_csv(self):
        if not self.transactions:
            messagebox.showinfo("Info", "Geen transacties om te exporteren.")
            return
            
        filename = f"transacties_{datetime.now().strftime('%Y%m%d')}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["date", "description", "category", "amount"])
                writer.writeheader()
                writer.writerows(self.transactions)
            messagebox.showinfo("Succes", f"Data succesvol geëxporteerd naar {filename}")
        except IOError as e:
            messagebox.showerror("Fout", f"Kon het bestand niet schrijven: {e}")


# --- Run the application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()