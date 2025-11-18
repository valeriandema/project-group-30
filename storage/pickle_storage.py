import pickle

from storage.storage_error_decorators import handle_load_errors, handle_save_errors
from storage.storage_interface import StorageInterface


class PickleStorage(StorageInterface):
    @handle_save_errors
    def save(self, data: object) -> bool:
        with open(self.file_path, "wb") as f:
            pickle.dump(data, f)
        return True

    @handle_load_errors
    def load(self) -> object:
        with open(self.file_path, "rb") as f:
            return pickle.load(f)
