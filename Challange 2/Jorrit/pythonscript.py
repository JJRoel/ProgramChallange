import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import datetime


class BudgetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker")
        self.setMinimumWidth(650)
        self.transactions = []
        self.json_file = "transacties.json"

        self.init_ui()
        self.load_transactions()

    def init_ui(self):
        layout = QVBoxLayout()

        # Invoervelden
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Datum (DD-MM-JJJJ)")  # Nederlands formaat dag-maand-jaar
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Bedrag (€)")
        self.category_input = QComboBox()
        self.category_input.addItems(["Boodschappen", "Huur", "Vervoer", "Overig"])

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.category_input)

        self.add_button = QPushButton("Voeg transactie toe")
        self.add_button.clicked.connect(self.add_transaction)

        layout.addLayout(input_layout)
        layout.addWidget(self.add_button)

        # Filters
        filter_layout = QHBoxLayout()
        self.month_filter = QComboBox()
        self.month_filter.addItem("Alle maanden")

        # Nederlandse maandnamen
        nederlandse_maanden = [
            "Januari", "Februari", "Maart", "April", "Mei", "Juni",
            "Juli", "Augustus", "September", "Oktober", "November", "December"
        ]
        for maand in nederlandse_maanden:
            self.month_filter.addItem(maand)

        self.year_filter = QComboBox()
        self.year_filter.addItem("Alle jaren")

        self.month_filter.currentTextChanged.connect(self.update_graph)
        self.year_filter.currentTextChanged.connect(self.update_graph)

        filter_layout.addWidget(QLabel("Filter op maand:"))
        filter_layout.addWidget(self.month_filter)
        filter_layout.addWidget(QLabel("Filter op jaar:"))
        filter_layout.addWidget(self.year_filter)

        layout.addLayout(filter_layout)

        # Grafiekstijl
        graph_style_layout = QHBoxLayout()
        self.graph_style = QComboBox()
        self.graph_style.addItems(["Staafdiagram", "Taartdiagram"])
        self.graph_style.currentTextChanged.connect(self.update_graph)

        graph_style_layout.addWidget(QLabel("Grafiekstijl:"))
        graph_style_layout.addWidget(self.graph_style)

        layout.addLayout(graph_style_layout)

        # Grafiek
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def add_transaction(self):
        date_str = self.date_input.text()
        try:
            date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()  # dag-maand-jaar
        except ValueError:
            print("Ongeldige datum ingevoerd:", date_str)
            return

        try:
            amount = float(self.amount_input.text())
        except ValueError:
            print("Ongeldig bedrag ingevoerd:", self.amount_input.text())
            return

        category = self.category_input.currentText()
        transaction = {
            "date": date_str,  # opgeslagen in dd-mm-jjjj formaat
            "amount": amount,
            "category": category
        }
        self.transactions.append(transaction)
        self.save_transactions()

        if str(date.year) not in [self.year_filter.itemText(i) for i in range(self.year_filter.count())]:
            self.year_filter.addItem(str(date.year))

        self.update_graph()
        self.date_input.clear()
        self.amount_input.clear()

    def update_graph(self):
        selected_month = self.month_filter.currentIndex()
        selected_year = self.year_filter.currentText()

        filtered = []
        for t in self.transactions:
            try:
                date = datetime.datetime.strptime(t["date"], '%d-%m-%Y').date()
            except ValueError:
                continue

            if selected_year != "Alle jaren" and date.year != int(selected_year):
                continue
            if selected_month != 0 and date.month != selected_month:
                continue
            filtered.append((t["amount"], t["category"]))

        # Groepeer per categorie
        data = {}
        for amount, category in filtered:
            data[category] = data.get(category, 0) + amount

        self.ax.clear()
        if data:
            if self.graph_style.currentText() == "Staafdiagram":
                categories = list(data.keys())
                values = list(data.values())
                n = len(categories)
                # print(f"Plot staafdiagram met {n} categorieën")  # eventueel voor debuggen

                bar_width = 0.6
                x_pos = range(n)

                self.ax.bar(x_pos, values, color='skyblue', width=bar_width)
                self.ax.set_xticks(x_pos)
                self.ax.set_xticklabels(categories, rotation=30, ha='right')
                self.ax.set_ylabel("Bedrag (€)")

                # Zorg dat x-limiet net iets groter is dan het aantal balken
                self.ax.set_xlim(-0.5, n - 0.5)

                # Zet y-limiet iets hoger dan max waarde
                ymax = max(values)
                if ymax == 0:
                    ymax = 1
                self.ax.set_ylim(0, ymax * 1.1)

            else:
                self.ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
                self.ax.axis('equal')

        else:
            # Geen data om te plotten, lege grafiek
            self.ax.text(0.5, 0.5, "Geen data om te tonen", ha='center', va='center')
            self.ax.axis('off')

        self.ax.set_title("Uitgaven per categorie")
        self.figure.tight_layout()  # voorkomt overlappende labels
        self.canvas.draw()

    def save_transactions(self):
        try:
            with open(self.json_file, "w") as f:
                json.dump(self.transactions, f, indent=4)
        except Exception as e:
            print("Fout bij opslaan JSON:", e)

    def load_transactions(self):
        if not os.path.exists(self.json_file):
            return

        with open(self.json_file, "r") as f:
            try:
                self.transactions = json.load(f)
            except json.JSONDecodeError:
                self.transactions = []

        # Voeg unieke jaren toe aan de jaarfilter
        jaren = sorted(set(
            str(datetime.datetime.strptime(t["date"], "%d-%m-%Y").year)
            for t in self.transactions
            if t.get("date")
        ))
        for jaar in jaren:
            if jaar not in [self.year_filter.itemText(i) for i in range(self.year_filter.count())]:
                self.year_filter.addItem(jaar)

        self.update_graph()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec())
