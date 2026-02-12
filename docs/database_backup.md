# database_backup.py

## Overview

The `database_backup.py` script provides comprehensive database backup and restore operations. It supports PostgreSQL, MySQL, MongoDB, and SQLite databases with features for backup compression, automated cleanup, and restoration capabilities.

## Features

- Multi-database support (PostgreSQL, MySQL, MongoDB, SQLite)
- Backup compression
- Restore operations
- Backup history management
- Automated cleanup
- Configuration management
- Logging

## Mermaid Diagram

```mermaid
flowchart TD
    A[Start: Database Backup] --> B{Select Database Type}
    B -->|PostgreSQL| C[PostgreSQL Backup]
    B -->|MySQL| D[MySQL Backup]
    B -->|MongoDB| E[MongoDB Backup]
    B -->|SQLite| F[SQLite Backup]

    C --> G[Initialize Manager]
    G --> H[Create Backup File]
    H --> I[Run pg_dump]
    I --> J[Save Backup]
    J --> K[Compress If Enabled]
    K --> L[Save Metadata]
    L --> M[Return Result]

    D --> N[Initialize Manager]
    N --> O[Create Backup File]
    O --> P[Run mysqldump]
    P --> Q[Save Backup]
    Q --> R[Compress If Enabled]
    R --> S[Save Metadata]
    S --> T[Return Result]

    E --> U[Initialize Manager]
    U --> V[Create Backup Path]
    V --> W[Run mongodump]
    W --> X[Save Backup]
    X --> Y[Return Result]

    F --> AA[Initialize Manager]
    AA --> AB[Create Backup Path]
    AB --> AC[Copy Database]
    AC --> AD[Save Backup]
    AD --> AE[Return Result]

    M --> AF[End]
    T --> AF
    Y --> AF
    AE --> AF
```

## Usage

### PostgreSQL Backup

```bash
python scripts/database_backup.py \
    --database postgresql \
    --name mydb \
    --user postgres
```

### MySQL Backup

```bash
python scripts/database_backup.py \
    --database mysql \
    --name mydb \
    --user root
```

### MongoDB Backup

```bash
python scripts/database_backup.py \
    --database mongodb \
    --name mydb
```

### SQLite Backup

```bash
python scripts/database_backup.py \
    --database sqlite \
    --name mydb
```

### Restore Backup

```bash
python scripts/database_backup.py \
    --restore mydb_20240101.sql \
    --name mydb
```

### List Backups

```bash
python scripts/database_backup.py \
    --list \
    --name mydb
```

### Cleanup Old Backups

```bash
python scripts/database_backup.py \
    --cleanup \
    --keep-days 7
```

### With Configuration File

```bash
python scripts/database_backup.py \
    --database postgresql \
    --name mydb \
    --config backup-config.json
```

## Commands

### Backup

```bash
python scripts/database_backup.py \
    --database postgresql \
    --name mydb \
    --user postgres
```

### Restore

```bash
python scripts/database_backup.py \
    --restore backup.sql \
    --name mydb
```

### List

```bash
python scripts/database_backup.py \
    --list \
    --name mydb
```

### Cleanup

```bash
python scripts/database_backup.py \
    --cleanup \
    --keep-days 7
```

## Architecture

```mermaid
classDiagram
    class DatabaseBackupManager {
        -Dict config
        -Path backup_dir
        -Logger logger
        +__init__(config_file: str) None
        +backup_postgresql(database: str, host: str, port: int, username: str, backup_file: str) Optional[str]
        +backup_mysql(database: str, host: str, port: int, username: str, backup_file: str) Optional[str]
        +backup_mongodb(database: str, host: str, port: int, username: str, backup_file: str) Optional[str]
        +backup_sqlite(database: str, backup_file: str) Optional[str]
        +_compress_file(filepath: Path) Optional[str]
        +restore(backup_file: str, database: str, host: str, port: int, username: str) bool
        +list_backups(database: str) List
        +cleanup_old_backups(days: Optional) None
        +_load_config(config_file: str) Dict
        +_setup_logger() Logger
    }

    class DatabaseConfig {
        +string database
        +string host
        +int port
        +string username
        +string password
        +string backup_dir
        +bool compression
        +int keep_days
    }

    class BackupFile {
        +string database
        +string filename
        +datetime timestamp
        +string size
        +string format
    }

    DatabaseBackupManager --> DatabaseConfig
    DatabaseBackupManager --> BackupFile
```

## Workflow

```mermaid
sequenceDiagram
    participant User
    participant Script
    participant DatabaseBackupManager
    participant FileIO
    participant DatabaseAPI

    User->>Script: --database postgresql --name mydb
    Script->>DatabaseBackupManager: DatabaseBackupManager()
    DatabaseBackupManager->>DatabaseAPI: pg_dump command
    DatabaseAPI-->>DatabaseBackupManager: Backup data
    DatabaseBackupManager->>FileIO: Save backup file
    DatabaseBackupManager->>DatabaseBackupManager: Compress if enabled
    DatabaseBackupManager->>FileIO: Save metadata
    DatabaseBackupManager->>Script: Return backup path
    Script->>User: Backup completed
```

## Database Types

### PostgreSQL

```bash
--database postgresql --name mydb --user postgres
```

### MySQL

```bash
--database mysql --name mydb --user root
```

### MongoDB

```bash
--database mongodb --name mydb
```

### SQLite

```bash
--database sqlite --name mydb
```

## Configuration

### Configuration File Example

```json
{
  "backup_dir": "backups",
  "compression": true,
  "keep_days": 7
}
```

## Supported Formats

- Plain SQL (.sql)
- Compressed SQL (.sql.gz)
- MongoDB dump (.dump)
- SQLite file (.db, .sqlite)

## Backup Locations

### Default Directory

```bash
./backups
```

### Custom Directory

```bash
python scripts/database_backup.py \
    --database postgresql \
    --name mydb \
    --backup-dir /path/to/backups
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
- PostgreSQL client (pg_dump)
- MySQL client (mysqldump)
- MongoDB client (mongodump)
- tar (for compression)

## Examples

### Complete Backup Workflow

```bash
# Backup PostgreSQL database
python scripts/database_backup.py \
    --database postgresql \
    --name production_db \
    --user postgres \
    --backup-file production_20240101.sql

# Backup MySQL database
python scripts/database_backup.py \
    --database mysql \
    --name analytics_db \
    --user root

# Backup MongoDB database
python scripts/database_backup.py \
    --database mongodb \
    --name user_db

# Backup SQLite database
python scripts/database_backup.py \
    --database sqlite \
    --name local_db

# List backups
python scripts/database_backup.py \
    --list \
    --name production_db

# Cleanup old backups (older than 7 days)
python scripts/database_backup.py \
    --cleanup \
    --keep-days 7

# Restore from backup
python scripts/database_backup.py \
    --restore production_20240101.sql \
    --name production_db
```

## Best Practices

1. **Regular backups** - Schedule automated backups
2. **Test restores** - Verify backup integrity
3. **Multiple copies** - Keep backups in multiple locations
4. **Compression** - Enable for space efficiency
5. **Retention policy** - Set appropriate keep_days
6. **Monitor backups** - Check backup success rates
7. **Encrypt backups** - Protect sensitive data
8. **Document procedures** - Keep backup documentation
