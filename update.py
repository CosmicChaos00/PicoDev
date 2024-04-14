import requests  # Make sure to install the 'requests' library if you haven't
from constantData import Constant
import wifi

class UpdatePico:
    def __init__(self, base_url, api_base_url, token, owner, repo, user_agent, hash_file):
        self.base_url = base_url.rstrip('/') + '/'
        self.api_base_url = api_base_url.rstrip('/') + '/'
        self.token = token
        self.owner = owner
        self.repo = repo
        self.user_agent = user_agent
        self.hash_file = hash_file
        self.local_hashes = self.load_local_hashes()

    def load_local_hashes(self):
        try:
            with open(self.hash_file, 'r') as f:
                return json.load(f)
        except OSError:  # Changed from FileNotFoundError to OSError
            print("File list not found or couldn't be opened.")
            return {}

    def save_local_hashes(self):
        with open(self.hash_file, 'w') as f:
            json.dump(self.local_hashes, f)

    def get_latest_commit_hash(self, filepath):
        url = f"{self.api_base_url}repos/{self.owner}/{self.repo}/commits?path={filepath}"
        headers = {
            'Authorization': f'token {self.token}',
            'User-Agent': self.user_agent
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            commits = response.json()
            if commits:
                return commits[0]['sha']  # Return the SHA of the latest commit
            else:
                return None
        else:
            print(f"Failed to fetch commit data for {filepath}, status code: {response.status_code}")
            print("Response:", response.text)
            return None

    def update_files(self):
        filepaths = Constant.getFiles()
        for filepath in filepaths:
            latest_commit_hash = self.get_latest_commit_hash(filepath)
            if latest_commit_hash and (self.local_hashes.get(filepath) != latest_commit_hash):
                response = requests.get(f"{self.base_url}{filepath}")
                if response.status_code == 200:
                    with open(filepath, 'wb') as file:
                        file.write(response.content)
                    self.local_hashes[filepath] = latest_commit_hash
                    print(f"Updated {filepath}")
                else:
                    print(f"Failed to download {filepath}, status code: {response.status_code}")
            else:
                print(f"{filepath} is up to date.")
        self.save_local_hashes()

# Usage
owner = Constant.getOwner()
repo = Constant.getRepo()
user_agent = Constant.getUserAgent()
token = Constant.getToken()
base_url = Constant.getHubURL()
api_base_url = Constant.getAPI_URL()
hash_file = "hashes.json"

updater = UpdatePico(base_url, api_base_url, token, owner, repo, user_agent, hash_file)
updater.update_files()
