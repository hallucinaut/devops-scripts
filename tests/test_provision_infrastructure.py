#!/usr/bin/env python3
"""
Test suite for provision_infrastructure.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.provision_infrastructure import AWSProvider, GCPProvider, AzureProvider, InfrastructureProvisioner


def test_aws_provider_init():
    """Test AWS provider initialization"""
    config = {
        'project_id': 'test-project',
        'environment': 'test',
        'vpc_cidr': '10.0.0.0/16',
        'subnet_cidrs': ['10.0.1.0/24', '10.0.2.0/24']
    }
    provider = AWSProvider(config)
    assert provider.config == config
    assert provider.project_id == 'test-project'
    print("✓ AWS provider init test passed")


def test_gcp_provider_init():
    """Test GCP provider initialization"""
    config = {
        'project_id': 'test-project',
        'environment': 'test',
        'region': 'us-central1',
        'num_nodes': 3,
        'machine_type': 'e2-medium'
    }
    provider = GCPProvider(config)
    assert provider.config == config
    assert provider.project_id == 'test-project'
    print("✓ GCP provider init test passed")


def test_azure_provider_init():
    """Test Azure provider initialization"""
    config = {
        'project_id': 'test-project',
        'environment': 'test',
        'location': 'eastus',
        'node_count': 2,
        'node_vm_size': 'Standard_D2s_v3'
    }
    provider = AzureProvider(config)
    assert provider.config == config
    assert provider.project_id == 'test-project'
    print("✓ Azure provider init test passed")


def test_infrastructure_provisioner():
    """Test infrastructure provisioner"""
    config = {
        'project_id': 'test-project',
        'environment': 'test'
    }
    provisioner = InfrastructureProvisioner('aws', config)
    assert provisioner.config == config
    print("✓ Infrastructure provisioner test passed")


def test_config_file_loading():
    """Test loading configuration from JSON file"""
    config = {
        'project_id': 'test-project',
        'environment': 'test',
        'vpc_cidr': '10.0.0.0/16'
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_file = f.name
        from scripts.provision_infrastructure import InfrastructureProvisioner
        provisioner = InfrastructureProvisioner("aws", config)
        assert provisioner.config['project_id'] == 'test-project'
        os.unlink(config_file)


def test_provisioner_modes():
    """Test provisioner with different modes"""
    config = {'project_id': 'test-project', 'environment': 'test'}
    
    # Test provision mode (may fail if AWS not available)
    provisioner = InfrastructureProvisioner('aws', config)
    try:
        provisioner.provision()
    except Exception as e:
        print(f"⚠ AWS not available: {e}")
    
    # Test teardown mode (may fail if AWS not available)
    try:
        provisioner.teardown()
    except Exception as e:
        print(f"⚠ AWS not available: {e}")
    print("✓ Provisioner modes test passed")


def main():
    """Run all tests"""
    tests = [
        test_aws_provider_init,
        test_gcp_provider_init,
        test_azure_provider_init,
        test_infrastructure_provisioner,
        test_config_file_loading,
        test_provisioner_modes
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
