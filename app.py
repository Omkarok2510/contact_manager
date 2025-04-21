import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton,
    QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox, QInputDialog
)
from PyQt5.QtCore import Qt

class ContactFormDialog(QDialog):
    def __init__(self, contact=None):
        super().__init__()
        self.setWindowTitle("Add/Edit Contact")
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.number_input = QLineEdit()
        self.email_input = QLineEdit()
        self.dob_input = QLineEdit()
        self.tag_input = QLineEdit()

        if contact:
            self.name_input.setText(contact["name"])
            self.number_input.setText(contact["number"])
            self.email_input.setText(contact["email"])
            self.dob_input.setText(contact["dob"])
            self.tag_input.setText(contact["tag"])

        layout.addRow("Name", self.name_input)
        layout.addRow("Number", self.number_input)
        layout.addRow("Email", self.email_input)
        layout.addRow("DOB (YYYY-MM-DD)", self.dob_input)
        layout.addRow("Tag (Favorite/Emergency)", self.tag_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_contact_data(self):
        return {
            "name": self.name_input.text(),
            "number": self.number_input.text(),
            "email": self.email_input.text(),
            "dob": self.dob_input.text(),
            "tag": self.tag_input.text()
        }

class ContactManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌙 Dark Contact Manager")
        self.setGeometry(100, 100, 500, 450)

        self.contacts = [
            {"name": "Omkar", "number": "8624012521", "email": "omkarok2510@gmail.com", "dob": "2005-10-25", "tag": "Favorite"},
            {"name": "Rushi", "number": "9881102781", "email": "omkarok158@gmail.com", "dob": "2005-11-11", "tag": "None"},
            {"name": "Aditya", "number": "9763624007", "email": "adityadehade2@gmail.com", "dob": "2005-06-12", "tag": "Emergency"},
        ]
        self.filtered_contacts = self.contacts.copy()

        self.init_ui()
        self.setStyleSheet(self.custom_dark_theme())

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search contacts...")
        self.search_input.textChanged.connect(self.search_contacts)
        layout.addWidget(self.search_input)

        self.contact_list = QListWidget()
        self.refresh_contacts()
        layout.addWidget(self.contact_list)

        add_button = QPushButton("➕ Add Contact")
        add_button.clicked.connect(self.add_contact)
        layout.addWidget(add_button)

        edit_button = QPushButton("✏️ Edit Selected")
        edit_button.clicked.connect(self.edit_contact)
        layout.addWidget(edit_button)

        delete_button = QPushButton("❌ Delete Selected")
        delete_button.clicked.connect(self.delete_contact)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def refresh_contacts(self):
        self.contact_list.clear()
        for contact in self.filtered_contacts:
            tag = f" ⭐ {contact['tag']}" if contact["tag"] != "None" else ""
            self.contact_list.addItem(f"{contact['name']} - {contact['number']} {tag}")

    def search_contacts(self, query):
        query = query.lower()
        self.filtered_contacts = [c for c in self.contacts if query in c['name'].lower()]
        self.refresh_contacts()

    def add_contact(self):
        dialog = ContactFormDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.contacts.append(dialog.get_contact_data())
            self.filtered_contacts = self.contacts.copy()
            self.refresh_contacts()

    def edit_contact(self):
        selected_index = self.contact_list.currentRow()
        if selected_index < 0:
            QMessageBox.warning(self, "No Selection", "Please select a contact to edit.")
            return
        contact = self.filtered_contacts[selected_index]
        dialog = ContactFormDialog(contact)
        if dialog.exec_() == QDialog.Accepted:
            updated = dialog.get_contact_data()
            index_in_main = self.contacts.index(contact)
            self.contacts[index_in_main] = updated
            self.filtered_contacts = self.contacts.copy()
            self.refresh_contacts()

    def delete_contact(self):
        selected_index = self.contact_list.currentRow()
        if selected_index < 0:
            QMessageBox.warning(self, "No Selection", "Please select a contact to delete.")
            return
        contact = self.filtered_contacts[selected_index]
        reply = QMessageBox.question(self, "Delete", f"Delete {contact['name']}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.contacts.remove(contact)
            self.filtered_contacts = self.contacts.copy()
            self.refresh_contacts()

    def custom_dark_theme(self):
        return """
        QWidget {
            background-color: #121212;
            color: #f0f0f0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        QLineEdit {
            background-color: #1e1e1e;
            border: 1px solid #555;
            border-radius: 6px;
            padding: 6px;
        }
        QListWidget {
            background-color: #1e1e1e;
            border: 1px solid #555;
            border-radius: 6px;
        }
        QPushButton {
            background-color: #00acc1;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #0097a7;
        }
        QPushButton:pressed {
            background-color: #007c91;
        }
        QDialog {
            background-color: #1e1e1e;
        }
        QFormLayout QLabel {
            color: #f0f0f0;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactManager()
    window.show()
    sys.exit(app.exec_())
