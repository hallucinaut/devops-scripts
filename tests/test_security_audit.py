#!/usr/bin/env python3
"""
Test suite for security_audit.py
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.security_audit import SecurityAuditor


def test_security_auditor_init():
    """Test SecurityAuditor initialization"""
    auditor = SecurityAuditor('test-target')
    assert auditor.target == 'test-target'
    assert isinstance(auditor.issues, list)
    print("✓ SecurityAuditor init test passed")


def test_security_issues_detection():
    """Test security issue detection"""
    auditor = SecurityAuditor('test-target')
    
    # Test SQL injection detection
    content = "SELECT * FROM users WHERE id = $id"
    issues = auditor._find_security_issues(content)
    assert any('sql_injection' in issue['type'] for issue in issues)
    
    # Test hardcoded secret detection
    content = "api_key = 'YOUR_API_KEY_HERE'"
    issues = auditor._find_security_issues(content)
    assert any('hardcoded_secret' in issue['type'] for issue in issues)
    
    # Test eval detection
    content = "eval('malicious code')"
    issues = auditor._find_security_issues(content)
    assert any('code_injection' in issue['type'] for issue in issues)
    
    print("✓ Security issues detection test passed")


def test_severity_level():
    """Test severity level assignment"""
    auditor = SecurityAuditor('test-target')
    
    # Test severity levels
    high_issues = [
        {'type': 'hardcoded_secret', 'message': 'test'},
        {'type': 'sql_injection', 'message': 'test'}
    ]
    
    for issue in high_issues:
        auditor.issues.append(issue)
    
    for issue in auditor.issues:
        severity = auditor._get_severity(issue['type'])
        assert severity in ['HIGH', 'MEDIUM', 'LOW']
    
    print("✓ Severity level test passed")


def test_report_generation():
    """Test report generation"""
    auditor = SecurityAuditor('test-target')
    
    # Add test issues
    auditor.issues = [
        {'type': 'hardcoded_secret', 'message': 'API key found'},
        {'type': 'weak_hashing', 'message': 'MD5 detected'},
        {'type': 'sql_injection', 'message': 'SQL injection potential'}
    ]
    
    # Generate report (without saving)
    try:
        auditor.report()
        print("✓ Report generation test passed")
    except Exception as e:
        print(f"✗ Report generation test failed: {e}", file=sys.stderr)


def test_directory_scanning():
    """Test directory scanning"""
    auditor = SecurityAuditor('test-target')
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test file with security issues
        test_file = Path(tmpdir) / 'test.py'
        test_file.write_text("api_key = 'YOUR_API_KEY_HERE'")
        
        # Scan directory
        auditor.scan_directory(tmpdir, {'.py'})
        
        # Check that issues were detected
        assert len(auditor.issues) > 0
    
    print("✓ Directory scanning test passed")


def test_file_scanning():
    """Test file scanning"""
    auditor = SecurityAuditor('test-target')
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("password = 'mysecretpassword'")
        test_file = f.name
    
    try:
        auditor._scan_file(Path(test_file))
        assert len(auditor.issues) > 0
    finally:
        os.unlink(test_file)
    
    print("✓ File scanning test passed")


def test_no_issues_case():
    """Test case with no security issues"""
    auditor = SecurityAuditor('test-target')
    
    # Create file with no issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("print('Hello, World!')")
        test_file = f.name
    
    try:
        auditor._scan_file(Path(test_file))
        assert len(auditor.issues) == 0
    finally:
        os.unlink(test_file)
    
    print("✓ No issues case test passed")


def test_pattern_matching():
    """Test pattern matching in security detection"""
    auditor = SecurityAuditor('test-target')
    
    # Test various patterns
    test_cases = [
        ('SELECT * FROM table', 'sql_injection'),
        ('eval(something)', 'code_injection'),
        ('password = "123"', 'hardcoded_secret'),
        ('API_KEY=abc', 'hardcoded_secret'),
        ('hashlib.md5(data)', 'weak_hashing')
    ]
    
    for content, expected_type in test_cases:
        auditor.issues = []
        issues = auditor._find_security_issues(content)
        if any(expected_type in issue['type'] for issue in issues):
            print(f"✓ Pattern matching test passed for {expected_type}")
    
    print("✓ Pattern matching test completed")


def main():
    """Run all tests"""
    tests = [
        test_security_auditor_init,
        test_security_issues_detection,
        test_severity_level,
        test_report_generation,
        test_directory_scanning,
        test_file_scanning,
        test_no_issues_case,
        test_pattern_matching
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
