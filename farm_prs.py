import urllib.request
import json
import os
import time

def make_request(url, headers, method="GET", data=None):
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, headers=headers, method=method, data=body)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status in [200, 201]:
                    return json.loads(response.read().decode())
                elif response.status == 204:
                    return True
        except Exception as e:
            if attempt == 2:
                print(f"Request failed: {url} - {e}")
            time.sleep(2)
    return None

def process_one_pr(i, base_url, headers, main_sha):
    branch_name = f"farm-{i}"
    
    # 1. Create branch
    ref = make_request(f"{base_url}/git/refs", headers, method="POST", data={
        "ref": f"refs/heads/{branch_name}",
        "sha": main_sha
    })
    if not ref:
        return False
        
    # 2. Put file
    file_res = make_request(f"{base_url}/contents/unlock/farm-{i}.txt", headers, method="PUT", data={
        "message": f"add file {i}",
        "content": "dW5sb2Nr", # base64 of 'unlock'
        "branch": branch_name
    })
    if not file_res:
        # Cleanup branch if file create fails
        make_request(f"{base_url}/git/refs/heads/{branch_name}", headers, method="DELETE")
        return False
        
    # 3. Create PR
    pr = make_request(f"{base_url}/pulls", headers, method="POST", data={
        "title": f"farm: merge PR {i}",
        "head": branch_name,
        "base": "main",
        "body": f"Farming PR number {i} for Pull Shark badge."
    })
    
    if pr and "number" in pr:
        pr_number = pr["number"]
        # 4. Merge PR with retry logic
        merged = False
        for attempt in range(5):
            res = make_request(f"{base_url}/pulls/{pr_number}/merge", headers, method="PUT", data={
                "commit_title": f"Merge PR {i}"
            })
            if res:
                merged = True
                break
            time.sleep(2)
            
        # 5. Delete branch
        make_request(f"{base_url}/git/refs/heads/{branch_name}", headers, method="DELETE")
        return merged
        
    # Cleanup branch if PR create failed
    make_request(f"{base_url}/git/refs/heads/{branch_name}", headers, method="DELETE")
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

    print("Checking current merged PR count...")
    search_url = "https://api.github.com/search/issues?q=repo:allanabtech/allanabtech+is:pr+is:merged"
    search_data = make_request(search_url, headers)
    current_merged = 0
    if search_data and "total_count" in search_data:
        current_merged = search_data["total_count"]
    print(f"Current merged PR count: {current_merged}")

    target = 1030
    needed = target - current_merged
    if needed <= 0:
        print("Gold tier already reached!")
        return

    print(f"Need to merge {needed} more PRs to reach target of {target}.")

    print("Fetching main branch ref...")
    ref_data = make_request(f"{base_url}/git/ref/heads/main", headers)
    if not ref_data:
        print("Failed to fetch main branch ref.")
        return
    main_sha = ref_data["object"]["sha"]
    print(f"Main SHA: {main_sha}")
    
    # Process sequentially to avoid lock contention on base branch updates
    completed = 0
    success_count = 0
    start_num = current_merged + 1
    
    for i in range(start_num, start_num + needed):
        print(f"Farming PR {i}...")
        success = process_one_pr(i, base_url, headers, main_sha)
        completed += 1
        if success:
            success_count += 1
        
        # Print progress every 10 PRs
        if completed % 10 == 0:
            print(f"Progress: {completed}/{needed} processed. Success: {success_count}/{completed}")
            # Refresh main_sha to point to the latest commit to avoid conflicts
            ref_data = make_request(f"{base_url}/git/ref/heads/main", headers)
            if ref_data:
                main_sha = ref_data["object"]["sha"]
        
        # Tiny sleep between PRs to be safe
        time.sleep(1)

    print(f"Farming complete! Successfully merged {success_count} PRs out of {needed} attempted.")

if __name__ == "__main__":
    main()
