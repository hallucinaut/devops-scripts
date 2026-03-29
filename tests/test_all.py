#!/usr/bin/env python3
"""
Master test runner for all DevOps scripts
"""

import sys
import subprocess
from pathlib import Path


def run_test_file(test_path: str) -> bool:
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {test_path}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_path}: {e}", file=sys.stderr)
        return False


def main():
    """Run all tests"""
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # List of test files
    test_files = [
        'test_provision_infrastructure.py',
        'test_k8s_deploy.py',
        'test_docker_manager.py',
        'test_security_audit.py',
        'test_database_backup.py',
        'test_git_operations.py',
        'test_terraform_manager.py',
        'test_config_manager.py'
    ]
    
    all_passed = True
    failed_tests = []
    
    for test_file in test_files:
        test_path = script_dir / test_file
        if test_path.exists():
            if not run_test_file(str(test_path)):
                all_passed = False
                failed_tests.append(test_file)
        else:
            print(f"⚠ Test file not found: {test_file}")
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if all_passed:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"✗ {len(failed_tests)} test(s) failed:")
        for test in failed_tests:
            print(f"  - {test}")
        sys.exit(1)


if __name__ == '__main__':
    main()
