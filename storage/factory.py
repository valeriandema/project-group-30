from pathlib import Path

from storage.json_storage import JSONStorage
from storage.pickle_storage import PickleStorage
from storage.storage_interface import StorageInterface

STORAGE_TYPES = {
    "pkl": PickleStorage,
    "json": JSONStorage,
}


class StorageFactory:
    @staticmethod
    def create_storage(
        storage_type: str, base_path: None | Path = None
    ) -> StorageInterface:
        storage_type = storage_type.lower()

        if storage_type not in STORAGE_TYPES:
            raise ValueError(
                f"Unsupported storage type: {storage_type}. "
                f"Supported types: {', '.join(STORAGE_TYPES.keys())}"
            )

        if base_path is None:
            base_path = Path(__file__).resolve().parent.parent / "files"

        # Create directory if it doesn't exist
        base_path.mkdir(parents=True, exist_ok=True)

        file_path = base_path / f"addressbook.{storage_type}"

        return STORAGE_TYPES[storage_type](file_path)

    @staticmethod
    def get_supported_types() -> list[str]:
        return list(STORAGE_TYPES.keys())
