import hashlib
from pathlib import Path


def compute_file_hash(file_path: Path) -> str:
    """
    Computes a SHA256 hash for the file content.
    """
    hash_algo = hashlib.sha256()
    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()
