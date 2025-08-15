import os
import shutil

def create_folder(folder_name: str):
    """Create a folder on the Desktop."""
    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def delete_folder(folder_name: str):
    """Delete a folder from the Desktop."""
    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(base_path, folder_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        return True
    return False

def list_folders():
    """List all folders on the Desktop."""
    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
