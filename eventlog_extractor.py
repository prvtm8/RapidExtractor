import os
import subprocess
from tqdm import tqdm

def copy_event_logs(target_dir):
    try:
        event_logs = [
            'Application',
            'Security',
            'System',
            'Setup',
            'ForwardedEvents'
        ]

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with tqdm(total=len(event_logs), desc="Copying Event Logs") as pbar:
            for log_name in event_logs:
                output_file = os.path.join(target_dir, f'{log_name}.evtx')
                command = f'wevtutil epl {log_name} {output_file}'
                try:
                    subprocess.run(command, check=True, shell=True)
                except subprocess.CalledProcessError as e:
                    print(f"Failed to export {log_name} log: {e}")
                pbar.update(1)
        print("All event logs have been copied successfully.")
    except Exception as e:
        print(f"An error occurred while copying event logs: {e}")
