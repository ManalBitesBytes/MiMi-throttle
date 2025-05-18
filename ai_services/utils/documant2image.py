import os
import subprocess
from datetime import datetime
import random
import string

from ai_services.utils.encoding_utils import generate_unique_name

def convert_word_to_pdf(document_path, output_directory):
    """
    Converts a Word document to a PDF using LibreOffice's command.

    Args:
        document_path (str): The path to the Word document.
        output_directory (str): The directory to save the converted PDF.

    Returns:
        str: The path to the converted PDF file.
    """
    # Generate a random file name
    file_name = "".join([random.choice(string.ascii_lowercase) for _ in range(15)]) + '.pdf'
    pdf_output_path = os.path.join(output_directory, file_name)

    # Convert the document to PDF
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_directory, document_path],check=True)

    # Rename the generated PDF to the custom file name
    original_pdf_path = os.path.join(output_directory, os.path.splitext(os.path.basename(document_path))[0] + '.pdf')
    os.rename(original_pdf_path, pdf_output_path)

    return pdf_output_path

def convert_pdf_to_images(pdf_file_path, jpeg_output_base_dir):
    """
    Converts a PDF file to JPEG images and saves them in a uniquely named directory.

    Args:
        pdf_file_path (str): The path to the PDF file.
        jpeg_output_base_dir (str): The base directory to store the JPEG images.

    Returns:
        str: The path to the directory containing the JPEG images.
    """
    try:
        unique_directory = f"{generate_unique_name(pdf_file_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        full_output_path = os.path.join(jpeg_output_base_dir, unique_directory)

        if not os.path.exists(full_output_path):
            os.makedirs(full_output_path)

        # Command to convert PDF to images, using -jpeg and specifying output prefix
        command = ['pdftoppm', '-jpeg', pdf_file_path, os.path.join(full_output_path, 'page')]
        subprocess.run(command, check=True)

        # Sort the output files based on their page numbers
        sorted_images = sorted([f for f in os.listdir(full_output_path) if f.startswith('page-')])

        return full_output_path  # Return only the path
    except Exception as e:
        return "", []  # Return empty string and list if an error occurs
