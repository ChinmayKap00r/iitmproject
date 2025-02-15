import os

def read_file(path):
    """Reads file content."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    with open(path, "r") as file:
        return file.read()
