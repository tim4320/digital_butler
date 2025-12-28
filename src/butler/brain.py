import json
import os
from pathlib import Path
from typing import Dict

# We store the memory in the user's home folder so it persists globally
MEMORY_FILE = Path.home() / ".butler_memory.json"

def _load_memory() -> Dict[str, str]:
    """Internal helper: Reads the JSON file."""
    if not MEMORY_FILE.exists():
        return {}
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_memory(data: Dict[str, str]) -> None:
    """Internal helper: Writes to the JSON file."""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def remember(key: str, value: str) -> None:
    """Saves a new fact."""
    data = _load_memory()
    data[key] = value
    _save_memory(data)
    print(f"🧠 I will remember: {key} = {value}")

def recall(key: str = None) -> None:
    """
    Retrieves facts.
    If a key is provided, look up that specific item.
    If no key is provided, list everything.
    """
    data = _load_memory()

    if not data:
        print("🧠 My memory is empty.")
        return

    print("\n🧠 --- MEMORY BANK ---")
    if key:
        # Look up specific item
        value = data.get(key)
        if value:
            print(f"✅ {key}: {value}")
        else:
            print(f"❌ I don't recall anything about '{key}'.")
    else:
        # List all items
        for k, v in data.items():
            print(f"🔹 {k}: {v}")
    print("----------------------")

def forget(key: str) -> None:
    """Deletes a fact."""
    data = _load_memory()
    if key in data:
        del data[key]
        _save_memory(data)
        print(f"🗑️ I have forgotten '{key}'.")
    else:
        print(f"❌ I never knew '{key}' to begin with.")
