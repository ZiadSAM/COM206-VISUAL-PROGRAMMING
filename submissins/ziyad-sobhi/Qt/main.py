import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QTableWidgetItem, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


app = QApplication(sys.argv)

ui_path = Path(__file__).parent / "main.ui"

ui_file = QFile(str(ui_path))
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
window = loader.load(ui_file)

ui_file.close()


def calculate_grade():
    try:
        midterm = float(window.midtermInput.text())
        final = float(window.finalInput.text())
        homework = float(window.homeworkInput.text())

        if (midterm < 0 or midterm > 100 or final < 0 or final > 100 or homework < 0 or homework > 100):
            QMessageBox.warning(window, "Invalid Grade", "Grades must be between 0 and 100.")
            return None

        total = (midterm * 0.30) + (final * 0.50) + (homework * 0.20)

        if total >= 90:
            grade = "A"
        elif total >= 80:
            grade = "B"
        elif total >= 70:
            grade = "C"
        elif total >= 60:
            grade = "D"
        else:
            grade = "F"

        if total >= 60:
            status = "Passed"
        else:
            status = "Failed"

        window.scoreLabel.setText(f"Score: {total:.2f}")
        window.gradeLabel.setText(f"Grade: {grade}")
        window.statusLabel.setText(f"Status: {status}")

        return total, grade, status

    except ValueError:
        QMessageBox.warning(window, "Invalid input", "Please enter numeric digits.")
        return None

def add_to_table():
    if (window.studentInput.text() == "" or
        window.courseInput.text() == "" or
        window.midtermInput.text() == "" or
        window.finalInput.text() == "" or
        window.homeworkInput.text() == ""):
        QMessageBox.warning(window, "Missing data", "Please fill all details.")
        return

    result = calculate_grade()

    if result is None:
        return

    row = window.gradeTable.rowCount()
    window.gradeTable.insertRow(row)

    data = [
        window.studentInput.text(),
        window.courseInput.text(),
        window.midtermInput.text(),
        window.finalInput.text(),
        window.homeworkInput.text(),
        window.scoreLabel.text().replace("Score: ", ""),
        window.gradeLabel.text().replace("Grade: ", ""),
        window.statusLabel.text().replace("Status: ", "")
    ]

    for column, value in enumerate(data):
        window.gradeTable.setItem(row, column, QTableWidgetItem(value))
    
    QMessageBox.information(window, "Success", "Data added successfully.")

def clear_inputs():
    window.studentInput.clear()
    window.courseInput.clear()
    window.midtermInput.clear()
    window.finalInput.clear()
    window.homeworkInput.clear()

    window.scoreLabel.setText("Score: -")
    window.gradeLabel.setText("Grade: -")
    window.statusLabel.setText("Status: -")

def delete_selected():
    selected_items = window.gradeTable.selectedItems()

    if selected_items:
        current_row = window.gradeTable.currentRow()
        window.gradeTable.removeRow(current_row)
    else:
        QMessageBox.warning(window, "No Selection", "Please select a row to delete.")

window.calculateButton.clicked.connect(calculate_grade)
window.addButton.clicked.connect(add_to_table)
window.clearButton.clicked.connect(clear_inputs)
window.deleteButton.clicked.connect(delete_selected)

window.show()
app.exec()
