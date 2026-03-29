# DevOps Python Scripts

A comprehensive collection of **10 Python scripts** for DevOps operations. All scripts are well-documented, type-annotated, and include comprehensive tests. These scripts serve as **examples and templates** for various DevOps tasks.

## Overview

This repository provides example implementations of common DevOps operations using Python. Each script demonstrates best practices, error handling, and command-line interface design that can be adapted to your specific needs.

## Scripts

### 1. provision_infrastructure.py
Manages cloud infrastructure provisioning for AWS, GCP, and Azure.
- Multi-cloud provider support
- VPC, subnet, and cluster creation
- Environment-specific configurations
- Examples showing provider abstractions

**Usage:**
```bash
python scripts/provision_infrastructure.py --provider aws --mode provision
```

### 2. k8s_deploy.py
Handles Kubernetes deployments, services, and configurations.
- Deployment, service, ConfigMap, and Secret management
- YAML manifest generation
- Namespace support

**Usage:**
```bash
python scripts/k8s_deploy.py --namespace production --deploy --deployment myapp
```

### 3. docker_manager.py
Manages Docker containers and images.
- Container lifecycle management (run, stop, remove)
- Image building and operations
- Log viewing and resource cleanup

**Usage:**
```bash
python scripts/docker_manager.py run --image nginx --name webserver
```

### 4. cicd_generator.py
Generates CI/CD pipeline configurations.
- GitHub Actions, GitLab CI, and Jenkins pipeline generation
- Customizable job templates
- Platform-specific configurations

**Usage:**
```bash
python scripts/cicd_generator.py --platform github --output .github/workflows/ci.yml
```

### 5. monitoring.py
System metrics collection and log monitoring.
- CPU, memory, disk, and network monitoring
- Process information
- Docker container logs
- Continuous monitoring loop

**Usage:**
```bash
python scripts/monitoring.py --monitor --interval 5 --duration 300
```

### 6. security_audit.py
Security vulnerability scanning and auditing.
- Hardcoded secrets detection
- SQL injection vulnerability checks
- Code injection detection
- Weak hashing algorithm detection

**Usage:**
```bash
python scripts/security_audit.py --scan directory --directory ./src
```

### 7. database_backup.py
Database backup and restore operations.
- PostgreSQL, MySQL, MongoDB, and SQLite support
- Backup compression
- Automated cleanup

**Usage:**
```bash
python scripts/database_backup.py --database postgresql --name mydb
```

### 8. git_operations.py
Git workflow automation.
- Commit, push, and pull operations
- Branch management
- Status monitoring

**Usage:**
```bash
python scripts/git_operations.py commit --message "Update configuration"
```

### 9. terraform_manager.py
Terraform configuration management.
- Terraform operations (init, plan, apply, destroy)
- State management
- Configuration validation

**Usage:**
```bash
python scripts/terraform_manager.py --dir terraform apply --auto-approve
```

### 10. config_manager.py
Configuration file management.
- Config file backup and restore
- Environment variable management
- YAML/JSON/INI support

**Usage:**
```bash
python scripts/config_manager.py env set --key API_KEY --value your_api_key_here
```

## Testing

All scripts include comprehensive test suites:

```bash
# Run all tests
python tests/test_all.py

# Run specific test file
python tests/test_provision_infrastructure.py
python tests/test_k8s_deploy.py
python tests/test_docker_manager.py
python tests/test_security_audit.py
python tests/test_database_backup.py
python tests/test_git_operations.py
python tests/test_terraform_manager.py
python tests/test_config_manager.py
```

## Installation

### Requirements

```bash
pip install -r requirements.txt
```

### Dependencies

- Python 3.7+
- PyYAML 6.0+

### Optional Dependencies

For full functionality with all providers:
- boto3 (AWS)
- google-cloud-storage (GCP)
- azure-storage-blob (Azure)
- psycopg2-binary (PostgreSQL)
- mysql-connector-python (MySQL)
- pymongo (MongoDB)
- docker (Docker SDK)
- kubernetes (Kubernetes client)

## Directory Structure

```
.
├── scripts/                 # All Python scripts
│   ├── provision_infrastructure.py
│   ├── k8s_deploy.py
│   ├── docker_manager.py
│   ├── cicd_generator.py
│   ├── monitoring.py
│   ├── security_audit.py
│   ├── database_backup.py
│   ├── git_operations.py
│   ├── terraform_manager.py
│   └── config_manager.py
├── docs/                   # Documentation
│   ├── provision_infrastructure.md
│   ├── k8s_deploy.md
│   ├── docker_manager.md
│   ├── cicd_generator.md
│   ├── monitoring.md
│   ├── security_audit.md
│   ├── database_backup.md
│   ├── git_operations.md
│   ├── terraform_manager.md
│   └── config_manager.md
├── tests/                   # Test files
│   ├── test_provision_infrastructure.py
│   ├── test_k8s_deploy.py
│   ├── test_docker_manager.py
│   ├── test_security_audit.py
│   ├── test_database_backup.py
│   ├── test_git_operations.py
│   ├── test_terraform_manager.py
│   ├── test_config_manager.py
│   └── test_all.py
├── logs/                    # Output directory for logs
├── backups/                 # Backup directory
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Documentation

Each script includes comprehensive documentation with:
- Usage examples
- Command reference
- Configuration details
- Architecture diagrams
- Workflow sequences

### Detailed Documentation

- [provision_infrastructure.md](docs/provision_infrastructure.md) - Cloud infrastructure provisioning
- [k8s_deploy.md](docs/k8s_deploy.md) - Kubernetes deployment management
- [docker_manager.md](docs/docker_manager.md) - Docker container operations
- [cicd_generator.md](docs/cicd_generator.md) - CI/CD pipeline generation
- [monitoring.md](docs/monitoring.md) - System monitoring and logging
- [security_audit.md](docs/security_audit.md) - Security vulnerability scanning
- [database_backup.md](docs/database_backup.md) - Database backup and restore
- [git_operations.md](docs/git_operations.md) - Git workflow automation
- [terraform_manager.md](docs/terraform_manager.md) - Terraform configuration management
- [config_manager.md](docs/config_manager.md) - Configuration file management

## Contributing

1. Add your script to the `scripts/` directory
2. Include comprehensive docstrings
3. Add type annotations
4. Create corresponding tests in `tests/`
5. Add documentation in `docs/`
6. Update this README

## Usage as Examples

These scripts are designed as **examples and templates** that demonstrate:
- Clean, modular Python code
- Proper error handling
- Command-line interface design
- Type annotations
- Comprehensive testing
- Documentation standards

You can:
- **Learn** by studying the implementations
- **Adapt** the scripts to your specific needs
- **Extend** with additional features
- **Reference** for similar operations

## Best Practices

1. **Always review** the code before using in production
2. **Customize** configurations to your environment
3. **Test thoroughly** in development before deployment
4. **Add logging** for production use
5. **Implement error handling** appropriate to your use case
6. **Securely manage** credentials and sensitive data
7. **Monitor** script outputs and logs
8. **Document** any customizations made

## License

This project is provided as-is for educational and reference purposes.

## Support

For issues or questions:
1. Review the inline documentation in each script
2. Check the detailed documentation in `docs/`
3. Examine the test files for usage examples
4. Create an issue in the repository

## Features

- **10 complete scripts** demonstrating DevOps operations
- **8 test files** with comprehensive test coverage
- **10 detailed documentation files** with mermaid diagrams
- **Type annotations** throughout all scripts
- **Error handling** for common scenarios
- **Command-line interfaces** with argparse
- **Logging capabilities**
- **Modular design** for easy customization
- **Extensive examples** and usage patterns

## Examples

### Example 1: Container Management

```bash
python scripts/docker_manager.py \
    build \
    --dockerfile Dockerfile \
    --tag myapp:latest

python scripts/docker_manager.py \
    run \
    --image myapp:latest \
    --name myapp \
    --port 8080:8080
```

### Example 2: Infrastructure Provisioning

```bash
python scripts/provision_infrastructure.py \
    --provider aws \
    --mode provision \
    --project-id my-project
```

### Example 3: Monitoring

```bash
python scripts/monitoring.py \
    --monitor \
    --interval 5 \
    --duration 60
```

## Getting Started

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Review the scripts** in `scripts/`
4. **Run the tests**: `python tests/test_all.py`
5. **Customize** as needed for your use case

## Notes

These scripts are **example implementations** designed to demonstrate:
- Python programming best practices
- DevOps automation techniques
- Command-line tool design
- Testing and documentation standards

Use them as **reference implementations** and adapt them to suit your specific needs. They are not production-ready out-of-the-box and may require additional configuration and testing for actual deployment.
