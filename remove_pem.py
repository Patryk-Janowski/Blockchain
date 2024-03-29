import os
import json

def remove_pem_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pem'):
            try:
                os.remove(os.path.join(directory, filename))
                print(f'Removed {filename}')
            except Exception as e:
                print(f'Error removing {filename}: {e}')

if __name__ == "__main__":
    current_directory = os.getcwd()
    remove_pem_files(current_directory)