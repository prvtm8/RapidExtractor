import os
import shutil
import logging

def copy_directory_with_metadata(src, dst):
    """
    Recursively copies a directory from the source path to the destination path, preserving metadata.

    Args:
    src (str): The source directory path.
    dst (str): The destination directory path.
    """
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory_with_metadata(s, d)
        else:
            shutil.copy2(s, d)

def copy_cbc_files(target_dir):
    """
    Copies CBC log files from the default source directory (C:\CBC\Logs) to the target directory.

    Args:
    target_dir (str): The directory where the log files will be copied.
    """
    try:
        logs_src = r"C:\CBC\Logs"
        logs_dst = os.path.join(target_dir, 'Logs')
        copy_directory_with_metadata(logs_src, logs_dst)
        print("CBC logs have been copied successfully.")
    except Exception as e:
        print(f"An error occurred while copying CBC logs: {e}")
        logging.error(f"Error copying CBC logs: {e}")

if __name__ == "__main__":
    # Configure logging to record debug information in a log file.
    logging.basicConfig(filename='logs/cbc_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "CBC_export"
    copy_cbc_files(target_directory)
    input("Press any key to close the window...")
