import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def move_file(source_path, destination_folder):
    try:
        source_path = Path(source_path)
        extension = source_path.suffix.lower()

        extension_folder = Path(destination_folder) / extension[1:]
        extension_folder.mkdir(parents=True, exist_ok=True)

        destination_path = extension_folder / source_path.name
        source_path.rename(destination_path)
        print(f"Moved: {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error moving {source_path}: {e}")

def sort_files(source_folder, destination_folder):
    source_folder = Path(source_folder)
    if not source_folder.exists():
        print(f"Source folder '{source_folder}' not found.")
        return

    destination_folder = Path(destination_folder)
    if not destination_folder.exists():
        destination_folder.mkdir(parents=True, exist_ok=True)
        print(f"Destination folder '{destination_folder}' created.")

    files_to_sort = [file for file in source_folder.rglob('*') if file.is_file()]

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(move_file, file, destination_folder): file for file in files_to_sort}
        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {file}: {e}")

    print("Sorting completed.")

if __name__ == "__main__":
    source_folder = r'D:\testfolder' # Path to sort
    destination_folder = r'D:\sortedfolder' # Sorted file

    sort_files(source_folder, destination_folder)