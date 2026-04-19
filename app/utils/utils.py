import os


def ensure_upload_folder(folder_path: str = "uploads") -> str:
    """
    Ensure the upload folder exists, create if it doesn't.
    
    Args:
        folder_path: Path to the upload folder (default: "uploads")
        
    Returns:
        The folder path
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path
