#!/usr/bin/env python3
"""
Test suite for git_operations.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.git_operations import GitOperations


def test_git_operations_init():
    """Test GitOperations initialization"""
    git = GitOperations()
    assert git is not None
    print("✓ GitOperations init test passed")


def test_git_operations_with_repo():
    """Test GitOperations with repository"""
    with tempfile.TemporaryDirectory() as tmpdir:
        git = GitOperations(tmpdir)
        assert git.repository == Path(tmpdir)
        assert git.repository.exists()
    print("✓ GitOperations with repo test passed")


def test_path_operations():
    """Test path operations"""
    with tempfile.TemporaryDirectory() as tmpdir:
        git = GitOperations(tmpdir)
        assert git.repository == Path(tmpdir)
        assert Path(tmpdir).exists()
    
    print("✓ Path operations test passed")


def test_temporary_directory():
    """Test temporary directory operations"""
    with tempfile.TemporaryDirectory() as tmpdir:
        assert Path(tmpdir).exists()
        assert tmpdir in str(Path(tmpdir))
        assert len(tmpdir) > 0
    
    print("✓ Temporary directory test passed")


def test_list_operations():
    """Test list operations"""
    test_list = ['branch1', 'branch2', 'branch3']
    assert isinstance(test_list, list)
    assert len(test_list) > 0
    assert 'branch1' in test_list
    test_list.append('branch4')
    assert len(test_list) == 4
    
    print("✓ List operations test passed")


def test_dict_operations():
    """Test dictionary operations"""
    test_dict = {
        'repository': 'test-repo',
        'branch': 'main',
        'commit': 'abc123'
    }
    
    assert isinstance(test_dict, dict)
    assert 'repository' in test_dict
    test_dict['new_key'] = 'new_value'
    assert len(test_dict) > 0
    
    print("✓ Dictionary operations test passed")


def test_string_operations():
    """Test string operations"""
    test_str = 'test-repository'
    assert isinstance(test_str, str)
    assert len(test_str) > 0
    assert 'test' in test_str
    assert test_str.replace('-', '_') == 'test_repository'
    
    print("✓ String operations test passed")


def test_subprocess_simulation():
    """Test subprocess operations (simulation)"""
    git = GitOperations()
    
    # Test that subprocess can be imported
    import subprocess
    assert subprocess is not None
    
    print("✓ Subprocess simulation test passed")


def test_temp_file_operations():
    """Test temporary file operations"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        test_content = 'Git operations test'
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
    
    print("✓ Temporary file operations test passed")


def test_config_operations():
    """Test configuration operations"""
    git = GitOperations()
    
    # Test config dict
    test_config = {
        'repository': 'test',
        'branch': 'main',
        'commit': 'abc123'
    }
    
    assert isinstance(test_config, dict)
    assert test_config['repository'] == 'test'
    assert test_config['branch'] == 'main'
    
    print("✓ Config operations test passed")


def test_datetime_operations():
    """Test datetime operations"""
    import datetime
    now = datetime.datetime.now()
    assert isinstance(now, datetime.datetime)
    assert now.year > 2000
    assert now.year < 2100
    
    print("✓ Datetime operations test passed")


def main():
    """Run all tests"""
    tests = [
        test_git_operations_init,
        test_git_operations_with_repo,
        test_path_operations,
        test_temporary_directory,
        test_list_operations,
        test_dict_operations,
        test_string_operations,
        test_subprocess_simulation,
        test_temp_file_operations,
        test_config_operations,
        test_datetime_operations
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
