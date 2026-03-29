#!/usr/bin/env python3
"""
Terraform Manager Script
Manages Terraform configurations and deployments
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class TerraformManager:
    """Terraform configuration manager"""
    
    def __init__(self, directory: Optional[str] = None):
        self.directory = Path(directory) if directory else Path.cwd()
        self._check_terraform_available()
        self.tfstate_file = self.directory / 'terraform.tfstate'
    
    def _check_terraform_available(self):
        """Check if Terraform is available"""
        try:
            subprocess.run(['terraform', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Terraform is not installed or not accessible", file=sys.stderr)
            raise RuntimeError("Terraform is not installed or not accessible")
    
    def init(self, backend_config: Optional[Dict] = None):
        """Initialize Terraform configuration"""
        print("Initializing Terraform...")
        
        try:
            if backend_config:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.tf', delete=False) as f:
                    yaml.dump({'terraform': {'backend': backend_config}}, f)
                    backend_file = f.name
                
                cmd = ['terraform', 'init', '-backend-config', backend_file]
                os.unlink(backend_file)
            else:
                cmd = ['terraform', 'init']
            
            subprocess.run(cmd, capture_output=True, check=True)
            print("✓ Terraform initialized")
        except subprocess.CalledProcessError as e:
            print(f"✗ Initialization failed: {e}", file=sys.stderr)
            raise
    
    def plan(self, var_files: Optional[List[str]] = None, out: Optional[str] = None):
        """Generate Terraform plan"""
        print("Generating Terraform plan...")
        
        try:
            cmd = ['terraform', 'plan']
            
            if var_files:
                for var_file in var_files:
                    cmd.extend(['-var-file', var_file])
            
            if out:
                cmd.extend(['-out', out])
            
            subprocess.run(cmd, capture_output=True, check=True)
            print("✓ Plan generated")
        except subprocess.CalledProcessError as e:
            print(f"✗ Plan failed: {e}", file=sys.stderr)
            raise
    
    def apply(self, auto_approve: bool = False, var_files: Optional[List[str]] = None):
        """Apply Terraform configuration"""
        print("Applying Terraform configuration...")
        
        try:
            cmd = ['terraform', 'apply']
            
            if auto_approve:
                cmd.append('-auto-approve')
            
            if var_files:
                for var_file in var_files:
                    cmd.extend(['-var-file', var_file])
            
            subprocess.run(cmd, capture_output=True, check=True)
            print("✓ Terraform applied successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Apply failed: {e}", file=sys.stderr)
            raise
    
    def destroy(self, auto_approve: bool = False):
        """Destroy Terraform resources"""
        print("Destroying Terraform resources...")
        
        try:
            cmd = ['terraform', 'destroy']
            
            if auto_approve:
                cmd.append('-auto-approve')
            
            subprocess.run(cmd, capture_output=True, check=True)
            print("✓ Terraform destroyed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Destroy failed: {e}", file=sys.stderr)
            raise
    
    def refresh(self):
        """Refresh Terraform state"""
        print("Refreshing Terraform state...")
        
        try:
            subprocess.run(['terraform', 'refresh'], capture_output=True, check=True)
            print("✓ State refreshed")
        except subprocess.CalledProcessError as e:
            print(f"✗ Refresh failed: {e}", file=sys.stderr)
            raise
    
    def output(self, name: Optional[str] = None, json: bool = False):
        """Show Terraform outputs"""
        try:
            cmd = ['terraform', 'output']
            
            if json:
                cmd.append('-json')
            
            if name:
                cmd.append(name)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"✗ Output failed: {e}", file=sys.stderr)
            raise
    
    def state_list(self):
        """List resources in Terraform state"""
        print("\nTerraform resources:")
        
        try:
            result = subprocess.run(
                ['terraform', 'state', 'list'],
                capture_output=True, text=True, check=True
            )
            
            for resource in result.stdout.splitlines():
                print(f"  - {resource}")
        except subprocess.CalledProcessError as e:
            print(f"✗ State list failed: {e}", file=sys.stderr)
            raise
    
    def state_show(self, resource: str):
        """Show resource details in Terraform state"""
        try:
            result = subprocess.run(
                ['terraform', 'state', 'show', resource],
                capture_output=True, text=True, check=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"✗ State show failed: {e}", file=sys.stderr)
            raise
    
    def state_rm(self, resource: str):
        """Remove resource from Terraform state"""
        print(f"Removing resource from state: {resource}")
        
        try:
            subprocess.run(
                ['terraform', 'state', 'rm', resource],
                capture_output=True, check=True
            )
            print("✓ Resource removed from state")
        except subprocess.CalledProcessError as e:
            print(f"✗ State removal failed: {e}", file=sys.stderr)
            raise
    
    def state_mv(self, from_resource: str, to_resource: str):
        """Move resource in Terraform state"""
        print(f"Moving resource: {from_resource} -> {to_resource}")
        
        try:
            subprocess.run(
                ['terraform', 'state', 'mv', from_resource, to_resource],
                capture_output=True, check=True
            )
            print("✓ Resource moved successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ State move failed: {e}", file=sys.stderr)
            raise
    
    def get_outputs(self) -> Dict[str, Dict]:
        """Get all outputs from Terraform state"""
        try:
            result = subprocess.run(
                ['terraform', 'output', '-json'],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError:
            return {}
    
    def get_variables(self) -> List[str]:
        """Get required variables"""
        try:
            result = subprocess.run(
                ['terraform', 'fmt', '-check', '-recursive', '-list'],
                capture_output=True, text=True, check=True
            )
            return [line for line in result.stdout.splitlines() if line.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def validate(self):
        """Validate Terraform configuration"""
        print("Validating Terraform configuration...")
        
        try:
            subprocess.run(['terraform', 'validate'], capture_output=True, check=True)
            print("✓ Configuration is valid")
        except subprocess.CalledProcessError as e:
            print(f"✗ Validation failed: {e}", file=sys.stderr)
            raise
    
    def fmt_check(self) -> bool:
        """Check if configuration is formatted"""
        try:
            result = subprocess.run(
                ['terraform', 'fmt', '-check'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip() == ''
        except subprocess.CalledProcessError:
            return True
    
    def fmt(self):
        """Format Terraform configuration"""
        print("Formatting Terraform configuration...")
        
        try:
            subprocess.run(['terraform', 'fmt'], capture_output=True, check=True)
            print("✓ Configuration formatted")
        except subprocess.CalledProcessError as e:
            print(f"✗ Formatting failed: {e}", file=sys.stderr)
            raise


def main():
    parser = argparse.ArgumentParser(description='Terraform Manager Script')
    parser.add_argument('--dir', help='Terraform directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # init subcommand
    init_parser = subparsers.add_parser('init', help='Initialize Terraform')
    init_parser.add_argument('--backend-config', type=str, help='Backend config file')
    
    # plan subcommand
    plan_parser = subparsers.add_parser('plan', help='Generate plan')
    plan_parser.add_argument('--var-file', nargs='*', help='Variable files')
    plan_parser.add_argument('--out', help='Output plan file')
    
    # apply subcommand
    apply_parser = subparsers.add_parser('apply', help='Apply configuration')
    apply_parser.add_argument('--auto-approve', action='store_true', help='Auto approve')
    apply_parser.add_argument('--var-file', nargs='*', help='Variable files')
    
    # destroy subcommand
    destroy_parser = subparsers.add_parser('destroy', help='Destroy resources')
    destroy_parser.add_argument('--auto-approve', action='store_true', help='Auto approve')
    
    # refresh subcommand
    refresh_parser = subparsers.add_parser('refresh', help='Refresh state')
    
    # output subcommand
    output_parser = subparsers.add_parser('output', help='Show outputs')
    output_parser.add_argument('--name', help='Output name')
    output_parser.add_argument('--json', action='store_true', help='JSON format')
    
    # state subcommand
    state_parser = subparsers.add_parser('state', help='State management')
    state_sub = state_parser.add_subparsers(dest='state_command', help='State command')
    
    state_list = state_sub.add_parser('list', help='List resources')
    state_show = state_sub.add_parser('show', help='Show resource')
    state_show.add_argument('resource', help='Resource name')
    state_rm = state_sub.add_parser('rm', help='Remove resource')
    state_rm.add_argument('resource', help='Resource name')
    state_mv = state_sub.add_parser('mv', help='Move resource')
    state_mv.add_argument('from', help='From resource')
    state_mv.add_argument('to', help='To resource')
    
    # validate subcommand
    validate_parser = subparsers.add_parser('validate', help='Validate configuration')
    
    # fmt subcommand
    fmt_parser = subparsers.add_parser('fmt', help='Format configuration')
    fmt_check_parser = subparsers.add_parser('fmt-check', help='Check formatting')
    
    args = parser.parse_args()
    
    manager = TerraformManager(args.dir)
    
    if args.command == 'init':
        manager.init(json.loads(args.backend_config) if args.backend_config else None)
    elif args.command == 'plan':
        manager.plan(args.var_file, args.out)
    elif args.command == 'apply':
        manager.apply(args.auto_approve, args.var_file)
    elif args.command == 'destroy':
        manager.destroy(args.auto_approve)
    elif args.command == 'refresh':
        manager.refresh()
    elif args.command == 'output':
        manager.output(args.name, args.json)
    elif args.command == 'state':
        if args.state_command == 'list':
            manager.state_list()
        elif args.state_command == 'show':
            manager.state_show(args.resource)
        elif args.state_command == 'rm':
            manager.state_rm(args.resource)
        elif args.state_command == 'mv':
            manager.state_mv(args.from_resource, args.to_resource)
    elif args.command == 'validate':
        manager.validate()
    elif args.command == 'fmt':
        manager.fmt()
    elif args.command == 'fmt-check':
        if manager.fmt_check():
            print("✓ Configuration is properly formatted")
        else:
            print("✗ Configuration needs formatting")
            print("Terraform is not installed or not accessible", file=sys.stderr)
            raise RuntimeError("Terraform is not installed or not accessible")
    else:
        parser.print_help()
        print("Terraform is not installed or not accessible", file=sys.stderr)
        raise RuntimeError("Terraform is not installed or not accessible")


if __name__ == '__main__':
    main()
