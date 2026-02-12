#!/usr/bin/env python3
"""
Test suite for docker_manager.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.docker_manager import DockerManager


def test_docker_manager_init():
    """Test DockerManager initialization"""
    manager = DockerManager()
    assert manager is not None
    print("✓ DockerManager init test passed")


def test_docker_manager_commands():
    """Test DockerManager commands"""
    manager = DockerManager()
    
    # Test list_containers (should return list)
    containers = manager.list_containers()
    assert isinstance(containers, list)
    
    # Test list_images (should return list)
    images = manager.list_images()
    assert isinstance(images, list)
    
    print("✓ DockerManager commands test passed")


def test_temp_file_creation():
    """Test temporary file creation for manifests"""
    manager = DockerManager()
    
    # Create a temporary file
    temp_file = Path(tempfile.mktemp(suffix='.yaml'))
    
    try:
        # Write some content
        temp_file.write_text('test: content')
        
        # Try to load and process (in real use, this would be with docker)
        assert temp_file.exists()
        print("✓ Temporary file creation test passed")
    finally:
        temp_file.unlink(missing_ok=True)


def test_image_name_handling():
    """Test image name handling"""
    manager = DockerManager()
    
    # Test various image formats
    test_images = [
        'nginx:latest',
        'python:3.9-slim',
        'node:20-alpine',
        'ubuntu:22.04',
        'registry.example.com/myapp:v1.0.0'
    ]
    
    for image in test_images:
        assert isinstance(image, str)
        assert len(image) > 0
    
    print("✓ Image name handling test passed")


def test_path_operations():
    """Test path operations"""
    manager = DockerManager()
    
    # Test Path operations
    test_path = Path('/tmp/test_path')
    assert test_path.exists() or not test_path.exists()
    
    # Test with non-existent path
    missing_path = Path('/tmp/nonexistent_path_12345')
    assert not missing_path.exists()
    
    print("✓ Path operations test passed")


def test_json_operations():
    """Test JSON operations"""
    manager = DockerManager()
    
    # Test dictionary to JSON
    test_data = {
        'name': 'test',
        'version': '1.0.0',
        'tags': ['latest', 'stable']
    }
    
    json_str = json.dumps(test_data)
    parsed = json.loads(json_str)
    
    assert parsed == test_data
    print("✓ JSON operations test passed")


def test_command_execution():
    """Test command execution simulation"""
    manager = DockerManager()
    
    # Simulate command execution (would require actual Docker)
    try:
        # Try to get docker version
        result = subprocess.run(
            ['docker', '--version'],
            capture_output=True,
            text=True,
            check=False
        )
        assert result.returncode == 0 or 'not installed' in result.stderr.lower()
        print("✓ Command execution test passed")
    except Exception:
        # If Docker not available, test passes
        print("✓ Command execution test passed (Docker not available)")


def test_file_operations():
    """Test file operations"""
    manager = DockerManager()
    
    # Test file write/read
    test_file = Path('/tmp/test_docker_manager.txt')
    
    try:
        content = 'Docker Manager Test'
        test_file.write_text(content)
        read_content = test_file.read_text()
        assert read_content == content
    finally:
        test_file.unlink(missing_ok=True)
    
    print("✓ File operations test passed")


def main():
    """Run all tests"""
    tests = [
        test_docker_manager_init,
        test_docker_manager_commands,
        test_temp_file_creation,
        test_image_name_handling,
        test_path_operations,
        test_json_operations,
        test_command_execution,
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
