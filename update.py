import urequests
import wifi
import constantData 
class Updater:
    def __init__(self, base_url, version_file_path, local_version_path):
        self.base_url = base_url.rstrip('/') + '/'
        self.version_file_path = version_file_path
        self.local_version_path = local_version_path

    def download_text(self, url):
        response = urequests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to download file:", url)
            return None

    def parse_version_data(self, version_content):
        lines = version_content.strip().split('\n')
        version_number = lines[0].strip()
        files = lines[1:]  # Assume the first line is the version number and rest are files
        return version_number, files

    def read_local_version(self):
        try:
            with open(self.local_version_path, 'r') as file:
                return file.read().strip()
        except OSError:
            return None

    def write_local_version(self, version_content):
        with open(self.local_version_path, 'w') as file:
            file.write(version_content)

    def update_files(self, file_list):
        for file_name in file_list:
            url = f"{self.base_url}{file_name.strip()}"
            file_content = self.download_text(url)
            if file_content:
                with open(file_name.strip(), 'w') as file:
                    file.write(file_content)
                print(f"Updated {file_name.strip()}")

    def check_for_updates(self):
        remote_version_content = self.download_text(f"{self.base_url}{self.version_file_path}")
        if remote_version_content is None:
            print("Failed to fetch remote version data.")
            return

        remote_version, remote_files = self.parse_version_data(remote_version_content)
        local_version = self.read_local_version()

        if local_version != remote_version:
            print(f"New version {remote_version} found. Starting update...")
            self.update_files(remote_files)
            self.write_local_version(remote_version_content)
            print("System update complete.")
        else:
            print("System is up to date.")

# Usage example
wifi.wifi_Login()
BASE_URL= constantData.getHubURL()
version_file_path = constantData.getVersionPath()
local_version_path = constantData.getLocalVersion_path()

updater = Updater(BASE_URL, version_file_path, local_version_path)
updater.check_for_updates()
