import os
from pathlib import Path

def patch_uyghur_latin_filenames(folder_path):
    path = Path(folder_path)
    if not path.exists():
        print(f"Directory not found: {folder_path}")
        return

    print(f"Patching filenames in: {path.name}")
    
    # We define a specific mapping for the missed characters
    patch_map = {
        'ې': 'e',
        'ى': 'i',
        'ئا': 'a',
        'ئە': 'e',
        'ئ': ''  # Remove any stray Hamza
    }

    files = list(path.glob("*.txt"))
    count = 0

    for file_path in files:
        old_name = file_path.name
        new_name = old_name
        
        # Replace based on our patch map
        for uyghur_char, latin_char in patch_map.items():
            new_name = new_name.replace(uyghur_char, latin_char)

        # Only rename if the name actually changed
        if old_name != new_name:
            new_file_path = file_path.with_name(new_name)
            try:
                # If the target name already exists, we skip to avoid overwriting
                if not new_file_path.exists():
                    file_path.rename(new_file_path)
                    print(f"Patched: {old_name} -> {new_name}")
                    count += 1
                else:
                    print(f"Skip (Already exists): {new_name}")
            except Exception as e:
                print(f"Error patching {old_name}: {e}")

    print(f"Finished. Patched {count} files in {path.name}.\n")

if __name__ == "__main__":
    folders = [
        "/media/abdulla-arishi/Volume/arishi.wiki/data/processed_files/uyghur_tibabet_ham_dora",
        "/media/abdulla-arishi/Volume/arishi.wiki/data/processed_files/titles_split"
    ]

    for folder in folders:
        patch_uyghur_latin_filenames(folder)
