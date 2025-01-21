# Win Cloud Explorer

**Win Cloud Explorer** is a powerful and user-friendly desktop application for managing Amazon S3 resources. This tool provides an intuitive interface for uploading, downloading, browsing, and managing files and folders in your Amazon S3 buckets.

## Features

-   **AWS S3 Integration**: Seamlessly connect to Amazon S3 buckets using your Access Key and Secret Key.
    
-   **Bucket Management**: Browse and manage your buckets with ease.
    
-   **File Operations**:
    
    -   Upload files to your bucket.
        
    -   Download files or entire folders to your local machine.
        
    -   Delete files or folders directly from your bucket.
        
-   **File Tree View**: View files and folders in a structured tree format.
    
-   **Progress Tracking**: Track file upload and download progress using a progress bar.
    
-   **Config Management**: Save and load bucket configurations for quick access.
    
-   **Responsive UI**: Easy-to-navigate interface for managing large data.
    
    

## Prerequisites

-   **Python**: Ensure Python 3.7 or higher is installed on your system.
    
-   **Dependencies**: Install the required libraries using the following command:
    
    ```
    pip install PyQt5 boto3
    ```
    

## Installation

1.  Clone the repository from GitHub:
    
    ```
    git clone https://github.com/shivampandya24/Win-Cloud-Explorer.git
    ```
    
2.  Navigate to the project directory:
    
    ```
    cd Win-Cloud-Explorer
    ```
    
3.  Run the application:
    
    ```
    python wce.py
    ```
    

## Usage

1.  Launch the application.
    
2.  Enter your **AWS Access Key**, **Secret Key**, and **Bucket Name**.
    
3.  Click **Connect to S3** to establish a connection to your bucket.
    
4.  Use the following features:
    
    -   **Upload File**: Upload files to the selected bucket.
        
    -   **Download File/Folder**: Download selected files or folders.
        
    -   **Delete File/Folder**: Delete selected items from the bucket.
        
5.  View and manage bucket contents using the file tree.
    

## Screenshots

<img width="293" alt="image" src="https://github.com/user-attachments/assets/d641b0f2-5bf2-4a28-bdb5-b9d9a5a14196" />

### File Tree

## Developer Information

**Developer**: Shivam Pandya

-   **GitHub**: [shivampandya24](https://github.com/shivampandya24/Win-Cloud-Explorer)
    

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

1.  Fork the repository.
    
2.  Create a new branch:
    
    ```
    git checkout -b feature-name
    ```
    
3.  Commit your changes:
    
    ```
    git commit -m "Add some feature"
    ```
    
4.  Push to the branch:
    
    ```
    git push origin feature-name
    ```
    
5.  Open a pull request.
    

## License

This project is licensed under the MIT License. See the LICENSE file for details.
