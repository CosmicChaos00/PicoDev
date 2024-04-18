from constantData import Constant
import urequests
import wifi
import machine
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
        version_number = lines[0].strip()  # Version number is expected to be on the first line
        files = lines[1:]  # Remaining lines are expected to be file names
        return version_number, files

    def read_local_version(self):
        try:
            with open(self.local_version_path, 'r') as file:
                # Only read the first line which should contain the version number
                local_version = file.readline().strip()
                print(f"Read local version: {local_version}")
                return local_version
        except OSError:
            print("Failed to read local version file.")
            return None

    def write_local_version(self, version_number):
        with open(self.local_version_path, 'w') as file:
            file.write(version_number)
        print(f"Wrote local version: {version_number}")

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

        print(f"Comparing local version '{local_version}' with remote version '{remote_version}'")
        if local_version != remote_version:
            print(f"New version {remote_version} found. Starting update...")
            self.update_files(remote_files)
            self.write_local_version(remote_version)
            print("System update complete.")
            print("restarting pico ...")
            machine.reset()
        else:
            print("System is up to date.")

