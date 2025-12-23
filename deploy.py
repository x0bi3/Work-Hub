#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Work-Hub GitHub Deployer
Uploads files to GitHub using REST API (no Git CLI required)
Reads credentials from .env file
"""

import sys
import os
import base64

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    from dotenv import load_dotenv
except ImportError:
    print("Installing python-dotenv...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

# Load .env file
load_dotenv()


class GitHubDeployer:
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_file_sha(self, file_path):
        """Get SHA of existing file."""
        url = f"{self.base_url}/contents/{file_path}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["sha"]
        return None

    def upload_file(self, file_path, file_content):
        """Upload file to GitHub."""
        url = f"{self.base_url}/contents/{file_path}"
        encoded_content = base64.b64encode(file_content.encode()).decode()
        
        sha = self.get_file_sha(file_path)
        
        data = {
            "message": f"Update {file_path}",
            "content": encoded_content,
        }
        
        if sha:
            data["sha"] = sha
        
        response = requests.put(url, json=data, headers=self.headers)
        return response.status_code in [200, 201]

    def deploy(self, files_to_upload):
        """Deploy all files."""
        print("\nUploading files to GitHub...")
        
        for file_path, file_content in files_to_upload:
            if self.upload_file(file_path, file_content):
                print(f"  [OK] {file_path}")
            else:
                print(f"  [FAIL] {file_path}")
                return False
        
        return True


def main():
    print("\n" + "="*60)
    print("WORK-HUB GITHUB DEPLOYMENT")
    print("="*60)
    
    # Get credentials from .env
    token = os.getenv("GITHUB_PAT")
    owner = os.getenv("GITHUB_USERNAME")
    repo = os.getenv("GITHUB_REPO_NAME")
    
    # Validate credentials
    if not token:
        print("\nGitHub PAT not found in .env")
        print("Create a .env file with GITHUB_PAT, GITHUB_USERNAME, and GITHUB_REPO_NAME")
        print("See .env.example for the format\n")
        return 1
    if not owner:
        print("Error: GITHUB_USERNAME not set in .env")
        return 1
    if not repo:
        print("Error: GITHUB_REPO_NAME not set in .env")
        return 1
    
    print(f"\nUsing credentials from .env:")
    print(f"  Username: {owner}")
    print(f"  Repo: {repo}")
    
    # Prepare files to upload dynamically
    project_root = os.getcwd()  # Root folder to upload
    files_to_upload = []

    for root, dirs, filenames in os.walk(project_root):
        for filename in filenames:
            # Skip hidden files except .gitignore
            if filename.startswith(".") and filename != ".gitignore":
                continue
            
            local_path = os.path.join(root, filename)
            # Preserve folder structure in GitHub
            relative_path = os.path.relpath(local_path, project_root).replace("\\", "/")
            
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    content = f.read()
                files_to_upload.append((relative_path, content))
            except Exception as e:
                print(f"Error reading {local_path}: {e}")

    if not files_to_upload:
        print("\nNo files to upload!")
        return 1
    
    # Deploy
    deployer = GitHubDeployer(token, owner, repo)
    
    print(f"\nDeploying to: https://github.com/{owner}/{repo}")
    
    if deployer.deploy(files_to_upload):
        print("\n" + "="*60)
        print("SUCCESS! Files uploaded to GitHub!")
        print("="*60)
        print(f"\nYour site: https://{owner}.github.io/{repo}/")
        print(f"\nRepo: https://github.com/{owner}/{repo}\n")
        return 0
    else:
        print("\nDeployment failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
