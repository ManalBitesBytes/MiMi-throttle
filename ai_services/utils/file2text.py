import os
import traceback
import shutil
import pandas as pd

from tika import parser
import pdfplumber
import docx2txt
from PIL import Image
import pytesseract

from ai_services.utils.constant import GENERAL_ERROR, PDF_TYPES, WORD_TYPES, OOTM_TYPES, \
    IMAGE_TYPES, VOICE_TYPES, LANG_MAPPING_LANGID
from ai_services.utils.slack import Slack
from ai_services.utils.documant2image import convert_pdf_to_images, convert_word_to_pdf

class File2Text:
    def extract_file_content(self, file_path, file_type, file_temp_path, langauges=None, skip_pdf=False, ):
        raw_text = ""
        output_path = None
        try:
            if not skip_pdf and file_type in PDF_TYPES:
                raw_text = self._extract_text_from_pdf(file_path, False)  # set True to extract fonts
                if not raw_text:
                    try:
                        output_path = convert_pdf_to_images(file_path, file_temp_path)
                        raw_text = self._extract_text_from_images_folder(output_path, langauges)
                    except Exception as e:
                        raw_text = ""
                    finally:
                        if output_path and os.path.exists(output_path):
                            shutil.rmtree(output_path)

            elif skip_pdf:
                convert_to_pdf = False
                if file_type in WORD_TYPES:
                    file_path = convert_word_to_pdf(file_path, file_temp_path)
                    convert_to_pdf = True
                try:
                    output_path = convert_pdf_to_images(file_path, file_temp_path)
                    raw_text = self._extract_text_from_images_folder(output_path, langauges)
                except Exception as e:
                    raw_text = ""
                finally:
                    if output_path and os.path.exists(output_path):
                        shutil.rmtree(output_path)
                    if convert_to_pdf:
                        os.remove(file_path)

            elif file_type in WORD_TYPES:
                raw_text = self._extract_text_from_docx(file_path)
            elif file_type in OOTM_TYPES:
                raw_text = self._extract_text_from_ootm(file_path)
            elif file_type in IMAGE_TYPES:
                raw_text = self._extract_text_from_image(file_path)
            elif file_type in VOICE_TYPES:
                raw_text = self._extract_text_from_audio(file_path, file_temp_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as ex:
            Slack().send_message_to_slack(GENERAL_ERROR, str(file_path) + str(traceback.format_exc()))
        return raw_text

    def _extract_text_from_ootm(self, file_path):
        """
        Extracts text content from any file as odt, ott, txt, md file.

        Args:
        file_path (str): The file path of the file to be processed.

        Returns:
        tuple: A tuple containing a list of non-empty lines and the full text content.
        """
        parsed = parser.from_file(file_path)
        raw_text = parsed['content']

        return raw_text

    def _extract_text_from_pdf(self, file_path, with_fonts=False):
        """
        Extracts text from a PDF file. Optionally, it extracts font information based on the 'with_fonts' parameter.

        Args:
        file (str): The path to the PDF file.
        with_fonts (bool): If True, extracts text along with font details; otherwise, extracts only text.

        Returns:
        tuple: Depending on 'with_fonts', either returns (lines, raw text, text with font DataFrame)
               or just the text (lines, raw text, placeholder DataFrame).
        """
        # Extracting the raw text from the PDF
        raw_text = parser.from_file(file_path, service='text')['content'] or ""
        if not raw_text:
            pdf = pdfplumber.open(file_path)
            raw_text = "\n".join([page.extract_text() for page in pdf.pages])
            pdf.close()
            # TODO: Add other methods, write script to return best result

        if with_fonts:
            # If with_fonts is True, extract fonts and return the respective DataFrame along with lines and raw text
            text_fonts_df = self._extract_fonts_from_pdf(file_path)
            return text_fonts_df, raw_text
        else:
            # If with_fonts is False, return lines and raw text with an empty DataFrame for fonts
            return raw_text

    def _extract_fonts_from_pdf(self, file_path):
        """
        Extracts text and font information from a PDF file. This function is specifically used
        when detailed font information is required alongside the text. It groups text by font
        and size, providing a detailed breakdown of the text styling in the document.

        Args:
        file (str): The path to the PDF file.

        Returns:
        pd.DataFrame: A DataFrame containing the text, font name, font size, and the length
                      of each text segment from the PDF.
        """
        pdf = pdfplumber.open(file_path)
        resume_lines = []

        for page in pdf.pages:
            dict_char = page.chars
            font_name = None
            font_size = None
            line = ""

            for element in dict_char:
                if font_name is None:
                    # Initialize the first character details
                    font_size = round(element['size'], 2)
                    font_name = element['fontname']
                    line += element['text']
                elif font_name != element['fontname'] or font_size != round(element['size'], 2):
                    # Font style or size changed, append the current line and start a new one
                    resume_lines.append([line, font_name, font_size, len(line)])
                    font_size = round(element['size'], 2)
                    font_name = element['fontname']
                    line = element['text']
                else:
                    # Continue appending text to the current line
                    line += element['text']
            # Add the last line if it's not empty
            if line:
                resume_lines.append([line, font_name, font_size, len(line)])

        pdf.close()
        font_df = pd.DataFrame(resume_lines, columns=["text", "fontname", "fontsize", "len"])
        return font_df

    def _extract_text_from_docx(self, docx_file):
        """
        Extracts text from a DOCX file using Apache Tika, and falls back to docx2txt if Tika returns no content.

        Args:
        docx_file (str): The file path of the DOCX file.

        Returns:
        tuple: A tuple containing a list of non-empty lines and the full text content.
        """
        raw_text = parser.from_file(docx_file, service='text')['content']

        if raw_text is None or raw_text.strip() == "":
            raw_text = docx2txt.process(docx_file)
        # TODO: Add other methods, write script to return best result

        return raw_text

    def _extract_text_from_image(self, image_path, language=None):
        """
        Extracts text from an image file using Tesseract OCR.

        Args:
        image_path (str): The path to the image file.
        language (str or list): The detected language code ('en' or 'ar').

        Returns:
        str: The extracted raw text content.
        """
        # Default to Arabic and English if no language is provided
        tesseract_lang = 'ara+eng'

        if language:
            # If language is a list, use the first detected language
            if isinstance(language, list) and len(language) > 0:
                language = language[0]

            # Map the detected language to Tesseract language codes
            tesseract_lang = LANG_MAPPING_LANGID.get(language, 'ara+eng')

        try:
            img = Image.open(image_path)
            raw_text = pytesseract.image_to_string(img, lang=tesseract_lang)  # Pass the mapped language code

            return raw_text
        except Exception as e:
            return ""  # Return empty string if an error occurs

    def _extract_text_from_images_folder(self, folder_path, langauge):
        """
        Processes all images in a given folder and extracts text from each image, combining the results in sorted order.

        Args:
            folder_path (str): The path to the folder containing images.
            langauge (str): The language for text extraction.

        Returns:
            str: The concatenated text content from all images in sorted order.
        """
        pages_texts = []
        try:
            # Get and sort files in the folder based on their filenames, assuming filenames have a numeric order
            sorted_files = sorted(os.listdir(folder_path),
                                  key=lambda x: int(x.split('-')[1].split('.')[0]) if '-' in x and len(
                                      x.split('-')) > 1 else float('inf'))

            for filename in sorted_files:
                file_path = os.path.join(folder_path, filename)
                if filename.lower().endswith(tuple(IMAGE_TYPES)):  # Ensure only image files are processed
                    try:
                        text = self._extract_text_from_image(file_path, langauge)  # Extract text from each image
                        pages_texts.append(text)  # Append extracted text
                    except Exception as e:
                        continue  # Skip the file if there's an error
        except Exception as e:
            return ""  # Return empty string if folder processing fails

        # Combine all extracted text into one string
        raw_text = '\n'.join(pages_texts)
        return raw_text
