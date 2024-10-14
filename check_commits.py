import requests
import os
import sys

# GitHub repository details
repoowner = "ralphfelix26"
reponame = "my-website"
GITHUB_API_URL = f"https://api.github.com/repos/{repoowner}/{reponame}/commits"

# File to store the last commit SHA
LAST_COMMIT_FILE = '/var/www/html/my-html-project/my-website/last_commit.txt'

def get_latest_commit():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        commits = response.json()
        return commits[0]['sha']
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        return None

def get_stored_commit():
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as f:
            return f.read().strip()
    return None

def update_stored_commit(sha):
    os.makedirs(os.path.dirname(LAST_COMMIT_FILE), exist_ok=True)  # Ensure the directory exists
    with open(LAST_COMMIT_FILE, 'w') as f:
        f.write(sha)

if __name__ == "__main__":
    latest_commit = get_latest_commit()
    if latest_commit:
        stored_commit = get_stored_commit()
        if latest_commit != stored_commit:
            print("New commit detected")
            update_stored_commit(latest_commit)
            # Add deployment script execution here if needed
        else:
            print("No new commit")