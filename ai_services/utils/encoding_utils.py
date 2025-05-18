import os
import base64
import uuid

def generate_unique_name(file_name):
    """
    Generates a unique directory name based on the PDF file name and a random UUID,
    encodes the combination, and then decodes it to simulate encryption/decryption,
    ensuring filesystem-friendly and unique directory names.

    Args:
        pdf_file (str): The path to the PDF file.

    Returns:
        str: "Decrypted" version of the unique directory name.
    """
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    random_uuid = uuid.uuid4().bytes
    encoded_string = base64.urlsafe_b64encode(random_uuid).decode('utf-8').rstrip('=')
    combined_encoded = base64.urlsafe_b64encode(f"{base_name}_{encoded_string}".encode('utf-8')).decode('utf-8')
    decrypted_name = base64.urlsafe_b64decode(combined_encoded.encode('utf-8')).decode('utf-8')
    return decrypted_name