#!/usr/bin/env python3
"""
CI/CD Pipeline Generator
Generates GitHub Actions, GitLab CI, or Jenkins pipeline configurations
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class PipelineGenerator:
    """CI/CD pipeline configuration generator"""
    
    def __init__(self, platform: str):
        self.platform = platform.lower()
        self.config = {
            'name': 'CI/CD Pipeline',
            'on': {
                'push': {'branches': ['main', 'master', 'develop']},
                'pull_request': {'branches': ['main', 'master']}
            },
            'jobs': {}
        }
    
    def add_job(self, name: str, image: str, steps: List[Dict], needs: Optional[List[str]] = None):
        """Add a job to the pipeline"""
        self.config['jobs'][name] = {
            'runs-on': self._get_runner(image),
            'steps': steps
        }
        if needs:
            self.config['jobs'][name]['needs'] = needs
    
    def _get_runner(self, image: str) -> str:
        """Determine runner based on image"""
        if 'windows' in image.lower() or 'windows' in image.lower():
            return 'windows-latest'
        return 'ubuntu-latest'
    
    def generate_github_actions(self, output_path: str):
        """Generate GitHub Actions workflow file"""
        if not output_path.endswith('.yml'):
            output_path += '.yml'
        
        workflow_dir = Path(output_path).parent
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        
        print(f"✓ GitHub Actions workflow generated: {output_path}")
    
    def generate_gitlab_ci(self, output_path: str):
        """Generate GitLab CI configuration file"""
        if not output_path.endswith('.yml'):
            output_path += '.yml'
        
        with open(output_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        
        print(f"✓ GitLab CI configuration generated: {output_path}")
    
    def generate_jenkinsfile(self, output_path: str):
        """Generate Jenkins pipeline configuration"""
        if not output_path.endswith('.groovy'):
            output_path += '.groovy'
        
        with open(output_path, 'w') as f:
            f.write("// Jenkins Pipeline\n")
            for job_name, job_config in self.config['jobs'].items():
                f.write(f"pipeline {{\n")
                f.write(f"  agent {{\n")
                f.write(f"    label \"{job_config['runs-on']}\"\n")
                f.write(f"  }}\n")
                f.write(f"  stages {{\n")
                for step in job_config['steps']:
                    self._write_jenkins_step(f, step)
                f.write(f"  }}\n")
                f.write(f"}}\n")
        
        print(f"✓ Jenkinsfile generated: {output_path}")
    
    def _write_jenkins_step(self, f, step: Dict):
        """Write a Jenkins step"""
        if 'checkout' in step.get('name', '').lower():
            f.write(f"    stage('Checkout') {{\n")
            f.write(f"      steps {{\n")
            f.write(f"        git url: '{step['uses']}', branch: 'main'\n")
            f.write(f"      }}\n")
            f.write(f"    }}\n")
        elif 'run' in step.get('name', '').lower() or 'execute' in step.get('name', '').lower():
            cmd = step.get('run', '').replace(' ', ' ')
            f.write(f"    stage('{step['name']}') {{\n")
            f.write(f"      steps {{\n")
            f.write(f"        sh '{cmd}'\n")
            f.write(f"      }}\n")
            f.write(f"    }}\n")
    
    def add_lint_job(self, language: str):
        """Add linting job"""
        self.add_job(
            'lint',
            f'node:20',
            [
                {'name': 'Checkout', 'uses': 'actions/checkout@v3'},
                {'name': 'Lint', 'run': f'npm run lint'}
            ]
        )
    
    def add_test_job(self, language: str):
        """Add testing job"""
        self.add_job(
            'test',
            f'node:20',
            [
                {'name': 'Checkout', 'uses': 'actions/checkout@v3'},
                {'name': 'Install', 'run': 'npm install'},
                {'name': 'Test', 'run': 'npm test'}
            ]
        )
    
    def add_deploy_job(self, environment: str, image_tag: str):
        """Add deployment job"""
        deploy_steps = [
            {'name': 'Checkout', 'uses': 'actions/checkout@v3'},
            {'name': 'Deploy', 'run': f'kubectl apply -f k8s/{environment}'}
        ]
        
        self.add_job(
            'deploy',
            f'node:20',
            deploy_steps,
            needs=['lint', 'test']
        )


def main():
    parser = argparse.ArgumentParser(description='CI/CD Pipeline Generator')
    parser.add_argument('--platform', required=True, choices=['github', 'gitlab', 'jenkins'],
                       help='CI/CD platform')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--add-lint', action='store_true', help='Add lint job')
    parser.add_argument('--add-test', action='store_true', help='Add test job')
    parser.add_argument('--add-deploy', action='store_true', help='Add deploy job')
    parser.add_argument('--language', default='nodejs', help='Programming language')
    parser.add_argument('--environment', default='dev', help='Deployment environment')
    parser.add_argument('--image-tag', default='latest', help='Docker image tag')
    
    args = parser.parse_args()
    
    generator = PipelineGenerator(args.platform)
    
    # Add default jobs
    if args.add_lint:
        generator.add_lint_job(args.language)
    
    if args.add_test:
        generator.add_test_job(args.language)
    
    if args.add_deploy:
        generator.add_deploy_job(args.environment, args.image_tag)
    
    # Generate output
    if args.platform == 'github':
        generator.generate_github_actions(args.output)
    elif args.platform == 'gitlab':
        generator.generate_gitlab_ci(args.output)
    elif args.platform == 'jenkins':
        generator.generate_jenkinsfile(args.output)


if __name__ == '__main__':
    main()
