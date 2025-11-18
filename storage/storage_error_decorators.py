import pickle
import json


def handle_save_errors(func):
    def wrapper(self, data):
        try:
            return func(self, data)
        except (IOError, OSError) as e:
            print(f"Can't save data to {self.file_path}: {e}")
            return False
        except (TypeError, pickle.PicklingError) as e:
            print(f"Can't serialize data: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error while saving: {e}")
            return False

    return wrapper


def handle_load_errors(func):
    def wrapper(self):
        try:
            return func(self)
        except FileNotFoundError:
            print(f"File {self.file_path} not found")
            return None
        except (pickle.UnpicklingError, EOFError, AttributeError) as e:
            print(f"File {self.file_path} is corrupted (pickle): {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"File {self.file_path} is corrupted (json): {e}")
            return None
        except Exception as e:
            print(f"Can't load data from {self.file_path}: {e}")
            return None

    return wrapper
