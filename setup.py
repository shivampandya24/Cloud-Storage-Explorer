import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel,
    QLineEdit, QFileDialog, QTreeWidget, QTreeWidgetItem, QMessageBox, QProgressBar, QComboBox, QHBoxLayout
)
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
import json
import webbrowser

CONFIG_FILE = "config.json"

class S3Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Win Cloud Explorer")
        self.setGeometry(200, 200, 600, 450)

        self.s3_client = None
        self.config_data = {}
        self.total_downloaded_size = 0

        self.initUI()
        self.load_config()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

        # AWS Credentials
        self.bucket_selector = QComboBox(self)
        self.bucket_selector.setPlaceholderText("Select or Add a Bucket")
        self.bucket_selector.currentIndexChanged.connect(self.on_bucket_selected)
        layout.addWidget(self.bucket_selector)

        self.access_key_input = QLineEdit(self)
        self.access_key_input.setPlaceholderText("Enter AWS Access Key")
        layout.addWidget(self.access_key_input)

        self.secret_key_input = QLineEdit(self)
        self.secret_key_input.setPlaceholderText("Enter AWS Secret Key")
        layout.addWidget(self.secret_key_input)

        self.bucket_name_input = QLineEdit(self)
        self.bucket_name_input.setPlaceholderText("Enter Bucket Name")
        layout.addWidget(self.bucket_name_input)

        # Buttons
        self.connect_button = QPushButton("Connect to S3", self)
        self.connect_button.clicked.connect(self.connect_to_s3)
        layout.addWidget(self.connect_button)

        self.file_tree = QTreeWidget(self)
        self.file_tree.setHeaderLabels(["Name", "Size (MB)"])
        layout.addWidget(self.file_tree)

        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setEnabled(False)
        layout.addWidget(self.upload_button)

        self.download_button = QPushButton("Download File/Folder", self)
        self.download_button.clicked.connect(self.download)
        self.download_button.setEnabled(False)
        layout.addWidget(self.download_button)

        self.delete_button = QPushButton("Delete File/Folder", self)
        self.delete_button.clicked.connect(self.delete)
        self.delete_button.setEnabled(False)
        layout.addWidget(self.delete_button)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status
        self.status_label = QLabel("", self)
        layout.addWidget(self.status_label)

        # Footer Section
        footer_layout = QHBoxLayout()
        footer_label = QLabel("Developed with 💗 by Shivam Pandya - V0.0.1")
        footer_label.setStyleSheet("font-size: 16px;")
        footer_button = QPushButton("GitHub")
        footer_button.setStyleSheet("font-size: 16px;")
        footer_button.clicked.connect(self.open_github)
        footer_layout.addWidget(footer_label)
        footer_layout.addWidget(footer_button)
        footer_layout.addStretch()
        layout.addLayout(footer_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_github(self):
        webbrowser.open("https://github.com/shivampandya24/Win-Cloud-Explorer")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as file:
                    self.config_data = json.load(file)
                    self.bucket_selector.addItems(self.config_data.keys())
            except Exception as e:
                self.show_error(f"Failed to load configuration: {str(e)}")

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as file:
                json.dump(self.config_data, file)
        except Exception as e:
            self.show_error(f"Failed to save configuration: {str(e)}")

    def on_bucket_selected(self):
        selected_bucket = self.bucket_selector.currentText()
        if selected_bucket and selected_bucket in self.config_data:
            config = self.config_data[selected_bucket]
            self.access_key_input.setText(config.get("access_key", ""))
            self.secret_key_input.setText(config.get("secret_key", ""))
            self.bucket_name_input.setText(config.get("bucket_name", ""))

    def connect_to_s3(self):
        access_key = self.access_key_input.text().strip()
        secret_key = self.secret_key_input.text().strip()
        bucket_name = self.bucket_name_input.text().strip()

        if not access_key or not secret_key or not bucket_name:
            self.show_error("Please provide all the required details.")
            return

        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            self.bucket_name = bucket_name

            # Save configuration
            self.config_data[bucket_name] = {
                "access_key": access_key,
                "secret_key": secret_key,
                "bucket_name": bucket_name
            }
            self.save_config()

            if bucket_name not in [self.bucket_selector.itemText(i) for i in range(self.bucket_selector.count())]:
                self.bucket_selector.addItem(bucket_name)

            # List files and folders in the bucket
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            self.file_tree.clear()
            total_size = 0

            if 'Contents' in response:
                folder_map = {}
                folder_sizes = {}
                for obj in response['Contents']:
                    key = obj['Key']
                    size = obj['Size'] / (1024 * 1024)  # Convert bytes to MB
                    total_size += size
                    parts = key.split('/')
                    parent = self.file_tree
                    current_path = ""
                    for i, part in enumerate(parts):
                        current_path = f"{current_path}/{part}" if current_path else part
                        if i == len(parts) - 1 and not key.endswith('/'):  # File
                            QTreeWidgetItem(parent, [part, f"{size:.2f} MB"])
                        else:  # Folder
                            if current_path not in folder_map:
                                folder_item = QTreeWidgetItem(parent, [part, "--"])
                                folder_map[current_path] = folder_item
                                folder_sizes[current_path] = 0
                            parent = folder_map[current_path]
                            folder_sizes[current_path] += size

                # Update folder sizes
                for path, size in folder_sizes.items():
                    if path in folder_map:
                        folder_map[path].setText(1, f"{size:.2f} MB")

            self.status_label.setText(f"Connected to S3 bucket successfully! Total size: {total_size:.2f} MB")
            self.upload_button.setEnabled(True)
            self.download_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        except NoCredentialsError:
            self.show_error("Invalid AWS credentials.")
        except PartialCredentialsError:
            self.show_error("Incomplete AWS credentials.")
        except Exception as e:
            self.show_error(str(e))

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if not file_path:
            return

        file_name = file_path.split("/")[-1]
        try:
            self.progress_bar.setValue(0)

            def progress_callback(bytes_transferred):
                self.progress_bar.setValue(int((bytes_transferred / total_size) * 100))

            total_size = os.path.getsize(file_path)
            self.s3_client.upload_file(
                file_path, 
                self.bucket_name, 
                file_name,
                Callback=progress_callback
            )
            self.status_label.setText(f"File '{file_name}' uploaded successfully!")
            self.connect_to_s3()  # Refresh the file tree
        except Exception as e:
            self.show_error(str(e))

    def download(self):
        selected_item = self.file_tree.currentItem()
        if not selected_item:
            self.show_error("Please select a file or folder to download.")
            return

        save_directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if not save_directory:
            return

        self.progress_bar.setValue(0)
        self.total_downloaded_size = 0
        self.download_recursive(selected_item, save_directory)
        self.status_label.setText(f"Download completed! Total downloaded size: {self.total_downloaded_size / (1024 * 1024):.2f} MB")

    def download_recursive(self, item, save_path):
        name = item.text(0)
        parent = item.parent()

        # Build the full path
        key = name
        while parent:
            key = f"{parent.text(0)}/{key}"
            parent = parent.parent()

        if item.childCount() == 0:  # File
            try:
                file_path = os.path.join(save_path, name)

                def progress_callback(bytes_transferred):
                    self.progress_bar.setValue(int((bytes_transferred / total_size) * 100))

                total_size = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)['ContentLength']
                with open(file_path, 'wb') as f:
                    self.s3_client.download_fileobj(self.bucket_name, key, f, Callback=progress_callback)

                self.total_downloaded_size += total_size
            except Exception as e:
                self.show_error(str(e))
        else:  # Folder
            folder_path = os.path.join(save_path, name)
            os.makedirs(folder_path, exist_ok=True)
            for i in range(item.childCount()):
                self.download_recursive(item.child(i), folder_path)

    def delete(self):
        selected_item = self.file_tree.currentItem()
        if not selected_item:
            self.show_error("Please select a file or folder to delete.")
            return

        name = selected_item.text(0)
        parent = selected_item.parent()

        # Build the full path
        key = name
        while parent:
            key = f"{parent.text(0)}/{key}"
            parent = parent.parent()

        try:
            if selected_item.childCount() == 0:  # File
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
                self.status_label.setText(f"File '{key}' deleted successfully!")
            else:  # Folder
                self.delete_folder(key)
                self.status_label.setText(f"Folder '{key}' deleted successfully!")

            self.connect_to_s3()  # Refresh the file tree
        except Exception as e:
            self.show_error(str(e))

    def delete_folder(self, folder_key):
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=folder_key):
            if 'Contents' in page:
                for obj in page['Contents']:
                    self.s3_client.delete_object(Bucket=self.bucket_name, Key=obj['Key'])

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = S3Manager()
    window.show()
    sys.exit(app.exec_())
