#!/usr/bin/env python3
"""
Kubernetes Deployment Script
Manages deployments, services, and configurations
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class KubernetesDeployer:
    """Kubernetes deployment manager"""
    
    def __init__(self, namespace: str = 'default'):
        self.namespace = namespace
        self.context = self._get_current_context()
    
    def _get_current_context(self) -> str:
        """Get current k8s context"""
        try:
            result = subprocess.run(
                ['kubectl', 'config', 'current-context'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return 'default'
    
    def create_namespace(self, namespace: str):
        """Create a new namespace"""
        print(f"Creating namespace: {namespace}")
        try:
            subprocess.run(
                ['kubectl', 'create', 'namespace', namespace],
                check=True
            )
            print(f"✓ Namespace '{namespace}' created")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create namespace: {e}", file=sys.stderr)
            raise
    
    def deploy_manifest(self, file_path: str, namespace: str = None):
        """Deploy a Kubernetes manifest file"""
        ns = namespace or self.namespace
        
        print(f"Deploying manifest: {file_path} in namespace: {ns}")
        try:
            subprocess.run(
                ['kubectl', 'apply', '-f', file_path, '-n', ns],
                check=True
            )
            print(f"✓ Manifest deployed")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to deploy manifest: {e}", file=sys.stderr)
            raise
    
    def deploy_deployment(self, name: str, image: str, replicas: int,
                         namespace: str = None, port: int = 8080,
                         env: Optional[Dict] = None):
        """Create a deployment"""
        ns = namespace or self.namespace
        
        print(f"Creating deployment: {name}")
        manifest = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': name,
                'namespace': ns,
                'labels': {
                    'app': name,
                    'version': 'v1'
                }
            },
            'spec': {
                'replicas': replicas,
                'selector': {
                    'matchLabels': {
                        'app': name
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': name,
                            'version': 'v1'
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': name,
                            'image': image,
                            'ports': [{'containerPort': port}],
                            'env': [{'name': k, 'value': v} for k, v in (env or {}).items()]
                        }]
                    }
                }
            }
        }
        
        self._write_and_deploy(manifest, name)
    
    def deploy_service(self, name: str, target: str, port: int,
                      namespace: str = None, service_type: str = 'ClusterIP'):
        """Create a Kubernetes service"""
        ns = namespace or self.namespace
        
        print(f"Creating service: {name}")
        manifest = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': name,
                'namespace': ns,
                'labels': {'app': target}
            },
            'spec': {
                'type': service_type,
                'selector': {
                    'app': target
                },
                'ports': [{
                    'protocol': 'TCP',
                    'port': port,
                    'targetPort': port
                }]
            }
        }
        
        self._write_and_deploy(manifest, f'{name}-service')
    
    def deploy_configmap(self, name: str, data: Dict, namespace: str = None):
        """Create a ConfigMap"""
        ns = namespace or self.namespace
        
        print(f"Creating ConfigMap: {name}")
        manifest = {
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {
                'name': name,
                'namespace': ns
            },
            'data': data
        }
        
        self._write_and_deploy(manifest, f'{name}-configmap')
    
    def deploy_secret(self, name: str, data: Dict, namespace: str = None):
        """Create a Kubernetes secret"""
        ns = namespace or self.namespace
        
        print(f"Creating secret: {name}")
        manifest = {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {
                'name': name,
                'namespace': ns
            },
            'type': 'Opaque',
            'data': {k: v.encode() for k, v in data.items()}
        }
        
        self._write_and_deploy(manifest, f'{name}-secret')
    
    def _write_and_deploy(self, manifest: Dict, name: str):
        """Write manifest to temp file and deploy"""
        temp_file = f'/tmp/k8s-{name}.yaml'
        
        with open(temp_file, 'w') as f:
            yaml.dump(manifest, f)
        
        try:
            subprocess.run(
                ['kubectl', 'apply', '-f', temp_file, '-n', self.namespace],
                check=True
            )
            print(f"✓ Resource deployed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to deploy: {e}", file=sys.stderr)
            raise
        finally:
            Path(temp_file).unlink(missing_ok=True)
    
    def get_deployments(self, namespace: str = None) -> List[str]:
        """Get list of deployments"""
        ns = namespace or self.namespace
        try:
            result = subprocess.run(
                ['kubectl', 'get', 'deployments', '-n', ns, '-o', 'json'],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return [d['metadata']['name'] for d in data.get('items', [])]
        except subprocess.CalledProcessError:
            return []
    
    def delete_deployment(self, name: str, namespace: str = None):
        """Delete a deployment"""
        ns = namespace or self.namespace
        print(f"Deleting deployment: {name}")
        try:
            subprocess.run(
                ['kubectl', 'delete', 'deployment', name, '-n', ns],
                check=True
            )
            print(f"✓ Deployment deleted")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to delete deployment", file=sys.stderr)
            raise


def main():
    parser = argparse.ArgumentParser(description='Kubernetes Deployment Script')
    parser.add_argument('--namespace', default='default',
                       help='Kubernetes namespace')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # deploy subcommand
    deploy_parser = subparsers.add_parser('deploy', help='Deploy resources')
    deploy_parser.add_argument('--manifest', help='Path to manifest file')
    deploy_parser.add_argument('--deployment', help='Deployment name')
    deploy_parser.add_argument('--image', help='Docker image')
    deploy_parser.add_argument('--replicas', type=int, default=1, help='Replica count')
    deploy_parser.add_argument('--port', type=int, default=8080, help='Container port')
    deploy_parser.add_argument('--env', nargs='*', metavar='KEY=VALUE',
                              help='Environment variables')
    
    # service subcommand
    service_parser = subparsers.add_parser('service', help='Create service')
    service_parser.add_argument('--name', required=True, help='Service name')
    service_parser.add_argument('--target', required=True, help='Deployment target')
    service_parser.add_argument('--port', type=int, required=True, help='Service port')
    service_parser.add_argument('--type', default='ClusterIP',
                               help='Service type')
    
    # configmap subcommand
    configmap_parser = subparsers.add_parser('configmap', help='Create ConfigMap')
    configmap_parser.add_argument('--name', required=True, help='ConfigMap name')
    configmap_parser.add_argument('--data', nargs='*', metavar='KEY=VALUE',
                                  help='Key-value pairs')
    
    # secret subcommand
    secret_parser = subparsers.add_parser('secret', help='Create secret')
    secret_parser.add_argument('--name', required=True, help='Secret name')
    secret_parser.add_argument('--data', nargs='*', metavar='KEY=VALUE',
                               help='Base64-encoded data')
    
    args = parser.parse_args()
    
    deployer = KubernetesDeployer(args.namespace)
    
    if args.command == 'deploy':
        if args.manifest:
            deployer.deploy_manifest(args.manifest, args.namespace)
        elif args.deployment:
            env = dict(e.split('=', 1) for e in args.env) if args.env else {}
            deployer.deploy_deployment(
                args.deployment, args.image, args.replicas,
                args.namespace, args.port, env
            )
    elif args.command == 'service':
        deployer.deploy_service(args.name, args.target, args.port,
                               args.namespace, args.type)
    elif args.command == 'configmap':
        data = dict(e.split('=', 1) for e in args.data) if args.data else {}
        deployer.deploy_configmap(args.name, data, args.namespace)
    elif args.command == 'secret':
        data = {k: v for k, v in (e.split('=', 1) for e in args.data)}
        deployer.deploy_secret(args.name, data, args.namespace)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
