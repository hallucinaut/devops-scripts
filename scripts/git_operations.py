#!/usr/bin/env python3
"""
Git Operations Script
Handles common git operations and workflows
"""

import argparse
import json
import os
import subprocess
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import yaml


class GitOperations:
    """Git operations manager"""
    
    def __init__(self, repository: Optional[str] = None):
        self.repository = Path(repository) if repository else Path.cwd()
        self._check_git_available()
    
    def _check_git_available(self):
        """Check if git is available"""
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Git is not installed or not accessible", file=sys.stderr)
            sys.exit(1)
    
    def get_current_branch(self) -> str:
        """Get current branch name"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return 'unknown'
    
    def get_commit_hash(self) -> str:
        """Get current commit hash"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()[:7]
        except subprocess.CalledProcessError:
            return 'unknown'
    
    def get_status(self) -> Dict[str, List[str]]:
        """Get git repository status"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, check=True
            )
            
            status = {
                'modified': [],
                'untracked': [],
                'staged': [],
                'deleted': [],
                'renamed': []
            }
            
            for line in result.stdout.splitlines():
                status_code = line[0]
                path = line[3:]
                
                if status_code == 'M':
                    status['modified'].append(path)
                elif status_code == 'A':
                    status['staged'].append(path)
                elif status_code == 'U':
                    status['staged'].append(path)
                elif status_code == 'R':
                    status['renamed'].append(path)
                elif status_code == 'D':
                    status['deleted'].append(path)
                elif status_code == '?':
                    status['untracked'].append(path)
                elif status_code == '!':
                    status['untracked'].append(path)
            
            return status
        except subprocess.CalledProcessError:
            return {'modified': [], 'untracked': [], 'staged': [], 'deleted': [], 'renamed': []}
    
    def commit(self, message: str, amend: bool = False):
        """Create a commit"""
        try:
            if amend:
                subprocess.run(['git', 'commit', '--amend', '-m', message],
                              capture_output=True, check=True)
            else:
                subprocess.run(['git', 'commit', '-m', message],
                              capture_output=True, check=True)
            print("✓ Commit created successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Commit failed: {e}", file=sys.stderr)
            raise
    
    def add_all(self, paths: Optional[List[str]] = None):
        """Stage files for commit"""
        try:
            if paths:
                for path in paths:
                    subprocess.run(['git', 'add', path], capture_output=True, check=True)
            else:
                subprocess.run(['git', 'add', '.'], capture_output=True, check=True)
            print("✓ Files staged")
        except subprocess.CalledProcessError as e:
            print(f"✗ Staging failed: {e}", file=sys.stderr)
            raise
    
    def push(self, branch: Optional[str] = None):
        """Push commits to remote"""
        try:
            branch = branch or self.get_current_branch()
            subprocess.run(['git', 'push', 'origin', branch],
                          capture_output=True, check=True)
            print("✓ Pushed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Push failed: {e}", file=sys.stderr)
            raise
    
    def pull(self, branch: Optional[str] = None):
        """Pull changes from remote"""
        try:
            branch = branch or self.get_current_branch()
            subprocess.run(['git', 'pull', 'origin', branch],
                          capture_output=True, check=True)
            print("✓ Pull successful")
        except subprocess.CalledProcessError as e:
            print(f"✗ Pull failed: {e}", file=sys.stderr)
            raise
    
    def fetch(self):
        """Fetch updates from remote"""
        try:
            subprocess.run(['git', 'fetch'], capture_output=True, check=True)
            print("✓ Fetched successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Fetch failed: {e}", file=sys.stderr)
            raise
    
    def create_branch(self, branch_name: str, start_point: str = 'HEAD'):
        """Create a new branch"""
        try:
            subprocess.run(['git', 'checkout', '-b', branch_name],
                          capture_output=True, check=True)
            print(f"✓ Branch '{branch_name}' created")
        except subprocess.CalledProcessError as e:
            print(f"✗ Branch creation failed: {e}", file=sys.stderr)
            raise
    
    def checkout_branch(self, branch_name: str):
        """Switch to a branch"""
        try:
            subprocess.run(['git', 'checkout', branch_name],
                          capture_output=True, check=True)
            print(f"✓ Switched to branch '{branch_name}'")
        except subprocess.CalledProcessError as e:
            print(f"✗ Checkout failed: {e}", file=sys.stderr)
            raise
    
    def merge_branch(self, branch_name: str, commit_message: Optional[str] = None):
        """Merge a branch into current branch"""
        try:
            subprocess.run(['git', 'merge', branch_name],
                          capture_output=True, check=True)
            if commit_message:
                self.commit(commit_message)
            print(f"✓ Merged branch '{branch_name}'")
        except subprocess.CalledProcessError as e:
            print(f"✗ Merge failed: {e}", file=sys.stderr)
            raise
    
    def get_branches(self) -> List[str]:
        """List all branches"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--format', '%(refname:short)'],
                capture_output=True, text=True, check=True
            )
            return [b.strip() for b in result.stdout.splitlines()]
        except subprocess.CalledProcessError:
            return []
    
    def get_commits(self, branch: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get recent commits"""
        try:
            cmd = ['git', 'log', '-n', str(limit), '--pretty=format:%H|%an|%ad|%s']
            if branch:
                cmd.append(branch)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            commits = []
            for line in result.stdout.splitlines():
                hash_, author, date, message = line.split('|')
                commits.append({
                    'hash': hash_,
                    'author': author,
                    'date': date,
                    'message': message
                })
            
            return commits
        except subprocess.CalledProcessError:
            return []
    
    def get_remote(self, name: str = 'origin') -> Optional[str]:
        """Get remote URL"""
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', name],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def checkout_file(self, file_path: str):
        """Checkout a specific file from index"""
        try:
            subprocess.run(['git', 'checkout', '--', file_path],
                          capture_output=True, check=True)
            print(f"✓ File '{file_path}' checked out")
        except subprocess.CalledProcessError as e:
            print(f"✗ Checkout failed: {e}", file=sys.stderr)
            raise
    
    def reset(self, mode: str = 'soft', commit: Optional[str] = None):
        """Reset repository state"""
        try:
            if commit:
                cmd = ['git', 'reset', '--' + mode, commit]
            else:
                cmd = ['git', 'reset', '--' + mode]
            
            subprocess.run(cmd, capture_output=True, check=True)
            print(f"✓ Reset to {mode} state")
        except subprocess.CalledProcessError as e:
            print(f"✗ Reset failed: {e}", file=sys.stderr)
            raise
    
    def create_tag(self, tag_name: str, message: Optional[str] = None):
        """Create a git tag"""
        try:
            cmd = ['git', 'tag', '-a', tag_name, '-m', message] if message else ['git', 'tag', tag_name]
            subprocess.run(cmd, capture_output=True, check=True)
            print(f"✓ Tag '{tag_name}' created")
        except subprocess.CalledProcessError as e:
            print(f"✗ Tag creation failed: {e}", file=sys.stderr)
            raise
    
    def get_tags(self) -> List[str]:
        """List all tags"""
        try:
            result = subprocess.run(
                ['git', 'tag', '--format', '%(refname:short)'],
                capture_output=True, text=True, check=True
            )
            return [t.strip() for t in result.stdout.splitlines()]
        except subprocess.CalledProcessError:
            return []
    
    def get_diff(self, commit: Optional[str] = None, file: Optional[str] = None) -> str:
        """Get diff of changes"""
        try:
            cmd = ['git', 'diff']
            if commit:
                cmd.append(commit)
            if file:
                cmd.append(file)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description='Git Operations Script')
    parser.add_argument('--repo', help='Repository path')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # commit subcommand
    commit_parser = subparsers.add_parser('commit', help='Create a commit')
    commit_parser.add_argument('--message', required=True, help='Commit message')
    commit_parser.add_argument('--amend', action='store_true', help='Amend last commit')
    
    # add subcommand
    add_parser = subparsers.add_parser('add', help='Stage files')
    add_parser.add_argument('--all', action='store_true', help='Stage all changes')
    add_parser.add_argument('files', nargs='*', help='Files to stage')
    
    # push subcommand
    push_parser = subparsers.add_parser('push', help='Push to remote')
    push_parser.add_argument('--branch', help='Branch name')
    
    # pull subcommand
    pull_parser = subparsers.add_parser('pull', help='Pull from remote')
    pull_parser.add_argument('--branch', help='Branch name')
    
    # fetch subcommand
    fetch_parser = subparsers.add_parser('fetch', help='Fetch from remote')
    
    # branch subcommand
    branch_parser = subparsers.add_parser('branch', help='Branch management')
    branch_parser.add_argument('name', help='Branch name')
    branch_parser.add_argument('--start-point', default='HEAD', help='Start point')
    
    # checkout subcommand
    checkout_parser = subparsers.add_parser('checkout', help='Checkout branch')
    checkout_parser.add_argument('branch', help='Branch name')
    checkout_parser.add_argument('--file', help='File to checkout from index')
    
    # merge subcommand
    merge_parser = subparsers.add_parser('merge', help='Merge branch')
    merge_parser.add_argument('branch', help='Branch to merge')
    merge_parser.add_argument('--message', help='Commit message')
    
    # status subcommand
    status_parser = subparsers.add_parser('status', help='Show repository status')
    
    # log subcommand
    log_parser = subparsers.add_parser('log', help='Show commit log')
    log_parser.add_argument('--branch', help='Branch name')
    log_parser.add_argument('--limit', type=int, default=10, help='Number of commits')
    
    # reset subcommand
    reset_parser = subparsers.add_parser('reset', help='Reset repository')
    reset_parser.add_argument('--mode', choices=['soft', 'mixed', 'hard'], default='mixed')
    reset_parser.add_argument('--commit', help='Commit hash')
    
    # tag subcommand
    tag_parser = subparsers.add_parser('tag', help='Create tag')
    tag_parser.add_argument('name', help='Tag name')
    tag_parser.add_argument('--message', help='Tag message')
    
    # diff subcommand
    diff_parser = subparsers.add_parser('diff', help='Show diff')
    diff_parser.add_argument('--commit', help='Commit hash')
    diff_parser.add_argument('--file', help='File to diff')
    
    args = parser.parse_args()
    
    git = GitOperations(args.repo)
    
    if args.command == 'commit':
        git.commit(args.message, args.amend)
    elif args.command == 'add':
        if args.all:
            git.add_all()
        elif args.files:
            git.add_all(args.files)
    elif args.command == 'push':
        git.push(args.branch)
    elif args.command == 'pull':
        git.pull(args.branch)
    elif args.command == 'fetch':
        git.fetch()
    elif args.command == 'branch':
        git.create_branch(args.name, args.start_point)
    elif args.command == 'checkout':
        if args.file:
            git.checkout_file(args.file)
        else:
            git.checkout_branch(args.branch)
    elif args.command == 'merge':
        git.merge_branch(args.branch, args.message)
    elif args.command == 'status':
        status = git.get_status()
        print(f"\nBranch: {git.get_current_branch()}")
        print(f"Commit: {git.get_commit_hash()}\n")
        print(f"Modified: {len(status['modified'])}")
        print(f"Staged: {len(status['staged'])}")
        print(f"Untracked: {len(status['untracked'])}")
        print(f"Deleted: {len(status['deleted'])}")
    elif args.command == 'log':
        commits = git.get_commits(args.branch, args.limit)
        print(f"\nRecent commits ({len(commits)}):\n")
        for commit in commits:
            print(f"  [{commit['hash']}] {commit['message']}")
            print(f"    Author: {commit['author']}")
            print(f"    Date: {commit['date']}")
            print()
    elif args.command == 'reset':
        git.reset(args.mode, args.commit)
    elif args.command == 'tag':
        git.create_tag(args.name, args.message)
    elif args.command == 'diff':
        diff = git.get_diff(args.commit, args.file)
        print(diff)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
