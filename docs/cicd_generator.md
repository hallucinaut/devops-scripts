# cicd_generator.py

## Overview

The `cicd_generator.py` script generates CI/CD pipeline configurations for popular platforms including GitHub Actions, GitLab CI, and Jenkins. It provides automated pipeline creation with support for multiple stages and jobs.

## Features

- GitHub Actions workflow generation
- GitLab CI configuration generation
- Jenkins pipeline generation
- Customizable job templates
- Environment-specific configurations
- Multi-stage pipeline support

## Mermaid Diagram

```mermaid
flowchart TD
    A[Start: CI/CD Generator] --> B{Select Platform}
    B -->|GitHub Actions| C[GitHub Actions Generator]
    B -->|GitLab CI| D[GitLab CI Generator]
    B -->|Jenkins| E[Jenkins Generator]

    C --> F[Parse Requirements]
    F --> G[Create Workflow File]
    G --> H[Generate Jobs]
    H --> I[Write YAML]
    I --> J[Return Result]

    D --> K[Parse Requirements]
    K --> L[Create Pipeline File]
    L --> M[Generate Stages]
    M --> N[Write YAML]
    N --> O[Return Result]

    E --> P[Parse Requirements]
    P --> Q[Create Jenkinsfile]
    Q --> R[Generate Pipeline]
    R --> S[Write Groovy]
    S --> T[Return Result]

    J --> U[End]
    O --> U
    T --> U
```

## Usage

### Generate GitHub Actions Workflow

```bash
python scripts/cicd_generator.py \
    --platform github \
    --output .github/workflows/ci.yml \
    --add-lint \
    --add-test \
    --add-deploy
```

### Generate GitLab CI Configuration

```bash
python scripts/cicd_generator.py \
    --platform gitlab \
    --output .gitlab-ci.yml \
    --add-lint \
    --add-test
```

### Generate Jenkins Pipeline

```bash
python scripts/cicd_generator.py \
    --platform jenkins \
    --output Jenkinsfile \
    --add-lint \
    --add-deploy
```

### With Custom Configuration

```bash
python scripts/cicd_generator.py \
    --platform github \
    --output .github/workflows/ci.yml \
    --add-lint \
    --add-test \
    --add-deploy \
    --language python \
    --environment production \
    --image-tag v1.0.0
```

## Commands

### GitHub Actions

```bash
python scripts/cicd_generator.py \
    --platform github \
    --output .github/workflows/ci.yml \
    --add-lint \
    --add-test \
    --add-deploy
```

### GitLab CI

```bash
python scripts/cicd_generator.py \
    --platform gitlab \
    --output .gitlab-ci.yml \
    --add-lint \
    --add-test
```

### Jenkins

```bash
python scripts/cicd_generator.py \
    --platform jenkins \
    --output Jenkinsfile \
    --add-lint \
    --add-deploy
```

## Architecture

```mermaid
classDiagram
    class PipelineGenerator {
        -string platform
        -Dict config
        +__init__(platform: str)
        +add_job(name: str, image: str, steps: List, needs: List) None
        +generate_github_actions(output: str) None
        +generate_gitlab_ci(output: str) None
        +generate_jenkinsfile(output: str) None
        +add_lint_job(language: str) None
        +add_test_job(language: str) None
        +add_deploy_job(environment: str, image_tag: str) None
        +_get_runner(image: str) str
        +_write_jenkins_step(f, step) None
    }

    class Job {
        +string name
        +string image
        +List steps
        +List needs
        +string runs_on
    }

    class Step {
        +string name
        +string uses
        +string run
        +Dict with
    }

    PipelineGenerator --> Job
    PipelineGenerator --> Step
```

## Workflow

```mermaid
sequenceDiagram
    participant User
    participant Script
    participant PipelineGenerator
    participant FileIO

    User->>Script: --platform github --output ci.yml
    Script->>PipelineGenerator: PipelineGenerator('github')
    PipelineGenerator->>PipelineGenerator: _get_runner()
    PipelineGenerator->>PipelineGenerator: add_job()
    PipelineGenerator->>PipelineGenerator: _write_jenkins_step()
    PipelineGenerator->>FileIO: generate_github_actions()
    FileIO->>Script: Return path
    Script->>User: Generated file path
```

## GitHub Actions Workflow

### Example Output

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main, master, develop]
  pull_request:
    branches: [main, master]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm test

  deploy:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: kubectl apply -f k8s/production
```

## GitLab CI Configuration

### Example Output

```yaml
name: CI/CD Pipeline

stages:
  - lint
  - test
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  DOCKER_DRIVER: overlay2

lint:
  stage: lint
  image: node:20
  script:
    - npm run lint

test:
  stage: test
  image: node:20
  script:
    - npm install
    - npm test

deploy:
  stage: deploy
  image: node:20
  script:
    - kubectl apply -f k8s/production
  only:
    - main
```

## Jenkins Pipeline

### Example Output

```groovy
pipeline {
    agent {
        label 'node'
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'git@github.com:myorg/myrepo.git', branch: 'main'
            }
        }
        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }
        stage('Test') {
            steps {
                sh 'npm install'
                sh 'npm test'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
```

## Configuration

### Language Support

- JavaScript/Node.js
- Python
- Go
- Ruby
- Java

### Environment Support

- Development
- Staging
- Production

## Return Codes

- `0`: Success
- `1`: Error

## Dependencies

- Python 3.7+
- PyYAML

## Examples

### Complete Pipeline

```bash
# Generate GitHub Actions pipeline
python scripts/cicd_generator.py \
    --platform github \
    --output .github/workflows/ci.yml \
    --add-lint \
    --add-test \
    --add-deploy \
    --language python \
    --environment production \
    --image-tag v1.0.0

# Generate GitLab CI pipeline
python scripts/cicd_generator.py \
    --platform gitlab \
    --output .gitlab-ci.yml \
    --add-lint \
    --add-test

# Generate Jenkins pipeline
python scripts/cicd_generator.py \
    --platform jenkins \
    --output Jenkinsfile \
    --add-lint \
    --add-deploy
```

## Best Practices

1. **Separate** lint, test, and deploy stages
2. **Use** matrix testing for multiple languages/versions
3. **Add** caching for build dependencies
4. **Configure** environment variables
5. **Include** notifications for pipeline status
6. **Use** required checks for main branch
