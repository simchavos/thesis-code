import os

from dotenv import load_dotenv

from src.python.results.Graphs import send_request

def check_repo(repo, headers):
    # Get the contents of the root directory of the repository
    url = f"https://api.github.com/repos/{repo}/contents/"
    response = send_request(url, headers)

    if response.status_code != 200:
        print(f"Failed to get repository contents: {response.status_code}")
        return False

    contents = response.json()

    # Look for .sh files in the top-level directory
    for item in contents:
        if item['type'] == 'file' and item['name'].endswith('.sh'):
            return True
    return False

def has_shell_scripts():
    python_repos = open(os.path.join("../data/python_sampled_repos.txt"), 'r')
    java_repos = open(os.path.join("../data/java_sampled_repos.txt"), 'r')
    repos = python_repos.readlines() + java_repos.readlines()

    load_dotenv()
    github_token = os.getenv("GITHUB_ISSUE_TOKEN")
    headers = {
        "Authorization": f"token {github_token}",
    }
    count = 0
    for repo in repos:
        if check_repo(repo.strip(), headers): count += 1

    return count

print(has_shell_scripts())
