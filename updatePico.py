import urequests

# Base GitHub URL for raw file content
base_github_url = 'https://raw.githubusercontent.com/CosmicChaos00/PicoDev/main/'

def update(filename):
    # Construct the full URL for the file
    github_devURL = base_github_url + filename
    try:
        # Send an HTTP GET request
        response = urequests.get(github_devURL, stream=True)
        
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Open the local file in write-binary mode
            with open(filename, 'wb') as f:
                # Assuming iter_content is supported; otherwise, use response.content directly
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Successfully updated {filename}.")
        else:
            print(f"Failed to download {filename}, HTTP status code: {response.status_code}")
        
        response.close()
    except Exception as e:
        print(f"Error updating {filename}: {e}")

def update_from_list(file_list='files_to_update.txt'):
    with open(file_list, 'r') as file:
        for line in file:
            filename = line.strip()  # Remove newline characters and extra spaces
            update(filename)

# Replace 'files_to_update.txt' with the path to your actual list of files, if necessary
update_from_list('files_to_update.txt')
