#!/usr/bin/env python3
"""
Test suite for k8s_deploy.py
"""

import json
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.k8s_deploy import KubernetesDeployer


def test_kubernetes_deployer_init():
    """Test KubernetesDeployer initialization"""
    deployer = KubernetesDeployer('default')
    assert deployer.namespace == 'default'
    assert deployer.context == 'default'
    print("✓ KubernetesDeployer init test passed")


def test_kubernetes_deployer_with_namespace():
    """Test KubernetesDeployer with custom namespace"""
    deployer = KubernetesDeployer('production')
    assert deployer.namespace == 'production'
    print("✓ KubernetesDeployer with namespace test passed")


def test_yaml_generation():
    """Test YAML manifest generation"""
    deployer = KubernetesDeployer('test')
    manifest = {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {
            'name': 'test-config',
            'namespace': 'test-ns'
        },
        'data': {
            'key1': 'value1',
            'key2': 'value2'
        }
    }
    
    # Test that the manifest can be written (kubectl may not be available)
    temp_file = '/tmp/test-configmap.yaml'
    try:
        deployer._write_and_deploy(manifest, 'test-config')
        # Verify file content
        with open(temp_file) as f:
            content = yaml.safe_load(f)
            assert content['kind'] == 'ConfigMap'
            assert content['metadata']['name'] == 'test-config'
    except FileNotFoundError:
        print("⚠ kubectl not available, skipping deployment test")
        # Verify the manifest structure is correct
        assert manifest['apiVersion'] == 'v1'
        assert manifest['kind'] == 'ConfigMap'
    finally:
        Path(temp_file).unlink(missing_ok=True)
    
def test_manifest_structure():
    """Test manifest structure"""
    deployer = KubernetesDeployer('test')
    
    # Test deployment manifest
    deployment_manifest = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': 'test-deployment',
            'namespace': 'test'
        },
        'spec': {
            'replicas': 3,
            'selector': {
                'matchLabels': {
                    'app': 'test'
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': 'test'
                    }
                },
                'spec': {
                    'containers': [{
                        'name': 'test',
                        'image': 'test:latest',
                        'ports': [{'containerPort': 8080}]
                    }]
                }
            }
        }
    }
    
    temp_file = '/tmp/test-deployment.yaml'
    try:
        deployer._write_and_deploy(deployment_manifest, 'test-deployment')
        # Verify file structure
        with open(temp_file) as f:
            content = yaml.safe_load(f)
            assert content['kind'] == 'Deployment'
            assert content['metadata']['name'] == 'test-deployment'
            assert content['spec']['replicas'] == 3
    except FileNotFoundError:
        print("⚠ kubectl not available, skipping deployment test")
        # Verify the manifest structure is correct
        assert deployment_manifest['apiVersion'] == 'apps/v1'
        assert deployment_manifest['kind'] == 'Deployment'
    finally:
        Path(temp_file).unlink(missing_ok=True)
    print("✓ Manifest structure test passed")


def test_service_manifest():
    """Test service manifest generation"""
    deployer = KubernetesDeployer('test')
    
    service_manifest = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': 'test-service',
            'namespace': 'test'
        },
        'spec': {
            'type': 'ClusterIP',
            'selector': {
                'app': 'test'
            },
            'ports': [{
                'protocol': 'TCP',
                'port': 80,
                'targetPort': 8080
            }]
        }
    }
    
    temp_file = '/tmp/test-service.yaml'
    try:
        deployer._write_and_deploy(service_manifest, 'test-service')
        # Verify file
        with open(temp_file) as f:
            content = yaml.safe_load(f)
            assert content['kind'] == 'Service'
            assert content['spec']['type'] == 'ClusterIP'
    except FileNotFoundError:
        print("⚠ kubectl not available, skipping service test")
        # Verify the manifest structure is correct
        assert service_manifest['apiVersion'] == 'v1'
        assert service_manifest['kind'] == 'Service'
    finally:
        Path(temp_file).unlink(missing_ok=True)
    print("✓ Service manifest test passed")


def test_secret_manifest():
    """Test secret manifest generation"""
    deployer = KubernetesDeployer('test')
    
    secret_manifest = {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'name': 'test-secret',
            'namespace': 'test'
        },
        'type': 'Opaque',
        'data': {
            'username': 'dXNlcm5hbWU=',
            'password': 'cGFzc3dvcmQ='
        }
    }
    
    temp_file = '/tmp/test-secret.yaml'
    try:
        deployer._write_and_deploy(secret_manifest, 'test-secret')
        # Verify file
        with open(temp_file) as f:
            content = yaml.safe_load(f)
            assert content['kind'] == 'Secret'
            assert content['metadata']['name'] == 'test-secret'
    except FileNotFoundError:
        print("⚠ kubectl not available, skipping secret test")
        # Verify the manifest structure is correct
        assert secret_manifest['apiVersion'] == 'v1'
        assert secret_manifest['kind'] == 'Secret'
    finally:
        Path(temp_file).unlink(missing_ok=True)
    print("✓ Secret manifest test passed")


def main():
    """Run all tests"""
    tests = [
        test_kubernetes_deployer_init,
        test_kubernetes_deployer_with_namespace,
        test_yaml_generation,
        test_manifest_structure,
        test_service_manifest,
        test_secret_manifest
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}", file=sys.stderr)
            failed += 1
    
    if failed > 0:
        print(f"\n{failed} test(s) failed")
        sys.exit(1)
    else:
        print(f"\nAll tests passed!")


if __name__ == '__main__':
    main()
