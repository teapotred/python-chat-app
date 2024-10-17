import subprocess
import os
from client_code import file_path as client_path
from server_code import file_path as server_path

files_to_run = [client_path, server_path]

def run_files(file_path):
    try:
        subprocess.run(['python3', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running file at path '{file_path}': {e}")
    except FileNotFoundError:
        print(f"File not found at path '{file_path}'.")

if __name__ == "__main__":
    print("Starting both server_code.py and client_code.py concurrently...")

    processes = []

    for file in files_to_run:
        process = subprocess.Popen(['python3', file])
        processes.append(process)

    for process in processes:
        process.wait()

    print("Both processes have completed.")
