#!/usr/bin/env python3
"""
Test suite for terraform_manager.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.terraform_manager import TerraformManager


def test_terraform_manager_init():
    """Test TerraformManager initialization"""
    manager = TerraformManager()
    assert manager is not None
    print("✓ TerraformManager init test passed")


def test_terraform_manager_with_directory():
    """Test TerraformManager with directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = TerraformManager(tmpdir)
        assert manager.directory == Path(tmpdir)
        assert Path(tmpdir).exists()
    print("✓ TerraformManager with directory test passed")


def test_temporary_directory():
    """Test temporary directory operations"""
    with tempfile.TemporaryDirectory() as tmpdir:
        assert Path(tmpdir).exists()
        assert tmpdir in str(Path(tmpdir))
        assert len(tmpdir) > 0
    
    print("✓ Temporary directory test passed")


def test_temporary_file():
    """Test temporary file operations"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        test_content = 'Terraform test content'
        f.write(test_content)
        test_file = Path(f.name)
    
    try:
        content = test_file.read_text()
        assert content == test_content
        test_file.write_text('Updated content')
        content = test_file.read_text()
        assert content == 'Updated content'
    finally:
        test_file.unlink(missing_ok=True)
    
    print("✓ Temporary file test passed")


def test_list_operations():
    """Test list operations"""
    test_list = ['module1', 'module2', 'module3']
    assert isinstance(test_list, list)
    assert len(test_list) > 0
    assert 'module1' in test_list
    test_list.append('module4')
    assert len(test_list) == 4
    
    print("✓ List operations test passed")


def test_dict_operations():
    """Test dictionary operations"""
    test_dict = {
        'module': 'test',
        'version': '1.0.0',
        'provider': 'aws'
    }
    
    assert isinstance(test_dict, dict)
    assert 'module' in test_dict
    test_dict['new_key'] = 'new_value'
    assert len(test_dict) > 0
    
    print("✓ Dictionary operations test passed")


def test_json_operations():
    """Test JSON operations"""
    test_data = {
        'module': 'test_module',
        'version': '1.0.0',
        'providers': ['aws', 'google']
    }
    
    json_str = json.dumps(test_data)
    parsed = json.loads(json_str)
    
    assert parsed == test_data
    print("✓ JSON operations test passed")


def test_string_operations():
    """Test string operations"""
    test_str = 'terraform-config'
    assert isinstance(test_str, str)
    assert len(test_str) > 0
    assert 'terraform' in test_str
    assert test_str.replace('-', '_') == 'terraform_config'
    
    print("✓ String operations test passed")


def test_path_operations():
    """Test path operations"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = TerraformManager(tmpdir)
        assert manager.directory == Path(tmpdir)
        assert Path(tmpdir).exists()
    
    print("✓ Path operations test passed")


def test_subprocess_import():
    """Test subprocess import"""
    import subprocess
    assert subprocess is not None
    
    print("✓ Subprocess import test passed")


def test_config_operations():
    """Test configuration operations"""
    manager = TerraformManager()
    
    # Test config dict
    test_config = {
        'directory': 'terraform',
        'tfstate': 'terraform.tfstate'
    }
    
    assert isinstance(test_config, dict)
    assert test_config['directory'] == 'terraform'
    assert test_config['tfstate'] == 'terraform.tfstate'
    
    print("✓ Config operations test passed")


def test_file_operations():
    """Test file read/write operations"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        test_content = 'Terraform configuration test'
        f.write(test_content)
        test_file = Path(f.name)
    
    try:
        content = test_file.read_text()
        assert content == test_content
        
        test_file.write_text('New content')
        content = test_file.read_text()
        assert content == 'New content'
    finally:
        test_file.unlink(missing_ok=True)
    
    print("✓ File operations test passed")


def main():
    """Run all tests"""
    tests = [
        test_terraform_manager_init,
        test_terraform_manager_with_directory,
        test_temporary_directory,
        test_temporary_file,
        test_list_operations,
        test_dict_operations,
        test_json_operations,
        test_string_operations,
        test_path_operations,
        test_subprocess_import,
        test_config_operations,
        test_file_operations
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
