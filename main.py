import os
import sys
import shutil
import time
import logging
from prefetch_extractor import copy_prefetch_files
from dir_tree_extractor import extract_dir_tree
from process_extractor import save_running_processes, save_running_tasks
from installed_programs_extractor import save_installed_programs
from teamviewer_extractor import copy_teamviewer_files
from cbc_extractor import copy_cbc_files
from browser_history_extractor import extract_browser_histories

def create_target_folder(target_device_name):
    """
    Create a target folder for the extraction process.

    Args:
        target_device_name (str): The name of the target device.

    Returns:
        str: The path to the created target directory.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    target_dir = os.path.join(base_dir, f'{target_device_name}_extraction')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return target_dir

def zip_directory(directory_path, zip_name):
    """
    Zip a directory and remove the original directory after zipping.

    Args:
        directory_path (str): The path to the directory to zip.
        zip_name (str): The name of the zip file to create.
    """
    logging.info(f"Zipping directory {directory_path} to {zip_name}.zip...")
    shutil.make_archive(zip_name, 'zip', directory_path)
    logging.info(f"Zipped {zip_name}.zip successfully.")
    shutil.rmtree(directory_path)
    logging.info(f"Removed original directory {directory_path}.")

def main(selected_modules, target_device_name):
    """
    Main function to perform the data extraction based on the selected modules.

    Args:
        selected_modules (list): List of selected modules for extraction.
        target_device_name (str): The name of the target device.
    """
    target_dir_base = create_target_folder(target_device_name)

    # Configure logging to use a file in the target directory
    log_file_path = os.path.join(target_dir_base, 'extraction.log')
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s [%(module)s] %(message)s')

    logging.info("Starting data extraction...")

    # Perform data extraction for each selected module
    if 'prefetch' in selected_modules:
        logging.info("Starting Prefetch extraction...")
        try:
            start_time = time.time()
            prefetch_target_dir = os.path.join(target_dir_base, 'Prefetch_export')
            copy_prefetch_files(prefetch_target_dir)
            zip_name = os.path.join(target_dir_base, 'Prefetch_export')
            zip_directory(prefetch_target_dir, zip_name)
            end_time = time.time()
            logging.info(f"Prefetch extraction completed in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"Prefetch extraction failed: {e}")

    if 'dir_tree' in selected_modules:
        logging.info("Starting Directory Tree extraction...")
        try:
            start_time = time.time()
            dir_tree_target_dir = os.path.join(target_dir_base, 'DirTree_export')
            extract_dir_tree(dir_tree_target_dir)
            zip_name = os.path.join(target_dir_base, 'DirTree_export')
            zip_directory(dir_tree_target_dir, zip_name)
            end_time = time.time()
            logging.info(f"Directory Tree extraction completed in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"Directory Tree extraction failed: {e}")

    if 'processes' in selected_modules:
        logging.info("Starting Running Processes and Tasks extraction...")
        try:
            start_time = time.time()
            processes_target_dir = os.path.join(target_dir_base, 'Processes_export')
            save_running_processes(processes_target_dir)
            save_running_tasks(processes_target_dir)
            zip_name = os.path.join(target_dir_base, 'Processes_export')
            zip_directory(processes_target_dir, zip_name)
            end_time = time.time()
            logging.info(f"Running Processes and Tasks extraction completed in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"Running Processes and Tasks extraction failed: {e}")

    if 'installed_programs' in selected_modules:
        logging.info("Starting Installed Programs extraction...")
        try:
            start_time = time.time()
            programs_target_dir = os.path.join(target_dir_base, 'InstalledPrograms_export')
            save_installed_programs(programs_target_dir)
            zip_name = os.path.join(target_dir_base, 'InstalledPrograms_export')
            zip_directory(programs_target_dir, zip_name)
            end_time = time.time()
            logging.info(f"Installed Programs extraction completed in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"Installed Programs extraction failed: {e}")

    if 'teamviewer' in selected_modules:
        logging.info("Starting TeamViewer extraction...")
        try:
            start_time = time.time()
            teamviewer_target_dir = os.path.join(target_dir_base, 'TeamViewer_export')
            copy_teamviewer_files(teamviewer_target_dir)
            zip_name = os.path.join(target_dir_base, 'TeamViewer_export')
            zip_directory(teamviewer_target_dir, zip_name)
            end_time = time.time()
            logging.info(f"TeamViewer extraction completed in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"TeamViewer extraction failed: {e}")

    if 'cbc' in selected_modules:
        logging.info("Starting CBC extraction...")
        try:
            start_time = time.time()
            cbc_target_dir = os.path.join(target_dir_base, 'CBC_export')
            copy_cbc_files(cbc_target_dir)
            zip_name = os.path.join(target_dir_base, 'CBC_export')
            zip_directory(cbc_target_dir, zip_name)
            end_time = time.time()
            logging.info(f"CBC extraction completed in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"CBC extraction failed: {e}")

    if 'browser_history' in selected_modules:
        logging.info("Starting Browser History extraction...")
        try:
            start_time = time.time()
            browser_history_target_dir = os.path.join(target_dir_base, 'BrowserHistory_export')
            extract_browser_histories(browser_history_target_dir)
            zip_name = os.path.join(target_dir_base, 'BrowserHistory_export')
            zip_directory(browser_history_target_dir, zip_name)
            end_time = time.time()
            logging.info(f"Browser History extraction completed in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            logging.error(f"Browser History extraction failed: {e}")

    logging.info("Data extraction completed. Only ZIP files are left in the Target folder.")
    input("Press any key to close the window...")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.py <selected_modules> <target_device_name>")
        sys.exit(1)
    
    selected_modules = sys.argv[1].split()
    target_device_name = sys.argv[2]
    try:
        main(selected_modules, target_device_name)
    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")
        sys.exit(1)
