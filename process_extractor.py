import os
import subprocess
from tqdm import tqdm
import logging

def save_running_processes(target_dir):
    """
    Saves a list of currently running processes to a text file.
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
    Saves a list of currently scheduled tasks to a text file.
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
