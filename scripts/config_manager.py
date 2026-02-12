#!/usr/bin/env python3
"""
Configuration Management Script
Manages configuration files and environment variables
"""

import argparse
import configparser
import json
import os
import subprocess
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import hashlib


class ConfigManager:
    """Configuration file manager"""
    
    def __init__(self, project_dir: str = '.'):
        self.project_dir = Path(project_dir)
        self.backup_dir = self.project_dir / '.config_backups'
        self.backup_dir.mkdir(exist_ok=True)
    
    def backup_file(self, file_path: str, compression: bool = True) -> Optional[str]:
        """Backup a configuration file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"{file_path.name}_{timestamp}"
        
        try:
            if compression:
                with open(file_path, 'rb') as f:
                    with tarfile.open(backup_path.with_suffix('.tar.gz'), 'w:gz') as tar:
                        tar.add(file_path, arcname=file_path.name)
                file_path.unlink()
            else:
                backup_path.write_text(file_path.read_text())
            
            print(f"✓ Backed up to: {backup_path}")
            return str(backup_path)
        except Exception as e:
            print(f"✗ Backup failed: {e}", file=sys.stderr)
            return None
    
    def restore_file(self, backup_path: str, file_path: Optional[str] = None) -> bool:
        """Restore a backed up configuration file"""
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            print(f"Backup not found: {backup_path}")
            return False
        
        if file_path is None:
            file_path = self.project_dir / backup_path.stem.replace(f'_{backup_path.suffix}', '')
        
        try:
            if backup_path.suffix == '.tar.gz':
                with tarfile.open(backup_path, 'r:gz') as tar:
                    tar.extractall(path=backup_path.parent)
            else:
                file_path.write_text(backup_path.read_text())
            
            print(f"✓ Restored from: {backup_path}")
            return True
        except Exception as e:
            print(f"✗ Restore failed: {e}", file=sys.stderr)
            return False
    
    def backup_all(self, patterns: Optional[List[str]] = None):
        """Backup all configuration files"""
        if patterns is None:
            patterns = ['.env', '.env.local', '.env.development', '.env.production',
                       'config.yaml', 'config.yml', 'settings.json', 'settings.ini']
        
        print("Backing up configuration files...")
        
        for pattern in patterns:
            for file in self.project_dir.glob(pattern):
                self.backup_file(str(file))
    
    def update_env_var(self, key: str, value: str, file: str = '.env', append: bool = False):
        """Update environment variable in .env file"""
        env_file = self.project_dir / file
        
        if not env_file.exists():
            env_file.touch()
        
        try:
            with open(env_file, 'r+') as f:
                lines = f.readlines()
                found = False
                
                for line in lines:
                    if line.strip().startswith(f'{key}='):
                        lines[lines.index(line)] = f'{key}={value}\n'
                        found = True
                        break
                
                if not found or append:
                    lines.append(f'{key}={value}\n')
                
                f.seek(0)
                f.writelines(lines)
            
            print(f"✓ Updated {file}: {key}={value}")
            return True
        except Exception as e:
            print(f"✗ Update failed: {e}", file=sys.stderr)
            return False
    
    def get_env_var(self, key: str, file: str = '.env', default: Optional[str] = None) -> Optional[str]:
        """Get environment variable from .env file"""
        env_file = self.project_dir / file
        
        if not env_file.exists():
            return default
        
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip().startswith(f'{key}='):
                        return line.strip().split('=', 1)[1]
            return default
        except Exception:
            return default
    
    def validate_config(self, file_path: str, config_type: str = 'json'):
        """Validate configuration file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"Configuration file not found: {file_path}")
            return False
        
        try:
            if config_type == 'json':
                json.loads(file_path.read_text())
                print(f"✓ JSON configuration is valid")
                return True
            elif config_type == 'yaml':
                yaml.safe_load(file_path.read_text())
                print(f"✓ YAML configuration is valid")
                return True
            elif config_type == 'ini':
                configparser.ConfigParser().read(file_path)
                print(f"✓ INI configuration is valid")
                return True
            else:
                print(f"✗ Unknown config type: {config_type}")
                return False
        except Exception as e:
            print(f"✗ Validation failed: {e}", file=sys.stderr)
            return False
    
    def diff_config(self, file1: str, file2: str):
        """Show differences between two config files"""
        file1 = Path(file1)
        file2 = Path(file2)
        
        if not file1.exists() or not file2.exists():
            print("One or both files not found")
            return
        
        try:
            result = subprocess.run(
                ['diff', '-u', str(file1), str(file2)],
                capture_output=True, text=True
            )
            print(result.stdout)
        except Exception as e:
            print(f"✗ Diff failed: {e}", file=sys.stderr)
    
    def get_config_value(self, file_path: str, key: str, separator: str = '=') -> Optional[str]:
        """Get value from config file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if key in line and separator in line:
                        return line.split(separator, 1)[1].strip()
            return None
        except Exception:
            return None
    
    def set_config_value(self, file_path: str, key: str, value: str,
                         separator: str = '=', append: bool = False):
        """Set value in config file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            file_path.touch()
        
        try:
            with open(file_path, 'r+') as f:
                content = f.read()
                lines = content.split('\n')
                
                key_found = False
                for i, line in enumerate(lines):
                    if key in line and separator in line:
                        lines[i] = f'{key}{separator}{value}'
                        key_found = True
                        break
                
                if not key_found or append:
                    lines.append(f'{key}{separator}{value}')
                
                f.seek(0)
                f.write('\n'.join(lines))
                f.truncate()
            
            print(f"✓ Set {key}={value} in {file_path}")
            return True
        except Exception as e:
            print(f"✗ Set failed: {e}", file=sys.stderr)
            return False
    
    def list_configs(self, patterns: Optional[List[str]] = None) -> List[Path]:
        """List configuration files"""
        if patterns is None:
            patterns = ['.env*', 'config.*', 'settings.*']
        
        configs = []
        for pattern in patterns:
            configs.extend(self.project_dir.glob(pattern))
        
        configs.sort()
        return configs
    
    def get_file_hash(self, file_path: str) -> Optional[str]:
        """Get hash of configuration file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None
        
        try:
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                sha256.update(f.read())
            return sha256.hexdigest()
        except Exception:
            return None
    
    def search_config(self, file_path: str, pattern: str, case_sensitive: bool = False):
        """Search for pattern in config file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return
        
        try:
            with open(file_path, 'r') as f:
                for i, line in enumerate(f, 1):
                    if case_sensitive:
                        if pattern in line:
                            print(f"Line {i}: {line.strip()}")
                    else:
                        if pattern.lower() in line.lower():
                            print(f"Line {i}: {line.strip()}")
        except Exception as e:
            print(f"✗ Search failed: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Configuration Management Script')
    parser.add_argument('--project', default='.', help='Project directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # backup subcommand
    backup_parser = subparsers.add_parser('backup', help='Backup configuration file')
    backup_parser.add_argument('--file', required=True, help='File to backup')
    backup_parser.add_argument('--all', action='store_true', help='Backup all configs')
    backup_parser.add_argument('--compression', action='store_true', default=True,
                              help='Enable compression')
    
    # restore subcommand
    restore_parser = subparsers.add_parser('restore', help='Restore backed up file')
    restore_parser.add_argument('--file', required=True, help='Backup file to restore')
    restore_parser.add_argument('--output', help='Output file path')
    
    # env subcommand
    env_parser = subparsers.add_parser('env', help='Environment variable management')
    env_sub = env_parser.add_subparsers(dest='env_command', help='Env command')
    
    env_set = env_sub.add_parser('set', help='Set environment variable')
    env_set.add_argument('--key', required=True, help='Key')
    env_set.add_argument('--value', required=True, help='Value')
    env_set.add_argument('--file', default='.env', help='Env file')
    env_set.add_argument('--append', action='store_true', help='Append if not exists')
    
    env_get = env_sub.add_parser('get', help='Get environment variable')
    env_get.add_argument('--key', required=True, help='Key')
    env_get.add_argument('--file', default='.env', help='Env file')
    env_get.add_argument('--default', help='Default value')
    
    # validate subcommand
    validate_parser = subparsers.add_parser('validate', help='Validate config file')
    validate_parser.add_argument('--file', required=True, help='Config file')
    validate_parser.add_argument('--type', default='json', help='Config type (json, yaml, ini)')
    
    # diff subcommand
    diff_parser = subparsers.add_parser('diff', help='Compare config files')
    diff_parser.add_argument('--file1', required=True, help='First file')
    diff_parser.add_argument('--file2', required=True, help='Second file')
    
    # search subcommand
    search_parser = subparsers.add_parser('search', help='Search config file')
    search_parser.add_argument('--file', required=True, help='Config file')
    search_parser.add_argument('--pattern', required=True, help='Pattern to search')
    search_parser.add_argument('--case-sensitive', action='store_true',
                               help='Case sensitive search')
    
    # list subcommand
    list_parser = subparsers.add_parser('list', help='List config files')
    list_parser.add_argument('--pattern', nargs='*', help='File patterns')
    
    args = parser.parse_args()
    
    manager = ConfigManager(args.project)
    
    if args.command == 'backup':
        if args.all:
            manager.backup_all(args.pattern)
        else:
            manager.backup_file(args.file, args.compression)
    elif args.command == 'restore':
        manager.restore_file(args.file, args.output)
    elif args.command == 'env':
        if args.env_command == 'set':
            manager.update_env_var(args.key, args.value, args.file, args.append)
        elif args.env_command == 'get':
            value = manager.get_env_var(args.key, args.file, args.default)
            if value is not None:
                print(value)
    elif args.command == 'validate':
        manager.validate_config(args.file, args.type)
    elif args.command == 'diff':
        manager.diff_config(args.file1, args.file2)
    elif args.command == 'search':
        manager.search_config(args.file, args.pattern, args.case_sensitive)
    elif args.command == 'list':
        configs = manager.list_configs(args.pattern)
        print(f"\nConfiguration files ({len(configs)}):\n")
        for config in configs:
            print(f"  - {config}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
