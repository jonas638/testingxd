import socket
import re
import platform
import subprocess
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
                    return mac_address.replace("-", ":")  # Ensure MAC address format is consistent
        else:
            print("Error:", result.stderr)
            return None
    except Exception as e:
        print("Error occurred while retrieving MAC address:", e)
        return None

def port_scan(target_ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Set socket timeout to 1 second
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    open_ports.append(port)
        except Exception as e:
            print(f"Error occurred while scanning port {port}: {e}")
    return open_ports

def write_to_file(file_path, open_ports):
    with open(file_path, 'w') as f:
        f.write("Open ports:\n")
        for port in open_ports:
            f.write(f"{port}\n")

def function_githubreq(file_path):
    repo_owner = 'jonas638'
    repo_name = 'testingxd'
    access_token = '' #use token
    base_url = 'https://api.github.com'

    with open(file_path, 'r') as f:
        file_content = f.read()
    encoded_content = base64.b64encode(file_content.encode()).decode()

    commit_message = 'Update file content'

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
    target_ip = "127.0.0.1"  
    start_port = 1
    end_port = 10 # kan veranderen 
    
    mac_address = get_mac_address()
    open_ports = port_scan(target_ip, start_port, end_port)
    file_name = f"{mac_address.replace(':', '_')}_port_scan_results.txt"
    write_to_file(file_name, open_ports)
    function_githubreq(file_name)
