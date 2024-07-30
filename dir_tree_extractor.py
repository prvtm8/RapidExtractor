import os
import time
from tqdm import tqdm

def generate_dir_tree(start_path, output_file):
    def tree(dir_path, prefix=''):
        try:
            contents = sorted(os.listdir(dir_path))
        except PermissionError:
            contents = []
            f.write(prefix + '    [Permission Denied]\n')
            progress_bar.update(1)
            return
        except FileNotFoundError:
            contents = []
            f.write(prefix + '    [File Not Found]\n')
            progress_bar.update(1)
            return

        pointers = [contents.index(item) == len(contents) - 1 for item in contents]

        for pointer, path in zip(pointers, contents):
            full_path = os.path.join(dir_path, path)
            connector = '└── ' if pointer else '├── '
            line = prefix + connector + path
            try:
                f.write(line + '\n')
                if os.path.isdir(full_path):
                    extension = '    ' if pointer else '│   '
                    tree(full_path, prefix + extension)
                progress_bar.update(1)
            except PermissionError:
                f.write(prefix + '    [Permission Denied]\n')
                progress_bar.update(1)
            except FileNotFoundError:
                f.write(prefix + '    [File Not Found]\n')
                progress_bar.update(1)

    print(f"Generating directory tree starting from {start_path}...")

    try:
        total_entries = sum([len(files) + len(dirs) for _, dirs, files in os.walk(start_path)])
        with open(output_file, 'w', encoding='utf-8') as f, tqdm(total=total_entries, desc="Generating Directory Tree") as progress_bar:
            tree(start_path)
        print(f"Directory tree has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while generating the directory tree: {e}")

def extract_dir_tree(target_dir):
    """Generate a directory tree of the C: drive and save it to a text file."""
    start_time = time.time()
    root_dir = "C:\\"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    output_file = os.path.join(target_dir, 'dir_tree.txt')
    print(f"Saving directory tree to {output_file}...")
    generate_dir_tree(root_dir, output_file)
    end_time = time.time()
    print(f"Directory tree successfully saved to {output_file}")
    print(f"Extraction took {end_time - start_time:.2f} seconds")
