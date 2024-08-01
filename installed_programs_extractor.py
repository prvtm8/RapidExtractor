import os  
import winreg  # Provides access to the Windows registry
import logging  
from datetime import datetime  # Used for date and time operations
from tqdm import tqdm  # Used for progress bars

def get_programs_from_registry():
    """
    Retrieve a list of installed programs from the Windows registry.

    Returns:
        list: A list of dictionaries containing program details.
    """
    uninstall_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products",
        r"SOFTWARE\Classes\Installer\Products"
    ]
    
    user_uninstall_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    programs = []

    # Check in HKEY_LOCAL_MACHINE
    for uninstall_path in uninstall_paths:
        programs.extend(query_registry_key(winreg.HKEY_LOCAL_MACHINE, uninstall_path))

    # Check in HKEY_CURRENT_USER
    for uninstall_path in user_uninstall_paths:
        programs.extend(query_registry_key(winreg.HKEY_CURRENT_USER, uninstall_path))

    return remove_duplicates(programs)

def query_registry_key(root_key, uninstall_path):
    """
    Query a specific registry key to retrieve installed programs.

    Args:
        root_key: The root key to start the query from.
        uninstall_path (str): The registry path to query.

    Returns:
        list: A list of dictionaries containing program details.
    """
    programs = []
    try:
        with winreg.OpenKey(root_key, uninstall_path) as reg_key:
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    subkey_name = winreg.EnumKey(reg_key, i)
                    with winreg.OpenKey(reg_key, subkey_name) as sub_key:
                        program = {}
                        program['name'] = query_registry_value(sub_key, 'DisplayName')
                        program['version'] = query_registry_value(sub_key, 'DisplayVersion')
                        program['install_location'] = query_registry_value(sub_key, 'InstallLocation')
                        if program['name'] != "Unknown":
                            programs.append(program)
                except FileNotFoundError:
                    continue
                except OSError:
                    continue
    except FileNotFoundError:
        pass
    except OSError:
        pass
    return programs

def query_registry_value(key, value_name):
    """
    Query a specific value from a registry key.

    Args:
        key: The registry key to query.
        value_name (str): The name of the value to retrieve.

    Returns:
        str: The value retrieved from the registry, or "Unknown" if not found.
    """
    try:
        value, regtype = winreg.QueryValueEx(key, value_name)
        if regtype == winreg.REG_SZ:
            return value
    except FileNotFoundError:
        return "Unknown"
    except OSError:
        return "Unknown"
    return "Unknown"

def remove_duplicates(programs):
    """
    Remove duplicate programs from the list.

    Args:
        programs (list): The list of programs to remove duplicates from.

    Returns:
        list: A list of unique programs.
    """
    seen = set()
    unique_programs = []
    for program in programs:
        identifier = (program['name'], program['version'], program['install_location'])
        if identifier not in seen:
            seen.add(identifier)
            unique_programs.append(program)
    return unique_programs

def get_file_times(file_path):
    """
    Retrieve the creation, modification, and access times of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        dict: A dictionary containing the creation, modification, and access times.
    """
    try:
        file_stats = os.stat(file_path)
        return {
            'created': datetime.fromtimestamp(file_stats.st_ctime),
            'modified': datetime.fromtimestamp(file_stats.st_mtime),
            'accessed': datetime.fromtimestamp(file_stats.st_atime)
        }
    except FileNotFoundError:
        return {
            'created': "Unknown",
            'modified': "Unknown",
            'accessed': "Unknown"
        }
    except Exception as e:
        logging.error(f"Error retrieving file times for {file_path}: {e}")
        return {
            'created': "Unknown",
            'modified': "Unknown",
            'accessed': "Unknown"
        }

def find_executables_in_directories(directories):
    """
    Find executable files in the specified directories.

    Args:
        directories (list): A list of directories to search for executables.

    Returns:
        list: A list of dictionaries containing executable file details.
    """
    executables = []
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.exe'):
                    file_path = os.path.join(root, file)
                    file_metadata = get_file_times(file_path)
                    executables.append({
                        'name': file,
                        'path': file_path,
                        'created': file_metadata['created'],
                        'modified': file_metadata['modified'],
                        'accessed': file_metadata['accessed']
                    })
    return executables

def save_installed_programs(target_dir):
    """
    Save the list of installed programs and executables to the specified target directory.

    Args:
        target_dir (str): The directory where the program details will be saved.
    """
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        programs = get_programs_from_registry()
        directories_to_search = [
            r"C:\Program Files",
            r"C:\Program Files (x86)"
        ]
        executables = find_executables_in_directories(directories_to_search)

        all_programs = programs + executables

        for program in tqdm(all_programs, desc="Saving installed programs and executables"):
            program_name = program['name'].replace(" ", "_").replace(":", "").replace("\\", "").replace("/", "")
            program_dir = os.path.join(target_dir, program_name)
            if not os.path.exists(program_dir):
                os.makedirs(program_dir)
            
            if 'path' in program:  # This is an executable
                file_times = {
                    'created': program['created'],
                    'modified': program['modified'],
                    'accessed': program['accessed']
                }
                install_location = program['path']
            else:  # This is a registered program
                file_times = get_file_times(program['install_location']) if program['install_location'] != "Unknown" else {
                    'created': "Unknown",
                    'modified': "Unknown",
                    'accessed': "Unknown"
                }
                install_location = program['install_location']
            
            with open(os.path.join(program_dir, 'details.txt'), 'w', encoding='utf-8') as f:
                f.write(f"Name: {program['name']}\n")
                if 'version' in program:
                    f.write(f"Version: {program['version']}\n")
                f.write(f"Install Location: {install_location}\n")
                f.write(f"Created: {file_times['created']}\n")
                f.write(f"Modified: {file_times['modified']}\n")
                f.write(f"Accessed: {file_times['accessed']}\n")

        print(f"Installed programs and executables have been saved to {target_dir}")
    except Exception as e:
        print(f"An error occurred while saving installed programs: {e}")
        logging.error(f"Error saving installed programs: {e}")

if __name__ == "__main__":
    logging.basicConfig(filename='installed_programs_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')  # Configure logging
    target_directory = "InstalledPrograms_export"  # Set the target directory for installed programs
    save_installed_programs(target_directory)  # Save the installed programs to the target directory
    input("Press any key to close the window...")  # Wait for user input before closing the window
