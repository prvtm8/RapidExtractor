import os
import winreg
import logging
from datetime import datetime

def get_programs_from_registry():
    uninstall_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    programs = []

    for uninstall_path in uninstall_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_path) as reg_key:
                for i in range(winreg.QueryInfoKey(reg_key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(reg_key, i)
                        with winreg.OpenKey(reg_key, subkey_name) as sub_key:
                            program = {}
                            program['name'] = winreg.QueryValueEx(sub_key, 'DisplayName')[0] if winreg.QueryValueEx(sub_key, 'DisplayName')[1] == winreg.REG_SZ else "Unknown"
                            program['version'] = winreg.QueryValueEx(sub_key, 'DisplayVersion')[0] if winreg.QueryValueEx(sub_key, 'DisplayVersion')[1] == winreg.REG_SZ else "Unknown"
                            program['install_location'] = winreg.QueryValueEx(sub_key, 'InstallLocation')[0] if winreg.QueryValueEx(sub_key, 'InstallLocation')[1] == winreg.REG_SZ else "Unknown"
                            programs.append(program)
                    except FileNotFoundError:
                        continue
                    except OSError:
                        continue
        except FileNotFoundError:
            continue
        except OSError:
            continue

    return programs

def get_file_times(file_path):
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

def save_installed_programs(target_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        programs = get_programs_from_registry()

        for program in programs:
            program_name = program['name'].replace(" ", "_").replace(":", "").replace("\\", "").replace("/", "")
            program_dir = os.path.join(target_dir, program_name)
            if not os.path.exists(program_dir):
                os.makedirs(program_dir)
            
            file_times = get_file_times(program['install_location']) if program['install_location'] != "Unknown" else {
                'created': "Unknown",
                'modified': "Unknown",
                'accessed': "Unknown"
            }
            
            with open(os.path.join(program_dir, 'details.txt'), 'w', encoding='utf-8') as f:
                f.write(f"Name: {program['name']}\n")
                f.write(f"Version: {program['version']}\n")
                f.write(f"Install Location: {program['install_location']}\n")
                f.write(f"Created: {file_times['created']}\n")
                f.write(f"Modified: {file_times['modified']}\n")
                f.write(f"Accessed: {file_times['accessed']}\n")

        print(f"Installed programs have been saved to {target_dir}")
    except Exception as e:
        print(f"An error occurred while saving installed programs: {e}")

if __name__ == "__main__":
    save_installed_programs(".")
