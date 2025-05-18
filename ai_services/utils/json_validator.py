from datetime import datetime


class JsonValidator:
    def validate_field(self, value, constraints):
        """
        Validate a single field based on constraints.

        :param value: The value to be validated.
        :param constraints: A dictionary of constraints.
        :return: True if the value is valid, False otherwise.
        """
        if constraints.get('type') is str:
            if not isinstance(value, str) or not value.strip():
                return False
            if 'max_length' in constraints and len(value) > constraints['max_length']:
                return False
            if 'min_length' in constraints and len(value) < constraints['min_length']:
                return False
            if 'date_format' in constraints:
                try:
                    datetime.strptime(value, constraints['date_format'])
                except ValueError:
                    return False
        elif constraints.get('type') is list:
            if not isinstance(value, list):
                return False
            if 'min_items' in constraints and len(value) < constraints['min_items']:
                return False
            if 'max_items' in constraints and len(value) > constraints['max_items']:
                return False
        elif constraints.get('type') in [int, float]:
            if not isinstance(value, constraints['type']):
                return False
            if 'min_value' in constraints and value < constraints['min_value']:
                return False
            if 'max_value' in constraints and value > constraints['max_value']:
                return False
            if 'between_min' in constraints and 'between_max' in constraints:
                if not (constraints['between_min'] <= value <= constraints['between_max']):
                    return False
        return True

    def replace_invalid_fields(self, json_data, required_fields):
        """
        Replace invalid fields in a JSON object based on constraints.

        :param json_data: The JSON data to be validated.
        :param required_fields: A dictionary of field constraints.
        :return: A JSON object with invalid fields replaced.
        """
        if isinstance(json_data, dict):
            updated_data = {}
            for key, value in json_data.items():
                constraints = required_fields.get(key, {})
                if self.validate_field(value, constraints):
                    if isinstance(value, (dict, list)):
                        updated_data[key] = self.replace_invalid_fields(value, required_fields)
                    else:
                        updated_data[key] = value
                else:
                    # Replace invalid fields based on type
                    if constraints.get('type') is list:
                        updated_data[key] = []
                    else:
                        updated_data[key] = None
            return updated_data

        elif isinstance(json_data, list):
            updated_list = []
            for item in json_data:
                updated_list.append(self.replace_invalid_fields(item, required_fields))
            return updated_list

        return json_data

    def fill_null_and_empty_lists(self, old_data, new_data):
        """
        Recursively fill null and empty list fields in `old_data` with corresponding values from `new_data`.

        :param old_data: JSON object with potentially null or empty list fields.
        :param new_data: JSON object with potential values to fill in `old_data`.
        :return: Updated JSON object with null and empty lists in `old_data` replaced by values from `new_data`.
        """
        if isinstance(old_data, dict) and isinstance(new_data, dict):
            for key, value in old_data.items():
                if key in new_data:
                    if value is None or (isinstance(value, list) and not value):
                        # Replace null or empty list with corresponding value from new_data
                        old_data[key] = new_data[key]
                    elif isinstance(value, (dict, list)) and isinstance(new_data[key], (dict, list)):
                        # Recursively process nested structures
                        old_data[key] = self.fill_null_and_empty_lists(value, new_data[key])
        elif isinstance(old_data, list) and isinstance(new_data, list):
            # Ensure both lists have the same length for safe replacement
            for index, value in enumerate(old_data):
                if index < len(new_data):
                    if value is None or (isinstance(value, list) and not value):
                        old_data[index] = new_data[index]
                    elif isinstance(value, (dict, list)) and isinstance(new_data[index], (dict, list)):
                        # Recursively process nested structures
                        old_data[index] = self.fill_null_and_empty_lists(value, new_data[index])
        return old_data

    def find_empty_or_null_fields(self, data, path=""):
        empty_or_null_fields = []

        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                if value is None or (isinstance(value, list) and not value):
                    empty_or_null_fields.append(current_path)
                elif isinstance(value, (dict, list)):
                    empty_or_null_fields.extend(self.find_empty_or_null_fields(value, current_path))

        elif isinstance(data, list):
            for index, item in enumerate(data):
                current_path = f"{path}[{index}]"
                if item is None or (isinstance(item, list) and not item):
                    empty_or_null_fields.append(current_path)
                elif isinstance(item, (dict, list)):
                    empty_or_null_fields.extend(self.find_empty_or_null_fields(item, current_path))

        return empty_or_null_fields