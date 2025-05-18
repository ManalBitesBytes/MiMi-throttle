import filetype
import magic
import mimetypes

from ai_services.utils.constant import ALLOWED_FILE_TYPES_LIST


class FileTypeHelper:
    def __init__(self, file_org_name, file_path, file_obj):
        self.file_org_name = file_org_name
        self.file_path = file_path
        self.file_obj = file_obj

    def get_file_type(self):
        file_type = None

        # check file type using file content
        try:
            # Use python-magic to determine file type based on content.
            file_type = mimetypes.guess_extension(magic.from_file(self.file_path, mime=True)).lstrip(".")

            if not file_type or file_type not in ALLOWED_FILE_TYPES_LIST:
                file_type = filetype.guess(self.file_path).extension
                if file_type not in ALLOWED_FILE_TYPES_LIST:
                    file_type = None
        except Exception as ex:
            file_type = None

        # if file type is empty, use file name to get file type
        try:
            if not file_type and len(self.file_org_name.lower().split(".")[-1]) > 1:
                file_type = self.file_org_name.lower().split(".")[-1]
                if file_type not in ALLOWED_FILE_TYPES_LIST:
                    file_type = None
        except:
            file_type = None

        return file_type
