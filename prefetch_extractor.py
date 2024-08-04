import os
import shutil
from tqdm import tqdm
import logging

def copy_prefetch_files(target_dir):
    """
    Copies all Prefetch files from the Windows Prefetch directory (%RootDir%\Windows\Prefetch) to the specified target directory.

    Args:
    target_dir (str): The directory where the Prefetch files will be copied.
    """
    try:
        prefetch_dir = os.path.join(os.environ['WINDIR'], 'Prefetch')
        if not os.path.exists(prefetch_dir):
            logging.warning(f"Prefetch directory not found: {prefetch_dir}")
            print(f"Prefetch directory not found: {prefetch_dir}")
            return

        total_files = sum(len(files) for _, _, files in os.walk(prefetch_dir))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with tqdm(total=total_files, desc="Copying Prefetch Files") as pbar:
            for root, dirs, files in os.walk(prefetch_dir):
                for file_name in files:
                    source_file = os.path.join(root, file_name)
                    rel_path = os.path.relpath(source_file, os.path.dirname(prefetch_dir))
                    target_file = os.path.join(target_dir, 'Windows', rel_path)

                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    shutil.copy2(source_file, target_file)
                    pbar.update(1)
        logging.info("All prefetch files have been copied successfully.")
        print("All prefetch files have been copied successfully.")
    except Exception as e:
        logging.error(f"An error occurred while copying prefetch files: {e}")
        print(f"An error occurred while copying prefetch files: {e}")

if __name__ == "__main__":
    # Configure logging to record debug information in a log file.
    logging.basicConfig(filename='logs/prefetch_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "Prefetch_export"
    copy_prefetch_files(target_directory)
    input("Press any key to close the window...")
