import os
import shutil
import logging
from tqdm import tqdm

def copy_file_with_metadata(src, dst):
    """
    Copy a file from src to dst, preserving metadata.
    
    :param src: Source file path
    :param dst: Destination file path
    """
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    shutil.copy2(src, dst)

def extract_edge_history(target_dir):
    """
    Extract Edge browser history to the target directory.
    
    :param target_dir: Directory where the history will be copied
    """
    try:
        # Path to Edge history file
        edge_history_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History')
        if os.path.exists(edge_history_path):
            edge_target_dir = os.path.join(target_dir, 'Edge')
            copy_file_with_metadata(edge_history_path, os.path.join(edge_target_dir, 'History'))
            print(f"Copied Edge history to {edge_target_dir}")
        else:
            logging.warning("Edge history file not found.")
    except Exception as e:
        logging.error(f"Error extracting Edge history: {e}")

def extract_firefox_history(target_dir):
    """
    Extract Firefox browser history from all profiles to the target directory.
    
    :param target_dir: Directory where the histories will be copied
    """
    try:
        # Path to Firefox profiles directory
        firefox_profile_dir = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')
        if os.path.exists(firefox_profile_dir):
            for profile in os.listdir(firefox_profile_dir):
                history_path = os.path.join(firefox_profile_dir, profile, 'places.sqlite')
                if os.path.exists(history_path):
                    firefox_target_dir = os.path.join(target_dir, 'Firefox', profile)
                    copy_file_with_metadata(history_path, os.path.join(firefox_target_dir, 'places.sqlite'))
                    print(f"Copied Firefox history for profile {profile} to {firefox_target_dir}")
        else:
            logging.warning("Firefox profiles directory not found.")
    except Exception as e:
        logging.error(f"Error extracting Firefox history: {e}")

def extract_chrome_history(target_dir):
    """
    Extract Chrome browser history to the target directory.
    
    :param target_dir: Directory where the history will be copied
    """
    try:
        # Path to Chrome profile directory
        chrome_profile_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default')
        if os.path.exists(chrome_profile_dir):
            chrome_history_path = os.path.join(chrome_profile_dir, 'History')
            if os.path.exists(chrome_history_path):
                chrome_target_dir = os.path.join(target_dir, 'Chrome')
                copy_file_with_metadata(chrome_history_path, os.path.join(chrome_target_dir, 'History'))
                print(f"Copied Chrome history to {chrome_target_dir}")
        else:
            logging.warning("Chrome profile directory not found.")
    except Exception as e:
        logging.error(f"Error extracting Chrome history: {e}")

def extract_browser_histories(target_dir):
    """
    Extract browser histories for Edge, Firefox, and Chrome to the target directory.
    
    :param target_dir: Directory where the histories will be copied
    """
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        extract_edge_history(target_dir)
        extract_firefox_history(target_dir)
        extract_chrome_history(target_dir)
        print("Browser histories have been copied successfully.")
    except Exception as e:
        print(f"An error occurred while extracting browser histories: {e}")
        logging.error(f"Error extracting browser histories: {e}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(filename='browser_history_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    
    # Define the target directory for exporting browser histories
    target_directory = "BrowserHistory_export"
    
    # Extract browser histories
    extract_browser_histories(target_directory)
    
    # Pause before closing the window
    input("Press any key to close the window...")
