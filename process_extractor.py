import os
import subprocess
from tqdm import tqdm

def save_running_processes(target_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        output_file = os.path.join(target_dir, 'running_processes.txt')
        command = 'tasklist'

        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        print(f"Running processes have been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving running processes: {e}")

def save_running_tasks(target_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        output_file = os.path.join(target_dir, 'running_tasks.txt')
        command = 'schtasks'

        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            f.write(result.stdout)
        print(f"Running tasks have been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving running tasks: {e}")
