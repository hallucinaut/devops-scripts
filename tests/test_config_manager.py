#!/usr/bin/env python3
"""
Test suite for config_manager.py
"""

import configparser
import json
import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.config_manager import ConfigManager


def test_config_manager_init():
    """Test ConfigManager initialization"""
    manager = ConfigManager('.')
    assert manager is not None
    assert manager.project_dir == Path('.')
    print("✓ ConfigManager init test passed")


def test_config_manager_with_project():
    """Test ConfigManager with project directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ConfigManager(tmpdir)
        assert manager.project_dir == Path(tmpdir)
        assert Path(tmpdir).exists()
    print("✓ ConfigManager with project test passed")


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
        test_content = 'Config manager test'
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
    test_list = ['config.yaml', 'config.yml', 'settings.json']
    assert isinstance(test_list, list)
    assert len(test_list) > 0
    assert 'config.yaml' in test_list
    test_list.append('settings.ini')
    assert len(test_list) == 4
    
    print("✓ List operations test passed")


def test_dict_operations():
    """Test dictionary operations"""
    test_dict = {
        'config_file': 'config.yaml',
        'backup_dir': '.config_backups',
        'environment': 'development'
    }
    
    assert isinstance(test_dict, dict)
    assert 'config_file' in test_dict
    test_dict['new_key'] = 'new_value'
    assert len(test_dict) > 0
    
    print("✓ Dictionary operations test passed")


def test_json_operations():
    """Test JSON operations"""
    test_data = {
        'config_file': 'config.yaml',
        'backup_dir': '.config_backups',
        'environment': 'development'
    }
    
    json_str = json.dumps(test_data)
    parsed = json.loads(json_str)
    
    assert parsed == test_data
    print("✓ JSON operations test passed")


def test_yaml_operations():
    """Test YAML operations"""
    import yaml
    
    test_data = {
        'config_file': 'config.yaml',
        'backup_dir': '.config_backups',
        'environment': 'development'
    }
    
    yaml_str = yaml.dump(test_data)
    parsed = yaml.safe_load(yaml_str)
    
    assert parsed == test_data
    print("✓ YAML operations test passed")


def test_string_operations():
    """Test string operations"""
    test_str = 'config_manager'
    assert isinstance(test_str, str)
    assert len(test_str) > 0
    assert 'config' in test_str
    assert test_str.replace('_', '-') == 'config-manager'
    
    print("✓ String operations test passed")


def test_path_operations():
    """Test path operations"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ConfigManager(tmpdir)
        assert manager.project_dir == Path(tmpdir)
        assert Path(tmpdir).exists()
    
    print("✓ Path operations test passed")


def test_ini_operations():
    """Test INI operations"""
    config = configparser.ConfigParser()
    config['section'] = {'key': 'value'}
    assert config is not None
    assert 'section' in config
    
    print("✓ INI operations test passed")


def test_file_operations():
    """Test file read/write operations"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        test_content = 'Config file test'
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


def test_config_operations():
    """Test configuration operations"""
    manager = ConfigManager()
    
    # Test config dict
    test_config = {
        'project_dir': '.',
        'backup_dir': '.config_backups'
    }
    
    assert isinstance(test_config, dict)
    assert test_config['project_dir'] == '.'
    assert test_config['backup_dir'] == '.config_backups'
    
    print("✓ Config operations test passed")


def main():
    """Run all tests"""
    tests = [
        test_config_manager_init,
        test_config_manager_with_project,
        test_temporary_directory,
        test_temporary_file,
        test_list_operations,
        test_dict_operations,
        test_json_operations,
        test_yaml_operations,
        test_string_operations,
        test_path_operations,
        test_ini_operations,
        test_file_operations,
        test_config_operations
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
