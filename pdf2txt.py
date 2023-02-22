import os
import sys
from PyQt5 import QtWidgets, QtGui
import PyPDF2


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("PDF to Text Converter")
        self.setAcceptDrops(True)
        self.setStyleSheet("QMainWindow { background-color: #333333; }")  # set the background color to dark gray

        # Create a label to display the dropped file names
        self.label = QtWidgets.QLabel("Drop PDF files here")
        self.label.setWordWrap(True)
        self.label.setStyleSheet("QLabel { background-color: #444444; border: 1px solid gray; padding: 10px; color: white; }")  # set the label's background color to light gray and its text color to white

        # Create a checkbox to enable automatic confirmation of overwrites
        self.overwrite_checkbox = QtWidgets.QCheckBox("Automatically confirm overwrites")
        self.overwrite_checkbox.setChecked(True)
        self.overwrite_checkbox.setStyleSheet("QCheckBox { color: white; }")  # set the checkbox's text color to white

        # Create a layout to hold the label and checkbox
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.overwrite_checkbox)

        # Set the layout as the central widget of the main window
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def dragEnterEvent(self, event):
        # Accept the drag event if a file is being dragged
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Get the file paths of the dropped files
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]

        # Check if all the files are PDF files
        if not all(path.endswith(".pdf") for path in file_paths):
            self.label.setText("Error: Not all files are PDF files")
            return

        # Convert the PDF files to text using PyPDF2
        converted_files = []
        for file_path in file_paths:
            file_name, _ = os.path.splitext(os.path.basename(file_path))
            output_path = os.path.join(os.path.dirname(file_path), file_name + ".txt")
            with open(file_path, 'rb') as input_file, open(output_path, 'w') as output_file:
                reader = PyPDF2.PdfFileReader(input_file)
                num_pages = reader.getNumPages()
                for i in range(num_pages):
                    page = reader.getPage(i)
                    text = page.extractText()
                    output_file.write(text)
            converted_files.append((file_path, output_path))

        # Update the label to show the conversion was successful
        self.label.setText("Successfully converted:\n" + "\n".join("{} to {}".format(input_path, output_path) for input_path, output_path in converted_files))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
