import os
import subprocess
from tqdm import tqdm
import logging

def save_running_processes(target_dir):
    """
    Saves the list of currently running processes to a specified directory.

    Args:
    target_dir (str): The directory where the running processes file will be saved.
    """
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        output_file = os.path.join(target_dir, 'running_processes.txt')
        command = 'tasklist'

        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        logging.info(f"Running processes have been saved to {output_file}")
        print(f"Running processes have been saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred while saving running processes: {e}")
        print(f"An error occurred while saving running processes: {e}")

def save_running_tasks(target_dir):
    """
    Saves the list of currently running scheduled tasks to a specified directory.

    Args:
    target_dir (str): The directory where the running tasks file will be saved.
    """
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        output_file = os.path.join(target_dir, 'running_tasks.txt')
        command = 'schtasks'

        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        logging.info(f"Running tasks have been saved to {output_file}")
        print(f"Running tasks have been saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred while saving running tasks: {e}")
        print(f"An error occurred while saving running tasks: {e}")

if __name__ == "__main__":
    # Configure logging to record debug information in a log file.
    logging.basicConfig(filename='logs/process_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "Processes_export"
    save_running_processes(target_directory)
    save_running_tasks(target_directory)
    input("Press any key to close the window...")
