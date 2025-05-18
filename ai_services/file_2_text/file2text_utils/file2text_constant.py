import os

MAX_FILE_SIZE = 5000000
LANG_MAPPING_LANGID = {
    'en': 'eng',
    'ar': 'ara', }

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
FILE_TEMP_PATH = PROJECT_ROOT + '/file_temp/'