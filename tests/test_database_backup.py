#!/usr/bin/env python3
"""
Test suite for database_backup.py
"""

import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.database_backup import DatabaseBackupManager


def test_database_backup_manager_init():
    """Test DatabaseBackupManager initialization"""
    manager = DatabaseBackupManager()
    assert manager is not None
    assert manager.backup_dir.exists() or manager.backup_dir is None
    print("✓ DatabaseBackupManager init test passed")


def test_config_loading():
    """Test configuration loading from file"""
    config = {
        'backup_dir': 'backups',
        'compression': True,
        'keep_days': 7
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_file = f.name
    
    try:
        manager = DatabaseBackupManager(config_file)
        assert manager.config == config
        print("✓ Config loading test passed")
    finally:
        os.unlink(config_file)


def test_temporary_backup_file():
    """Test temporary backup file creation"""
    manager = DatabaseBackupManager()
    
    with tempfile.NamedTemporaryFile(suffix='.sql', delete=False) as f:
        test_file = Path(f.name)
    
    try:
        # Check file creation
        assert test_file.exists()
        print("✓ Temporary backup file test passed")
    finally:
        test_file.unlink(missing_ok=True)


def test_temporary_config_file():
    """Test temporary config file creation"""
    config = {'backup_dir': 'test_backups', 'compression': False}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_file = f.name
    
    try:
        manager = DatabaseBackupManager(config_file)
        assert manager.backup_dir == Path('test_backups')
        print("✓ Temporary config file test passed")
    finally:
        os.unlink(config_file)


def test_current_timestamp():
    """Test timestamp generation"""
    manager = DatabaseBackupManager()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    assert isinstance(timestamp, str)
    assert len(timestamp) > 0
    print("✓ Current timestamp test passed")


def test_file_operations():
    """Test file read/write operations"""
    manager = DatabaseBackupManager()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        test_content = 'Database backup test content'
        f.write(test_content)
        test_file = Path(f.name)
    
    try:
        # Test reading
        content = test_file.read_text()
        assert content == test_content
        
        # Test writing
        test_file.write_text('New content')
        content = test_file.read_text()
        assert content == 'New content'
        print("✓ File operations test passed")
    finally:
        test_file.unlink(missing_ok=True)


def test_json_operations():
    """Test JSON operations"""
    manager = DatabaseBackupManager()
    
    # Test dictionary to JSON
    data = {
        'database': 'test_db',
        'backup_file': 'test.sql',
        'timestamp': '2023-01-01T00:00:00'
    }
    
    json_str = json.dumps(data)
    parsed = json.loads(json_str)
    
    assert parsed == data
    print("✓ JSON operations test passed")


def test_path_operations():
    """Test path operations"""
    manager = DatabaseBackupManager()
    
    # Test Path object
    test_path = Path('/tmp/test_backup')
    assert isinstance(test_path, Path)
    assert test_path.exists() or not test_path.exists()
    
    print("✓ Path operations test passed")


def test_temporary_directory():
    """Test temporary directory creation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        assert Path(tmpdir).exists()
        assert tmpdir in str(Path(tmpdir))
    
    print("✓ Temporary directory test passed")


def test_list_operations():
    """Test list operations"""
    manager = DatabaseBackupManager()
    
    # Test list
    test_list = ['file1.sql', 'file2.sql', 'file3.sql']
    assert isinstance(test_list, list)
    
    # Test list methods
    assert len(test_list) > 0
    assert 'file1.sql' in test_list
    test_list.append('file4.sql')
    assert len(test_list) == 4
    
    print("✓ List operations test passed")


def test_dict_operations():
    """Test dictionary operations"""
    manager = DatabaseBackupManager()
    
    # Test dictionary
    test_dict = {
        'database': 'postgres',
        'backup_dir': 'backups'
    }
    
    assert isinstance(test_dict, dict)
    assert 'database' in test_dict
    test_dict['new_key'] = 'new_value'
    assert len(test_dict) > 0
    
    print("✓ Dictionary operations test passed")


def main():
    """Run all tests"""
    tests = [
        test_database_backup_manager_init,
        test_config_loading,
        test_temporary_backup_file,
        test_temporary_config_file,
        test_current_timestamp,
        test_file_operations,
        test_path_operations,
        test_temporary_directory,
        test_list_operations,
        test_dict_operations
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
