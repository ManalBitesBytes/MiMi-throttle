import re


def replace_empty_with_none_or_remove(data):
    if isinstance(data, dict):
        return {k: replace_empty_with_none_or_remove(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_empty_with_none_or_remove(item) for item in data if item != ""]
    elif data == "":
        return None
    else:
        return data


def _clean_key(key):
    # Remove special characters
    key = re.sub(r'[^a-zA-Z0-9_]', ' ', key)
    # Capitalize each word
    key = key.title()
    # Remove extra spaces
    key = re.sub(r'\s+', ' ', key).strip()
    return key


# Function to convert dictionary to a text representation
def json_to_text(data, indent=0):
    text = ""
    for key, value in data.items():
        # Skip empty lists and null values
        if value is None or (isinstance(value, list) and not value):
            continue

        cleaned_key = _clean_key(key)

        if isinstance(value, dict):
            nested_text = json_to_text(value, indent + 4)
            # Only add if the nested dictionary is not empty
            if nested_text.strip():
                text += " " * indent + f"{cleaned_key}:\n" + nested_text
        elif isinstance(value, list):
            # Check if the list is not empty and contains dictionaries
            if value and isinstance(value[0], dict):
                text += " " * indent + f"{cleaned_key}:\n"
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        nested_text = json_to_text(item, indent + 4)
                        if nested_text.strip():
                            text += nested_text
                    else:
                        text += " " * (indent + 4) + f"- {item}\n"
                    # Add a new line after each dictionary item except the last one
                    if i < len(value) - 1:
                        text += "\n"
            elif value:
                text += " " * indent + f"{cleaned_key}:\n"
                for item in value:
                    if isinstance(item, dict):
                        nested_text = json_to_text(item, indent + 4)
                        if nested_text.strip():
                            text += nested_text
                    else:
                        text += " " * (indent + 4) + f"- {item}\n"
        else:
            text += " " * indent + f"{cleaned_key}: {value}\n"

    return text


def get_all_values(json_obj):
    values = []

    def extract(obj):
        """Recursively extract values from the JSON object."""
        if isinstance(obj, dict):
            for value in obj.values():
                extract(value)
        elif isinstance(obj, list):
            for item in obj:
                extract(item)
        else:
            if obj:
                values.append(obj)

    extract(json_obj)
    return values


def extract_fields_from_json(data_json, paths):
    """
    Extracts only the fields specified in `paths` (dot-notation)
    from the nested dictionary `data_json`.

    :param data_json: The original nested dictionary (JSON-like).
    :param paths:     A list of strings denoting nested fields in dot-notation.
    :return:          A new dictionary containing only the requested fields.
    """
    # This dictionary will be our final result.
    output = {}

    grouped_paths = {}
    for path in paths:
        parts = path.split(".")
        parent_path = ".".join(parts[:-1])  # everything except last
        last_key = parts[-1]  # final key

        if parent_path not in grouped_paths:
            grouped_paths[parent_path] = []
        grouped_paths[parent_path].append(last_key)

    # Step 2: For each parent path in `grouped_paths`,
    # traverse `data_json` to get the relevant object/list.
    for parent_path, final_keys in grouped_paths.items():
        # Split the parent path into its components (dot-notation).
        parent_parts = parent_path.split(".") if parent_path else []

        # Traverse `data_json` to get to the parent object.
        current_obj = data_json
        for part in parent_parts:
            if isinstance(current_obj, dict) and part in current_obj:
                current_obj = current_obj[part]
            else:
                # The path does not exist; skip
                current_obj = None
                break

        # If we couldn’t reach a valid object, skip.
        if current_obj is None:
            continue

        # Step 3: Depending on whether current_obj is a dict or a list,
        # extract fields differently.
        if isinstance(current_obj, dict):
            # We need to build the parallel structure in `output`.
            out_ref = output
            for i, part in enumerate(parent_parts):
                if part not in out_ref or not isinstance(out_ref[part], dict):
                    out_ref[part] = {}
                out_ref = out_ref[part]

            # `out_ref` is now the dictionary at the same level as `current_obj`.
            # Extract only the requested final_keys.
            for key in final_keys:
                if key in current_obj:
                    out_ref[key] = current_obj[key]

        elif isinstance(current_obj, list):
            # Create the matching list structure in `output`.
            out_ref = output

            for i, part in enumerate(parent_parts):
                # We still might be walking through nested dict keys
                # before we get to the final list.
                if i < len(parent_parts) - 1:
                    # Not at the last parent part yet
                    if part not in out_ref or not isinstance(out_ref[part], dict):
                        out_ref[part] = {}
                    out_ref = out_ref[part]
                else:
                    # The final part should match a list
                    if part not in out_ref or not isinstance(out_ref[part], list):
                        out_ref[part] = []
                    out_ref = out_ref[part]

            # Now `out_ref` is the list in the output that parallels current_obj.
            trimmed_list = []
            for item in current_obj:
                if isinstance(item, dict):
                    # Build a new dict with only the final_keys we want
                    trimmed_item = {}
                    for key in final_keys:
                        if key in item:
                            trimmed_item[key] = item[key]
                    trimmed_list.append(trimmed_item)
                else:
                    # If it's not a dict, append as-is or handle differently
                    trimmed_list.append(item)

            out_ref.extend(trimmed_list)

    return output
