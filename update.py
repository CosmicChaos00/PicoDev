import urequests
import uos

def get_remote_version():
    response = urequests.get("https://github.com/CosmicChaos00/PicoDev/tree/main/version")
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

def get_local_version():
    try:
        with open("version.txt", "r") as file:
            return file.read().strip()
    except OSError:
        return None

def download_file(url, path):
    response = urequests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download {path}")

def update_system():
    remote_version = get_remote_version()
    if remote_version is None:
        print("Failed to fetch remote version.")
        return

    local_version = get_local_version()
    if local_version != remote_version:
        print("New version found. Updating...")
        # Add all the file URLs you need to update
        files_to_update = [
            ("https://raw.githubusercontent.com/yourusername/yourrepo/master/main.py", "main.py"),
            # Add more files as needed
        ]
        for file_url, file_path in files_to_update:
            download_file(file_url, file_path)
        # Update local version.txt file
        with open("version.txt", "w") as file:
            file.write(remote_version)
        print("Update complete.")
    else:
        print("System is up to date.")

# Run the update check
update_system()
