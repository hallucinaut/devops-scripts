#!/usr/bin/env python3
"""
Security Audit Script
Performs security checks and vulnerability scanning
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set
import re


class SecurityAuditor:
    """Security audit and vulnerability scanner"""
    
    def __init__(self, target: str):
        self.target = target
        self.issues: List[Dict[str, str]] = []
    
    def scan_directory(self, directory: str, extensions: Optional[Set[str]] = None):
        """Scan directory for security issues"""
        if extensions is None:
            extensions = {'.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.sh'}
        
        directory = Path(directory)
        
        if not directory.exists():
            print(f"Directory not found: {directory}")
            return
        
        print(f"Scanning directory: {directory}")
        
        for file in directory.rglob('*'):
            if file.is_file() and file.suffix.lower() in extensions:
                self._scan_file(file)
    
    def _scan_file(self, file_path: Path):
        """Scan individual file for security issues"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            issues = self._find_security_issues(content)
            
            if issues:
                for issue in issues:
                    issue['file'] = str(file_path)
                    issue['severity'] = self._get_severity(issue['type'])
                    self.issues.append(issue)
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
    
    def _find_security_issues(self, content: str) -> List[Dict[str, str]]:
        """Find security issues in content"""
        issues = []
        
        # Check for hardcoded secrets
        secrets = [
            r'(api[_-]?key|secret|token|password|auth[_-]?token)\s*[:=]\s*["\']',
            r'password\s*[:=]\s*[\'"]',
            r'api[_-]?key\s*[:=]\s*[\'"]',
            r'token\s*[:=]\s*[\'"]',
        ]
        
        for pattern in secrets:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append({
                    'type': 'hardcoded_secret',
                    'message': f'Potential hardcoded {pattern.split()[0]} found'
                })
        
        # Check for SQL injection vulnerabilities
        if re.search(r'(SELECT|INSERT|UPDATE|DELETE|DROP|TRUNCATE)\s+\*', content, re.IGNORECASE):
            issues.append({
                'type': 'sql_injection',
                'message': 'Potential SQL injection vulnerability'
            })
        
        # Check for eval usage
        if re.search(r'\beval\s*\(', content, re.IGNORECASE):
            issues.append({
                'type': 'code_injection',
                'message': 'Potential eval usage detected'
            })
        
        # Check for eval usage
        if re.search(r'\bexec\s*\(', content, re.IGNORECASE):
            issues.append({
                'type': 'code_injection',
                'message': 'Potential exec usage detected'
            })
        
        # Check for insecure file operations
        if re.search(r'file.*writ', content, re.IGNORECASE):
            issues.append({
                'type': 'insecure_file_operation',
                'message': 'Potential insecure file operation'
            })
        
        # Check for weak hashing
        if re.search(r'(md5|md4|sha1)', content, re.IGNORECASE):
            issues.append({
                'type': 'weak_hashing',
                'message': 'Potential weak hashing algorithm detected'
            })
        
        return issues
    
    def _get_severity(self, issue_type: str) -> str:
        """Get severity level for issue type"""
        high_severity = {'hardcoded_secret', 'sql_injection', 'code_injection'}
        medium_severity = {'weak_hashing', 'insecure_file_operation'}
        
        if issue_type in high_severity:
            return 'HIGH'
        elif issue_type in medium_severity:
            return 'MEDIUM'
        return 'LOW'
    
    def run_nessus_scan(self, target: str):
        """Run Nessus vulnerability scan"""
        try:
            print(f"Running Nessus scan on {target}")
            subprocess.run(
                ['nessus', '-X', f'scan={target}'],
                check=True
            )
            print("✓ Nessus scan completed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ Nessus not available or scan failed")
    
    def run_openvas_scan(self, target: str):
        """Run OpenVAS vulnerability scan"""
        try:
            print(f"Running OpenVAS scan on {target}")
            subprocess.run(
                ['gvm-cli --gmp-username admin --gmp-password password --socket /var/run/gvm/gvmd.sock --execute-commands',
                 f'scanner-info-get-scanners'],
                check=True
            )
            print("✓ OpenVAS scan completed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ OpenVAS not available or scan failed")
    
    def run_snyk_scan(self, project_dir: str):
        """Run Snyk vulnerability scan"""
        try:
            print(f"Running Snyk scan for {project_dir}")
            subprocess.run(
                ['snyk', 'test', '--file', project_dir],
                check=True
            )
            print("✓ Snyk scan completed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ Snyk not available or scan failed")
    
    def report(self, output_file: Optional[str] = None):
        """Generate security audit report"""
        print("\n" + "="*50)
        print("SECURITY AUDIT REPORT")
        print("="*50)
        
        if not self.issues:
            print("✓ No security issues found")
            return
        
        # Group by severity
        by_severity = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for issue in self.issues:
            severity = issue.get('severity', 'LOW')
            if severity in by_severity:
                by_severity[severity].append(issue)
        
        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            if by_severity[severity]:
                print(f"\n{severity}-Severity Issues ({len(by_severity[severity])}):")
                print("-" * 50)
                for issue in by_severity[severity]:
                    print(f"  [{issue['type']}] {issue['message']}")
                    print(f"    File: {issue['file']}")
                    print()
        
        # Save report
        if output_file:
            report = {
                'summary': {
                    'total_issues': len(self.issues),
                    'high': len(by_severity['HIGH']),
                    'medium': len(by_severity['MEDIUM']),
                    'low': len(by_severity['LOW'])
                },
                'issues': self.issues
            }
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\nReport saved to: {output_file}")
    
    def check_dependencies(self, package_file: str = 'package.json'):
        """Check for vulnerable dependencies"""
        if not os.path.exists(package_file):
            print(f"No {package_file} found")
            return
        
        print(f"Checking {package_file} for vulnerabilities...")
        
        if package_file.endswith('.json'):
            # Simple check for package.json
            try:
                with open(package_file) as f:
                    data = json.load(f)
                
                dependencies = list(data.get('dependencies', {}).keys())
                dev_dependencies = list(data.get('devDependencies', {}).keys())
                
                print(f"  Dependencies: {len(dependencies)}")
                print(f"  Dev Dependencies: {len(dev_dependencies)}")
                
                # Run npm audit
                try:
                    subprocess.run(['npm', 'audit'], check=True)
                except subprocess.CalledProcessError:
                    print("  ⚠ Vulnerabilities found (run 'npm audit fix')")
                
            except json.JSONDecodeError:
                pass


def main():
    parser = argparse.ArgumentParser(description='Security Audit Script')
    parser.add_argument('--target', help='Target directory or URL')
    parser.add_argument('--scan', choices=['directory', 'web', 'container'],
                       help='Scan type')
    parser.add_argument('--directory', help='Directory to scan')
    parser.add_argument('--file', help='File to scan')
    parser.add_argument('--nessus', action='store_true', help='Run Nessus scan')
    parser.add_argument('--openvas', action='store_true', help='Run OpenVAS scan')
    parser.add_argument('--snyk', action='store_true', help='Run Snyk scan')
    parser.add_argument('--package', help='Package file (package.json, requirements.txt)')
    parser.add_argument('--report', type=str, help='Output report file')
    
    args = parser.parse_args()
    
    auditor = SecurityAuditor(args.target or '.')
    
    if args.scan == 'directory':
        auditor.scan_directory(args.directory or '.')
    elif args.scan == 'web':
        print("Web vulnerability scanning...")
        # Would integrate with OWASP ZAP or similar
        print("  Web scanning requires additional tools")
    elif args.scan == 'container':
        print("Container scanning...")
        # Would integrate with Trivy or similar
        print("  Container scanning requires additional tools")
    
    if args.package:
        auditor.check_dependencies(args.package)
    
    if args.nessus:
        auditor.run_nessus_scan(args.target or '.')
    
    if args.openvas:
        auditor.run_openvas_scan(args.target or '.')
    
    if args.snyk:
        auditor.run_snyk_scan(args.directory or '.')
    
    auditor.report(args.report)


if __name__ == '__main__':
    main()
