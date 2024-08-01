import os
import shutil
from tqdm import tqdm
import logging

def copy_files_from_path(path, target_dir):
    """
    Copies .txt and .log files from the given path to the target directory.
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
    Copies TeamViewer log files from standard directories to the target directory.
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
    logging.basicConfig(filename='teamviewer_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "TeamViewer_export"
    copy_teamviewer_files(target_directory)
    input("Press any key to close the window...")
