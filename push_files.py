#!/usr/bin/env python
import os
import sys
import base64
from pathlib import Path
from dotenv import load_dotenv
import requests

# Clear any existing env vars that might override .env
if 'GITHUB_PAT' in os.environ:
    del os.environ['GITHUB_PAT']
if 'GITHUB_USERNAME' in os.environ:
    del os.environ['GITHUB_USERNAME']
if 'GITHUB_REPO_NAME' in os.environ:
    del os.environ['GITHUB_REPO_NAME']

# Load fresh from .env
load_dotenv(override=True)

token = os.getenv('GITHUB_PAT')
owner = os.getenv('GITHUB_USERNAME')
repo = os.getenv('GITHUB_REPO_NAME')

print(f'Token: {token[:10] if token else "NONE"}...')
print(f'Owner: {owner}')
print(f'Repo: {repo}')
sys.stdout.flush()

if not all([token, owner, repo]):
    print('ERROR: Missing credentials')
    sys.exit(1)

print(f'Pushing to {owner}/{repo}')
sys.stdout.flush()

base_url = f'https://api.github.com/repos/{owner}/{repo}'
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
}

# Test: Get repo info
print('Testing repo access...')
sys.stdout.flush()
resp = requests.get(base_url, headers=headers, timeout=10)
print(f'Repo check: {resp.status_code}')
sys.stdout.flush()

if resp.status_code != 200:
    print(f'Error: {resp.text[:200]}')
    sys.exit(1)

print('Repo accessible! Starting push...')
sys.stdout.flush()

# Collect all files
files_to_push = {}
for file_path in Path('.').rglob('*'):
    if not file_path.is_file():
        continue
    if any(p in str(file_path) for p in ['.git', '__pycache__', '.env']):
        continue
    if file_path.name.startswith('.') and file_path.name != '.gitignore':
        continue
    
    rel_path = str(file_path.relative_to('.')).replace('\\', '/')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            files_to_push[rel_path] = f.read()
    except:
        try:
            with open(file_path, 'rb') as f:
                files_to_push[rel_path] = f.read()
        except:
            pass

print(f'Found {len(files_to_push)} files to push')
sys.stdout.flush()

# Push files
success_count = 0
failed = []

for file_path, content in files_to_push.items():
    url = f'{base_url}/contents/{file_path}'
    
    try:
        # Get existing SHA
        resp = requests.get(url, headers=headers, timeout=10)
        sha = resp.json().get('sha') if resp.status_code == 200 else None
        
        # Prepare content
        if isinstance(content, str):
            encoded = base64.b64encode(content.encode()).decode()
        else:
            encoded = base64.b64encode(content).decode()
        
        data = {
            'message': f'Update {file_path}',
            'content': encoded,
        }
        if sha:
            data['sha'] = sha
        
        # Upload
        resp = requests.put(url, json=data, headers=headers, timeout=30)
        if resp.status_code in [200, 201]:
            print(f'[OK] {file_path}')
            success_count += 1
        else:
            print(f'[FAIL] {file_path} ({resp.status_code}): {resp.text[:100]}')
            failed.append(file_path)
    except Exception as e:
        print(f'[ERROR] {file_path}: {str(e)[:100]}')
        failed.append(file_path)
    
    sys.stdout.flush()

print(f'\nPUSH COMPLETE: {success_count} succeeded, {len(failed)} failed')
if success_count > 0:
    print(f'Repository: https://github.com/{owner}/{repo}')
sys.stdout.flush()
