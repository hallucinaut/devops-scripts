#!/usr/bin/env python3
"""
Database Backup Script
Handles database backups, restores, and maintenance
"""

import argparse
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import logging


class DatabaseBackupManager:
    """Database backup and restore manager"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.logger = self._setup_logger()
        self.backup_dir = Path(self.config.get('backup_dir', 'backups'))
        self.backup_dir.mkdir(exist_ok=True)
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        if not config_file:
            return {
                'backup_dir': 'backups',
                'compression': True,
                'keep_days': 7
            }
        
        with open(config_file) as f:
            return json.load(f)
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logger"""
        logger = logging.getLogger('database_backup')
        logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler(
            self.backup_dir / 'backup.log'
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'
        ))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def backup_postgresql(self, database: str, host: str = 'localhost',
                         port: int = 5432, username: str = None,
                         backup_file: Optional[str] = None) -> Optional[str]:
        """Backup PostgreSQL database"""
        print(f"Backing up PostgreSQL database: {database}")
        
        if not username:
            username = os.getenv('PGUSER', 'postgres')
        
        if backup_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'{database}_{timestamp}.sql'
        
        try:
            cmd = [
                'pg_dump',
                f'postgresql://{username}@{host}:{port}/{database}',
                '--format=plain'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            backup_file.write_text(result.stdout)
            self.logger.info(f"Backup created: {backup_file}")
            
            if self.config.get('compression', True):
                return self._compress_file(backup_file)
            
            return str(backup_file)
        except subprocess.CalledProcessError as e:
            print(f"✗ Backup failed: {e}", file=sys.stderr)
            self.logger.error(f"Backup failed: {e}")
            return None
    
    def backup_mysql(self, database: str, host: str = 'localhost',
                     port: int = 3306, username: str = None,
                     backup_file: Optional[str] = None) -> Optional[str]:
        """Backup MySQL database"""
        print(f"Backing up MySQL database: {database}")
        
        if not username:
            username = os.getenv('MYSQL_USER', 'root')
        
        if backup_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'{database}_{timestamp}.sql'
        
        try:
            cmd = [
                'mysqldump',
                f'-h{host}',
                f'-P{port}',
                f'-u{username}',
                '--single-transaction',
                '--routines',
                '--triggers',
                database
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            backup_file.write_text(result.stdout)
            self.logger.info(f"Backup created: {backup_file}")
            
            if self.config.get('compression', True):
                return self._compress_file(backup_file)
            
            return str(backup_file)
        except subprocess.CalledProcessError as e:
            print(f"✗ Backup failed: {e}", file=sys.stderr)
            self.logger.error(f"Backup failed: {e}")
            return None
    
    def backup_mongodb(self, database: str, host: str = 'localhost',
                      port: int = 27017, username: str = None,
                      backup_file: Optional[str] = None) -> Optional[str]:
        """Backup MongoDB database"""
        print(f"Backing up MongoDB database: {database}")
        
        if backup_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'{database}_{timestamp}.dump'
        
        try:
            cmd = [
                'mongodump',
                f'--uri={f"mongodb://{username}@{host}:{port}" if username else f"mongodb://{host}:{port}"}',
                '--db={database}'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            self.logger.info(f"Backup created: {backup_file}")
            return str(backup_file)
        except subprocess.CalledProcessError as e:
            print(f"✗ Backup failed: {e}", file=sys.stderr)
            self.logger.error(f"Backup failed: {e}")
            return None
    
    def backup_sqlite(self, database: str, backup_file: Optional[str] = None) -> Optional[str]:
        """Backup SQLite database"""
        print(f"Backing up SQLite database: {database}")
        
        if backup_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'{database}_{timestamp}.sql'
        
        try:
            # SQLite doesn't need backup command, just copy
            source = Path(database)
            backup_file.write_text(source.read_text())
            self.logger.info(f"Backup created: {backup_file}")
            return str(backup_file)
        except Exception as e:
            print(f"✗ Backup failed: {e}", file=sys.stderr)
            self.logger.error(f"Backup failed: {e}")
            return None
    
    def _compress_file(self, filepath: Path) -> Optional[str]:
        """Compress backup file"""
        compressed = filepath.with_suffix(filepath.suffix + '.tar.gz')
        
        try:
            with tarfile.open(compressed, 'w:gz') as tar:
                tar.add(filepath, arcname=filepath.name)
            
            # Remove original file
            filepath.unlink()
            
            print(f"✓ Compressed backup: {compressed}")
            self.logger.info(f"Compressed backup: {compressed}")
            return str(compressed)
        except Exception as e:
            print(f"✗ Compression failed: {e}", file=sys.stderr)
            self.logger.error(f"Compression failed: {e}")
            return None
    
    def restore(self, backup_file: str, database: str, host: str = 'localhost',
                port: int = 5432, username: str = None):
        """Restore database from backup"""
        print(f"Restoring database: {database}")
        
        if backup_file.endswith('.tar.gz'):
            # Extract and restore
            with tarfile.open(backup_file, 'r:gz') as tar:
                tar.extractall(path=self.backup_dir)
                extracted_file = tar.getnames()[0]
                backup_file = self.backup_dir / extracted_file
        
        if backup_file.endswith('.sql'):
            if not username:
                username = os.getenv('PGUSER', 'postgres')
            
            try:
                cmd = [
                    'psql',
                    f'postgresql://{username}@{host}:{port}/{database}',
                    '-f', backup_file
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                print("✓ Database restored successfully")
                self.logger.info(f"Database restored: {database}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Restore failed: {e}", file=sys.stderr)
                self.logger.error(f"Restore failed: {e}")
        elif backup_file.endswith('.dump'):
            print("✗ MongoDB restore requires additional tools")
        else:
            print("✗ Unsupported backup format")
    
    def list_backups(self, database: Optional[str] = None) -> List[Path]:
        """List available backups"""
        if database:
            pattern = f'{database}_*.sql*'
        else:
            pattern = '*.sql*'
        
        backups = list(self.backup_dir.glob(pattern))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        return backups
    
    def cleanup_old_backups(self, days: Optional[int] = None):
        """Remove backups older than specified days"""
        print("Cleaning up old backups...")
        
        if days is None:
            days = self.config.get('keep_days', 7)
        
        cutoff = datetime.now().timestamp() - (days * 86400)
        
        for backup in self.list_backups():
            if backup.stat().st_mtime < cutoff:
                backup.unlink()
                print(f"✓ Removed old backup: {backup}")
                self.logger.info(f"Removed old backup: {backup}")


def main():
    parser = argparse.ArgumentParser(description='Database Backup Script')
    parser.add_argument('--database', required=True, help='Database type (postgresql, mysql, mongodb, sqlite)')
    parser.add_argument('--name', required=True, help='Database name')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', type=int, help='Database port')
    parser.add_argument('--user', help='Database user')
    parser.add_argument('--backup-file', help='Custom backup file path')
    parser.add_argument('--config', help='Configuration file')
    parser.add_argument('--restore', help='Restore from backup file')
    parser.add_argument('--list', action='store_true', help='List backups')
    parser.add_argument('--cleanup', action='store_true', help='Clean up old backups')
    parser.add_argument('--keep-days', type=int, help='Days to keep backups')
    
    args = parser.parse_args()
    
    manager = DatabaseBackupManager(args.config)
    
    if args.list:
        backups = manager.list_backups(args.name)
        print(f"\nAvailable backups for {args.name}:")
        for backup in backups:
            size = backup.stat().st_size / 1024  # KB
            print(f"  {backup.name} ({size:.2f} KB, {backup.stat().st_mtime})")
        return
    
    if args.restore:
        manager.restore(args.restore, args.name, args.host, args.port, args.user)
        return
    
    if args.cleanup:
        manager.cleanup_old_backups(args.keep_days)
        return
    
    # Perform backup
    if args.database == 'postgresql':
        manager.backup_postgresql(args.name, args.host, args.port, args.user, args.backup_file)
    elif args.database == 'mysql':
        manager.backup_mysql(args.name, args.host, args.port, args.user, args.backup_file)
    elif args.database == 'mongodb':
        manager.backup_mongodb(args.name, args.host, args.port, args.user, args.backup_file)
    elif args.database == 'sqlite':
        manager.backup_sqlite(args.name, args.backup_file)
    else:
        print(f"✗ Unsupported database type: {args.database}")


if __name__ == '__main__':
    main()
