import os
import sys
import argparse
import requests
from github import Github

# GitHub API端点
API_URL = "https://api.github.com"

# 源仓库和目标仓库信息 
SOURCE_REPO = "zhangwt-cn/notes"
TARGET_REPO = "zhangwt-cn/blog"
TARGET_DIR = "src/content/post"

# GitHub访问令牌
ACCESS_TOKEN = os.environ["GITHUB_TOKEN"]

def get_issues(repo):
    """获取指定仓库的所有issues"""
    url = f"{API_URL}/repos/{repo}/issues?state=all"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"获取issues失败: {err}")
        sys.exit(1)

def get_issue(repo, issue_number):
    """获取指定仓库的单个issue"""
    url = f"{API_URL}/repos/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"获取issue失败: {err}")
        sys.exit(1)

def create_file(repo, path, content, message):
    """在指定仓库创建或更新文件"""
    g = Github(ACCESS_TOKEN)
    r = g.get_repo(repo)
    
    try:
        contents = r.get_contents(path)
        r.update_file(path, message, content, contents.sha)
        print(f"更新文件成功: {path}")
    except:
        r.create_file(path, message, content)
        print(f"创建文件成功: {path}")

def delete_file(repo, path, message):
    """在指定仓库删除文件"""  
    g = Github(ACCESS_TOKEN)
    r = g.get_repo(repo)
    
    contents = r.get_contents(path)
    r.delete_file(path, message, contents.sha)
    print(f"删除文件成功: {path}")

def sync_issue(issue_number, action):
    """同步单个issue到目标仓库"""
    issue = get_issue(SOURCE_REPO, issue_number)
    
    # 生成front matter
    front_matter = f"""---
title: "{issue['title']}"  
description: "{issue['title']}"
publishDate: "{issue['created_at'][:10]}"
tags: {[label['name'] for label in issue['labels']]}
---

"""
    
    # 将issue转换为Markdown格式,并添加front matter
    content = f"{front_matter} \n{issue['body']}"
    
    # 生成目标文件路径 
    filename = f"issue-{issue['number']}.md"
    filepath = os.path.join(TARGET_DIR, filename)
    
    # 根据action参数执行相应操作
    if action == 'create':
        message = f"Create issue #{issue['number']} from {SOURCE_REPO}"
        create_file(TARGET_REPO, filepath, content, message)
    elif action == 'update':
        message = f"Update issue #{issue['number']} from {SOURCE_REPO}"
        create_file(TARGET_REPO, filepath, content, message)
    elif action == 'delete':
        message = f"Delete issue #{issue['number']} from {SOURCE_REPO}"
        delete_file(TARGET_REPO, filepath, message)
    else:
        print(f"无效的操作: {action}")
        sys.exit(1)

def sync_all_issues():
    """同步所有issues到目标仓库"""  
    source_issues = get_issues(SOURCE_REPO)
    
    for issue in source_issues:
        # 生成front matter
        front_matter = f"""---
title: "{issue['title']}"
description: "{issue['body'][:100]}..."  
publishDate: "{issue['created_at'][:10]}"
tags: {[label['name'] for label in issue['labels']]}
---

"""
        
        # 将issue转换为Markdown格式,并添加front matter
        content = f"{front_matter}# {issue['title']}\n\n{issue['body']}"
        
        # 生成目标文件路径
        filename = f"issue-{issue['number']}.md"
        filepath = os.path.join(TARGET_DIR, filename)
        
        # 在目标仓库创建或更新文件  
        message = f"Sync issue #{issue['number']} from {SOURCE_REPO}"
        create_file(TARGET_REPO, filepath, content, message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='同步GitHub仓库的issues到另一个仓库')
    parser.add_argument('--all', action='store_true', help='同步所有issues')
    parser.add_argument('--issue', type=int, help='要同步的issue编号')
    parser.add_argument('--action', choices=['create', 'update', 'delete'], help='要执行的操作')
    
    args = parser.parse_args()
    
    if args.all:
        sync_all_issues()
    elif args.issue and args.action:
        sync_issue(args.issue, args.action)
    else:
        parser.print_help()