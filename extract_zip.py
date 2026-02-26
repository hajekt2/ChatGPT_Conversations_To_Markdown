import zipfile
import os
import shutil
from pathlib import Path

def _find_conversation_jsons(base_dir):
    """Find conversation JSON files in old and new ChatGPT export formats."""
    base_dir = Path(base_dir)

    # Newest export format: sharded files (conversations-001.json, ...)
    shards = sorted(base_dir.rglob("conversations-*.json"))
    if shards:
        return shards

    # Legacy export format: single conversations.json
    legacy = list(base_dir.rglob("conversations.json"))
    return legacy


def extract_chatgpt_zip(zip_path, extract_to=None):
    """
    Extract ChatGPT export ZIP file.

    Args:
        zip_path: Path to the ZIP file (string or Path)
        extract_to: Where to extract (defaults to temp folder)

    Returns:
        Path to extracted ChatGPT export directory
    """
    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"Not a valid ZIP file: {zip_path}")

    # Default extraction location
    if extract_to is None:
        extract_to = zip_path.parent / "ChatGPT_Export"
    else:
        extract_to = Path(extract_to)

    print(f"📦 Extracting ZIP file...")
    print(f"   From: {zip_path}")
    print(f"   To: {extract_to}")

    # Create extraction directory
    extract_to.mkdir(parents=True, exist_ok=True)

    # Extract all files
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Find conversation data files (legacy single-file OR new sharded format)
    conversation_files = _find_conversation_jsons(extract_to)

    if not conversation_files:
        raise FileNotFoundError(
            "No conversation JSON files found in ZIP. "
            "Expected conversations.json or conversations-*.json. "
            "Make sure you exported the correct ChatGPT data."
        )

    # Use the parent dir of first conversation file as input directory
    extract_to = conversation_files[0].parent

    print(f"✅ Extracted successfully!")
    if any(p.name.startswith("conversations-") for p in conversation_files):
        print(f"   Found {len(conversation_files)} sharded conversation files at: {extract_to}")
    else:
        print(f"   Found conversations.json at: {extract_to}")

    return extract_to

def cleanup_extracted_files(extract_path):
    """Remove extracted files (optional cleanup)"""
    extract_path = Path(extract_path)
    if extract_path.exists() and extract_path.is_dir():
        shutil.rmtree(extract_path)
        print(f"🧹 Cleaned up extracted files: {extract_path}")

def is_zip_file(path):
    """Check if path is a ZIP file"""
    path = Path(path)
    return path.exists() and zipfile.is_zipfile(path)

def is_extracted_directory(path):
    """Check if path is an already-extracted ChatGPT export directory."""
    path = Path(path)
    if not path.exists() or not path.is_dir():
        return False

    return bool(_find_conversation_jsons(path))

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_zip.py <path_to_zip>")
        sys.exit(1)

    zip_path = sys.argv[1].strip('"')  # Remove quotes if present
    extracted_path = extract_chatgpt_zip(zip_path)
    print(f"\n📁 Use this path for input: {extracted_path}")
