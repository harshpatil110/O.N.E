import os
from github import Github
from langchain_core.tools import tool

# Initialize Github Client
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_TARGET_REPO = os.getenv("GITHUB_TARGET_REPO", "harshpatil110/O.N.E") # Fallback repo if not set in .env
github_client = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()

@tool("get_open_pull_requests")
def get_open_pull_requests() -> str:
    """Use this tool to fetch the latest open pull requests (PRs) from the company GitHub repository."""
    try:
        repo = github_client.get_repo(GITHUB_TARGET_REPO)
        pulls = repo.get_pulls(state='open', sort='created', direction='desc')
        pr_list = list(pulls[:5])
        if not pr_list:
            return "There are currently no open pull requests."
        
        result = "Top 5 Open Pull Requests:\n"
        for pr in pr_list:
            result += f"- [PR #{pr.number}] {pr.title} (by @{pr.user.login})\n"
        return result
    except Exception as e:
        return f"Error fetching pull requests: {str(e)}"

@tool("get_recent_commits")
def get_recent_commits() -> str:
    """Use this tool to fetch the most recent commits to the main branch of the company GitHub repository."""
    try:
        repo = github_client.get_repo(GITHUB_TARGET_REPO)
        commits = repo.get_commits()
        commit_list = list(commits[:5])
        if not commit_list:
            return "No recent commits found."
        
        result = "Top 5 Recent Commits:\n"
        for commit in commit_list:
            author = commit.author.login if commit.author else commit.commit.author.name
            result += f"- [{commit.sha[:7]}] {commit.commit.message.splitlines()[0]} (by @{author})\n"
        return result
    except Exception as e:
        return f"Error fetching commits: {str(e)}"

@tool("get_repository_issues")
def get_repository_issues() -> str:
    """Use this tool to fetch open issues from the GitHub repository. Helpful when a developer asks what bugs they can work on."""
    try:
        repo = github_client.get_repo(GITHUB_TARGET_REPO)
        issues = repo.get_issues(state='open', sort='created', direction='desc')
        # Filter out pull requests which are also considered issues by GitHub API
        issue_list = []
        for issue in issues:
            if not issue.pull_request:
                issue_list.append(issue)
            if len(issue_list) >= 5:
                break
        
        if not issue_list:
            return "There are currently no open issues."
        
        result = "Top 5 Open Issues:\n"
        for issue in issue_list:
            labels = ", ".join([label.name for label in issue.labels])
            label_str = f" [Labels: {labels}]" if labels else ""
            result += f"- [Issue #{issue.number}] {issue.title}{label_str}\n"
        return result
    except Exception as e:
        return f"Error fetching issues: {str(e)}"
