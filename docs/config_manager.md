# config_manager.py

## Overview

The `config_manager.py` script provides comprehensive configuration file management. It handles backup, restore, environment variable management, file validation, searching, and diffing of configuration files.

## Features

- Configuration file backup and restore
- Environment variable management
- File validation (JSON, YAML, INI)
- Config searching and diffing
- Backup history management
- Custom configuration support

## Mermaid Diagram

```mermaid
flowchart TD
    A[Start: Config Manager] --> B{Select Action}
    B -->|Backup| C[Backup Manager]
    B -->|Restore| D[Restorer]
    B -->|Env| E[Environment Manager]
    B -->|Validate| F[Validator]
    B -->|Diff| G[Diff Viewer]
    B -->|Search| H[Searcher]
    B -->|List| I[Lister]

    C --> J[Parse File Path]
    J --> K[Check File Exists]
    K --> L[Create Backup Path]
    L --> M[Backup File]
    M --> N[Compress If Enabled]
    N --> O[Save Metadata]
    O --> P[Return Result]

    D --> Q[Parse Backup Path]
    Q --> R[Check Backup Exists]
    R --> S[Parse Output Path]
    S --> T[Extract Backup]
    T --> U[Restore File]
    U --> V[Return Result]

    E --> W[Parse Key/Value]
    W --> X[Parse File Path]
    X --> Y[Read File]
    Y --> Z{Key Exists?}
    Z -->|Yes| AA[Update Value]
    Z -->|No| AB[Append Value]
    AA --> AC[Write File]
    AB --> AC

    F --> AD[Parse File Path]
    AD --> AE[Check File Exists]
    AE --> AF{Config Type}
    AF -->|JSON| AG[Validate JSON]
    AF -->|YAML| AH[Validate YAML]
    AF -->|INI| AI[Validate INI]
    AG --> AJ[Return Result]
    AH --> AJ
    AI --> AJ

    G --> AK[Parse File1]
    G --> AL[Parse File2]
    AK --> AM[Check File1 Exists]
    AL --> AN[Check File2 Exists]
    AM --> AO{Both Exist}
    AO -->|Yes| AP[Run Diff Command]
    AP --> AQ[Return Diff Output]
    AO -->|No| AR[Return Error]

    H --> AS[Parse File Path]
    AS --> AT[Check File Exists]
    AT --> AU{File Exists}
    AU -->|Yes| AV[Parse Pattern]
    AV --> AW[Read File]
    AW --> AX{Case Sensitive}
    AX -->|Yes| AY[Search Case Sensitive]
    AX -->|No| AZ[Search Case Insensitive]
    AY --> BA[Return Matches]
    AZ --> BA

    I --> BB[Parse Patterns]
    BB --> BC[Create Glob Patterns]
    BC --> BD[Iterate Files]
    BD --> BE[Collect Files]
    BE --> BF[Sort Files]
    BF --> BG[Return List]

    P --> BH[End]
    V --> BH
    AC --> BH
    AJ --> BH
    AQ --> BH
    BA --> BH
    BG --> BH
```

## Usage

### Backup File

```bash
python scripts/config_manager.py \
    backup \
    --file .env \
    --all
```

### Restore File

```bash
python scripts/config_manager.py \
    restore \
    --file .env.backup.tar.gz \
    --output .env
```

### Set Environment Variable

```bash
python scripts/config_manager.py \
    env \
    set \
    --key API_KEY \
    --value secret123 \
    --file .env
```

### Set with Append

```bash
python scripts/config_manager.py \
    env \
    set \
    --key NEW_KEY \
    --value new_value \
    --file .env \
    --append
```

### Get Environment Variable

```bash
python scripts/config_manager.py \
    env \
    get \
    --key API_KEY \
    --file .env \
    --default default_value
```

### Validate Config File

```bash
python scripts/config_manager.py \
    validate \
    --file config.yaml \
    --type yaml
```

### Diff Files

```bash
python scripts/config_manager.py \
    diff \
    --file1 config1.yaml \
    --file2 config2.yaml
```

### Search Config File

```bash
python scripts/config_manager.py \
    search \
    --file config.yaml \
    --pattern DATABASE_URL \
    --case-sensitive
```

### List Config Files

```bash
python scripts/config_manager.py \
    list \
    --pattern .env* config.*
```

## Commands

### Backup

```bash
python scripts/config_manager.py \
    backup \
    --file .env \
    --all
```

### Restore

```bash
python scripts/config_manager.py \
    restore \
    --file backup.tar.gz \
    --output .env
```

### Env Set

```bash
python scripts/config_manager.py \
    env \
    set \
    --key KEY \
    --value VALUE \
    --file .env
```

### Env Get

```bash
python scripts/config_manager.py \
    env \
    get \
    --key KEY \
    --file .env \
    --default default
```

### Validate

```bash
python scripts/config_manager.py \
    validate \
    --file config.yaml \
    --type yaml
```

### Diff

```bash
python scripts/config_manager.py \
    diff \
    --file1 config1.yaml \
    --file2 config2.yaml
```

### Search

```bash
python scripts/config_manager.py \
    search \
    --file config.yaml \
    --pattern PATTERN
```

### List

```bash
python scripts/config_manager.py \
    list \
    --pattern .env*
```

## Architecture

```mermaid
classDiagram
    class ConfigManager {
        -Path project_dir
        -Path backup_dir
        +__init__(project_dir: str) None
        +backup_file(file_path: str, compression: bool) Optional[str]
        +restore_file(backup_path: str, output_path: Optional) bool
        +backup_all(patterns: Optional) None
        +update_env_var(key: str, value: str, file: str, append: bool) bool
        +get_env_var(key: str, file: str, default: Optional) Optional[str]
        +validate_config(file_path: str, config_type: str) bool
        +diff_config(file1: str, file2: str) None
        +get_config_value(file_path: str, key: str, separator: str) Optional[str]
        +set_config_value(file_path: str, key: str, value: str, separator: str, append: bool) bool
        +list_configs(patterns: Optional) List
        +get_file_hash(file_path: str) Optional[str]
        +search_config(file_path: str, pattern: str, case_sensitive: bool) None
        +_load_config(config_file: str) Dict
    }

    class ConfigFile {
        +string name
        +string path
        +string hash
        +datetime timestamp
        +string format
    }

    class EnvironmentVar {
        +string key
        +string value
        +string file
    }

    ConfigManager --> ConfigFile
    ConfigManager --> EnvironmentVar
```

## Workflow

```mermaid
sequenceDiagram
    participant User
    participant Script
    participant ConfigManager
    participant FileIO

    User->>Script: --backup --file .env
    Script->>ConfigManager: ConfigManager('.')
    ConfigManager->>FileIO: Create backup path
    ConfigManager->>FileIO: Copy file
    ConfigManager->>FileIO: Compress if needed
    ConfigManager->>Script: Return backup path
    Script->>User: Backup completed

    User->>Script: --env set --key API_KEY
    Script->>ConfigManager: update_env_var()
    ConfigManager->>FileIO: Read file
    ConfigManager->>FileIO: Update key-value
    ConfigManager->>FileIO: Write file
    ConfigManager->>Script: Return success
    Script->>User: Variable updated
```

## Supported Config Formats

### JSON

```json
{
  "database": {
    "url": "postgres://localhost:5432"
  }
}
```

### YAML

```yaml
database:
  url: postgres://localhost:5432
  name: mydb
```

### INI

```ini
[database]
url=postgres://localhost:5432
name=mydb
```

### Environment Variables

```bash
DATABASE_URL=postgres://localhost:5432
DATABASE_NAME=mydb
```

## Configuration Files

### .env

```bash
API_KEY=your_api_key
DATABASE_URL=postgres://localhost:5432
DATABASE_NAME=mydb
```

### config.yaml

```yaml
app:
  name: myapp
  version: 1.0.0

database:
  host: localhost
  port: 5432
  name: mydb
```

## Backup Locations

### Default Backup Directory

```bash
./.config_backups
```

### Custom Directory

```bash
python scripts/config_manager.py \
    backup \
    --file .env \
    --project /custom/path
```

## Compression

### Enable Compression

```json
{
  "compression": true
}
```

### Disable Compression

```json
{
  "compression": false
}
```

## Return Codes

- `0`: Success
- `1`: Error

## Dependencies

- Python 3.7+
- PyYAML
- configparser
- tarfile
- hashlib

## Examples

### Complete Configuration Workflow

```bash
# Backup .env file
python scripts/config_manager.py \
    backup \
    --file .env

# Backup all config files
python scripts/config_manager.py \
    backup \
    --all

# Set environment variable
python scripts/config_manager.py \
    env \
    set \
    --key API_KEY \
    --value secret123 \
    --file .env

# Get environment variable
python scripts/config_manager.py \
    env \
    get \
    --key API_KEY \
    --file .env

# Validate config file
python scripts/config_manager.py \
    validate \
    --file config.yaml \
    --type yaml

# Diff config files
python scripts/config_manager.py \
    diff \
    --file1 config1.yaml \
    --file2 config2.yaml

# Search config file
python scripts/config_manager.py \
    search \
    --file config.yaml \
    --pattern DATABASE

# List config files
python scripts/config_manager.py \
    list \
    --pattern .env* config.*
```

## Best Practices

1. **Backup frequently** - Backup before making changes
2. **Organize backups** - Use timestamped backup names
3. **Encrypt sensitive data** - Protect sensitive configurations
4. **Use environment variables** - For sensitive data
5. **Validate configuration** - Before deployment
6. **Document changes** - Keep track of configuration changes
7. **Use version control** - Track config files
8. **Separate environments** - Different configs for dev/prod
9. **Test restores** - Ensure backups are valid
10. **Clean up old backups** - Remove unused backups
