import urllib.request
import json
import os
import time

def make_request(url, method="GET", data=None):
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
        
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        
    req = urllib.request.Request(url, headers=headers, method=method, data=body)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 201]:
                return json.loads(response.read().decode())
            elif response.status == 204:
                return True
    except Exception as e:
        print(f"Error on {method} {url}: {e}")
        if hasattr(e, "read"):
            print("Response:", e.read().decode())
    return None

def unlock_badges():
    owner = "allanabtech"
    repo = "allanabtech"
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    print("=== Step 1: Unlocking YOLO and Pull Shark ===")
    
    # 1. Get main branch SHA
    ref_url = f"{base_url}/git/ref/heads/main"
    ref_data = make_request(ref_url)
    if not ref_data:
        print("Failed to get main ref.")
        return
    main_sha = ref_data["object"]["sha"]
    print(f"Main SHA: {main_sha}")
    
    # 2. Create a new branch 'badge-unlock'
    create_ref_url = f"{base_url}/git/refs"
    ref_payload = {
        "ref": "refs/heads/badge-unlock",
        "sha": main_sha
    }
    new_ref = make_request(create_ref_url, method="POST", data=ref_payload)
    if not new_ref:
        print("Failed to create branch or branch already exists.")
    else:
        print("Branch 'badge-unlock' created.")
        
    # 3. Create a dummy file in the branch
    file_url = f"{base_url}/contents/unlock-badge.txt"
    file_payload = {
        "message": "add unlock file",
        "content": "dW5sb2NrX2JhZGdlcw==", # base64 of 'unlock_badges'
        "branch": "badge-unlock"
    }
    file_data = make_request(file_url, method="PUT", data=file_payload)
    if not file_data:
        print("Failed to create file.")
        return
    print("Dummy file created in branch.")
    
    # 4. Create Pull Request
    pr_url = f"{base_url}/pulls"
    pr_payload = {
        "title": "chore: unlock YOLO & Pull Shark badges",
        "head": "badge-unlock",
        "base": "main",
        "body": "This Pull Request is opened and merged programmatically to unlock the YOLO and Pull Shark badges on GitHub."
    }
    pr_data = make_request(pr_url, method="POST", data=pr_payload)
    if not pr_data:
        print("Failed to create Pull Request.")
        return
    pr_number = pr_data["number"]
    print(f"Pull Request #{pr_number} created.")
    
    # 5. Merge Pull Request (instantly unlocks YOLO & Pull Shark!)
    merge_url = f"{base_url}/pulls/{pr_number}/merge"
    merge_payload = {
        "commit_title": "chore: merge badge-unlock branch",
        "merge_method": "merge"
    }
    merge_data = make_request(merge_url, method="PUT", data=merge_payload)
    if merge_data and merge_data.get("merged"):
        print("Pull Request merged successfully! YOLO and Pull Shark unlocked.")
    else:
        print("Failed to merge Pull Request.")
        
    # 6. Delete branch 'badge-unlock'
    delete_ref_url = f"{base_url}/git/refs/heads/badge-unlock"
    make_request(delete_ref_url, method="DELETE")
    print("Branch deleted.")
    
    print("\n=== Step 2: Unlocking Quickdraw ===")
    
    # 1. Create an issue
    issue_url = f"{base_url}/issues"
    issue_payload = {
        "title": "chore: unlock Quickdraw badge",
        "body": "This issue is opened and closed within seconds to unlock the Quickdraw badge on GitHub."
    }
    issue_data = make_request(issue_url, method="POST", data=issue_payload)
    if not issue_data:
        print("Failed to create issue.")
        return
    issue_number = issue_data["number"]
    print(f"Issue #{issue_number} created.")
    
    # 2. Wait 1 second
    time.sleep(1)
    
    # 3. Close the issue (instant Quickdraw unlock!)
    close_issue_url = f"{base_url}/issues/{issue_number}"
    close_payload = {
        "state": "closed",
        "state_reason": "completed"
    }
    closed_data = make_request(close_issue_url, method="PATCH", data=close_payload)
    if closed_data and closed_data.get("state") == "closed":
        print("Issue closed successfully! Quickdraw unlocked.")
    else:
        print("Failed to close issue.")

if __name__ == "__main__":
    unlock_badges()
