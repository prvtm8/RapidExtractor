import os  # Provides a way to interact with the operating system
import shutil  # Used for high-level file operations
import logging  # Used for logging messages

def copy_directory_with_metadata(src, dst):
    """
    Recursively copy a directory and its contents, preserving metadata.

    Args:
        src (str): The source directory to copy from.
        dst (str): The destination directory to copy to.
    """
    if not os.path.exists(dst):  # Check if the destination directory exists
        os.makedirs(dst)  # Create the destination directory if it does not exist
    for item in os.listdir(src):  # Iterate over all items in the source directory
        s = os.path.join(src, item)  # Full path of the source item
        d = os.path.join(dst, item)  # Full path of the destination item
        if os.path.isdir(s):  # If the item is a directory
            copy_directory_with_metadata(s, d)  # Recursively copy the directory
        else:  # If the item is a file
            shutil.copy2(s, d)  # Copy the file, preserving metadata

def copy_cbc_files(target_dir):
    """
    Copy CBC log files to the specified target directory.

    Args:
        target_dir (str): The directory where the CBC logs should be copied.
    """
    try:
        logs_src = r"C:\CBC\Logs"  # Source directory of CBC logs
        logs_dst = os.path.join(target_dir, 'Logs')  # Destination directory for CBC logs
        copy_directory_with_metadata(logs_src, logs_dst)  # Copy the logs directory and its contents
        print("CBC logs have been copied successfully.")  # Print success message
    except Exception as e:  # Catch any exception that occurs during copying
        print(f"An error occurred while copying CBC logs: {e}")  # Print error message
        logging.error(f"Error copying CBC logs: {e}")  # Log the error message

if __name__ == "__main__":
    logging.basicConfig(filename='cbc_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')  # Configure logging
    target_directory = "CBC_export"  # Set the target directory for CBC logs
    copy_cbc_files(target_directory)  # Copy CBC logs to the target directory
    input("Press any key to close the window...")  # Wait for user input before closing the window
