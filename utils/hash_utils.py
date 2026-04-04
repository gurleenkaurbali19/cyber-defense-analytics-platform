import hashlib

def generate_file_hash(file):
    """
    Generates MD5 hash for the uploaded file.
    Works with Streamlit UploadedFile.
    """
    file.seek(0)  # reset pointer
    file_bytes = file.read()
    file.seek(0)  # reset again so file can be reused

    return hashlib.md5(file_bytes).hexdigest()
