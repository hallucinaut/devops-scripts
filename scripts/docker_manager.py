#!/usr/bin/env python3
"""
Docker Management Script
Handles Docker containers, images, and volumes
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import time


class DockerManager:
    """Docker container and image manager"""
    
    def __init__(self):
        self._ensure_docker_available()
    
    def _ensure_docker_available(self):
        """Check if Docker is available"""
        try:
            subprocess.run(['docker', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Docker is not installed or not accessible", file=sys.stderr)
            sys.exit(1)
    
    def build_image(self, dockerfile: str, tag: str, context: str = '.'):
        """Build Docker image"""
        print(f"Building image: {tag}")
        try:
            subprocess.run(
                ['docker', 'build', '-t', tag, '-f', dockerfile, context],
                check=True
            )
            print(f"✓ Image '{tag}' built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to build image: {e}", file=sys.stderr)
            return False
    
    def run_container(self, image: str, container_name: str, 
                      ports: Optional[Dict] = None,
                      volumes: Optional[Dict] = None,
                      environment: Optional[Dict] = None,
                      detach: bool = True,
                      command: Optional[str] = None):
        """Run a Docker container"""
        print(f"Running container: {container_name}")
        
        # Build docker run command
        cmd = ['docker', 'run', '--name', container_name]
        
        if detach:
            cmd.append('-d')
        
        if ports:
            for host_port, container_port in ports.items():
                cmd.extend(['-p', f"{host_port}:{container_port}"])
        
        if volumes:
            for host_path, container_path in volumes.items():
                cmd.extend(['-v', f"{host_path}:{container_path}"])
        
        if environment:
            for key, value in environment.items():
                cmd.extend(['-e', f"{key}={value}"])
        
        cmd.append(image)
        if command:
            cmd.extend(command.split())
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ Container '{container_name}' started")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to run container: {e}", file=sys.stderr)
            return False
    
    def stop_container(self, container_name: str):
        """Stop a running container"""
        print(f"Stopping container: {container_name}")
        try:
            subprocess.run(
                ['docker', 'stop', container_name],
                check=True
            )
            print(f"✓ Container '{container_name}' stopped")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to stop container: {e}", file=sys.stderr)
            return False
    
    def remove_container(self, container_name: str, force: bool = False):
        """Remove a container"""
        print(f"Removing container: {container_name}")
        try:
            if force:
                subprocess.run(
                    ['docker', 'rm', '-f', container_name],
                    check=True
                )
            else:
                subprocess.run(
                    ['docker', 'rm', container_name],
                    check=True
                )
            print(f"✓ Container '{container_name}' removed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to remove container: {e}", file=sys.stderr)
            return False
    
    def list_containers(self, all_: bool = False) -> List[str]:
        """List all containers"""
        cmd = ['docker', 'ps', '-a', '--format', '{{.Names}}']
        if all_:
            cmd.append('-a')
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return [c.strip() for c in result.stdout.splitlines() if c.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def list_images(self) -> List[str]:
        """List all images"""
        try:
            result = subprocess.run(
                ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'],
                capture_output=True, text=True, check=True
            )
            return [img.strip() for img in result.stdout.splitlines() if img.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def prune_containers(self, force: bool = False):
        """Prune stopped containers"""
        print("Pruning stopped containers...")
        try:
            if force:
                subprocess.run(['docker', 'container', 'prune', '-f'], check=True)
            else:
                subprocess.run(['docker', 'container', 'prune'], check=True)
            print("✓ Pruned stopped containers")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to prune containers: {e}", file=sys.stderr)
            return False
    
    def prune_images(self, force: bool = False, all_: bool = False):
        """Prune unused images"""
        print("Pruning unused images...")
        try:
            cmd = ['docker', 'image', 'prune']
            if force:
                cmd.append('-f')
            if all_:
                cmd.append('-a')
            subprocess.run(cmd, check=True)
            print("✓ Pruned unused images")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to prune images: {e}", file=sys.stderr)
            return False
    
    def get_container_info(self, container_name: str) -> Optional[Dict]:
        """Get detailed info about a container"""
        try:
            result = subprocess.run(
                ['docker', 'inspect', container_name],
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError:
            return None
    
    def exec_command(self, container_name: str, command: str):
        """Execute command in a container"""
        print(f"Executing command in '{container_name}': {command}")
        try:
            subprocess.run(
                ['docker', 'exec', container_name, 'sh', '-c', command],
                check=True
            )
            print("✓ Command executed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to execute command: {e}", file=sys.stderr)
            return False
    
    def logs(self, container_name: str, tail: int = 100):
        """Get container logs"""
        try:
            result = subprocess.run(
                ['docker', 'logs', '--tail', str(tail), container_name],
                capture_output=True, text=True, check=True
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to get logs: {e}", file=sys.stderr)
            return False
    
    def save_image(self, image_name: str, output_path: str):
        """Save image to tar file"""
        print(f"Saving image '{image_name}' to {output_path}")
        try:
            subprocess.run(
                ['docker', 'save', '-o', output_path, image_name],
                check=True
            )
            print(f"✓ Image saved to {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to save image: {e}", file=sys.stderr)
            return False
    
    def load_image(self, input_path: str):
        """Load image from tar file"""
        print(f"Loading image from {input_path}")
        try:
            subprocess.run(
                ['docker', 'load', '-i', input_path],
                check=True
            )
            print("✓ Image loaded successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to load image: {e}", file=sys.stderr)
            return False


def main():
    parser = argparse.ArgumentParser(description='Docker Management Script')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # build subcommand
    build_parser = subparsers.add_parser('build', help='Build Docker image')
    build_parser.add_argument('--dockerfile', default='Dockerfile', help='Dockerfile path')
    build_parser.add_argument('--tag', required=True, help='Image tag')
    build_parser.add_argument('--context', default='.', help='Build context')
    
    # run subcommand
    run_parser = subparsers.add_parser('run', help='Run container')
    run_parser.add_argument('--image', required=True, help='Docker image')
    run_parser.add_argument('--name', required=True, help='Container name')
    run_parser.add_argument('--port', nargs='*', metavar='HOST_PORT:CONTAINER_PORT',
                            help='Port mappings')
    run_parser.add_argument('--volume', nargs='*', metavar='HOST_PATH:CONTAINER_PATH',
                            help='Volume mappings')
    run_parser.add_argument('--env', nargs='*', metavar='KEY=VALUE',
                            help='Environment variables')
    run_parser.add_argument('--detach', action='store_true', help='Run in background')
    run_parser.add_argument('--command', help='Command to run')
    
    # stop subcommand
    stop_parser = subparsers.add_parser('stop', help='Stop container')
    stop_parser.add_argument('--name', required=True, help='Container name')
    
    # remove subcommand
    remove_parser = subparsers.add_parser('remove', help='Remove container')
    remove_parser.add_argument('--name', required=True, help='Container name')
    remove_parser.add_argument('--force', action='store_true', help='Force removal')
    
    # logs subcommand
    logs_parser = subparsers.add_parser('logs', help='View container logs')
    logs_parser.add_argument('--name', required=True, help='Container name')
    logs_parser.add_argument('--tail', type=int, default=100, help='Lines to show')
    
    # prune subcommand
    prune_parser = subparsers.add_parser('prune', help='Prune unused resources')
    prune_parser.add_argument('--containers', action='store_true', help='Prune containers')
    prune_parser.add_argument('--images', action='store_true', help='Prune images')
    prune_parser.add_argument('--force', action='store_true', help='Force prune')
    prune_parser.add_argument('--all', action='store_true', help='Prune all images')
    
    # exec subcommand
    exec_parser = subparsers.add_parser('exec', help='Execute command in container')
    exec_parser.add_argument('--name', required=True, help='Container name')
    exec_parser.add_argument('--command', required=True, help='Command to execute')
    
    # save/load subcommand
    save_parser = subparsers.add_parser('save', help='Save image to tar')
    save_parser.add_argument('--image', required=True, help='Image name')
    save_parser.add_argument('--output', required=True, help='Output file path')
    
    load_parser = subparsers.add_parser('load', help='Load image from tar')
    load_parser.add_argument('--input', required=True, help='Input tar file path')
    
    args = parser.parse_args()
    manager = DockerManager()
    
    if args.command == 'build':
        manager.build_image(args.dockerfile, args.tag, args.context)
    elif args.command == 'run':
        ports = dict(p.split(':') for p in args.port) if args.port else None
        volumes = dict(v.split(':') for v in args.volume) if args.volume else None
        env = dict(e.split('=', 1) for e in args.env) if args.env else None
        manager.run_container(args.image, args.name, ports, volumes, env, args.detach, args.command)
    elif args.command == 'stop':
        manager.stop_container(args.name)
    elif args.command == 'remove':
        manager.remove_container(args.name, args.force)
    elif args.command == 'logs':
        manager.logs(args.name, args.tail)
    elif args.command == 'prune':
        if args.containers:
            manager.prune_containers(args.force)
        if args.images:
            manager.prune_images(args.force, args.all)
    elif args.command == 'exec':
        manager.exec_command(args.name, args.command)
    elif args.command == 'save':
        manager.save_image(args.image, args.output)
    elif args.command == 'load':
        manager.load_image(args.input)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
