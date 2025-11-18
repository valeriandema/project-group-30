import json
from datetime import datetime
from storage.storage_interface import StorageInterface
from storage.storage_error_decorators import handle_save_errors, handle_load_errors


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class JSONStorage(StorageInterface):
    @handle_save_errors
    def save(self, data: object) -> bool:
        data_dict = self._serialize(data)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder)
        return True

    @handle_load_errors
    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self._deserialize(data)

    def _serialize(self, obj) -> dict:
        if hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                if isinstance(value, list):
                    result[key] = [self._serialize(item) for item in value]
                elif isinstance(value, dict):
                    result[key] = {k: self._serialize(v) for k, v in value.items()}
                elif hasattr(value, "__dict__"):
                    result[key] = self._serialize(value)
                else:
                    result[key] = value
            return result
        return obj

    def _deserialize(self, data):
        if isinstance(data, dict):
            return {k: self._deserialize(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._deserialize(item) for item in data]
        return data
