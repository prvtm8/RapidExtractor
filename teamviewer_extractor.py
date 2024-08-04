import os
import shutil
from tqdm import tqdm
import logging

def copy_files_from_path(path, target_dir):
    """
    Copies all .txt and .log files from the specified path to the target directory.

    Args:
    path (str): The source directory to search for files.
    target_dir (str): The destination directory where files will be copied.

    Returns:
    int: The number of files copied.
    """
    files_copied = 0
    
    if not os.path.exists(path):
        logging.warning(f"Path not found: {path}")
        print(f"Path not found: {path}")
        return files_copied
    
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt') or file_name.endswith('.log'):
                source_file = os.path.join(root, file_name)
                rel_path = os.path.relpath(source_file, path)
                target_file = os.path.join(target_dir, rel_path)

                os.makedirs(os.path.dirname(target_file), exist_ok=True)

                shutil.copy2(source_file, target_file)
                files_copied += 1
                logging.info(f"Copied {source_file} to {target_file}")
                print(f"Copied {source_file} to {target_file}")
    
    return files_copied

def copy_teamviewer_files(target_dir):
    """
    Copies TeamViewer log and text files from common directories to the specified target directory.

    Args:
    target_dir (str): The directory where the files will be copied.
    """
    try:
        paths_to_search = [
            r"C:\Program Files (x86)\TeamViewer",
            r"C:\Users",
        ]
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        files_copied = 0
        
        for base_path in paths_to_search:
            if base_path == r"C:\Users":
                for user_folder in os.listdir(base_path):
                    user_path = os.path.join(base_path, user_folder, "AppData", "Local", "TeamViewer", "Logs")
                    if os.path.exists(user_path):
                        files_copied += copy_files_from_path(user_path, target_dir)
            else:
                files_copied += copy_files_from_path(base_path, target_dir)
        
        if files_copied == 0:
            logging.warning("No TeamViewer text files or log files found.")
            print("No TeamViewer text files or log files found.")
        else:
            logging.info(f"All TeamViewer files have been copied successfully. Total files copied: {files_copied}")
            print(f"All TeamViewer files have been copied successfully. Total files copied: {files_copied}")
    except Exception as e:
        logging.error(f"An error occurred while copying TeamViewer files: {e}")
        print(f"An error occurred while copying TeamViewer files: {e}")

if __name__ == "__main__":
    # Configure logging to record debug information in a log file.
    logging.basicConfig(filename='logs/teamviewer_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    # Set the target directory for exporting TeamViewer files.
    target_directory = "TeamViewer_export"
    # Copy TeamViewer files to the target directory.
    copy_teamviewer_files(target_directory)
    # Wait for user input before closing the script.
    input("Press any key to close the window...")
