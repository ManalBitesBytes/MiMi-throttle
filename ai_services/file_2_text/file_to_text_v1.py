import re
import traceback

import os
import random
import string
import shutil

from ai_services.common.langauge_helper import detect_language
from ai_services.file_2_text.file2text_utils.file2text_constant import FILE_TEMP_PATH
from ai_services.utils.constant import ALLOWED_FILE_TYPES_LIST, PDF_TYPES, WORD_TYPES, IMAGE_TYPES
from ai_services.utils.file2text import File2Text
from ai_services.utils.spell_checker import TextReadabilityChecker
from ai_services.utils.file_type_helper import FileTypeHelper
from ai_services.utils.slack import Slack
from ai_services.utils.text_helper import basic_clean_text, advanced_clean_text


class File2TextConverter:
    def convert_file_to_text(self, request_id, file_obj, text_length_limit = 20000):
        file_type = None
        file_org_name = file_obj.name
        file_content = None
        text_langs = []

        file_buffer = file_obj.read()
        file_name = "".join([random.choice(string.ascii_lowercase) for i in range(15)])
        file_path = FILE_TEMP_PATH + file_name
        f = open(file_path, 'wb')
        f.write(file_buffer)
        f.close()

        try:

            file_type = FileTypeHelper(file_org_name, file_path, file_buffer[:1024]).get_file_type()
            if not file_type or file_type not in ALLOWED_FILE_TYPES_LIST:  # file type check
                file_type = -1
                return file_type, file_content, text_langs

            file2text = File2Text()
            spell = TextReadabilityChecker()

            file_content = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH) or ""

            if ("".join(file_content.replace("\n", "").split()) == "") and file_type in PDF_TYPES:  # if PDF is images
                file_content = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH, skip_pdf=True) or ""

            text_langs = detect_language(file_content)

            # English
            if file_type in PDF_TYPES and "en" in text_langs:
                txt_tika = ' '.join(file_content.replace('\n', ' ').split())
                txt_ocr = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH, langauges=text_langs,
                                                                  skip_pdf=True)
                # check correct words counts, and return higher correct one
                # [1] return number of correct words
                tika_num_correct = spell.check_text_readability(txt_tika,language="en")[1]
                ocr_num_correct = spell.check_text_readability(txt_ocr,language="en")[1]
                # file_content -> the most count correct words
                if ocr_num_correct > tika_num_correct:
                    file_content = txt_ocr
                else:
                    file_content = txt_tika

            elif file_type in WORD_TYPES and "en" in text_langs:
                txt_tika = ' '.join(file_content.replace('\n', ' ').split())
                txt_ocr = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH, langauges=text_langs,
                                                         skip_pdf=True)
                # check correct words counts, and return higher correct one
                # [1] return number of correct words
                tika_num_correct = spell.check_text_readability(txt_tika, language="en")[1]
                ocr_num_correct = spell.check_text_readability(txt_ocr,language="en")[1]
                # file_content -> the most count correct words
                if ocr_num_correct > tika_num_correct:
                    file_content = txt_ocr
                else:
                    file_content = txt_tika

            elif file_type in IMAGE_TYPES and "en" in text_langs:
                file_content = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH, langauges=text_langs, skip_pdf=False)

            # Arabic
            if file_type in PDF_TYPES and "ar" in text_langs:
                txt_tika = ' '.join(file_content.replace('\n', ' ').split())
                txt_ocr = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH, langauges=text_langs,
                                                         skip_pdf=True)
                tika_num_correct = spell.check_text_readability(txt_tika, language="ar")[1]
                ocr_num_correct = spell.check_text_readability(txt_ocr, language="ar")[1]
                # file_content -> the most count correct words
                if tika_num_correct > ocr_num_correct:
                    file_content = txt_tika
                    file_content = re.sub(r'[\u200e\u200f\xa0]+', ' ', re.sub(r'\n+', '\n', file_content)).strip()
                else:
                    # Remove duplicate words/punctuation, extra spaces, and newlines while preserving the original order
                    english_text = ' '.join(
                        dict.fromkeys(re.findall(r'[a-zA-Z0-9@.,:|()\[\]{}<>+=!#$%^&*;?/\\\'"_-]+', txt_tika))).replace(
                        '\n', ' ').strip()
                    file_content = re.sub(r'[\u200e\u200f\xa0]+', ' ', re.sub(r'\n+', '\n', txt_ocr)).strip()
                    file_content = ' '.join(file_content.replace('\n', ' ').split())
                    file_content = file_content + "\n English Extracted data: \n" + english_text

            elif file_type in WORD_TYPES and "ar" in text_langs:
                txt_tika = ' '.join(file_content.replace('\n', ' ').split())
                txt_ocr = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH, langauges=text_langs,
                                                         skip_pdf=True)
                tika_num_correct = spell.check_text_readability(txt_tika, language="ar")[1]
                ocr_num_correct = spell.check_text_readability(txt_ocr, language="ar")[1]
                # file_content -> the most count correct words
                if tika_num_correct > ocr_num_correct:
                    file_content = txt_tika
                    file_content = re.sub(r'[\u200e\u200f\xa0]+', ' ', re.sub(r'\n+', '\n', file_content)).strip()
                else:
                    # Remove duplicate words/punctuation, extra spaces, and newlines while preserving the original order
                    english_text = ' '.join(
                        dict.fromkeys(re.findall(r'[a-zA-Z0-9@.,:|()\[\]{}<>+=!#$%^&*;?/\\\'"_-]+', txt_tika))).replace(
                        '\n', ' ').strip()
                    file_content = re.sub(r'[\u200e\u200f\xa0]+', ' ', re.sub(r'\n+', '\n', txt_ocr)).strip()
                    file_content = ' '.join(file_content.replace('\n', ' ').split())
                    file_content = file_content + "\n English Extracted data: \n" + english_text

            elif file_type in IMAGE_TYPES and "ar" in text_langs:
                file_content = file2text.extract_file_content(file_path, file_type, FILE_TEMP_PATH, langauges=text_langs, skip_pdf=False)
                file_content = file_content.replace("اال", "الا")
                file_content = re.sub(r'[\u200e\u200f\xa0]+', ' ', re.sub(r'\n+', '\n', file_content)).strip()
        except Exception as ex:
            os.remove(file_path)
            print(str(traceback.format_exc()))
            Slack().send_message_to_slack("File2Text General Error:",
                                          f"request_id: {str(request_id)}  \n" + str(traceback.format_exc()))
        finally:
            try:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as ex:
                        Slack().send_message_to_slack(
                            "File2Text General Error:",
                            f"request_id: {str(request_id)}  \n{traceback.format_exc()}"
                        )

                for item in os.listdir(os.path.dirname(file_path)):
                    try:
                        if os.path.basename(file_path) in item:
                            path = os.path.join(os.path.dirname(file_path), item)
                            if os.path.isfile(path):
                                try:
                                    os.remove(path)
                                except Exception as ex:
                                    Slack().send_message_to_slack(
                                        "File2Text General Error:",
                                        f"request_id: {str(request_id)}  \n{traceback.format_exc()}"
                                    )
                            else:
                                try:
                                    shutil.rmtree(path)
                                except Exception as ex:
                                    Slack().send_message_to_slack(
                                        "File2Text General Error:",
                                        f"request_id: {str(request_id)}  \n{traceback.format_exc()}"
                                    )
                    except:
                        Slack().send_message_to_slack(
                            "File2Text General Error:",
                            f"request_id: {str(request_id)}  \n{traceback.format_exc()}"
                        )

            except Exception as ex:
                Slack().send_message_to_slack(
                    "File2Text General Error:",
                    f"request_id: {str(request_id)}  \n{traceback.format_exc()}"
                )

        file_content = advanced_clean_text(file_content)

        return file_type, file_content, text_langs
