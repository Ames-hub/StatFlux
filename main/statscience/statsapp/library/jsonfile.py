import json
import os

class jsontemplates:
    """
    A class which contains the expected format of JSON files for the project.
    """
    SETTINGS = {
        'database': {
            'user': None,
            'password': None,
            'host': None,
            'port': None,
            'database': None,
        }
    }

class jmod:
    """
    A Class used to manage JSON files without a big hassle.
    """
    def __init__(self, filepath: str, expected_template: dict):
        self.filepath = filepath
        self.template = expected_template
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            self.write_json(self.template)
        else:
            with open(self.filepath, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

            # Merge template keys (non-destructive)
            merged = self.merge_dicts(self.template, data)
            self.write_json(merged)

    def merge_dicts(self, default: dict, current: dict) -> dict:
        for key, value in default.items():
            if key not in current:
                current[key] = value
            elif isinstance(value, dict) and isinstance(current[key], dict):
                current[key] = self.merge_dicts(value, current[key])
        return current

    def write_json(self, data: dict):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    # noinspection PyMethodMayBeStatic
    def navigate(self, data: dict, key_path: str, create_missing=False):
        keys = key_path.split('.')
        for key in keys[:-1]:
            if key not in data:
                if create_missing:
                    data[key] = {}
                else:
                    raise KeyError(f"Missing key in path: {key}")
            data = data[key]
        return data, keys[-1]

    def set_value(self, key_path: str, value):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        ref, last_key = self.navigate(data, key_path, create_missing=True)
        ref[last_key] = value
        self.write_json(data)

    def get_value(self, key_path: str):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        ref, last_key = self.navigate(data, key_path)
        return ref[last_key]
