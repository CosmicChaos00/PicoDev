import urequests
import os
import json
from constantData import Constant
import wifiLogin

class UpdatePico:
    def __init__(self, base_url, api_base_url, file_list_name='files_to_update.txt', hash_file='last_commit_hashes.json'):
        self.base_url = base_url
        self.api_base_url = api_base_url
        self.file_list_name = file_list_name
        self.hash_file = hash_file

    def read_file_list(self):
        """ Read the list of files from a local text file. """
        try:
            with open(self.file_list_name, 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("File list not found.")
            return []

    def get_latest_commit_hash(self, filepath):
        """ Fetch the latest commit hash for a file from GitHub. """
        try:
            response = urequests.get(self.api_base_url + filepath)
            if response.status_code == 200:
                commit_data = json.loads(response.text)
                return commit_data[0]['sha']  # Get the hash of the latest commit
            else:
                print(f"Failed to fetch commit data for {filepath}, status code:", response.status_code)
        except Exception as e:
            print(f"Error fetching commit hash for {filepath}:", e)
        return None

    def update_files(self):
        file_list = self.read_file_list()
        if not os.listdir().count(self.hash_file):  # Checks if the file is in the current directory listing
            print(f"Hash file {self.hash_file} does not exist. Assuming first run.")
            hashes = {}          
        else:
            try:
                with open(self.hash_file, 'r') as f:
                    hashes = json.load(f)
            except OSError as e:
                print(f"Failed to open hash file {self.hash_file}: {e}")
                return {}
        
        for filename in file_list:
            latest_commit_hash = self.get_latest_commit_hash(filename)
            if latest_commit_hash is None:
                continue
            
            local_commit_hash = hashes.get(filename)
            
            if local_commit_hash != latest_commit_hash:
                response = urequests.get(self.base_url + filename, stream=True)
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)
                    hashes[filename] = latest_commit_hash  # Update the hash in the dictionary
                    print(f"Updated {filename}.")
                else:
                    print(f"Failed to download {filename}, HTTP status code:", response.status_code)
                response.close()

        # Write the updated hashes back to the file
        with open(self.hash_file, 'w') as f:
            json.dump(hashes, f)

# Example usage

hub_url = Constant.getHubURL()
api_url = Constant.getAPI_URL()

updater = UpdatePico(hub_url,api_url)
updater.update_files()
