import os
import sys
import datetime
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QSpinBox, QTableWidget, QTableWidgetItem, QMenu
from PyQt5.QtCore import Qt

class FileSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Search Application')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Directory selection
        self.dir_label = QLabel('Directory:')
        self.dir_edit = QLineEdit()
        self.dir_button = QPushButton('Browse')
        self.dir_button.clicked.connect(self.browse_directory)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.dir_edit)
        dir_layout.addWidget(self.dir_button)

        # File name search
        self.name_label = QLabel('File Name Contains:')
        self.name_edit = QLineEdit()

        # File content search
        self.content_label = QLabel('File Content Contains:')
        self.content_edit = QLineEdit()

        # File extension search
        self.ext_label = QLabel('File Extension:')
        self.ext_edit = QLineEdit()

        # File size search
        self.size_label = QLabel('File Size (KB):')
        self.size_min = QSpinBox()
        self.size_min.setMaximum(999999)
        self.size_max = QSpinBox()
        self.size_max.setMaximum(999999)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel('Min:'))
        size_layout.addWidget(self.size_min)
        size_layout.addWidget(QLabel('Max:'))
        size_layout.addWidget(self.size_max)

        # Search button
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_files)

        # Result display
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['File Name', 'File Path', 'File Size (KB)', 'Creation Date'])
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.result_table.setSelectionMode(QTableWidget.SingleSelection)
        self.result_table.cellDoubleClicked.connect(self.open_file)
        self.result_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.result_table.customContextMenuRequested.connect(self.context_menu)

        # Adding widgets to layout
        layout.addWidget(self.dir_label)
        layout.addLayout(dir_layout)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_edit)
        layout.addWidget(self.ext_label)
        layout.addWidget(self.ext_edit)
        layout.addWidget(self.size_label)
        layout.addLayout(size_layout)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            self.dir_edit.setText(dir_path)

    def search_files(self):
        self.result_table.setRowCount(0)
        dir_path = self.dir_edit.text()
        name_contains = self.name_edit.text()
        content_contains = self.content_edit.text()
        extension = self.ext_edit.text()
        size_min = self.size_min.value() * 1024
        size_max = self.size_max.value() * 1024

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_creation_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

                if name_contains and name_contains not in file:
                    continue
                if extension and not file.endswith(extension):
                    continue
                if size_min and file_size < size_min:
                    continue
                if size_max and file_size > size_max:
                    continue
                if content_contains:
                    with open(file_path, 'r', errors='ignore') as f:
                        try:
                            content = f.read()
                        except:
                            continue
                        if content_contains not in content:
                            continue

                row_position = self.result_table.rowCount()
                self.result_table.insertRow(row_position)
                self.result_table.setItem(row_position, 0, QTableWidgetItem(file))
                self.result_table.setItem(row_position, 1, QTableWidgetItem(file_path.replace('/', '\\')))
                self.result_table.setItem(row_position, 2, QTableWidgetItem(str(file_size // 1024)))
                self.result_table.setItem(row_position, 3, QTableWidgetItem(file_creation_date))

    def open_file(self, row, column):
        file_path = self.result_table.item(row, 1).text()
        os.startfile(file_path)

    def context_menu(self, position):
        menu = QMenu()
        open_action = menu.addAction("Open")
        remove_action = menu.addAction("Remove")
        show_in_explorer_action = menu.addAction("Show in Explorer")
        options_action = menu.addAction("Options")

        action = menu.exec_(self.result_table.viewport().mapToGlobal(position))

        if action == open_action:
            self.open_selected_file()
        elif action == remove_action:
            self.remove_selected_file()
        elif action == show_in_explorer_action:
            self.show_in_explorer()
        elif action == options_action:
            self.show_options()

    def open_selected_file(self):
        current_row = self.result_table.currentRow()
        if current_row >= 0:
            file_path = self.result_table.item(current_row, 1).text()
            os.startfile(file_path)

    def remove_selected_file(self):
        current_row = self.result_table.currentRow()
        if current_row >= 0:
            file_path = self.result_table.item(current_row, 1).text()
            os.remove(file_path)
            self.result_table.removeRow(current_row)

    def show_in_explorer(self):
        current_row = self.result_table.currentRow()
        if current_row >= 0:
            file_path = self.result_table.item(current_row, 1).text()
            folder_path = os.path.dirname(file_path)
            subprocess.Popen(f'explorer /select,"{file_path}"')

    def show_options(self):
        # Placeholder for additional options functionality
        print("Options menu clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileSearchApp()
    ex.show()
    sys.exit(app.exec_())
