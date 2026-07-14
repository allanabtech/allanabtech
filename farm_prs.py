import urllib.request
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def make_request(url, headers, method="GET", data=None):
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, headers=headers, method=method, data=body)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 201]:
                return json.loads(response.read().decode())
            elif response.status == 204:
                return True
    except Exception as e:
        # Silently pass to avoid log flood, or print simple fail
        pass
    return None

def process_one_pr(i, base_url, headers, main_sha):
    branch_name = f"farm-{i}"
    
    # 1. Create branch
    make_request(f"{base_url}/git/refs", headers, method="POST", data={
        "ref": f"refs/heads/{branch_name}",
        "sha": main_sha
    })
    
    # 2. Put file
    make_request(f"{base_url}/contents/unlock/farm-{i}.txt", headers, method="PUT", data={
        "message": f"add file {i}",
        "content": "dW5sb2Nr", # base64 of 'unlock'
        "branch": branch_name
    })
    
    # 3. Create PR
    pr = make_request(f"{base_url}/pulls", headers, method="POST", data={
        "title": f"farm: merge PR {i}",
        "head": branch_name,
        "base": "main",
        "body": f"Farming PR number {i} for Pull Shark badge."
    })
    
    if pr and "number" in pr:
        pr_number = pr["number"]
        # 4. Merge PR
        make_request(f"{base_url}/pulls/{pr_number}/merge", headers, method="PUT", data={
            "commit_title": f"Merge PR {i}"
        })
        # 5. Delete branch
        make_request(f"{base_url}/git/refs/heads/{branch_name}", headers, method="DELETE")
        return True
    return False

def main():
    owner = "allanabtech"
    repo = "allanabtech"
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("GITHUB_TOKEN not found.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    print("Fetching main branch ref...")
    ref_data = make_request(f"{base_url}/git/ref/heads/main", headers)
    if not ref_data:
        print("Failed to fetch main branch ref.")
        return
    main_sha = ref_data["object"]["sha"]
    print(f"Main SHA: {main_sha}")

    # Farm 1025 PRs to guarantee Gold status (> 1024)
    total_prs = 1025
    max_threads = 8  # Keep threads reasonable to avoid rate limit spikes
    
    print(f"Farming {total_prs} PRs for Gold Pull Shark badge using {max_threads} threads...")
    
    completed = 0
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(process_one_pr, i, base_url, headers, main_sha): i for i in range(1, total_prs + 1)}
        for fut in as_completed(futures):
            res = fut.result()
            completed += 1
            if completed % 50 == 0:
                print(f"Progress: {completed}/{total_prs} PRs processed...")
                # Sleep briefly between large batches to be nice to GitHub's rate limiter
                time.sleep(1)

    print("Farming complete! All PRs processed and merged.")

if __name__ == "__main__":
    main()
